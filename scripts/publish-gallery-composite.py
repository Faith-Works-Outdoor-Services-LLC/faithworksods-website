#!/usr/bin/env python3
"""Register one composite in the brand gallery and optionally queue/deploy it."""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from html import escape
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
CONFIG = json.loads((ROOT / "scripts" / "composite-brand.json").read_text(encoding="utf-8"))
GALLERY_DIR = ROOT / CONFIG["gallery_dir"]
MANIFEST_PATH = ROOT / CONFIG["job_manifest"]
DETAIL_DIR = ROOT / "gallery"
SMM_ROOT = Path(r"E:\KnightLogics-Growth-System\Social\Social-Media-Manager")
POPULATOR = SMM_ROOT / "scheduled_brand_posting" / "populate_brand_gallery.py"


def run(cmd: list[str], *, cwd: Path = ROOT) -> None:
    print("+", " ".join(str(item) for item in cmd))
    subprocess.run(cmd, cwd=cwd, check=True)


def load_manifest() -> dict:
    if not MANIFEST_PATH.is_file():
        return {"version": 1, "brand": CONFIG["brand"], "projects": []}
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8-sig"))


def update_manifest(base: str, title: str) -> dict:
    manifest = load_manifest()
    projects = manifest.setdefault("projects", [])
    entry = {
        "id": base,
        "title": title,
        "summary": f"Before, process, and after project proof from {CONFIG['company_title']}.",
        "image": f"{CONFIG['gallery_public_path']}/{base}.webp",
        "social_image": f"{CONFIG['gallery_public_path']}/{base}-social.jpg",
        "detail_url": f"gallery/{base}.html",
        "published_at": datetime.now(timezone.utc).isoformat(),
    }
    existing = next((item for item in projects if item.get("id") == base), None)
    if existing:
        existing.update(entry)
    else:
        projects.insert(0, entry)
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return entry


def write_detail(entry: dict) -> Path:
    DETAIL_DIR.mkdir(parents=True, exist_ok=True)
    path = DETAIL_DIR / f"{entry['id']}.html"
    title = escape(str(entry["title"]))
    summary = escape(str(entry["summary"]))
    company = escape(str(CONFIG["company_title"]))
    image = escape(f"../{entry['image']}", quote=True)
    canonical = escape(f"{CONFIG['website_url']}/{entry['detail_url']}", quote=True)
    social_image = escape(f"{CONFIG['website_url']}/{entry['social_image']}", quote=True)
    contact_url = escape(str(CONFIG["contact_url"]), quote=True)
    html = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} Project | {company}</title>
<meta name="description" content="{summary}"><link rel="canonical" href="{canonical}">
<meta property="og:image" content="{social_image}">
<style>body{{margin:0;background:{CONFIG['background']};color:{CONFIG['text']};font-family:Arial,sans-serif}}main{{width:min(1120px,calc(100% - 32px));margin:auto;padding:36px 0 64px}}a{{color:{CONFIG['accent']};}}img{{display:block;width:100%;height:auto;border:2px solid {CONFIG['accent']};border-radius:14px}}h1{{font-size:clamp(2rem,6vw,4rem);margin:.35em 0}}.eyebrow{{color:{CONFIG['accent']};font-weight:800;letter-spacing:.12em}}.cta{{display:inline-block;padding:14px 20px;border-radius:8px;background:{CONFIG['accent']};color:{CONFIG['background']};font-weight:800;text-decoration:none}}</style></head>
<body><main><p class="eyebrow">COMPLETED PROJECT</p><h1>{title}</h1><p>{summary}</p>
<img src="{image}" alt="{title} before process and after project by {company}" width="1600" height="900">
<p><a class="cta" href="{contact_url}">Request an estimate</a> &nbsp; <a href="../gallery.html">View all projects</a></p>
</main></body></html>"""
    path.write_text(html, encoding="utf-8")
    return path


def update_sitemap(detail_url: str) -> None:
    path = ROOT / "sitemap.xml"
    if not path.is_file():
        return
    namespace = "http://www.sitemaps.org/schemas/sitemap/0.9"
    ET.register_namespace("", namespace)
    tree = ET.parse(path)
    root = tree.getroot()
    target = f"{CONFIG['website_url']}/{detail_url}"
    if any((node.text or "").strip() == target for node in root.findall(f"{{{namespace}}}url/{{{namespace}}}loc")):
        return
    url = ET.SubElement(root, f"{{{namespace}}}url")
    ET.SubElement(url, f"{{{namespace}}}loc").text = target
    ET.SubElement(url, f"{{{namespace}}}lastmod").text = datetime.now(timezone.utc).date().isoformat()
    tree.write(path, encoding="utf-8", xml_declaration=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--basename", required=True)
    parser.add_argument("--title", default="")
    parser.add_argument("--fan-out", action="store_true")
    parser.add_argument("--deploy", action="store_true")
    parser.add_argument("--commit-message", default="")
    args = parser.parse_args()
    base = re.sub(r"[^a-z0-9-]+", "-", args.basename.lower()).strip("-")
    webp = GALLERY_DIR / f"{base}.webp"
    social = GALLERY_DIR / f"{base}-social.jpg"
    missing = [path for path in (webp, social) if not path.is_file()]
    if missing:
        raise SystemExit(f"Missing required files: {', '.join(str(path) for path in missing)}")
    title = args.title.strip() or re.sub(r"^before-process-after-", "", base).replace("-", " ").title()
    entry = update_manifest(base, title)
    detail = write_detail(entry)
    if CONFIG.get("build_command"):
        run([sys.executable, str(ROOT / CONFIG["build_command"])])
    update_sitemap(entry["detail_url"])
    if args.fan_out:
        if not POPULATOR.is_file():
            raise SystemExit(f"Missing Social Ops populator: {POPULATOR}")
        run([sys.executable, str(POPULATOR), "--brand", CONFIG["brand"], "--only", base, "--status", "ready", "--fan-out"], cwd=SMM_ROOT)
    if args.deploy:
        paths = [webp.relative_to(ROOT), social.relative_to(ROOT), MANIFEST_PATH.relative_to(ROOT), detail.relative_to(ROOT)]
        for generated in (ROOT / "gallery.html", ROOT / "sitemap.xml"):
            if generated.is_file():
                paths.append(generated.relative_to(ROOT))
        run(["git", "add", *[str(path) for path in paths]])
        staged = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=ROOT)
        if staged.returncode == 1:
            run(["git", "commit", "-m", args.commit_message or f"Add {CONFIG['brand'].upper()} project composite {base}"])
        elif staged.returncode != 0:
            raise SystemExit("Unable to inspect staged website changes")
        run(["git", "push", "origin", "main"])
    print(json.dumps({"status": "ok", "entry": entry, "manifest": str(MANIFEST_PATH), "detail": str(detail)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

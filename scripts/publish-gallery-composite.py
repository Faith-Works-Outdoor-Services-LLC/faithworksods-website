#!/usr/bin/env python3
"""Register one composite in the Faith Works gallery and queue social posts."""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = json.loads((ROOT / "scripts" / "composite-brand.json").read_text(encoding="utf-8"))
GALLERY_DIR = ROOT / CONFIG["gallery_dir"]
MANIFEST_PATH = ROOT / CONFIG["job_manifest"]
SMM_ROOT = Path(r"E:\KnightLogics-Growth-System\Social\Social-Media-Manager")
POPULATOR = SMM_ROOT / "scheduled_brand_posting" / "populate_brand_gallery.py"


def run(cmd: list[str], *, cwd: Path = ROOT) -> None:
    print("+", " ".join(str(item) for item in cmd))
    subprocess.run(cmd, cwd=cwd, check=True)


def load_manifest() -> dict:
    if not MANIFEST_PATH.is_file():
        return {"version": 1, "brand": CONFIG["brand"], "projects": []}
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8-sig"))


def load_facts(path: Path | None) -> dict:
    if not path or not path.is_file():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError):
        return {}
    return payload if isinstance(payload, dict) else {}


def update_manifest(base: str, title: str, facts: dict) -> dict:
    manifest = load_manifest()
    projects = manifest.setdefault("projects", [])
    public = CONFIG["gallery_public_path"]
    entry = {
        "id": base,
        "title": title,
        "summary": facts.get("summary") or f"Before, process, and after project proof from {CONFIG['company_title']}.",
        "image": f"{public}/{base}.webp",
        "social_image": f"{public}/{base}-social.jpg",
        "gbp_image": f"{public}/{base}-gbp.jpg",
        "detail_url": f"gallery/{base}.html",
        "scope_url": f"gallery/{base}-scope.html",
        "service_slugs": facts.get("service_slugs") or [],
        "city_name": facts.get("city_name") or "",
        "city_slug": facts.get("city_slug") or "",
        "county_name": facts.get("county_name") or "",
        "photo_before": int(facts.get("photo_before") or 0),
        "photo_process": int(facts.get("photo_process") or 0),
        "photo_after": int(facts.get("photo_after") or 0),
        "published_at": datetime.now(timezone.utc).isoformat(),
    }
    existing = next((item for item in projects if item.get("id") == base), None)
    if existing:
        existing.update({k: v for k, v in entry.items() if v not in ("", [], 0) or k in {"title", "image", "detail_url", "scope_url"}})
        existing.update({"image": entry["image"], "social_image": entry["social_image"], "gbp_image": entry["gbp_image"], "detail_url": entry["detail_url"], "scope_url": entry["scope_url"], "title": entry["title"]})
        entry = existing
    else:
        projects.insert(0, entry)
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return entry


def rebuild_gallery_pages() -> None:
    script = ROOT / "website" / "_build_site.py"
    run([sys.executable, str(script), "--gallery-only"], cwd=ROOT / "website")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--basename", required=True)
    parser.add_argument("--title", default="")
    parser.add_argument("--facts-json", type=Path, default=None)
    parser.add_argument("--fan-out", action="store_true")
    parser.add_argument("--deploy", action="store_true")
    parser.add_argument("--commit-message", default="")
    args = parser.parse_args()
    base = re.sub(r"[^a-z0-9-]+", "-", args.basename.lower()).strip("-")
    webp = GALLERY_DIR / f"{base}.webp"
    social = GALLERY_DIR / f"{base}-social.jpg"
    gbp = GALLERY_DIR / f"{base}-gbp.jpg"
    missing = [path for path in (webp, social) if not path.is_file()]
    if missing:
        raise SystemExit(f"Missing required files: {', '.join(str(path) for path in missing)}")
    title = args.title.strip() or re.sub(r"^before-process-after-", "", base).replace("-", " ").title()
    facts = load_facts(args.facts_json)
    entry = update_manifest(base, title, facts)
    rebuild_gallery_pages()
    detail = ROOT / entry["detail_url"]
    scope = ROOT / entry["scope_url"]
    if args.fan_out:
        if not POPULATOR.is_file():
            raise SystemExit(f"Missing Social Ops populator: {POPULATOR}")
        run(
            [sys.executable, str(POPULATOR), "--brand", CONFIG["brand"], "--only", base, "--status", "ready", "--fan-out"],
            cwd=SMM_ROOT,
        )
    if args.deploy:
        paths = [
            webp.relative_to(ROOT),
            social.relative_to(ROOT),
            MANIFEST_PATH.relative_to(ROOT),
        ]
        if gbp.is_file():
            paths.append(gbp.relative_to(ROOT))
        for generated in (
            ROOT / "gallery.html",
            ROOT / "sitemap.xml",
            ROOT / "styles.css",
            detail,
            scope,
        ):
            if generated.is_file():
                paths.append(generated.relative_to(ROOT))
        run(["git", "add", *[str(path) for path in paths]])
        staged = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=ROOT)
        if staged.returncode == 1:
            run(["git", "commit", "-m", args.commit_message or f"Add {CONFIG['brand'].upper()} project composite {base}"])
        elif staged.returncode != 0:
            raise SystemExit("Unable to inspect staged website changes")
        run(["git", "push", "origin", "HEAD"])
    print(json.dumps({"status": "ok", "entry": entry, "manifest": str(MANIFEST_PATH), "detail": str(detail), "scope": str(scope)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

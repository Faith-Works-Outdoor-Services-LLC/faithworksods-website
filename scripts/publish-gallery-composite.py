#!/usr/bin/env python3
"""Publish a before/process/after composite to Faith Works Gallery + social queue.

Expects in Gallery/:
  {basename}.webp
  {basename}-social.jpg
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GALLERY_DIR = ROOT / "Gallery"
SMM_ROOT = Path(r"E:\KnightLogics-Growth-System\Social\Social-Media-Manager")
POPULATE_FW = SMM_ROOT / "scheduled_brand_posting" / "populate_fw_gallery.py"


def run(cmd: list[str], *, cwd: Path | None = None) -> None:
    print("+", " ".join(cmd))
    subprocess.run(cmd, cwd=str(cwd or ROOT), check=True)


def main() -> int:
    parser = argparse.ArgumentParser(description="Publish Faith Works gallery composite")
    parser.add_argument(
        "--basename",
        required=True,
        help="Base name without extension, e.g. before-process-after-land-clearing-job",
    )
    parser.add_argument("--deploy", action="store_true", help="Git commit and push social/webp assets")
    parser.add_argument("--fan-out", action="store_true", help="Queue new social JPG in FW media + platform queues")
    parser.add_argument("--commit-message", default="", help="Git commit message")
    args = parser.parse_args()

    base = re.sub(r"[^\w\-]+", "-", args.basename.strip()).strip("-").lower()
    webp = GALLERY_DIR / f"{base}.webp"
    social = GALLERY_DIR / f"{base}-social.jpg"
    missing = [p for p in (webp, social) if not p.is_file()]
    if missing:
        raise SystemExit(f"Missing required files: {', '.join(str(p) for p in missing)}")

    if args.fan_out:
        if not POPULATE_FW.is_file():
            raise SystemExit(f"Missing queue populator: {POPULATE_FW}")
        run([sys.executable, str(POPULATE_FW), "--only", base, "--fan-out"])

    if args.deploy:
        msg = args.commit_message or f"Add gallery composite {base}"
        paths = [
            str(webp.relative_to(ROOT)),
            str(social.relative_to(ROOT)),
            ".gitignore",
        ]
        run(["git", "add", *paths], cwd=ROOT)
        run(["git", "status", "-sb"], cwd=ROOT)
        run(["git", "commit", "-m", msg], cwd=ROOT)
        run(["git", "push", "origin", "main"], cwd=ROOT)
        print("Deployed to origin/main")

    print(f"\nPublished {base}")
    print(f"  Social JPG: https://faithworksclearing.com/Gallery/{social.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

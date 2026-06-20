#!/usr/bin/env python3
"""Quick duplicate-content check for area pages."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "areas"


def main() -> None:
    pairs = [
        ("brandon-fl", "valrico-fl"),
        ("mulberry-fl", "bartow-fl"),
        ("ocoee-fl", "apopka-fl"),
        ("polk-county-fl", "hillsborough-county-fl"),
        ("kissimmee-fl", "orlando-fl"),
    ]

    def body(text: str) -> str:
        i = text.find("area-rich-content")
        chunk = text[i : i + 12000] if i >= 0 else text
        return re.sub(r"\s+", " ", chunk)

    for a, b in pairs:
        ba = body((ROOT / f"{a}.html").read_text(encoding="utf-8"))
        bb = body((ROOT / f"{b}.html").read_text(encoding="utf-8"))
        wa, wb = set(ba.lower().split()), set(bb.lower().split())
        overlap = len(wa & wb) / max(len(wa | wb), 1)
        print(f"{a} vs {b}: {overlap:.1%} word overlap")

    metas: list[str] = []
    for path in ROOT.glob("*.html"):
        text = path.read_text(encoding="utf-8")
        match = re.search(r'<meta name="description" content="([^"]+)"', text)
        if match:
            metas.append(match.group(1))
    print(f"area pages: {len(metas)}, unique meta descriptions: {len(set(metas))}")


if __name__ == "__main__":
    main()

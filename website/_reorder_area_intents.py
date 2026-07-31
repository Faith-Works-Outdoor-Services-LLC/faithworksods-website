#!/usr/bin/env python3
"""Reorder city/county area intent routes and common jobs to match service priority ladder."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# Lower = higher priority (matches PHASE1_PRIORITY + follow-ons)
SLUG_RANK = {
    "land-clearing": 0,
    "forestry-mulching": 1,
    "brush-clearing": 2,
    "overgrowth-removal": 3,
    "demolition": 4,
    "fence-line-clearing": 5,
    "stump-removal": 6,
    "driveway-demo": 7,
    "access-road-clearing": 8,
    "trail-clearing": 9,
    "pond-bank-clearing": 10,
    "pond-cleanup": 11,
    "pond-management": 12,
    "ditch-clearing": 13,
    "ditch-maintenance": 14,
    "acreage-cleanup": 15,
    "lot-cleanup": 16,
    "property-cleanup": 17,
    "debris-removal": 18,
    "yard-debris-removal": 19,
    "storm-debris-cleanup": 20,
    "tractor-services": 21,
    "equipment-services": 22,
    "pool-dig-out-support": 23,
    "property-maintenance": 24,
}

JOB_RANK_PATTERNS = [
    (0, re.compile(r"land clear|lot clear|acreage clear|overgrown lot|selective clear", re.I)),
    (1, re.compile(r"forestry mulch|mulching", re.I)),
    (2, re.compile(r"\bdemo|tear-?down|shed|outbuilding", re.I)),
    (3, re.compile(r"fence", re.I)),
    (4, re.compile(r"\bstump", re.I)),
    (5, re.compile(r"driveway", re.I)),
    (6, re.compile(r"access (road|path)|trail reopen|private road", re.I)),
    (7, re.compile(r"pond|canal|shoreline|lake edge|water edge|retention", re.I)),
    (8, re.compile(r"\bditch|swale|drainage", re.I)),
    (9, re.compile(r"\bbrush\b|overgrowth", re.I)),
    (10, re.compile(r"storm|debris|haul-?off", re.I)),
    (11, re.compile(r"pool dig|pool ", re.I)),
]


def slug_rank(slug: str) -> int:
    return SLUG_RANK.get(slug, 50)


def job_rank(text: str) -> int:
    for rank, pattern in JOB_RANK_PATTERNS:
        if pattern.search(text):
            return rank
    return 40


def reorder_intent_block(block: str) -> str:
    """Reorder dicts inside an intent_routes = [ ... ] list literal."""
    items = re.findall(
        r'\{\s*"label":\s*"[^"]*",\s*"slug":\s*"([^"]+)",\s*"text":\s*"[^"]*"\s*\}',
        block,
        flags=re.S,
    )
    if len(items) < 2:
        return block

    full_items = re.findall(
        r'(\{\s*"label":\s*"[^"]*",\s*"slug":\s*"[^"]+",\s*"text":\s*"[^"]*"\s*\})',
        block,
        flags=re.S,
    )
    if len(full_items) < 2:
        return block

    paired = []
    for raw in full_items:
        m = re.search(r'"slug":\s*"([^"]+)"', raw)
        if not m:
            continue
        paired.append((slug_rank(m.group(1)), raw.strip()))
    paired.sort(key=lambda x: (x[0], x[1]))
    rebuilt = ",\n            ".join(item for _, item in paired)
    return re.sub(
        r'\[\s*(?:\{.*?\},?\s*)+\]',
        f"[\n            {rebuilt},\n        ]",
        block,
        count=1,
        flags=re.S,
    )


def reorder_jobs_block(block: str) -> str:
    jobs = re.findall(r'"([^"]+)"', block)
    if len(jobs) < 2:
        return block
    # Only treat as common_jobs if strings look like job descriptions (long-ish)
    if not all(len(j) > 20 for j in jobs):
        return block
    ranked = sorted(jobs, key=lambda j: (job_rank(j), j))
    rebuilt = ",\n            ".join(f'"{j}"' for j in ranked)
    return f"[\n            {rebuilt},\n        ]"


def patch_file(path: Path) -> int:
    text = path.read_text(encoding="utf-8")
    original = text
    changes = 0

    def intent_sub(match: re.Match[str]) -> str:
        nonlocal changes
        key = match.group(1)
        body = match.group(2)
        new_body = reorder_intent_block(body)
        if new_body != body:
            changes += 1
        return f'{key}{new_body}'

    text = re.sub(
        r'(["\']intent_routes["\']\s*:\s*)(\[[^\]]*?(?:\{[^\]]*?"slug"[^\]]*?\})[^\]]*?\])',
        intent_sub,
        text,
        flags=re.S,
    )

    def jobs_sub(match: re.Match[str]) -> str:
        nonlocal changes
        key = match.group(1)
        body = match.group(2)
        new_body = reorder_jobs_block(body)
        if new_body != body:
            changes += 1
        return f"{key}{new_body}"

    text = re.sub(
        r'(["\']common_jobs["\']\s*:\s*)(\[[^\]]+\])',
        jobs_sub,
        text,
        flags=re.S,
    )

    if text != original:
        path.write_text(text, encoding="utf-8", newline="\n")
    return changes


def main() -> None:
    targets = [
        ROOT / "city_area_profiles.py",
        ROOT / "city_profiles_remaining.py",
        ROOT / "area_page_content.py",
    ]
    total = 0
    for path in targets:
        if not path.is_file():
            print(f"skip missing {path.name}")
            continue
        n = patch_file(path)
        total += n
        print(f"{path.name}: {n} blocks reordered")
    print(f"done ({total} blocks)")


if __name__ == "__main__":
    main()

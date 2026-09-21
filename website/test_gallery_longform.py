"""Gallery longform uniqueness, length, and PII guards for Faith Works."""
from __future__ import annotations

import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from gallery_longform import MIN_WORDS, build_gallery_longform  # noqa: E402
from gallery_public_web import strip_html_words  # noqa: E402


def _land(slug: str, city: str, notes: str) -> dict:
    return {
        "id": slug,
        "title": "Land clearing project — before, process, and after",
        "city_name": city,
        "city_slug": f"{city.lower().replace(' ', '-')}-fl",
        "county_name": "Polk County",
        "service_slugs": ["land-clearing", "lot-cleanup", "acreage-cleanup"],
        "work_notes": notes,
        "photo_before": 3,
        "photo_process": 4,
        "photo_after": 2,
        "image": f"gallery/{slug}.webp",
    }


def test_two_pages_meet_750_and_stay_unique():
    a = build_gallery_longform(_land("before-process-after-land-clearing-job", "Auburndale", "Opened the overgrown lot and stacked brush for haul-off."))
    b = build_gallery_longform(
        {
            "id": "before-process-after-pond-bank-winter-haven-abc123aa",
            "title": "Pond bank clearing — before, process, and after",
            "city_name": "Winter Haven",
            "city_slug": "winter-haven-fl",
            "county_name": "Polk County",
            "service_slugs": ["pond-bank-clearing"],
            "work_notes": "Cleared woody brush from the agreed bank and left a walkable edge.",
            "photo_before": 2,
            "photo_process": 3,
            "photo_after": 2,
            "image": "gallery/before-process-after-pond-bank-winter-haven-abc123aa.webp",
        }
    )
    assert a["detail"]["word_count"] == strip_html_words(a["detail"]["body_html"])
    assert a["scope"]["word_count"] == strip_html_words(a["scope"]["body_html"])
    assert a["detail"]["word_count"] >= MIN_WORDS
    assert a["scope"]["word_count"] >= MIN_WORDS
    assert b["detail"]["word_count"] >= MIN_WORDS
    assert b["scope"]["word_count"] >= MIN_WORDS
    assert a["detail"]["body_html"] != a["scope"]["body_html"]
    assert a["detail"]["body_html"] != b["detail"]["body_html"]
    assert a["scope"]["body_html"] != b["scope"]["body_html"]
    for page in (a["detail"]["body_html"], a["scope"]["body_html"]):
        assert "land-clearing.html" in page
        assert "contact.html" in page
        assert "gallery.html" in page
        assert "areas/auburndale-fl.html" in page
        assert "fw-project-composite" in page
        assert "before-process-after-land-clearing-job.webp" in page


def test_longform_strips_ticket_pii():
    page = build_gallery_longform(
        _land(
            "before-process-after-land-clearing-deadbeef",
            "Lakeland",
            "Work at 1234 Palmetto Drive billed $480.00 ticket FW-20260921-ABC",
        )
    )
    blob = page["detail"]["body_html"] + page["scope"]["body_html"]
    assert "1234 Palmetto" not in blob
    assert "480.00" not in blob
    assert "FW-20260921-ABC" not in blob
    assert "Lakeland" in blob
    assert "ticket numbers" in blob.lower() or "Addresses, ticket numbers" in blob


if __name__ == "__main__":
    test_two_pages_meet_750_and_stay_unique()
    test_longform_strips_ticket_pii()
    print("test_gallery_longform: OK")

"""HTML-side PII sweep for generated Faith Works gallery pages.

Ticket prices, street addresses, customer phones, emails, and ticket numbers
never ship in public HTML even if export facts were incomplete.
"""
from __future__ import annotations

import re

FW_PHONE_DISPLAY = "(863) 272-1596"
FW_PHONE_TEL = "8632721596"
FW_EMAIL = "tyler@faithworksclearing.com"

_STREET_RE = re.compile(
    r"\b\d{1,6}\s+(?:[NSEW]\.?\s+)?(?:[A-Za-z0-9.'-]+\s+){0,7}"
    r"(?:street|st|avenue|ave|drive|dr|road|rd|lane|ln|boulevard|blvd|"
    r"court|ct|way|place|pl|terrace|ter|circle|cir)\b[^,;]*",
    re.I,
)
_EMAIL_RE = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I)
_PHONE_RE = re.compile(r"(?:\+?1[\s.-]?)?(?:\(?\d{3}\)?[\s.-]?)\d{3}[\s.-]?\d{4}")
_MONEY_RE = re.compile(r"\$\s*\d[\d,]*(?:\.\d{2})?")
_TICKET_RE = re.compile(
    r"\b(?:FW|KG|ST|RM)-?\d{4,8}-?[A-Z0-9]{0,8}\b|\b(?:WO|ticket)\s*#?\s*[A-Z0-9-]{5,}\b",
    re.I,
)
_ZIP_RE = re.compile(r"\b\d{5}(?:-\d{4})?\b")


def alt_place_phrase(city_name: str = "", county_name: str = "") -> str:
    city = str(city_name or "").strip()
    county = str(county_name or "Polk County").strip() or "Polk County"
    if city:
        return f"{city} FL"
    return f"{county} FL"


def strip_html_words(html: str) -> int:
    text = re.sub(r"<[^>]+>", " ", html or "")
    text = re.sub(r"&[a-z]+;", " ", text, flags=re.I)
    return len(re.findall(r"[A-Za-z0-9']+", text))


def sanitize_page_text(html: str, *, extra_needles: list[str] | None = None) -> str:
    text = html or ""
    text = text.replace(FW_PHONE_DISPLAY, "FWPHONE")
    text = text.replace("863-272-1596", "FWPHONE")
    text = text.replace("tel:+18632721596", "FWTEL")
    text = text.replace(FW_EMAIL, "FWEMAIL")
    for needle in extra_needles or []:
        raw = str(needle or "").strip()
        if len(raw) >= 8 and "@" not in raw:
            continue
    text = _EMAIL_RE.sub(" ", text)
    text = _PHONE_RE.sub(" ", text)
    text = _STREET_RE.sub(" ", text)
    text = _TICKET_RE.sub(" ", text)
    text = _MONEY_RE.sub(" ", text)
    text = _ZIP_RE.sub(" ", text)
    text = text.replace("FWPHONE", FW_PHONE_DISPLAY)
    text = text.replace("FWTEL", "tel:+18632721596")
    text = text.replace("FWEMAIL", FW_EMAIL)
    text = re.sub(r"[ \t]{2,}", " ", text)
    return text

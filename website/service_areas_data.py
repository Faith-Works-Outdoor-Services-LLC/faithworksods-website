"""Launch service area cities and counties for Faith Works Outdoor Services.

The launch footprint is intentionally focused for Google Business Profile and
local SEO relevance. Larger Central Florida acreage or equipment-assisted
cleanup projects can still be reviewed case by case through the estimate form.
"""

from __future__ import annotations

HOME_ZIP = "33823"
HOME_CITY = "Auburndale"
SERVICE_RADIUS_MILES = 35

COUNTIES = [
    {
        "name": "Polk County",
        "slug": "polk-county-fl",
        "description": "Primary service area - Auburndale, Winter Haven, Lakeland, Lake Alfred, Bartow, Haines City, Davenport, Lake Wales, Polk City, and nearby Polk County communities.",
    },
    {
        "name": "Hillsborough County",
        "slug": "hillsborough-county-fl",
        "description": "Nearby larger-job coverage for Plant City and eastern Hillsborough acreage, land clearing, pond bank, ditch, and equipment-assisted cleanup projects.",
    },
]

CITIES = [
    {"slug": "auburndale-fl", "name": "Auburndale", "county": "Polk County", "featured": True},
    {"slug": "winter-haven-fl", "name": "Winter Haven", "county": "Polk County", "featured": True},
    {"slug": "lakeland-fl", "name": "Lakeland", "county": "Polk County", "featured": True},
    {"slug": "lake-alfred-fl", "name": "Lake Alfred", "county": "Polk County", "featured": True},
    {"slug": "bartow-fl", "name": "Bartow", "county": "Polk County", "featured": True},
    {"slug": "haines-city-fl", "name": "Haines City", "county": "Polk County", "featured": True},
    {"slug": "davenport-fl", "name": "Davenport", "county": "Polk County", "featured": True},
    {"slug": "lake-wales-fl", "name": "Lake Wales", "county": "Polk County", "featured": True},
    {"slug": "polk-city-fl", "name": "Polk City", "county": "Polk County", "featured": True},
    {"slug": "plant-city-fl", "name": "Plant City", "county": "Hillsborough County", "featured": True},
]

COUNTY_BY_NAME = {c["name"]: c for c in COUNTIES}
COUNTY_BY_SLUG = {c["slug"]: c for c in COUNTIES}
CITY_BY_SLUG = {c["slug"]: c for c in CITIES}
CITY_NAMES = [c["name"] for c in CITIES]
FEATURED_CITIES = [c for c in CITIES if c.get("featured")]


def cities_in_county(county_name: str) -> list[dict]:
    return [c for c in CITIES if c["county"] == county_name]


def city_href(slug: str) -> str:
    return f"areas/{slug}.html"

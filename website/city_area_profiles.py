"""Unique per-city content for Faith Works service area pages."""

from __future__ import annotations

from city_profiles_remaining import REMAINING_CITY_PROFILES

# Hand-authored home-base and flagship Polk cities
_BASE_CITY_PROFILES: dict[str, dict] = {
    "auburndale-fl": {
        "meta_description": (
            "Auburndale land clearing, forestry mulching, light demo, fence lines, stump removal, and driveway demo "
            "from Faith Works. Owner-operated from 33823. Call or text Tyler."
        ),
        "hook": (
            "Auburndale is where Faith Works Outdoor Services is headquartered — Tyler Edwards runs estimates, "
            "scheduling, and field work from this Polk County lake-country community."
        ),
        "context": (
            "Between Lake Ariana, Lake Juliana, and the I-4 corridor, Auburndale mixes in-town neighborhoods "
            "with citrus acreage, old sheds and pads, fence rows that creep shut, and small-lake frontage. "
            "Priority jobs here start with land clearing, mulching, light outdoor demo, stumps, and driveway removal — "
            "with pond and ditch bank clearing available when edges need mechanical cleanup."
        ),
        "local_detail": (
            "Because we are based here, Auburndale jobs typically get the fastest response for site visits "
            "and equipment mobilization across eastern Polk County."
        ),
        "property_types": [
            "In-town lots with overgrown rear acreage toward Lake Ariana",
            "Citrus grove edges and abandoned grove cleanup parcels",
            "Properties with old sheds, pads, or leftover stumps after tree work",
            "Lakefront homes with unmanaged pond or canal banks",
            "Vacant parcels being opened for new construction near Berkley Road",
        ],
        "common_jobs": [
            "Forestry mulching and brush removal around homes, sheds, and fence lines",
            "Pond bank brush removal along small Auburndale lakes",
            "Light demolition of old sheds, outbuildings, and outdoor pads",
            "Old driveway demo and haul-off",
            "Stump removal after tree work or clearing",
            "Clearing overgrown residential lots before listing or building",
        ],
        "intent_routes": [
            {"label": "Lake-country lot clearing", "slug": "land-clearing", "text": "Open overgrown Auburndale lots backed by woods, groves, or water edges."},
            {"label": "Citrus acreage mulching", "slug": "forestry-mulching", "text": "Mulch saplings and thick undergrowth on former grove and pasture parcels."},
            {"label": "Shed and pad demo", "slug": "demolition", "text": "Tear down old sheds, lean-tos, and outdoor pads when access fits compact equipment."},
            {"label": "Fence lines and stumps", "slug": "fence-line-clearing", "text": "Reopen fence rows and clear leftover stumps that block mowing or fencing."},
            {"label": "Pond and canal banks", "slug": "pond-bank-clearing", "text": "Mechanical brush cutback on private pond, canal, and retention edges — not chemical pond spraying."},
        ],
        "unique_faqs": [
            (
                "Does Faith Works offer same-day estimates in Auburndale?",
                "Auburndale is our home base, so photo-based estimates and scheduling often move faster here than for distant travel jobs. Send property photos and your Auburndale address for the quickest review.",
            ),
            (
                "Can Faith Works clear land near Lake Ariana or Lake Juliana?",
                "Yes. Lake-adjacent lots and pond banks around Auburndale's small lakes are common requests — we match compact equipment to bank access and vegetation density after reviewing your photos. Pond work is mechanical bank clearing, not aquatic herbicide spraying.",
            ),
        ],
        "strip_note": "Home-base response for Auburndale land clearing, mulching, light demo, and pond bank work.",
    },
    "winter-haven-fl": {
        "meta_description": (
            "Winter Haven land clearing, forestry mulching, light demo, fence lines, stump removal, and pond bank "
            "clearing. Faith Works serves Chain of Lakes properties from nearby Auburndale."
        ),
        "hook": (
            "Winter Haven's Chain of Lakes geography puts overgrown lots, fence rows, leftover stumps, and pond edges "
            "at the center of outdoor property projects Faith Works handles in Polk County."
        ),
        "context": (
            "From downtown lakefront neighborhoods to Cypress Gardens Boulevard acreage, Winter Haven properties "
            "often combine managed front yards with unmanaged rear lots, old outbuildings, and bank edges that "
            "standard lawn crews will not touch with forestry or mulching equipment."
        ),
        "local_detail": (
            "Canal-side homes and larger lots toward Dundee and Eagle Lake frequently need brush cut back "
            "without disturbing seawalls or neighbor sight lines — scope is confirmed from photos before work."
        ),
        "property_types": [
            "Chain of Lakes homes with overgrown rear lots or canal banks",
            "Residential lots with rear conservation or wetland buffers",
            "Acreage parcels between Winter Haven and Haines City",
            "Vacant land near Cypress Gardens area being prepared for build",
            "Properties with old sheds, pads, or leftover stumps after tree work",
        ],
        "common_jobs": [
            "Land clearing and brush removal on overgrown rear lots",
            "Forestry mulching on sapling-choked acreage",
            "Light demolition of sheds and outdoor pads",
            "Fence line clearing and stump removal",
            "Pond and canal bank brush removal for visibility and access",
            "Outdoor storm debris cleanup along lakefront neighborhoods",
        ],
        "intent_routes": [
            {"label": "Rear lot and acreage clearing", "slug": "land-clearing", "text": "Reclaim usable space on overgrown lots across Winter Haven neighborhoods."},
            {"label": "Dense growth mulching", "slug": "forestry-mulching", "text": "Mulch thick undergrowth on Winter Haven acreage and wooded edges."},
            {"label": "Shed and pad demo", "slug": "demolition", "text": "Remove old sheds, lean-tos, and outdoor pads when access allows."},
            {"label": "Fence lines and stumps", "slug": "stump-removal", "text": "Clear leftover stumps and reopen fence rows after tree work or clearing."},
            {"label": "Chain of Lakes pond banks", "slug": "pond-bank-clearing", "text": "Mechanical brush cleanup on Winter Haven lake, canal, and retention edges."},
        ],
        "unique_faqs": [
            (
                "Does Faith Works work on Winter Haven canal and lake banks?",
                "Yes. Chain of Lakes properties often need pond bank and canal edge clearing — we review bank slope, access, and vegetation type from photos before confirming Winter Haven jobs. This is mechanical bank work, not algae or herbicide spraying.",
            ),
            (
                "Can you clear conservation buffers behind Winter Haven homes?",
                "We clear private outdoor property areas you own or maintain — not protected public conservation. Send photos showing property lines and access so scope stays accurate.",
            ),
        ],
        "strip_note": "Winter Haven land clearing, mulching, light demo, and Chain of Lakes pond bank work.",
    },
    "lakeland-fl": {
        "meta_description": (
            "Lakeland land clearing, forestry mulching, light demo, stump removal, driveway demo, and brush clearing "
            "from Faith Works. Photo-based estimates for lakefront, rear-lot, and south Polk properties."
        ),
        "hook": (
            "Lakeland spans from historic lakefront neighborhoods around Lake Morton and Lake Hollingsworth "
            "to rural land toward Mulberry and south Polk — each with different clearing, demo, and cleanup needs."
        ),
        "context": (
            "Faith Works handles Lakeland jobs where rear acreage, wooded buffers, old sheds, leftover stumps, "
            "failed driveways, and pond edges have outgrown routine maintenance. Compact equipment fits many "
            "in-town access constraints when photos show gate width, slopes, and obstacles clearly."
        ),
        "local_detail": (
            "South and southwest Lakeland toward the Polk Parkway often mix suburban lots with larger parcels "
            "needing forestry mulching, fence line work, stump removal, and debris haul-off in one project."
        ),
        "property_types": [
            "Historic district homes with large rear wooded sections",
            "Lake Morton and Lake Hollingsworth adjacent properties",
            "South Lakeland acreage toward Mulberry and Bartow",
            "Commercial and industrial pads with unmanaged perimeters",
            "Build-ready vacant parcels needing selective clearing or light demo",
        ],
        "common_jobs": [
            "Land clearing and rear acreage brush clearing on oversized Lakeland lots",
            "Forestry mulching on sapling-choked sections",
            "Light demolition and old driveway demo",
            "Fence line clearing and stump removal",
            "Pond and lake edge cleanup on private water features",
            "Ditch and swale vegetation maintenance on drainage easements",
        ],
        "intent_routes": [
            {"label": "Oversized lot clearing", "slug": "land-clearing", "text": "Clear dense growth on Lakeland lots too large for standard lawn service."},
            {"label": "South Polk mulching", "slug": "forestry-mulching", "text": "Mulch thick undergrowth on larger parcels toward Mulberry and Bartow."},
            {"label": "Shed, pad, and driveway demo", "slug": "demolition", "text": "Tear down outdoor structures and haul failed driveway sections when access allows."},
            {"label": "Stumps and fence rows", "slug": "stump-removal", "text": "Remove leftover stumps and reopen fence lines after clearing or tree work."},
            {"label": "Lakefront edge work", "slug": "pond-bank-clearing", "text": "Mechanical brush trim on private lake and pond banks across Lakeland neighborhoods."},
        ],
        "unique_faqs": [
            (
                "Does Faith Works serve north and south Lakeland equally?",
                "Yes. We travel throughout Lakeland within our service radius — from lakefront neighborhoods to south Polk acreage. Photos and address help confirm access and scheduling.",
            ),
            (
                "Can you work on Lakeland properties near Florida Southern or downtown lakes?",
                "Many downtown-adjacent lots have tight access. Send gate measurements and photos of the work area so we can confirm equipment fit before scheduling Lakeland jobs.",
            ),
        ],
        "strip_note": "Lakeland land clearing, mulching, light demo, stump removal, and pond bank projects.",
    },
}

CITY_PROFILES: dict[str, dict] = {**_BASE_CITY_PROFILES, **REMAINING_CITY_PROFILES}


def city_profile(slug: str) -> dict:
    if slug not in CITY_PROFILES:
        raise KeyError(f"Missing city profile for {slug}")
    return CITY_PROFILES[slug]

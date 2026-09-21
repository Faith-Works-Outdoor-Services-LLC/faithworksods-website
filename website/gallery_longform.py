"""Unique 750-word detail and scope pages for Faith Works gallery composites.

Ticket prices, streets, customer phones, and ticket numbers are never interpolated.
Each composite produces two distinct pages that share the branded proof image.
"""
from __future__ import annotations

import hashlib
import html
import random
import re
from typing import Any

from gallery_public_web import alt_place_phrase, sanitize_page_text, strip_html_words
from service_areas_data import CITIES, CITY_BY_SLUG, COUNTY_BY_NAME
from services_data import NOT_OFFERED, SERVICE_BY_SLUG

MIN_WORDS = 750
BRAND = "Faith Works Outdoor Services"
OWNER = "Tyler"

_CLUSTER_NEEDLES: list[tuple[str, tuple[str, ...]]] = [
    ("forestry_mulching", ("mulch", "forestry")),
    ("pond", ("pond", "shoreline", "bank", "lake front", "lakefront")),
    ("ditch", ("ditch", "swale")),
    ("stump", ("stump",)),
    ("fence", ("fence",)),
    ("driveway", ("driveway", "drive")),
    ("demo", ("demo", "demolition", "shed", "tear-down", "teardown")),
    ("pool", ("pool", "dig-out", "dig out")),
    ("storm", ("storm", "hurricane")),
    ("trail", ("trail", "access road")),
    ("acreage", ("acreage", "acre")),
    ("brush", ("brush", "overgrowth")),
    ("land_clearing", ("land clearing", "lot clearing", "clearing")),
    ("cleanup", ("cleanup", "debris", "haul")),
]

_SERVICE_HINTS: list[tuple[str, str]] = [
    ("forestry-mulching", "forestry-mulching"),
    ("lake front", "pond-bank-clearing"),
    ("lakefront", "pond-bank-clearing"),
    ("pond-bank", "pond-bank-clearing"),
    ("pond-cleanup", "pond-cleanup"),
    ("ditch-maintenance", "ditch-maintenance"),
    ("ditch", "ditch-clearing"),
    ("stump", "stump-removal"),
    ("fence", "fence-line-clearing"),
    ("driveway", "driveway-demo"),
    ("demolition", "demolition"),
    ("demo", "demolition"),
    ("pool", "pool-dig-out-support"),
    ("storm", "storm-debris-cleanup"),
    ("trail", "trail-clearing"),
    ("access-road", "access-road-clearing"),
    ("acreage", "acreage-cleanup"),
    ("lot-cleanup", "lot-cleanup"),
    ("brush", "brush-clearing"),
    ("overgrowth", "overgrowth-removal"),
    ("land-clearing", "land-clearing"),
    ("debris", "debris-removal"),
    ("cleanup", "property-cleanup"),
    ("tractor", "tractor-services"),
]


def infer_cluster(title: str, explicit: str = "") -> str:
    if explicit:
        return explicit
    lower = f"{title or ''}".lower()
    for cluster, needles in _CLUSTER_NEEDLES:
        if any(needle in lower for needle in needles):
            return cluster
    return "land_clearing"


def infer_service_slugs(title: str, existing: list[str] | None = None) -> list[str]:
    slugs: list[str] = []
    lower = f"{title or ''}".lower()
    for needle, slug in _SERVICE_HINTS:
        if needle in lower and slug in SERVICE_BY_SLUG and slug not in slugs:
            slugs.append(slug)
    for item in existing or []:
        slug = str(item or "").strip()
        if slug in SERVICE_BY_SLUG and slug not in slugs:
            slugs.append(slug)
    if not slugs:
        slugs.append("land-clearing")
    if "equipment-services" not in slugs:
        slugs.append("equipment-services")
    return slugs[:5]


def infer_city(text: str, *, fallback_city: str = "Auburndale") -> dict[str, str]:
    blob = f"{text or ''}"
    matches: list[dict[str, str]] = []
    for city in CITIES:
        name = city["name"]
        if re.search(rf"\b{re.escape(name)}\b", blob, flags=re.I):
            matches.append(city)
    if matches:
        matches.sort(key=lambda item: len(item["name"]), reverse=True)
        city = matches[0]
        return {
            "city_name": city["name"],
            "city_slug": city["slug"],
            "county_name": city["county"],
        }
    fallback = next((item for item in CITIES if item["name"] == fallback_city), None)
    if fallback:
        return {
            "city_name": fallback["name"],
            "city_slug": fallback["slug"],
            "county_name": fallback["county"],
        }
    return {"city_name": "Auburndale", "city_slug": "auburndale-fl", "county_name": "Polk County"}


def _esc(value: Any) -> str:
    return html.escape(str(value or "").strip())


def _seed(*parts: str) -> random.Random:
    digest = hashlib.sha256("|".join(parts).encode("utf-8")).hexdigest()
    return random.Random(int(digest, 16))


def _pick(rng: random.Random, options: list[str]) -> str:
    return options[rng.randrange(len(options))]


def _take(rng: random.Random, options: list[str], count: int) -> list[str]:
    pool = list(options)
    rng.shuffle(pool)
    return pool[: max(1, min(count, len(pool)))]


def _service_name(slug: str) -> str:
    service = SERVICE_BY_SLUG.get(slug) or {}
    return str(service.get("name") or slug.replace("-", " ").title())


def _county_slug(county_name: str) -> str:
    county = COUNTY_BY_NAME.get(county_name) or {}
    return str(county.get("slug") or "polk-county-fl")


def _photo_sentence(before: int, process: int, after: int) -> str:
    before = max(0, int(before or 0))
    process = max(0, int(process or 0))
    after = max(0, int(after or 0))
    if process:
        return (
            f"The branded composite on this page stacks {before} before photo"
            f"{'s' if before != 1 else ''}, {process} in-progress frame"
            f"{'s' if process != 1 else ''}, and {after} after photo"
            f"{'s' if after != 1 else ''} so a homeowner can see the starting condition, the work, and the finished ground in one proof image."
        )
    return (
        f"The branded composite on this page stacks {before} before photo"
        f"{'s' if before != 1 else ''} and {after} after photo"
        f"{'s' if after != 1 else ''} so the starting condition and the finished ground are visible in one proof image."
    )


def _cluster_detail_pool(cluster: str, city: str, county: str, service: str) -> list[str]:
    climate = (
        f"Central Florida vegetation in {city} and the rest of {county} does not pause for a tidy calendar. "
        f"Palmetto, Brazilian pepper, grapevine, and wet-season grasses thicken through the summer rains, then dry into a fire load by late winter. "
        f"That is why {service.lower()} here is not a one-afternoon yard cleanup. Access, soil moisture, and where the debris will go all change the work."
    )
    neighbors = (
        f"Residential and rural lots around {city} often share fence lines, pond easements, or a neighbor's citrus or pasture. "
        f"Faith Works keeps the work inside the agreed edges so the finished property is usable without pushing material onto the next parcel. "
        f"That boundary discipline is part of why photo estimates matter before a machine rolls."
    )
    result = (
        f"The after condition we want is simple to describe and hard to fake: the agreed vegetation is down, the travel path is open, and leftover material is piled, mulched, or hauled according to the written scope. "
        f"Homeowners in {county} can then walk the property, see grade issues that were hidden in the brush, and decide on the next outdoor step without guessing from a single thumbnail."
    )
    common = {
        "land_clearing": [
            f"This {city} land clearing job started as unmanaged growth that made the lot hard to walk, mow, or plan around. Brush, saplings, and vine hid the real grade and fence line.",
            f"Land clearing in {county} is usually a mix of cutting, mulching, and stacking. The right mix depends on how thick the stand is and whether the owner wants chips left as a ground cover or debris hauled off.",
            "Before photos show the wall of growth. Process photos show the machine path and the moment the lot starts to open. After photos show what is actually left on the ground — not a stock image of a tractor.",
            "We do not treat land clearing as site development. Underground utilities, stormwater design, and engineered pads stay with the trades licensed for that work. Sunshine 811 still belongs on the calendar before digging.",
            climate,
            neighbors,
            result,
            f"If a similar lot in {city} is too thick to photograph from the street, send several angles plus any pond, ditch, or fence you need protected. That is enough for a written photo estimate.",
        ],
        "forestry_mulching": [
            f"Forestry mulching on this {city} property was the faster way to reduce dense undergrowth without opening a giant burn pile. The machine grinds standing brush into a mulch layer instead of loading every stem.",
            f"Mulching is a good fit in {county} when the owner wants the lot opened and the chips left to suppress the next flush of weeds. It is the wrong tool when the material has to leave the property or when stumps must come out.",
            "Process frames on a mulching job usually show the head working a lane, then the same lane as a walkable carpet of chips. After photos should still show trunks, wet pockets, and fence wire so the scope stays honest.",
            climate,
            neighbors,
            result,
            "Mulch left on site is not a finished landscape bed. It is a working surface. Owners who want sod, gravel, or a building pad still need a follow-up conversation after the stand is down.",
            f"Send photos of canopy height, fence lines, and any trees to save. {BRAND} will say if mulching, cutting-and-hauling, or a mix is the honest scope.",
        ],
        "brush": [
            f"Brush and overgrowth on this {city} lot had closed the usable yard. Grapevine and palmetto make small equipment work slower than a mower owner expects, which is why the before column looks like a wall.",
            f"Brush clearing in {county} is often the first pass before fence-line work, a trail, or a pond bank. Getting the stand down is what lets everyone see the real problem.",
            climate,
            neighbors,
            result,
            "We keep ornamental trees and marked keepers out of the cutting path when they are identified before the job. Unmarked stems in the agreed clearing area come down with the rest of the stand.",
            "After brush work, leftover chips or piles should match the estimate. If haul-off was included, the after photos should not still show a debris mountain against the fence.",
            f"A similar {city} brush job starts with photos of the thickest corner and the access gate. That is more useful than a street-view screenshot.",
        ],
        "pond": [
            f"Pond bank work in {city} is mechanical shoreline clearing, not chemical algae treatment. The before photos usually show Brazilian pepper, cattail, or woody brush eating the usable bank.",
            f"Owners in {county} call when they cannot walk the bank, see the water, or keep a mower from dropping a wheel. Clearing the vegetation is the outdoor-property job; licensed aquatic pesticide work is not.",
            "Process photos matter on pond jobs because the machine has to stay on stable ground. After photos should show a walked bank and the vegetation that was left as a buffer, not a scraped bathtub.",
            climate,
            neighbors,
            result,
            "We do not spray ponds. If the water itself is the complaint, that is a different license and a different contractor. Faith Works stays on the bank, the brush, and the debris.",
            f"Photo estimates for pond banks should include the slope, the fence, and where a trailer can sit. Soft {city} shorelines change the equipment choice.",
        ],
        "ditch": [
            f"This ditch line in {city} had vegetation and silted debris that hid the flow path. Before photos show why water sat instead of moving after a storm.",
            f"Ditch clearing in {county} is outdoor maintenance with compact equipment, not a stormwater-system rebuild. We open the agreed line, pull vegetation, and leave the ditch inspectable.",
            climate,
            neighbors,
            result,
            "Utility locates still matter. Ditch work looks shallow until a blade finds a marked or unmarked line. Sunshine 811 is part of the prep, not an afterthought.",
            "After photos should show the opened line and the spoil placement. Spoil dumped onto a neighbor or into the road is not a completed ditch job.",
            f"If a {city} ditch clogs every wet season, say so in the estimate request. Maintenance after the first clearing is often cheaper than waiting for the next flood.",
        ],
        "stump": [
            f"Stump work on this {city} property was leftover after tree cutting or clearing. A stump that looks small in grass is a trip hazard and a mower killer once you start using the yard again.",
            f"Stump removal in {county} is excavation of the agreed stumps and root balls, then backfill or haul as written. It is not a promise to regrade the whole lot or to replant sod the same afternoon.",
            climate,
            neighbors,
            result,
            "Before photos should show each stump in context. After photos should show holes backfilled or the open hole if the owner asked to see the void before dirt goes back.",
            "Large trunks, buried concrete, or a stump against a foundation change the method. Those conditions belong in the photo set, not in a surprise on job day.",
            f"Send a wide shot and a close shot of each stump. That is how {BRAND} prices {city} stump work without guessing.",
        ],
        "fence": [
            f"Fence-line clearing in {city} is about reopening the row so the fence can be seen, repaired, or rebuilt — not installing a new fence. Before photos usually show vines and saplings fused to the wire or boards.",
            f"In {county}, fence rows collect Brazilian pepper and grapevine faster than interior yard. Clearing them without dropping the fence takes a slower pass than open-lot mulching.",
            climate,
            neighbors,
            result,
            "We do not rebuild fence as a licensed fence contractor on these pages. If a post is already failed, the clearing scope still stops at vegetation unless the written estimate says otherwise.",
            "After photos should show the opened line and any sections that were too rotten or buried to save. That honesty is the point of a proof page.",
            f"Mark the corners and any gate before the crew arrives. A {city} fence row is easy to over-cut when the property line is only a guess in the brush.",
        ],
        "demo": [
            f"This {city} outdoor demo job was a light tear-down — shed, pad, or leftover structure — not a commercial building demolition. Before photos show why the structure had to come down before the lot could be used.",
            f"Light demolition in {county} only proceeds when access, overhead lines, and what is inside the structure are understood. Hidden junk, fuel, or asbestos-looking material stops the machine until the owner decides.",
            climate,
            neighbors,
            result,
            "We do not run structural commercial demolition that belongs with a general contractor. Outdoor sheds, pads, and similar residential structures are the lane.",
            "After photos should show a clear pad or a dirt patch ready for the next use, plus the debris loaded or stacked as estimated.",
            f"Photo estimates for {city} demo need all four sides of the structure and the path a trailer will use. Tight side yards change the plan more than square footage does.",
        ],
        "driveway": [
            f"Old driveway demo in {city} is removal of the agreed surface so the owner can rebuild, regrade, or reclaim the lane. Before photos show cracked concrete, buried asphalt, or a failed shell drive.",
            f"Driveway demo in {county} is not new paving. Faith Works removes what is written, loads the spoil, and leaves the grade as agreed — not a finished asphalt job.",
            climate,
            neighbors,
            result,
            "Buried extras — irrigation, electric dog fence, unmarked drain pipe — show up during driveway demo. Photo estimates cannot see underground, which is why locates and a written out-of-scope note matter.",
            "After photos should show the opened lane and the truck path, not a staged landscaping shot that hides remaining slab.",
            f"If a {city} drive shares an easement, say so. Shared lanes change where spoil can sit.",
        ],
        "pool": [
            f"Pool dig-out support in {city} is cleanup and material handling around a pool builder's excavation — not installing the pool. Before photos show spoil piles, mud, and the mess a homeowner cannot move with a wheelbarrow.",
            f"In {county}, pool builders need compact equipment and haul-off more than another licensed pool contractor. Faith Works stays in that support lane.",
            climate,
            neighbors,
            result,
            "We do not build, plumb, or permit swimming pools. If the builder needs the spoil gone and the yard passable, that is the outdoor-property job on this page.",
            "After photos should show the agreed spoil gone and access restored, not a finished pool deck.",
            f"Coordinate the {city} visit with the pool builder's schedule. Dig-out support done on the wrong day just makes a new pile.",
        ],
        "storm": [
            f"Storm debris on this {city} property was vegetation and yard wreckage, not a roof or interior rebuild. Before photos show why a pickup and a rake were not going to finish it.",
            f"Storm cleanup in {county} fills dump trailers fast. The estimate has to say what leaves the property and what is mulched in place, because those are different days of work.",
            climate,
            neighbors,
            result,
            "We do not dry-in roofs or rebuild houses. Downed vegetation, fence-row blowdown, and yard debris are the outdoor scope.",
            "After photos should show travel paths open and debris either gone or in a single agreed pile for a later haul.",
            f"After a named storm, {city} owners should send photos the same day they want on the calendar. Access changes as neighbors start stacking in the right-of-way.",
        ],
        "trail": [
            f"Trail and access-road clearing in {city} is about a usable path for people, mowers, or equipment — not a county road. Before photos show where the lane disappeared into growth.",
            f"In {county}, a trail that stays wet will fail again if the scope only cuts tops and leaves roots and ruts. The written work should match how the owner actually uses the path.",
            climate,
            neighbors,
            result,
            "We do not build paved roads or stormwater systems. Compact-equipment trail opening and debris handling are the job.",
            "After photos should show width, overhead clearance, and any wet hole that still needs a later decision.",
            f"Mark keepers and gates on a {city} trail before the machine starts. A ribbon on a tree is cheaper than an argument after the cut.",
        ],
        "acreage": [
            f"Acreage cleanup in {city} is a larger outdoor property job than a suburban side yard. Before photos should show the stand, the fence, and how far the growth actually runs.",
            f"Owners in {county} often want a homestead pocket opened first, then a second pass on the back five. Phasing belongs in the estimate so the composite you see here matches the paid scope.",
            climate,
            neighbors,
            result,
            "Acreage work still is not site development. Pads, utilities, and engineered drainage stay with those trades.",
            "After photos on acreage should include a wide shot. Close-ups alone hide how much of the tract is still standing.",
            f"For a {city} acreage quote, include a simple sketch or pin of the priority acres. Photos without a boundary turn into a moving target.",
        ],
        "cleanup": [
            f"Property cleanup in {city} is the finish pass: vegetation down, debris staged, and the ground left in a condition a homeowner can walk. Before photos show the mess that made the lot feel abandoned.",
            f"Cleanup in {county} often follows clearing, a storm, or a demo. The composite is useful because customers can see that haul-off actually happened.",
            climate,
            neighbors,
            result,
            "Cleanup is not junk-hauling of household appliances unless the estimate says so. Outdoor vegetation, brush piles, and job debris are the default.",
            "After photos should show broom-clean or equipment-clean according to the write-up — those are different standards, and this page should not pretend they are the same.",
            f"If a {city} cleanup includes a burn pile or a dump run, that choice belongs in the estimate. It changes time and price more than people expect.",
        ],
    }
    common["land_clearing"] = common.get("land_clearing") or []
    return common.get(cluster) or common["land_clearing"]


def _cluster_scope_pool(cluster: str, city: str, county: str, service: str) -> list[str]:
    offered = (
        f"The written {service.lower()} scope for a {city} job is the only promise. "
        f"Photo estimates turn into a short list of what the machine will cut, what will be left standing, where debris goes, and what access the crew can use. "
        f"Anything not on that list stays off the property even if it would be convenient to grab while we are there."
    )
    not_offered = (
        "Faith Works does not install underground utilities, stormwater systems, sewer, water mains, or engineered drainage. "
        "Pond work is mechanical bank and shoreline clearing — not aquatic herbicide. "
        "Light outdoor demo is not a general-contractor building demolition. Those limits keep the gallery honest."
    )
    access = (
        f"Access in {county} decides the equipment more often than acreage does. A Kubota compact tractor or mini excavator that fits a residential gate is useless if the only entrance is a wet swale or a locked cattle gap nobody mentioned. "
        f"Scope pages exist so that conversation happens before the trailer is loaded."
    )
    debris = (
        f"Debris handling is its own line. Mulch in place, stack for the owner, or haul to a legal dump are three different jobs. "
        f"A {city} composite that looks 'done' in after photos still has to match whichever of those three was paid."
    )
    locate = (
        "Sunshine 811 belongs on the calendar at least two full business days before digging. "
        "Gallery pages are not a substitute for locates. If the scope includes stumps, driveway demo, or anything below grade, locates are part of being ready — not a surprise fee discussion in the driveway."
    )
    aftercare = (
        f"Florida rain in {county} will sprout a new flush through chips and disturbed soil. "
        f"Aftercare is usually mowing, a possible follow-up brush pass, or the owner's own herbicide plan — not a hidden second clearing unless it is written. "
        f"This scope page says that out loud so the composite is not mistaken for a permanent landscape."
    )
    extra = {
        "land_clearing": [
            f"Land-clearing scope in {city} usually names the vegetation types, the keepers, and whether stumps stay. A lot that is 'cleared' with stumps left is a different product than a lot ready for a mower.",
            "If forestry mulching is in the mix, the scope should say whether chips stay as a working surface. If haul-off is in the mix, it should say how many loads are included before extra dump runs.",
        ],
        "forestry_mulching": [
            f"Mulching scope in {city} should list maximum stem size the head will take and any trees tagged to save. Oversized trunks become a cutting-and-hauling change order, not a silent extra.",
            "Mulch depth varies. The scope is reduction of the stand, not a uniform four-inch landscape bed. Owners who need a pad or sod still have a second project.",
        ],
        "pond": [
            f"Pond-bank scope in {city} should name how close to water the machine may work and whether a vegetation buffer stays. Scraping to bare mud is rarely the right shoreline outcome.",
            "Aquatic weeds in the water column are out of scope without the proper pesticide license. Do not read a bank-clearing composite as algae treatment.",
        ],
        "ditch": [
            "Ditch scope should name the length, the spoil placement, and whether culverts are to be exposed or left buried. Cleaning a yard swale is not replacing a county outfall.",
            "Repeat ditch maintenance can be scheduled after the first opening. That is a separate scope, not an automatic subscription.",
        ],
        "stump": [
            f"Stump scope in {city} should count the stumps, note diameter, and say whether holes are backfilled with on-site soil or left open. Grind-only versus full root-ball removal are different prices.",
            "Concrete around a stump, buried fence, or a stump against a slab must be in the notes. Those are the conditions that stop a 'simple stump' job.",
        ],
        "fence": [
            "Fence-line scope is vegetation. Fence rebuild, new posts, and hog wire are outside unless the estimate explicitly adds them.",
            f"On a shared {city} line, both owners should know which side of the wire is being cut. Gallery composites cannot show a recorded survey.",
        ],
        "demo": [
            f"Demo scope in {city} should list the structure, what is inside it, and the dump plan. Unknown contents are a hold, not a guess.",
            "Utilities to a shed must be confirmed dead. Cutting a live conductor is not outdoor property work we will 'just do'.",
        ],
        "driveway": [
            "Driveway-demo scope names the material and the dump. It does not include a new paved surface.",
            "Thickness surprises happen. The scope should say how we handle extra depth or a second hidden slab.",
        ],
        "pool": [
            "Pool dig-out support scope is spoil, mud, and access — scheduled with the builder. It is not pool construction.",
            "If the builder changes the dig overnight, the Faith Works scope may need a same-day rewrite. Composites capture the day that was actually worked.",
        ],
        "storm": [
            f"Storm scope in {city} must separate vegetation from household contents. Mixed piles slow the machine and can be refused.",
            "Right-of-way debris that belongs to the county should not be silently added to a private-property composite.",
        ],
        "trail": [
            "Trail scope includes width and overhead clearance. A walking path and a tractor lane are different cuts.",
            "Wet holes on a trail may be flagged in after photos as remaining work rather than secretly filled with random debris.",
        ],
        "acreage": [
            f"Acreage scope in {city} should be drawn. 'The back' is not a measurement. The composite reflects the acres that were actually cut.",
            "Wildlife, cattle, and hunting stands belong in the walkthrough. They change lanes more than a map does.",
        ],
        "cleanup": [
            "Cleanup scope states the cleanliness standard: equipment-clean, pile-and-leave, or haul-all. Those three finish lines look different in after photos.",
            f"Household junk mixed into a {city} brush pile is a change. Say it in the estimate request.",
        ],
        "brush": [
            f"Brush scope in {city} should name the height class and whether ornamental beds are inside the cut. A 'take it all down' instruction still needs keepers marked.",
            "If a second pass after leaf-out is likely, put it in writing. Gallery pages should not imply a one-cut forever result in Florida.",
        ],
    }
    base = [
        offered,
        not_offered,
        access,
        debris,
        locate,
        aftercare,
        f"Equipment on {service.lower()} jobs is owner-operated compact machinery — typically Kubota tractor, loader, grapple, box blade, and mini excavator support matched to the gate and the ground. {OWNER} is the person who quoted the job and the person running the work, which is why the composite can be explained without a subcontractor chain.",
        f"Homeowners comparing {county} contractors should read this scope page against the service pages for {_service_name('land-clearing')}. The gallery proves a day of work; the service pages explain the offer for the next property.",
    ]
    base.extend(extra.get(cluster) or extra["land_clearing"])
    return base


def _detail_faqs(cluster: str, city: str, service: str) -> list[tuple[str, str]]:
    return [
        (
            f"Is this {city} photo from a real Faith Works job?",
            f"Yes. The composite is built from before, process, and after photos taken on the actual property. Addresses, ticket numbers, and prices are kept off the page. The image is here so you can judge {service.lower()} quality before you send your own photos.",
        ),
        (
            f"Can Faith Works do the same {service.lower()} on my lot?",
            f"If your property is in the service area and the access fits compact equipment, yes — after a photo estimate. {city} lots vary by wet ground, fence lines, and keepers, so the next job is never a copy-paste of this composite.",
        ),
        (
            "Why are there two gallery pages for one composite?",
            "The details page explains the problem and the finished condition. The scope page explains what was in and out of the work. Both carry the same proof image and both link to the service and area pages a homeowner actually needs.",
        ),
        (
            "Do you publish the street address?",
            f"No. Public gallery pages use city and county only. Send new photos from your {city} property when you want a quote — do not try to reverse-engineer a neighbor's address from a composite.",
        ),
    ]


def _scope_faqs(cluster: str, city: str, service: str) -> list[tuple[str, str]]:
    limits = "; ".join(NOT_OFFERED[:4])
    return [
        (
            f"What was actually included in this {service.lower()} scope?",
            f"Only the outdoor work described on this page and in the original written estimate: vegetation, debris handling, and compact-equipment time on the agreed {city} ground. Underground utilities and engineered systems were not included.",
        ),
        (
            "What do you not do on jobs like this?",
            f"{limits}. Read the related service pages if your need is adjacent but not the same.",
        ),
        (
            "Will you start from this composite without a new estimate?",
            f"No. This page is proof of a finished {city} job, not a price list. Send photos of your property for a current written estimate.",
        ),
        (
            "Do I need 811 locates?",
            "Yes whenever the work goes below grade — stumps, driveway demo, or digging. Call Sunshine 811 at least two full business days before that work. Clearing only above grade still needs a conversation about buried extras you already know about.",
        ),
    ]


def _links_html(
    *,
    root_prefix: str,
    service_slugs: list[str],
    city_slug: str,
    county_name: str,
    sibling_href: str,
    sibling_label: str,
) -> str:
    service_links = []
    for slug in service_slugs:
        name = _service_name(slug)
        service_links.append(f'<a href="{root_prefix}{slug}.html">{_esc(name)}</a>')
    extras = [
        f'<a href="{sibling_href}">{_esc(sibling_label)}</a>',
        f'<a href="{root_prefix}gallery.html">Project gallery</a>',
        f'<a href="{root_prefix}contact.html">Request an estimate</a>',
        f'<a href="{root_prefix}services.html">All outdoor services</a>',
    ]
    city = CITY_BY_SLUG.get(city_slug)
    if city:
        extras.append(f'<a href="{root_prefix}areas/{city_slug}.html">{_esc(city["name"])} service area</a>')
    county_slug = _county_slug(county_name)
    if county_name in COUNTY_BY_NAME:
        extras.append(f'<a href="{root_prefix}areas/{county_slug}.html">{_esc(county_name)} outdoor services</a>')
    extras.extend(
        [
            f'<a href="{root_prefix}about.html">About Faith Works</a>',
            f'<a href="{root_prefix}equipment-services.html">Equipment services</a>',
        ]
    )
    items = "".join(f"<li>{item}</li>" for item in service_links + extras)
    return f"<ul class=\"fw-project-links\">{items}</ul>"


def _p(text: str) -> str:
    return f"<p>{text}</p>"


def _h2(text: str) -> str:
    return f"<h2>{_esc(text)}</h2>"


def _ul(items: list[str]) -> str:
    return "<ul>" + "".join(f"<li>{item}</li>" for item in items) + "</ul>"


def _composite_figure(image_href: str, alt: str, caption: str) -> str:
    return (
        f'<figure class="fw-project-composite">'
        f'<img src="{_esc(image_href)}" alt="{_esc(alt)}" width="1600" height="900" loading="eager">'
        f"<figcaption>{_esc(caption)}</figcaption>"
        f"</figure>"
    )


def _filler_bank(kind: str, city: str, county: str, service: str) -> list[str]:
    if kind == "detail":
        return [
            f"A {city} homeowner reading this page should be able to match the composite to a real outdoor problem: growth that blocked a fence, a pond bank that could not be walked, a stump that wrecked a mower, or a lot that had not been opened in years. The {service.lower()} photos are the evidence, and the surrounding copy is here so searchers in {county} are not sent to a dead-end thumbnail.",
            f"Faith Works is owner-operated from Auburndale and takes {county} work when access, distance, and scope fit compact equipment. That is a narrower promise than a statewide directory listing, and it is the reason these gallery pages name {city} instead of pretending every Florida lot is identical.",
            f"Internal links on this details page exist for humans and for crawlers. A {service.lower()} proof image should not be an orphan file. It should sit next to the service page, the city page, the contact form, and the scope page that explains what the machine was allowed to do.",
            f"Central Florida soil in {city} can be sugar sand one week and standing water the next. After photos that look dry were not necessarily easy ground on the morning the trailer arrived. The composite is a record of the finished day, not a weather report, which is why the scope page still talks about access.",
            f"If you arrived from image search, stay long enough to read how {BRAND} documents work. The gold-and-black composite is branded on purpose so a stolen crop still points back to faithworksclearing.com. The longform is here so the URL is a real project page, not a lightbox.",
        ]
    return [
        f"Scope language has to survive a rainy {county} season. If this {service.lower()} composite is the only thing a {city} owner remembers, they may think every future flush of palmetto was included. It was not, unless the estimate said a return visit was included.",
        f"Written estimates still beat hallway conversations. Gallery scope pages repeat the same limits that live on the service pages so a crawler and a customer see one company position: outdoor property work, compact equipment, photo estimates, no utility contracting.",
        f"When two pages share one composite, they must not share one essay. This scope URL is the methods and boundaries page. The details URL is the problem and result page. Linking them keeps {city} proof usable without stuffing every sentence onto a single thin file.",
        f"Dump runs, chip beds, and owner-kept piles are not interchangeable. A {service.lower()} composite from {city} that looks tidy can still have been any of those three finishes. The scope page is where that distinction belongs.",
        f"If your project is outside {county}, check the service-area radius from Auburndale before you assume the trailer is coming. Distance, wet access, and a one-off tiny job can all be a no. The contact form is the honest next step.",
    ]


def _ensure_min_words(html_body: str, extras: list[str], rng: random.Random) -> str:
    body = html_body
    unused = list(extras)
    rng.shuffle(unused)
    while strip_html_words(body) < MIN_WORDS and unused:
        body += _p(unused.pop(0))
    if strip_html_words(body) < MIN_WORDS:
        raise RuntimeError("Gallery longform fell short of 750 words after extras were applied")
    return body


def _notes_sentence(notes: str) -> str:
    clean = sanitize_page_text(notes or "").strip()
    clean = re.sub(r"\s+", " ", clean)
    if len(clean) < 24:
        return ""
    if len(clean) > 280:
        clean = clean[:277].rsplit(" ", 1)[0] + "."
    return f"Crew notes that are safe to publish: {_esc(clean)}"


def build_gallery_longform(project: dict[str, Any], *, root_prefix: str = "../") -> dict[str, Any]:
    slug = str(project.get("id") or "project").strip()
    title = str(project.get("title") or slug.replace("-", " ")).strip()
    cluster = infer_cluster(title, str(project.get("cluster") or ""))
    city_bits = infer_city(
        " ".join(
            str(project.get(key) or "")
            for key in ("city_name", "city", "address", "title", "summary")
        ),
        fallback_city=str(project.get("city_name") or "Auburndale"),
    )
    if project.get("city_name"):
        explicit = str(project["city_name"]).strip()
        city_bits["city_name"] = explicit
        match = next((item for item in CITIES if item["name"].lower() == explicit.lower()), None)
        if match:
            city_bits["city_slug"] = match["slug"]
            city_bits["county_name"] = match["county"]
        else:
            city_bits["city_slug"] = ""
            named_county = str(project.get("county_name") or "").strip()
            if named_county:
                city_bits["county_name"] = named_county
            elif "panasoffkee" in explicit.lower():
                city_bits["county_name"] = "Sumter County"
            else:
                city_bits["county_name"] = "Central Florida"
    if project.get("city_slug") and str(project["city_slug"]) in CITY_BY_SLUG:
        city_bits["city_slug"] = str(project["city_slug"])
        city_bits["county_name"] = CITY_BY_SLUG[city_bits["city_slug"]]["county"]
    if project.get("county_name"):
        city_bits["county_name"] = str(project["county_name"])
    city = city_bits["city_name"]
    city_slug = city_bits["city_slug"]
    county = city_bits["county_name"]
    services = infer_service_slugs(title, list(project.get("service_slugs") or []))
    primary = services[0]
    service_name = _service_name(primary)
    before = int(project.get("photo_before") or 0)
    process = int(project.get("photo_process") or 0)
    after = int(project.get("photo_after") or 0)
    if before + after == 0:
        before, process, after = 2, 3, 2
    image_name = str(project.get("image") or f"gallery/{slug}.webp").replace("\\", "/").split("/")[-1]
    image_href = image_name
    place = alt_place_phrase(city, county)
    alt = f"{title} — before, process, and after {service_name.lower()} in {place} by {BRAND}"
    detail_path = f"gallery/{slug}.html"
    scope_path = f"gallery/{slug}-scope.html"

    detail_rng = _seed(slug, "detail")
    scope_rng = _seed(slug, "scope")
    detail_pool = _cluster_detail_pool(cluster, city, county, service_name)
    scope_pool = _cluster_scope_pool(cluster, city, county, service_name)
    detail_paras = _take(detail_rng, detail_pool, min(8, len(detail_pool)))
    scope_paras = _take(scope_rng, scope_pool, min(8, len(scope_pool)))
    notes = _notes_sentence(str(project.get("work_notes") or project.get("notes") or ""))

    detail_body = "".join(
        [
            _h2(f"What this {city} job looked like"),
            _p(detail_paras[0] if detail_paras else f"This {service_name.lower()} job in {city} is documented with a branded before, process, and after composite."),
            _composite_figure(image_href, alt, f"{title} | {place}"),
            _p(_photo_sentence(before, process, after)),
            _h2("The problem on the property"),
            "".join(_p(p) for p in detail_paras[1:4]),
            _p(notes) if notes else "",
            _h2("What the finished ground shows"),
            "".join(_p(p) for p in detail_paras[4:]),
            _p(
                f"If you need the same kind of {service_name.lower()} in {city} or elsewhere in {county}, start with the "
                f'<a href="{root_prefix}{primary}.html">{_esc(service_name)}</a> page, then send photos from the '
                f'<a href="{root_prefix}contact.html">estimate form</a>. The '
                f'<a href="{slug}-scope.html">scope of work page</a> for this composite explains what was in and out of the job.'
            ),
            _h2("Related Faith Works pages"),
            _p(
                f"Use these internal links to move from this {city} proof image to the service, city, and estimate pages that match a new project."
            ),
            _links_html(
                root_prefix=root_prefix,
                service_slugs=services,
                city_slug=city_slug,
                county_name=county,
                sibling_href=f"{slug}-scope.html",
                sibling_label="Scope of work for this job",
            ),
            _h2("Details FAQs"),
        ]
    )
    detail_faqs = _detail_faqs(cluster, city, service_name)
    detail_body += "".join(f"<h3>{_esc(q)}</h3>{_p(a)}" for q, a in detail_faqs)
    detail_body = _ensure_min_words(
        detail_body,
        [p for p in detail_pool if p not in detail_paras] + _filler_bank("detail", city, county, service_name),
        detail_rng,
    )
    detail_body = sanitize_page_text(detail_body)

    scope_lists = [
        f"Outdoor {service_name.lower()} inside the agreed {city} boundary",
        "Compact equipment matched to the access that was confirmed before the visit",
        "Debris handling exactly as written — mulch, stack, or haul",
        "Photo documentation used to build the public composite",
        "Direct communication with Tyler from estimate through the finished pass",
    ]
    out_lists = [
        "Underground utility installation or repair",
        "Stormwater, sewer, or water-main construction",
        "Aquatic herbicide or chemical pond treatment",
        "Licensed pool construction",
        "Structural commercial demolition beyond light outdoor tear-down",
    ]
    scope_body = "".join(
        [
            _h2(f"Scope of work for this {city} {service_name.lower()} job"),
            _p(scope_paras[0] if scope_paras else offered_fallback(city, service_name)),
            _composite_figure(image_href, alt, f"{title} scope proof | {place}"),
            _p(_photo_sentence(before, process, after)),
            _h2("In scope"),
            _ul(scope_lists),
            "".join(_p(p) for p in scope_paras[1:4]),
            _h2("Out of scope"),
            _ul(out_lists),
            "".join(_p(p) for p in scope_paras[4:]),
            _p(
                f"The companion <a href=\"{slug}.html\">project details page</a> explains the problem and the finished look. "
                f"For a new {city} estimate, use <a href=\"{root_prefix}contact.html\">contact</a> or the "
                f'<a href="{root_prefix}{primary}.html">{_esc(service_name)}</a> page. '
                f"City context lives on <a href=\"{root_prefix}areas/{city_slug}.html\">{_esc(city)} outdoor services</a>."
            ),
            _h2("Scope links"),
            _links_html(
                root_prefix=root_prefix,
                service_slugs=services,
                city_slug=city_slug,
                county_name=county,
                sibling_href=f"{slug}.html",
                sibling_label="Project details for this job",
            ),
            _h2("Scope FAQs"),
        ]
    )
    scope_faqs = _scope_faqs(cluster, city, service_name)
    scope_body += "".join(f"<h3>{_esc(q)}</h3>{_p(a)}" for q, a in scope_faqs)
    scope_body = _ensure_min_words(
        scope_body,
        [p for p in scope_pool if p not in scope_paras] + _filler_bank("scope", city, county, service_name),
        scope_rng,
    )
    scope_body = sanitize_page_text(scope_body)

    summary = (
        f"{service_name} in {city}, {county} — before, process, and after proof from {BRAND}. "
        f"See the project details and the written-style scope of work. Photo estimates. Owner-operated."
    )
    return {
        "id": slug,
        "cluster": cluster,
        "city_name": city,
        "city_slug": city_slug,
        "county_name": county,
        "service_slugs": services,
        "primary_service": primary,
        "image_filename": image_name,
        "alt": alt,
        "summary": summary[:220],
        "detail": {
            "path": detail_path,
            "title": f"{title} in {city} FL | {BRAND}",
            "h1": title,
            "meta": (
                f"{title} in {city}, {county} — before, process, and after {service_name.lower()} "
                f"by {BRAND}. Owner-operated. Free photo estimate."
            )[:158],
            "body_html": detail_body,
            "word_count": strip_html_words(detail_body),
            "faqs": detail_faqs,
        },
        "scope": {
            "path": scope_path,
            "title": f"Scope of Work: {title} in {city} FL | {BRAND}",
            "h1": f"Scope of work — {title}",
            "meta": (
                f"Scope of work for {title} in {city}, {county}: what {BRAND} included, excluded, "
                f"and documented on the before/process/after composite."
            )[:158],
            "body_html": scope_body,
            "word_count": strip_html_words(scope_body),
            "faqs": scope_faqs,
        },
    }


def offered_fallback(city: str, service_name: str) -> str:
    return (
        f"The written {service_name.lower()} scope for this {city} job is the outdoor work that was actually photographed: "
        "vegetation, debris handling, and compact equipment inside the agreed boundary."
    )

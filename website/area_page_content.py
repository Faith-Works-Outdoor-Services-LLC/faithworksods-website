"""SEO / AEO / GEO content generators for city and county service area pages."""

from __future__ import annotations

from service_areas_data import (
    COUNTIES,
    COUNTY_BY_NAME,
    HOME_CITY,
    HOME_ZIP,
    SERVICE_RADIUS_MILES,
    cities_in_county,
)
from services_data import (
    NOT_OFFERED,
    NOT_OFFERED_NOTE,
    SERVICE_CATEGORIES,
    SERVICES,
    SITE_POSITIONING,
    services_for_category,
)

BRAND = "Faith Works Outdoor Services"
OWNER = "Tyler R. Edwards"

COUNTY_PROFILES: dict[str, dict] = {
    "Polk County": {
        "region": "Central Florida's lake country",
        "terrain": "flat to gently rolling land with lakes, ponds, citrus groves, pasture, and mixed residential acreage",
        "property_types": [
            "Residential lots with overgrown back acreage",
            "Lakefront and pond-adjacent homes",
            "Rural homesteads and small farms",
            "Vacant land and build-ready parcels",
            "Commercial and church property with unmanaged edges",
        ],
        "common_jobs": [
            "Overgrown lot and acreage clearing before fencing or building",
            "Pond bank brush removal and visibility cleanup",
            "Ditch and swale vegetation clearing after rainy seasons",
            "Trail and access path reopening across larger properties",
            "Storm debris and yard cleanup after wind events",
            "Pool dig-out dirt removal support under licensed pool builders",
        ],
        "local_note": (
            "Polk County properties often combine open pasture, wooded edges, and water features — "
            "which means brush, pond banks, and ditch lines need ongoing outdoor maintenance, not just one-time mowing."
        ),
        "nearby_counties": ["Osceola County", "Hillsborough County", "Lake County", "Hardee County", "Highlands County"],
    },
    "Osceola County": {
        "region": "south Central Florida",
        "terrain": "a mix of suburban growth corridors, ranch land, and rural acreage south of Polk County",
        "property_types": [
            "Subdivision lots with rear conservation or wet areas",
            "Ranch and equestrian properties with fence lines to maintain",
            "Retention pond edges near newer development",
            "Acreage parcels between Kissimmee and Poinciana",
            "Vacant land being prepared for future use",
        ],
        "common_jobs": [
            "Brush clearing along fence lines and property boundaries",
            "Retention and pond edge cleanup where growth has taken over",
            "Access road and trail clearing on multi-acre parcels",
            "Forestry mulching for overgrown sections of acreage",
            "Debris haul-off after clearing or storm cleanup",
            "Ongoing ditch and drainage path vegetation removal",
        ],
        "local_note": (
            "Osceola County includes fast-growing communities and large rural parcels — "
            "property owners often need equipment that can work around ponds, tree lines, and long fence runs."
        ),
        "nearby_counties": ["Polk County", "Orange County", "Lake County", "Highlands County"],
    },
    "Orange County": {
        "region": "Greater Orlando",
        "terrain": "suburban residential neighborhoods, larger lot subdivisions, and rural edges toward Apopka and west Orange",
        "property_types": [
            "Oversized residential lots with unmanaged rear acreage",
            "Properties backing to woods, ponds, or conservation",
            "Small-acreage homes needing brush and trail work",
            "Land being opened for outbuildings, fencing, or access",
            "Post-storm yard and property debris cleanup",
        ],
        "common_jobs": [
            "Back-lot and rear acreage brush clearing",
            "Pond and wet-area edge cleanup where allowed on private property",
            "Fence line and boundary clearing",
            "Forestry mulching for dense undergrowth",
            "Property and lot cleanup before listing or building",
            "Trail clearing for access to barns, sheds, or rear fields",
        ],
        "local_note": (
            "Orange County homeowners often call when rear acreage, pond edges, or conservation borders "
            "have grown beyond what a lawn service can handle — that is where outdoor property equipment makes the difference."
        ),
        "nearby_counties": ["Osceola County", "Lake County", "Polk County", "Seminole County"],
    },
    "Lake County": {
        "region": "Florida's lake and hill country",
        "terrain": "rolling terrain with lakes, horse properties, rural acreage, and lake-country residential lots",
        "property_types": [
            "Lakefront homes with steep or overgrown banks",
            "Horse and equestrian properties with paddock edges",
            "Rural acreage with woods and pasture mix",
            "Residential lots with pond or retention features",
            "Vacant land needing selective clearing",
        ],
        "common_jobs": [
            "Pond bank and lake edge brush removal",
            "Trail and driveway access clearing on acreage",
            "Forestry mulching in wooded sections",
            "Fence line and pasture edge maintenance",
            "Property cleanup after years of deferred maintenance",
            "Ditch and runoff path vegetation clearing",
        ],
        "local_note": (
            "Lake County's mix of hills, lakes, and larger lots creates unique access challenges — "
            "compact equipment and experienced operators matter when banks, slopes, and tree lines are involved."
        ),
        "nearby_counties": ["Orange County", "Polk County", "Sumter County", "Marion County"],
    },
    "Hillsborough County": {
        "region": "Tampa Bay's eastern corridor",
        "terrain": "suburban Brandon and Valrico neighborhoods, agricultural land around Plant City, and rural edges toward Pasco",
        "property_types": [
            "Suburban homes with large back lots or wooded rear acreage",
            "Plant City and eastern Hillsborough rural parcels",
            "Properties with ditches, ponds, or retention areas",
            "Acreage being cleared for fencing, barns, or access",
            "Post-storm debris and brush cleanup",
        ],
        "common_jobs": [
            "Land and lot clearing on residential acreage",
            "Brush cutting and forestry mulching along overgrown edges",
            "Ditch clearing where vegetation blocks runoff paths",
            "Pond bank cleanup on private water features",
            "Access road and trail reopening",
            "Pool dig-out support under licensed pool contractors",
        ],
        "local_note": (
            "From Plant City strawberry country to Brandon subdivisions with oversized lots, Hillsborough properties "
            "often need the same core outdoor services: clear growth, open access, and haul debris — without utility excavation work."
        ),
        "nearby_counties": ["Polk County", "Pasco County", "Manatee County"],
    },
    "Pasco County": {
        "region": "north of Tampa Bay",
        "terrain": "rolling rural Pasco, Zephyrhills highlands, and growing Wesley Chapel subdivisions with larger lots",
        "property_types": [
            "Rural acreage and homestead parcels",
            "Equestrian and hobby farm properties",
            "Large-lot subdivisions with rear wooded areas",
            "Vacant land and future build sites",
            "Properties with pond or ditch maintenance needs",
        ],
        "common_jobs": [
            "Acreage and overgrown lot clearing",
            "Trail and access path cutting through wooded sections",
            "Fence line and boundary brush removal",
            "Forestry mulching for dense undergrowth",
            "Pond bank and ditch edge cleanup",
            "Storm and yard debris removal",
        ],
        "local_note": (
            "Pasco County still has substantial rural land alongside fast-growing suburbs — "
            "property owners often need one contractor who can handle brush, trails, ponds, and debris on the same visit."
        ),
        "nearby_counties": ["Hillsborough County", "Polk County", "Sumter County", "Hernando County"],
    },
    "Hardee County": {
        "region": "south Central Florida ranch country",
        "terrain": "agricultural acreage, cattle ranch land, and rural homesteads",
        "property_types": [
            "Cattle ranch and pasture properties",
            "Large rural acreage parcels",
            "Homesteads with overgrown fence lines",
            "Vacant agricultural land",
            "Properties with pond or ditch edges needing cleanup",
        ],
        "common_jobs": [
            "Fence line and pasture edge clearing",
            "Access road and trail maintenance across acreage",
            "Overgrowth removal in unused sections of ranch land",
            "Forestry mulching for thick brush and saplings",
            "Pond bank brush removal",
            "Debris haul-off after clearing projects",
        ],
        "local_note": (
            "Hardee County work is often about reopening access — fence lines, ranch roads, and pond edges "
            "that have grown shut after a season or two without equipment maintenance."
        ),
        "nearby_counties": ["Polk County", "DeSoto County", "Highlands County", "Manatee County"],
    },
    "Highlands County": {
        "region": "south Central Florida lake plateau",
        "terrain": "lakes, rural residential lots, and agricultural acreage around Sebring and Avon Park",
        "property_types": [
            "Lakefront and pond-adjacent homes",
            "Rural residential acreage",
            "Vacant land and small farms",
            "Properties with unmanaged ditch or swale lines",
            "Lots needing cleanup before sale or development",
        ],
        "common_jobs": [
            "Land and lot clearing for usable space",
            "Pond bank and lake edge brush removal",
            "Property cleanup after deferred maintenance",
            "Trail and access clearing on multi-acre parcels",
            "Storm debris and yard cleanup",
            "Forestry mulching in wooded sections",
        ],
        "local_note": (
            "Highlands County properties frequently combine water features with unmanaged edges — "
            "pond banks, ditches, and back-acreage brush are common reasons owners reach out."
        ),
        "nearby_counties": ["Polk County", "Hardee County", "Osceola County", "Okeechobee County"],
    },
    "DeSoto County": {
        "region": "southwest Central Florida ranch land",
        "terrain": "wide-open pasture, cattle ranch acreage, and rural homesteads centered on Arcadia",
        "property_types": [
            "Large ranch and agricultural parcels",
            "Rural homestead acreage",
            "Vacant land needing selective clearing",
            "Properties with pond or drainage ditch edges",
            "Fence line and boundary maintenance projects",
        ],
        "common_jobs": [
            "Acreage cleanup and overgrowth removal",
            "Fence line and ranch road clearing",
            "Forestry mulching on overgrown sections",
            "Pond bank brush cutting",
            "Access trail reopening",
            "Debris removal after clearing or storms",
        ],
        "local_note": (
            "DeSoto County jobs often cover larger acreage with long fence runs and pond edges — "
            "equipment mobility and clear scope planning matter before work begins."
        ),
        "nearby_counties": ["Hardee County", "Manatee County", "Sarasota County", "Charlotte County"],
    },
    "Sumter County": {
        "region": "Central Florida's growing retirement and acreage corridor",
        "terrain": "The Villages area growth, Bushnell rural land, and rolling acreage between Orlando and Ocala",
        "property_types": [
            "Acreage homes with pond or retention features",
            "Rural parcels with overgrown edges",
            "Properties needing trail or access clearing",
            "Lots being prepared for fencing or outbuildings",
            "Homes with ditch or swale vegetation buildup",
        ],
        "common_jobs": [
            "Brush and overgrowth removal on acreage lots",
            "Pond bank and water-edge cleanup",
            "Property cleanup before move-in or sale",
            "Trail and access path clearing",
            "Forestry mulching in wooded sections",
            "Ditch line vegetation removal",
        ],
        "local_note": (
            "Sumter County includes both active retirement communities and rural acreage — "
            "owners often want outdoor property work handled carefully around homes, ponds, and established landscaping."
        ),
        "nearby_counties": ["Lake County", "Marion County", "Pasco County", "Polk County"],
    },
    "Manatee County": {
        "region": "Tampa Bay's southern reach",
        "terrain": "Bradenton suburban neighborhoods, Parrish growth areas, and rural edges within travel range from Auburndale",
        "property_types": [
            "Suburban homes with larger back lots",
            "Rural Parrish and eastern Manatee acreage",
            "Properties with pond or ditch maintenance needs",
            "Vacant land being opened for use",
            "Post-storm property cleanup projects",
        ],
        "common_jobs": [
            "Land and lot clearing on residential acreage",
            "Brush cutting and forestry mulching",
            "Pond bank edge cleanup",
            "Fence line and boundary clearing",
            "Debris removal after clearing or weather events",
            "Pool dig-out support under licensed pool contractors",
        ],
        "local_note": (
            "Northern Manatee County properties within our travel range often mirror Polk and Hillsborough jobs — "
            "overgrown edges, pond banks, and acreage cleanup rather than utility or site-development excavation."
        ),
        "nearby_counties": ["Hillsborough County", "Polk County", "Sarasota County", "DeSoto County"],
    },
}

CITY_HOOKS: dict[str, str] = {
    "auburndale-fl": (
        f"As our home base in {HOME_ZIP}, Auburndale is where Faith Works Outdoor Services is rooted — "
        "with quick response across Polk County lake country and nearby communities."
    ),
    "lakeland-fl": (
        "Lakeland sits between Tampa and Orlando with in-town residential lots, lake-adjacent properties, "
        "and rural land toward Mulberry and south Polk — a common mix of pond banks, acreage edges, and overgrown rear lots."
    ),
    "winter-haven-fl": (
        "Winter Haven's Chain of Lakes area means many properties combine residential yards with pond edges, "
        "ditch lines, and back-lot growth that standard lawn services cannot tackle."
    ),
    "orlando-fl": (
        "Orlando homeowners and property owners often need rear-acreage clearing, pond edge cleanup, and brush removal "
        "on larger lots — especially where properties back to woods, water, or conservation areas."
    ),
    "kissimmee-fl": (
        "Kissimmee and nearby Osceola communities include both suburban lots with wet rear areas and larger rural parcels "
        "where fence lines, ponds, and access trails need equipment-based clearing."
    ),
    "plant-city-fl": (
        "Plant City and eastern Hillsborough combine agricultural acreage with suburban neighborhoods — "
        "property owners call for brush clearing, ditch work, and land cleanup on a wide range of lot sizes."
    ),
    "clermont-fl": (
        "Clermont's rolling lake-country terrain often means steeper pond banks, wooded acreage edges, "
        "and trail access that benefits from compact equipment and experienced outdoor property operators."
    ),
    "the-villages-fl": (
        "The Villages area includes many acreage-style homes with ponds, retention features, and rear property lines "
        "that need periodic brush cutting and outdoor cleanup beyond routine yard maintenance."
    ),
    "tampa-fl": (
        "Tampa properties within our travel range often involve larger suburban lots, rear wooded acreage, "
        "or pond and ditch edges where forestry mulching and brush cutting open usable space again."
    ),
}


def county_profile(county_name: str) -> dict:
    return COUNTY_PROFILES.get(county_name, {
        "region": "Central Florida",
        "terrain": "residential, rural, and acreage properties",
        "property_types": ["Residential lots", "Rural acreage", "Vacant land", "Properties with ponds or ditches"],
        "common_jobs": ["Land clearing", "Brush cutting", "Pond bank cleanup", "Debris removal", "Trail clearing"],
        "local_note": f"Property owners across {county_name} often need outdoor clearing, mulching, and cleanup — not utility excavation.",
        "nearby_counties": [],
    })


def city_page_title(city_name: str) -> str:
    return f"{SITE_POSITIONING} in {city_name}, FL"


def city_meta_description(city_name: str, county_name: str) -> str:
    return (
        f"{BRAND} serves {city_name}, {county_name} with land clearing, pond bank clearing, ditch clearing, "
        f"forestry mulching, brush cutting, debris removal, acreage cleanup, and outdoor property services. "
        f"Owner-operated from {HOME_CITY}, FL ({HOME_ZIP}) — {SERVICE_RADIUS_MILES}-mile service radius. "
        f"Free photo-based estimates. Call (863) 272-1596."
    )


def county_meta_description(county_name: str, city_count: int) -> str:
    return (
        f"{BRAND} serves {county_name}, FL — {city_count} cities including land clearing, pond bank clearing, "
        f"ditch clearing, brush cutting, forestry mulching, debris removal, and outdoor property cleanup. "
        f"Based in {HOME_CITY} within {SERVICE_RADIUS_MILES} miles. Free estimates."
    )


def _list_html(items: list[str]) -> str:
    return "<ul>\n" + "\n".join(f"            <li>{item}</li>" for item in items) + "\n          </ul>"


def area_services_by_category(root_prefix: str, place_name: str) -> str:
    blocks = ""
    for cat in SERVICE_CATEGORIES:
        group = services_for_category(cat["id"])
        if not group:
            continue
        links = "\n".join(
            f'              <li><a href="{root_prefix}{s["slug"]}.html">{s["nav"]} in {place_name}</a> — {s["desc"].split(".")[0]}.</li>'
            for s in group
        )
        blocks += f"""
          <div class="area-service-group">
            <h3>{cat["label"]}</h3>
            <p>{cat["description"]}</p>
            <ul class="area-service-list">
{links}
            </ul>
          </div>"""
    return blocks


def area_intent_cards(root_prefix: str, place_name: str, intent_routes: list[dict]) -> str:
    cards = ""
    for i, item in enumerate(intent_routes):
        label = SERVICE_BY_SLUG_LABEL(item["slug"])
        cards += f"""
          <article class="intent-card" data-fw-enter="bottom" style="--fw-enter-delay: {(i % 6) * 60}ms;">
            <h3><a href="{root_prefix}{item['slug']}.html">{item['label']} in {place_name}</a></h3>
            <p>{item['text']}</p>
            <a class="intent-card__cta" href="{root_prefix}{item['slug']}.html">Learn about {label} &rarr;</a>
          </article>"""
    return f'<div class="intent-grid area-intent-grid">{cards}\n        </div>'


def SERVICE_BY_SLUG_LABEL(slug: str) -> str:
    for s in SERVICES:
        if s["slug"] == slug:
            return s["nav"]
    return slug.replace("-", " ").title()


def city_intro_html(city: dict) -> str:
    name = city["name"]
    county = city["county"]
    profile = county_profile(county)
    hook = CITY_HOOKS.get(city["slug"], "")
    hook_para = f"<p>{hook}</p>" if hook else ""
    return f"""
          <h2>Land Clearing &amp; Outdoor Property Services in {name}, {county}</h2>
          {hook_para}
          <p>
            {BRAND} helps property owners in <strong>{name}, Florida</strong> reclaim usable outdoor space through
            {SITE_POSITIONING.lower()}. Based in {HOME_CITY} ({HOME_ZIP}), we travel throughout {county} and
            Central Florida within approximately <strong>{SERVICE_RADIUS_MILES} miles</strong> of our Auburndale base.
          </p>
          <p>
            {name} sits in {profile['region']} where {profile['terrain']}. {profile['local_note']}
            Whether you need an overgrown lot opened up, a pond bank cleaned back, a ditch line cleared, or storm debris
            hauled away, {OWNER} reviews your photos and confirms scope before scheduling.
          </p>
          <p>
            Faith Works is owner-operated outdoor property service — not a utility excavation contractor. We do not install
            underground utilities, stormwater systems, sewer lines, water mains, engineered drainage, or pools. Pool
            dig-out support is available under licensed pool contractors when your builder needs dirt removal and site cleanup.
          </p>"""


def city_property_section(city: dict) -> str:
    name = city["name"]
    profile = county_profile(city["county"])
    return f"""
          <h2>Property Types We Serve in {name}, FL</h2>
          <p>
            {name} property owners call Faith Works for a wide range of outdoor projects. Common property types include:
          </p>
          {_list_html(profile["property_types"])}
          <p>
            If your {name} property has unmanaged growth, blocked access, pond or ditch edges that need attention, or debris
            piled after clearing or weather events, send photos through our estimate form — that is the fastest way to get an
            accurate scope review.
          </p>"""


def city_common_jobs_section(city: dict) -> str:
    name = city["name"]
    county = city["county"]
    profile = county_profile(county)
    return f"""
          <h2>Common Outdoor Projects in {name}, {county}</h2>
          <p>These are the jobs {name} and {county} property owners request most often:</p>
          {_list_html(profile["common_jobs"])}
          <p>
            Every property is different. Access, vegetation density, water edges, and debris volume all affect equipment choice
            and scheduling. That is why Faith Works uses photo-based estimates before confirming {name} jobs.
          </p>"""


def city_process_section(city_name: str) -> str:
    return f"""
          <h2>How to Get Service in {city_name}, FL</h2>
          <div class="process-grid area-process-grid">
            <article class="process-step">
              <span>1</span>
              <h3>Send Photos</h3>
              <p>Upload property photos, your {city_name} address or cross streets, and a short description of what you need cleared or cleaned up.</p>
            </article>
            <article class="process-step">
              <span>2</span>
              <h3>Scope Review</h3>
              <p>{OWNER} reviews access, vegetation, pond or ditch edges, debris, and equipment needs — then follows up with next steps.</p>
            </article>
            <article class="process-step">
              <span>3</span>
              <h3>Estimate &amp; Schedule</h3>
              <p>Once scope is clear, you receive pricing and scheduling options for your {city_name} property before work begins.</p>
            </article>
            <article class="process-step">
              <span>4</span>
              <h3>Outdoor Property Work</h3>
              <p>Faith Works completes clearing, mulching, brush cutting, cleanup, or debris removal — outdoor property services only, not utility excavation.</p>
            </article>
          </div>"""


def city_scope_section() -> str:
    not_offered = "\n".join(f"            <li>{item}</li>" for item in NOT_OFFERED)
    return f"""
          <h2>What Faith Works Does &amp; Does Not Do</h2>
          <h3>Outdoor property services we provide</h3>
          <p>{SITE_POSITIONING} — including all {len(SERVICES)} service pages listed on this site, from land clearing and forestry mulching to pond bank work, ditch clearing, debris removal, and tractor services.</p>
          <h3>Work we do not perform</h3>
          <p>{NOT_OFFERED_NOTE}</p>
          <ul>
{not_offered}
          </ul>
          <p class="utility-note"><strong>Sunshine 811:</strong> For any digging or soil-moving work, contact Sunshine 811 at least two full business days before work begins so underground utilities can be marked.</p>"""


def city_area_faqs(city_name: str, county_name: str) -> list[tuple[str, str]]:
    return [
        (
            f"Does Faith Works Outdoor Services serve {city_name}, FL?",
            f"Yes. {BRAND} serves {city_name} in {county_name} from our base in {HOME_CITY}, Florida ({HOME_ZIP}). {city_name} is within our approximately {SERVICE_RADIUS_MILES}-mile service radius. Send photos and your project details for a free estimate.",
        ),
        (
            f"What land clearing services are available in {city_name}, FL?",
            f"Faith Works provides land clearing, forestry mulching, brush clearing, trail clearing, pond bank clearing, ditch clearing, debris removal, acreage cleanup, pool dig-out support, and tractor services in {city_name}. See our service pages for full details on each outdoor property service.",
        ),
        (
            f"How do I get a free estimate for outdoor property work in {city_name}?",
            f"Use the contact form on this page or visit our contact page. Upload photos of the area you need cleared or cleaned in {city_name}, include your phone number, and describe access notes or deadlines. {OWNER} reviews the scope and follows up directly.",
        ),
        (
            f"Does Faith Works clear pond banks and ditches near {city_name}?",
            f"Yes. Pond bank clearing and ditch clearing are core services in {city_name} and throughout {county_name}. We remove brush and vegetation from outdoor pond edges and ditch lines using mulching equipment, brush cutters, and tractors — not engineered stormwater or utility system installation.",
        ),
        (
            f"How far does Faith Works travel from Auburndale to {city_name}?",
            f"Faith Works is based in {HOME_CITY} and regularly travels up to about {SERVICE_RADIUS_MILES} miles for outdoor property jobs. {city_name} is within that Central Florida service area. Travel and scheduling are confirmed when {OWNER} reviews your estimate request.",
        ),
        (
            f"Is Faith Works an excavation contractor in {city_name}?",
            f"No. Faith Works is not a utility excavation contractor. We focus on {SITE_POSITIONING.lower()} — outdoor clearing, mulching, cleanup, and maintenance. We do not install sewer systems, stormwater infrastructure, water mains, or pools.",
        ),
        (
            f"Can Faith Works help with rural acreage near {city_name}?",
            f"Yes. Many {city_name} and {county_name} jobs involve rural acreage, fence lines, access trails, and pond edges. Forestry mulching, brush cutting, and acreage cleanup are common requests for larger properties outside dense neighborhoods.",
        ),
        (
            f"What should I include when requesting service in {city_name}?",
            f"Include your {city_name} address or nearest cross streets, photos of the work area, vegetation or debris type, access notes (gates, slopes, water edges), and any deadline. The more detail you provide, the faster Faith Works can confirm scope and scheduling.",
        ),
        (
            f"Does Faith Works offer storm debris cleanup in {city_name}, FL?",
            f"Yes, when access and scope allow. After wind or storm events, {city_name} property owners often need limbs, brush piles, and blocked areas cleared. Send photos of storm debris and property access for the fastest response.",
        ),
        (
            f"Who owns Faith Works Outdoor Services?",
            f"{OWNER} owns and operates {BRAND}. {city_name} clients work directly with the owner from estimate through completion — not through a subcontractor chain.",
        ),
    ]


def county_intro_html(county: dict, cities: list[dict]) -> str:
    profile = county_profile(county["name"])
    city_names = ", ".join(c["name"] for c in cities[:8])
    extra = f", and more" if len(cities) > 8 else ""
    return f"""
          <h2>{SITE_POSITIONING} Across {county['name']}</h2>
          <p>
            {BRAND} serves property owners throughout <strong>{county['name']}, Florida</strong> from our home base in
            {HOME_CITY} ({HOME_ZIP}). We travel within approximately {SERVICE_RADIUS_MILES} miles for land clearing,
            pond bank clearing, ditch clearing, brush cutting, forestry mulching, debris removal, and outdoor property cleanup.
          </p>
          <p>
            {county['name']} is part of {profile['region']}, where {profile['terrain']}. {profile['local_note']}
          </p>
          <p>
            Cities and communities we serve in {county['name']} include <strong>{city_names}</strong>{extra}.
            Each city page includes localized service details, FAQs, and a photo-based estimate form.
          </p>
          <p>
            Faith Works is owner-operated by {OWNER}. You get direct communication from estimate through job completion —
            not a call-center handoff. We focus on outdoor property work, not utility trenching, engineered drainage, or pool installation.
          </p>"""


def county_property_section(county_name: str) -> str:
    profile = county_profile(county_name)
    return f"""
          <h2>Property Types in {county_name}</h2>
          <p>{county_name} property owners across {profile['region']} commonly need help with:</p>
          {_list_html(profile["property_types"])}
          <h2>Common Projects in {county_name}</h2>
          {_list_html(profile["common_jobs"])}"""


def county_area_faqs(county_name: str, cities: list[dict]) -> list[tuple[str, str]]:
    city_sample = ", ".join(c["name"] for c in cities[:5])
    extra = " and surrounding communities" if len(cities) > 5 else ""
    return [
        (
            f"What cities does Faith Works serve in {county_name}?",
            f"Faith Works serves {len(cities)} communities in {county_name}, including {city_sample}{extra}. See the city links on this page for localized service details and estimates.",
        ),
        (
            f"Does Faith Works provide land clearing in {county_name}, FL?",
            f"Yes. Land clearing, forestry mulching, brush cutting, and acreage cleanup are core services throughout {county_name}. Faith Works is based in {HOME_CITY} and travels within approximately {SERVICE_RADIUS_MILES} miles.",
        ),
        (
            f"How do I request an outdoor property estimate in {county_name}?",
            f"Choose your city on this page or use our contact form. Upload property photos, describe the clearing or cleanup needed, and include access notes. {OWNER} reviews scope and follows up directly.",
        ),
        (
            f"Does Faith Works clear pond banks and ditches in {county_name}?",
            f"Yes. Pond bank clearing, pond cleanup, ditch clearing, and ditch maintenance are available across {county_name} for private outdoor property — not engineered stormwater or utility installation.",
        ),
        (
            f"Is Faith Works licensed for utility excavation in {county_name}?",
            f"No. Faith Works does not perform utility trenching, storm sewer installation, water main work, site development excavation, or pool contracting. The focus is {SITE_POSITIONING.lower()}.",
        ),
        (
            f"How far will Faith Works travel into {county_name}?",
            f"Faith Works serves {county_name} within an approximately {SERVICE_RADIUS_MILES}-mile radius from {HOME_CITY} ({HOME_ZIP}). Send your address and photos — travel and scheduling are confirmed during estimate review.",
        ),
        (
            f"What equipment does Faith Works use in {county_name}?",
            f"Faith Works uses owner-operated Kubota compact equipment — excavators, tractors with loaders and attachments, brush cutters, and forestry mulching equipment suited to {county_name} residential lots, pond edges, and rural acreage.",
        ),
        (
            f"Can Faith Works handle multiple services on one {county_name} property?",
            f"Often yes. Land clearing, debris removal, pond bank work, and trail clearing are frequently combined on the same property. Send photos of all areas you want addressed so scope can be planned together.",
        ),
        (
            f"Does Faith Works offer pool dig-out support in {county_name}?",
            f"Yes, as support under a licensed pool contractor — not as a pool installer. Dirt removal and site cleanup support is available when your pool builder needs outdoor property help.",
        ),
        (
            f"Who should I contact for Faith Works service in {county_name}?",
            f"Contact {OWNER} through the estimate form on this site, email contact@faithworksods.com, or call (863) 272-1596. Include your {county_name} city and property photos for the fastest response.",
        ),
    ]


def nearby_cities_html(city: dict, limit: int = 8) -> str:
    siblings = [c for c in cities_in_county(city["county"]) if c["slug"] != city["slug"]]
    return "".join(f'<a href="{c["slug"]}.html">{c["name"]}, FL</a>' for c in siblings[:limit])


def nearby_counties_html(county_name: str, root_prefix: str) -> str:
    profile = county_profile(county_name)
    links = []
    for name in profile.get("nearby_counties", []):
        county = COUNTY_BY_NAME.get(name)
        if county:
            links.append(f'<a href="{root_prefix}areas/{county["slug"]}.html">{name}</a>')
    for c in COUNTIES:
        if c["name"] != county_name and c["name"] not in profile.get("nearby_counties", []):
            if len(links) >= 11:
                break
            if f'<a href="{root_prefix}areas/{c["slug"]}.html">{c["name"]}</a>' not in links:
                links.append(f'<a href="{root_prefix}areas/{c["slug"]}.html">{c["name"]}</a>')
    return " &nbsp;&middot;&nbsp; ".join(links[:11])


def area_webpage_schema(name: str, description: str, canonical_path: str) -> str:
    import json

    return json.dumps({
        "@context": "https://schema.org",
        "@type": "WebPage",
        "@id": f"https://faithworksods.com/{canonical_path}#webpage",
        "name": name,
        "description": description,
        "url": f"https://faithworksods.com/{canonical_path}",
        "isPartOf": {"@id": "https://faithworksods.com/#website"},
        "about": {"@type": "Place", "name": name},
        "speakable": {
            "@type": "SpeakableSpecification",
            "cssSelector": [".sp-content h2", ".sp-content p", ".faq-question"],
        },
    }, indent=2)

"""Faith Works site safety policy.

Facts already published on the site and in the 2026-10-05 vendor packet.
No invented certifications, insurance limits, or employee coverage.
"""

from __future__ import annotations

SECTIONS: list[tuple[str, list[str]]] = [
    (
        "Who is on the machine",
        [
            "Faith Works Outdoor Services LLC is owner-operated. Tyler R. Edwards runs the equipment on the job he quoted.",
            "He holds a Florida construction-industry Certificate of Election to be Exempt from workers' compensation, certificate E02433175, effective 9/24/2026 through 9/23/2028. That exemption covers Tyler R. Edwards only. It is not a company workers' compensation policy, and it is not a contractor license from the Department of Business and Professional Regulation.",
            "The exemption does not cover employees, hired helpers, or anyone a desk could treat as an employee. If a site needs more than the owner-operator, that is said before the machine is scheduled.",
        ],
    ),
    (
        "Utilities and digging",
        [
            "Before stump removal, grading, driveway demo, or any other digging or soil-moving work, Sunshine 811 is contacted at least two full business days ahead so public utilities can be marked.",
            "Private lines are the property side of the locate: irrigation, septic, electric to an outbuilding, pool piping, and similar lines that 811 does not mark. The person who books the site marks those or has their contractor mark them before digging starts.",
            "Faith Works does not locate private utilities, does not trench for a new utility, and does not install sewer, water mains, or engineered stormwater.",
        ],
    ),
    (
        "Where the work stops",
        [
            "The written estimate is the scope. If the site does not match that scope, the work stops and a new number is given before more machine time is used.",
            "Stops include unmarked utilities, ground the machine cannot sit on safely, an occupied building, access the trailer cannot make, and any ask to spray a pond.",
            "Faith Works does not apply aquatic herbicides, copper algaecides, or other chemical water treatments, and does not hold an FDACS Aquatic pesticide applicator license. Pond and ditch work is mechanical clearing only.",
            "Light outdoor demolition means sheds, lean-tos, small outbuildings, and accessible pads. Occupied buildings and structural commercial tear-downs are outside the policy.",
            "Driveway work is removal and haul-off of existing concrete or asphalt. New paving and new concrete are not part of the job.",
        ],
    ),
    (
        "People, pets, and the work area",
        [
            "Bystanders, pets, and vehicles that are not part of the job stay out of the swing and travel path of the machine.",
            "Gate codes, lockboxes, and where to park the truck and trailer are confirmed before the machine comes off the trailer.",
            "Forestry mulch stays on the site when mulch-in-place is the scope. Haul-off happens only when the estimate includes it.",
        ],
    ),
    (
        "Equipment",
        [
            "The crew uses compact Kubota equipment, trailers, and the attachment that fits the written scope: clearing, mulching, grapple, stump, or light demo.",
            "The machine stays on the agreed work area. It is not used to pull vehicles, lift people, or open a path that was not in the estimate.",
        ],
    ),
    (
        "Weather",
        [
            "Work pauses for lightning or for ground and haul conditions that make the machine unsafe.",
            "A new arrival time is set with the person who booked the site. A paused day is not treated as a finished closeout.",
        ],
    ),
    (
        "Closeout",
        [
            "A vendor closeout is a wide photo before the work, a wide photo when it is done, and one closer frame of the cleared line, stump, or debris pile.",
            "The property address or the desk's work-order number goes in the email subject so the file can be matched without a phone call.",
        ],
    ),
    (
        "Documents a desk can hold",
        [
            "The public vendor packet includes the signed IRS W-9 (Faith Works Outdoor Services LLC, EIN 42-28665997), the Sunbiz entity detail (L26000289354, ACTIVE), this safety policy, the services one-pager, and the workers' compensation exemption.",
            "A filled general-liability certificate is not in that packet yet. A blank form is not proof of coverage. Email tyler@faithworksclearing.com with the exact certificate-holder legal name when an issued ACORD 25 is required.",
            "Bank and ACH details are not in the public packet.",
        ],
    ),
]


def plain_text() -> str:
    lines = [
        "Faith Works Outdoor Services LLC — Site safety policy",
        "For property managers, builders, HOAs, and landowners",
        "3925 Roberts Ave, Auburndale, FL 33823",
        "Tyler R. Edwards · (863) 272-1596 · tyler@faithworksclearing.com",
        "https://faithworksclearing.com/safety-policy.html",
        "",
        "This is the operating policy for outdoor sites. It is not an OSHA program certificate, not a contractor license, and not a statement that a company workers' compensation policy or a filled liability certificate is on file.",
        "",
    ]
    for title, paragraphs in SECTIONS:
        lines.append(title.upper())
        lines.append("")
        lines.extend(paragraphs)
        lines.append("")
    return "\n".join(lines).strip() + "\n"


def html_sections() -> str:
    blocks = []
    for title, paragraphs in SECTIONS:
        body = "".join(f"<p>{paragraph}</p>" for paragraph in paragraphs)
        blocks.append(f"<h3>{title}</h3>{body}")
    return "\n".join(blocks)

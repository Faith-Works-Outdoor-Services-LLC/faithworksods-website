#!/usr/bin/env python3
"""Build the public Faith Works vendor packet from Tyler's 2026-10-05 zip.

Source: Ops\\clients\\faith-works\\vendor-packet\\inbox-2026-10-05
Public: website vendor/

The insurance file in that zip is a blank ACORD 25. It is not copied.
The W-9 scan is six pages and about 10 MB; only the signed page is published,
recompressed so a property manager can download it.
"""

from __future__ import annotations

import zipfile
from datetime import date
from pathlib import Path

import fitz

from safety_policy import plain_text as safety_policy_plain

ROOT = Path(__file__).resolve().parent.parent
INBOX = Path(
    r"E:\KnightLogics-Growth-System\Ops\clients\faith-works\vendor-packet"
    r"\inbox-2026-10-05\Faith_Works_Outdoor_Services_Vendor_Packages.zip"
)
PREFIX = "Faith_Works_Outdoor_Services_Vendor Packages/"
SITE_VENDOR = ROOT / "vendor"
TODAY = date.today().isoformat()

# (zip member, public filename, readme label)
PUBLIC_DOCS: list[tuple[str, str, str]] = [
    (
        PREFIX + "Faith_Works_Outdoor_Services_W9 Completed - Signed 10-5-2026.pdf",
        "faith-works-w9.pdf",
        "Signed IRS W-9 (Faith Works Outdoor Services LLC, EIN 42-28665997, signed 10/05/2026)",
    ),
    (
        PREFIX + "Faith_Works_Outdoor_Services_Entity Detail.pdf",
        "faith-works-sunbiz-entity.pdf",
        "Florida Sunbiz entity detail (L26000289354, ACTIVE)",
    ),
    (
        PREFIX + "Faith_Works_Outdoor_Services_Workmancomp Exemption Doc.pdf",
        "faith-works-wc-exemption-tyler-edwards.pdf",
        "Florida WC construction exemption — Tyler R. Edwards (9/24/2026 through 9/23/2028, E02433175)",
    ),
    (
        PREFIX + "Faith_Works_Outdoor_Services_One_Pager_UPDATED.pdf",
        "faith-works-services-one-pager.pdf",
        "Services one-pager",
    ),
]

ZIP_NAME = "faith-works-vendor-packet.zip"
SAFETY_PDF = "faith-works-safety-policy.pdf"
SKIPPED = PREFIX + "Faith_Works_Outdoor_Services_Insurance COI Blank.pdf"

README = f"""Faith Works Outdoor Services LLC — vendor packet
Updated {TODAY}

Legal name: Faith Works Outdoor Services LLC
Sunbiz: L26000289354 (ACTIVE)
FEIN: 42-28665997 (on the W-9; the Sunbiz print still lists FEI/EIN as NONE)
Address: 3925 Roberts Ave, Auburndale, FL 33823
Contact: Tyler R. Edwards · (863) 272-1596 · tyler@faithworksclearing.com

Included
""" + "\n".join(
    f"  - {dest}: {label}" for _src, dest, label in PUBLIC_DOCS
) + """

Not included (on purpose)
  - Filled ACORD 25 general liability certificate — not on file yet. The copy received 2026-10-05 is a blank form and is not proof of coverage.
  - Additional-insured wording — email tyler@faithworksclearing.com with the exact certificate-holder legal name once a filled certificate exists
  - Company workers' compensation policy — Tyler R. Edwards holds a construction-industry officer exemption only. It does not cover employees.
  - ACH / bank details

https://faithworksclearing.com/property-managers.html
"""


def signed_w9_page(pdf_bytes: bytes) -> bytes:
    """Keep the signed first page and drop the IRS instruction pages."""
    src = fitz.open(stream=pdf_bytes, filetype="pdf")
    try:
        page = src[0]
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False)
        jpeg = pix.tobytes("jpeg", jpg_quality=72)
        out = fitz.open()
        try:
            new_page = out.new_page(width=page.rect.width, height=page.rect.height)
            new_page.insert_image(page.rect, stream=jpeg)
            return out.tobytes(garbage=4, deflate=True)
        finally:
            out.close()
    finally:
        src.close()


def write_safety_pdf(dest: Path) -> None:
    """Paginate the published policy. This PDF is generated, not taken from Tyler's zip."""
    doc = fitz.open()
    try:
        page = doc.new_page()
        y = 54.0
        width = 504.0
        size = 11
        leading = 15

        def new_page() -> None:
            nonlocal page, y
            page = doc.new_page()
            y = 54.0

        for block in safety_policy_plain().split("\n"):
            if not block.strip():
                y += 8
                if y > 740:
                    new_page()
                continue
            words = block.split()
            line = ""
            lines: list[str] = []
            for word in words:
                trial = f"{line} {word}".strip()
                if fitz.get_text_length(trial, fontname="helv", fontsize=size) > width:
                    lines.append(line)
                    line = word
                else:
                    line = trial
            if line:
                lines.append(line)
            for wrapped in lines:
                if y > 740:
                    new_page()
                page.insert_text((54, y), wrapped, fontsize=size, fontname="helv", color=(0.1, 0.1, 0.1))
                y += leading
        dest.write_bytes(doc.tobytes(garbage=4, deflate=True))
    finally:
        doc.close()


def main() -> int:
    if not INBOX.is_file():
        raise FileNotFoundError(f"Missing Tyler packet zip: {INBOX}")
    SITE_VENDOR.mkdir(parents=True, exist_ok=True)
    copied: list[Path] = []
    with zipfile.ZipFile(INBOX) as zf:
        names = set(zf.namelist())
        if SKIPPED not in names:
            raise FileNotFoundError("Expected blank COI member was not in the source zip")
        for src_name, dest_name, _label in PUBLIC_DOCS:
            if src_name not in names:
                raise FileNotFoundError(f"Missing packet file: {src_name}")
            data = zf.read(src_name)
            if dest_name == "faith-works-w9.pdf":
                data = signed_w9_page(data)
            dest = SITE_VENDOR / dest_name
            dest.write_bytes(data)
            copied.append(dest)
            print(f"wrote vendor/{dest_name} ({dest.stat().st_size} bytes)")

    safety = SITE_VENDOR / SAFETY_PDF
    write_safety_pdf(safety)
    copied.append(safety)
    print(f"wrote vendor/{SAFETY_PDF} ({safety.stat().st_size} bytes)")

    readme_text = README.replace(
        "Not included (on purpose)",
        f"  - {SAFETY_PDF}: Site safety policy (operating rules published on the site; not an OSHA certificate)\n\nNot included (on purpose)",
    )
    readme = SITE_VENDOR / "README.txt"
    readme.write_text(readme_text, encoding="utf-8")
    zip_path = SITE_VENDOR / ZIP_NAME
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("README.txt", readme_text)
        for dest in copied:
            zf.write(dest, dest.name)
        if any("Insurance" in name or "COI" in name for name in zf.namelist()):
            raise RuntimeError("Blank COI was included in the public zip")
    print(f"wrote vendor/{ZIP_NAME} ({zip_path.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

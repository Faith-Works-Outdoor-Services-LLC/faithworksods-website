#!/usr/bin/env python3
"""Shorten <title>/og:title/twitter:title over 60 chars (Ahrefs 'title too long').
Never touches NAP/JSON-LD business data. Usage: python scripts/shorten-titles.py [--dry]"""
import re, sys, html
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
SKIP = ("_backups", "website-audit", "gsc-audit", "seo-engine", "vendor", "node_modules", "website")
MANUAL = {
    "gallery/before-process-after-clear-fence-line-of-overgrown-brush-39122bea-scope.html": "Scope: Fence Line Clearing, Auburndale FL | Faith Works",
    "gallery/before-process-after-clear-fence-line-of-overgrown-brush-39122bea.html": "Fence Line Brush Clearing in Auburndale FL | Faith Works",
    "gallery/before-process-after-clear-lake-front-and-remove-all-brush-and-bring-d7425afb.html": "Lakefront Clearing in Lake Panasoffkee FL | Faith Works",
    "gallery/before-process-after-excavator-stump-removal-count-not-stated-557698bf-scope.html": "Scope: Stump Removal in Auburndale FL | Faith Works",
    "gallery/before-process-after-hedge-removal-sod-installation-cdccd15f-scope.html": "Scope: Hedge Removal & Sod in Orlando FL | Faith Works",
    "gallery/before-process-after-land-clearing-brush-cutting-13e6d87d-scope.html": "Scope: Land Clearing in Thonotosassa FL | Faith Works",
    "gallery/before-process-after-land-clearing-brush-cutting-13e6d87d.html": "Land Clearing & Brush in Thonotosassa FL | Faith Works",
    "gallery/before-process-after-lot-clearing-underbrush-acreage-not-stated-7275c58d-scope.html": "Scope: Lot Clearing in Clermont FL | Faith Works",
    "gallery/before-process-after-pond-bank-clearing-underbrush-e9165277-scope.html": "Scope: Pond Bank Clearing in Auburndale FL | Faith Works",
    "gallery/before-process-after-pond-bank-clearing-underbrush-e9165277.html": "Pond Bank Clearing in Auburndale FL | Faith Works",
    "areas/eagle-lake-fl.html": "Eagle Lake FL Gravel Lanes & Access Clearing | Faith Works",
    "areas/mulberry-fl.html": "Private Road Clearing in Mulberry FL | Faith Works",
    "areas/auburndale-fl.html": "Land Clearing & Private Roads Auburndale FL | Faith Works",
    "areas/bushnell-fl.html": "Forestry Mulching in Bushnell FL | Faith Works",
    "contact.html": "Contact Faith Works | Free Land Clearing Estimate",
    "forestry-mulching.html": "Forestry Mulching Near Me | Polk County FL | Faith Works",
    "access-road-clearing.html": "Private Road Clearing Mulberry & Auburndale | Faith Works",
    "property-maintenance.html": "Outdoor Property Maintenance in Polk County FL | Faith Works",
    "equipment-services.html": "Outdoor Equipment Services in Polk County FL | Faith Works",
    "pond-management.html": "Pond Shoreline Maintenance in Polk County FL | Faith Works",
    "gallery.html": "Land Clearing Project Gallery | Faith Works",
    "property-cleanup.html": "Property Cleanup Services in Polk County FL | Faith Works",
    "acreage-cleanup.html": "Acreage Cleanup Services in Polk County FL | Faith Works",
    "gallery/before-process-after-clear-lake-front-and-remove-all-brush-and-bring-d7425afb-scope.html": "Scope: Lakefront Clearing, Lake Panasoffkee FL | Faith Works",
    "gallery/before-process-after-land-clearing-job.html": "Land Clearing Before & After in Auburndale FL | Faith Works",
    "gallery/before-process-after-land-clearing-job-scope.html": "Scope: Land Clearing Project, Auburndale FL | Faith Works",
}
def auto(t):
    t = html.unescape(t).replace("| Faith Works Outdoor Services", "| Faith Works")
    t = t.replace("Scope of Work: ", "Scope: ").replace(" (acreage not stated)", "").replace(" (count not stated)", "")
    t = re.sub(r"\bin (auburndale|seffner)\b", lambda m: "in " + m.group(1).title(), t)
    t = re.sub(r"^(.+?) Outdoor Property Services \| Faith Works$", r"\1 FL Outdoor Services | Faith Works", t)
    return t
dry = "--dry" in sys.argv; changed = []
for p in ROOT.rglob("*.html"):
    rel = p.relative_to(ROOT).as_posix()
    if rel.split("/")[0] in SKIP: continue
    s = p.read_text(encoding="utf-8")
    m = re.search(r"<title>([^<]*)</title>", s)
    if not m or len(html.unescape(m.group(1))) <= 60: continue
    old = m.group(1); new = MANUAL.get(rel) or auto(old)
    if len(new) > 60: print("STILL LONG", len(new), rel, new)
    enc = html.escape(new, quote=False)
    s2 = s.replace(f"<title>{old}</title>", f"<title>{enc}</title>")
    s2 = re.sub(r'(<meta (?:property="og:title"|name="twitter:title") content=")' + re.escape(html.escape(html.unescape(old), quote=True)) + '"', lambda mm: mm.group(1) + html.escape(new, quote=True) + '"', s2)
    s2 = re.sub(r'(<meta (?:property="og:title"|name="twitter:title") content=")' + re.escape(old) + '"', lambda mm: mm.group(1) + html.escape(new, quote=True) + '"', s2)
    changed.append((rel, len(html.unescape(old)), len(new), new))
    if not dry: p.write_text(s2, encoding="utf-8")
for c in changed: print(f"{c[1]}->{c[2]} | {c[0]} | {c[3]}")
print(len(changed), "titles", "(dry run)" if dry else "rewritten")



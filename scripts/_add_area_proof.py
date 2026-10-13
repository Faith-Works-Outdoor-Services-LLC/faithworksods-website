import json, html, re
from pathlib import Path
R = Path(".")
jobs = json.loads((R/"gallery/job-gallery.json").read_text(encoding="utf-8"))["projects"]
revs = json.loads((R/"data/google-reviews.json").read_text(encoding="utf-8"))["reviews"]
def clean(t): return re.sub(r"\s*\((?:acreage|count) not stated\)", "", t).replace("\u2014"," - ").rstrip(".")
NEAR = {
 "auburndale": ("Auburndale", ["Auburndale"], "Most of our documented Polk County jobs are right here in Auburndale, so these are real local projects, not stock photos."),
 "winter-haven": ("Winter Haven", ["Auburndale"], "Winter Haven is next door to our Auburndale base. These documented jobs are in Auburndale, a short drive up US-92 and Recker Hwy."),
 "lakeland": ("Lakeland", ["Plant City", "Auburndale"], "These documented jobs are in Auburndale and Plant City, on either side of Lakeland along I-4."),
}
for slug, (city, cities, intro) in NEAR.items():
    p = R/f"areas/{slug}-fl.html"; s = p.read_text(encoding="utf-8")
    if "area-recent-projects" in s: continue
    picks = [j for c in cities for j in jobs if (j.get("city_name") or "").lower() == c.lower()][:4]
    items = "\n".join(f'            <li><a href="../{j["detail_url"].lstrip("/")}">{html.escape(clean(j["title"]))}</a> - {html.escape(j["city_name"].title())}, FL</li>' for j in picks)
    rv = [r for r in revs if r.get("stars") == 5 and len(r.get("text","")) < 200][:2]
    quotes = "\n".join(f'          <blockquote class="area-review"><p>&ldquo;{html.escape(r["text"])}&rdquo;</p><cite>{html.escape(r["name"])}, Google review</cite></blockquote>' for r in rv)
    block = f'''          <section class="area-recent-projects" aria-labelledby="recent-{slug}">
          <h2 id="recent-{slug}">Recent Faith Works Projects Near {city}</h2>
          <p>{intro} Each one has before, during and after photos.</p>
          <ul>
{items}
          </ul>
          <p><a href="../gallery.html">See all before &amp; after projects</a></p>
          <h3>What Faith Works customers say</h3>
{quotes}
          </section>

'''
    anchor = f"          <h2>How to Get Service in {city}, FL</h2>"
    assert anchor in s, slug
    p.write_text(s.replace(anchor, block + anchor, 1), encoding="utf-8")
    print(slug, len(picks), "projects", len(rv), "quotes")


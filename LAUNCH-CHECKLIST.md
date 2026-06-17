# Faith Works Outdoor Services — Launch Checklist

## Business identity
| Item | Value |
|------|-------|
| Legal name | Faith Works Outdoor Services LLC |
| Brand name | Faith Works Outdoor Services |
| Short brand | Faith Works ODS |
| Domain | faithworksods.com |
| Email | contact@faithworksods.com |
| Owner | Tyler R. Edwards |
| Location | Based in Auburndale, FL |
| Service region | Polk County & Central Florida |
| Entity | Active Florida LLC (May 2026) |

## Before go-live — update these in `website/_build_site.py` then run `python website/_build_site.py`

1. **Phone number** — replace `(863) 000-0000` / `8630000000`
2. **Facebook URL** — replace `PLACEHOLDER`
3. **YouTube URL** — replace `PLACEHOLDER`
4. **Formspree form ID** — create at formspree.io for `contact@faithworksods.com`
5. **GA4 measurement ID** — replace `G-PLACEHOLDER`
6. **Microsoft Clarity ID** — replace `PLACEHOLDER`

## Website pages built
- `/` — Homepage with hero form, services, gallery teaser, process, FAQ
- `/pool-digging.html`
- `/land-clearing.html`
- `/trail-clearing.html`
- `/pond-bank-clearing.html`
- `/ditch-clearing.html`
- `/debris-removal.html`
- `/gallery.html`
- `/about.html`
- `/contact.html` — Full estimate form with photo upload
- `/service-areas.html`
- `/privacy-policy.html`

## Recommended launch order
1. **Website first** — connect DNS A/CNAME for `faithworksods.com` and `www` (do not change Microsoft 365 MX/SPF/DKIM)
2. **GBP same day or next** — use live website URL, hide street address (service-area business)
3. **Search Console + Bing** — submit sitemap.xml
4. **Clarity + GA4** — verify form and phone click events

## GBP access
- Primary owner: Google Account using `contact@faithworksods.com` (non-Gmail is fine)
- Backup owner: Tyler's Gmail
- Manager: Knight Logics email

## GBP category suggestions
- Primary: Excavating contractor (if accurate)
- Secondary (only if accurate): Land clearing service, Debris removal service

## Do not publish on website/GBP
- Home street address (service-area business)
- Unlicensed claims (licensed excavation contractor, drainage engineering, pool installation, etc.)

## DNS (Microsoft 365 email safe)
Only add/modify:
- A record → hosting IP
- CNAME `www` → hosting
- TXT for Google/Bing verification

Do **not** remove Microsoft MX, SPF, DKIM, or DMARC records.

## Compensation terms (Knight Logics)
- $500 due when domain is connected and site is live
- 10% of **net collected profit** from jobs attributed to website, GBP, Facebook, YouTube, or managed marketing systems
- Net profit = collected payment minus direct job costs (materials, disposal, rentals, subs, permits)

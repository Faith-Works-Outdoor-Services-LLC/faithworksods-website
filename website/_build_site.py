#!/usr/bin/env python3
"""Generate Faith Works Outdoor Services static website."""

from __future__ import annotations

import json
import os
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent  # E:\All Client Websites\Faith Works


def formspree_endpoint() -> str:
    env_id = os.environ.get("FORMSPREE_FORM_ID", "").strip()
    id_file = ROOT / "formspree-id.txt"
    form_id = env_id or (id_file.read_text(encoding="utf-8").strip() if id_file.exists() else "PLACEHOLDER")
    return f"https://formspree.io/f/{form_id}"


SITE = {
    "url": "https://faithworksods.com",
    "legal_name": "Faith Works Outdoor Services LLC",
    "brand": "Faith Works Outdoor Services",
    "short": "Faith Works ODS",
    "owner": "Tyler R. Edwards",
    "email": "contact@faithworksods.com",
    "phone_display": "(863) 000-0000",  # UPDATE when Tyler confirms number
    "phone_tel": "8630000000",
    "city": "Auburndale",
    "region": "FL",
    "area": "Polk County & Central Florida",
    "geo_lat": "28.0653",
    "geo_lng": "-81.7887",
    "facebook": "https://www.facebook.com/profile.php?id=PLACEHOLDER",
    "youtube": "https://www.youtube.com/@PLACEHOLDER",
    "formspree": "https://formspree.io/f/PLACEHOLDER",
    "ga4": "G-PLACEHOLDER",
    "clarity": "PLACEHOLDER",
}

SERVICES = [
    {
        "slug": "pool-digging",
        "name": "Pool Digging",
        "nav": "Pool Digging",
        "title": "Pool Digging & Dirt Removal Support in Auburndale, FL",
        "h1": "Pool Digging & Dirt Removal Support — Auburndale & Polk County",
        "desc": "Pool dig-out support and dirt removal for pool installation projects in Auburndale, Lakeland, Winter Haven, and Polk County. Free photo-based estimates.",
        "keyword": "pool digging Auburndale FL",
        "intro": "Installing a pool often means moving a serious amount of dirt. Faith Works Outdoor Services provides pool dig-out support and dirt removal so your pool contractor can focus on the install while your property gets cleaned up properly.",
        "bullets": [
            "Pool dig-out dirt removal and haul-off support",
            "Excavation support for residential pool projects",
            "Site cleanup after pool digging",
            "Coordination with pool installers and contractors",
            "Property access planning for equipment",
        ],
        "benefits": [
            "Keeps the job site cleaner and safer during pool work",
            "Reduces delays caused by piled-up fill and debris",
            "Helps restore usable yard space after digging",
            "Owner-operated communication from estimate to completion",
        ],
    },
    {
        "slug": "land-clearing",
        "name": "Land Clearing",
        "nav": "Land Clearing",
        "title": "Land Clearing Services in Polk County, FL",
        "h1": "Land Clearing Services — Polk County & Central Florida",
        "desc": "Land clearing for overgrown lots, brush, and outdoor spaces in Auburndale, Lakeland, Winter Haven, and surrounding Polk County areas.",
        "keyword": "land clearing Polk County FL",
        "intro": "Overgrown lots, thick brush, and unmanaged vegetation make property harder to use and harder to maintain. Faith Works Outdoor Services clears land for homeowners, property owners, and contractors across Polk County.",
        "bullets": [
            "Overgrown lot and property clearing",
            "Brush and vegetation removal",
            "Selective clearing around structures and fences",
            "Small-acreage and residential clearing",
            "Cleanup and debris removal after clearing",
        ],
        "benefits": [
            "Opens up usable property space",
            "Improves visibility and access",
            "Prepares land for fencing, trails, or future projects",
            "Equipment-ready service for tough Florida growth",
        ],
    },
    {
        "slug": "trail-clearing",
        "name": "Trail Clearing",
        "nav": "Trail Clearing",
        "title": "Trail Clearing & Trail Maintenance in Central Florida",
        "h1": "Trail Clearing & Trail Maintenance — Central Florida",
        "desc": "Cut new trails or restore overgrown trails on private property in Auburndale, Polk County, and surrounding Central Florida areas.",
        "keyword": "trail clearing Florida",
        "intro": "Whether you need a new access path cut in or an existing trail reopened after years of overgrowth, Faith Works Outdoor Services helps property owners reclaim usable trails with the right equipment and careful clearing.",
        "bullets": [
            "New trail cutting and path opening",
            "Overgrown trail restoration",
            "Brush and low-hanging vegetation removal along paths",
            "Trail edge cleanup and widening where needed",
            "Debris removal from trail work",
        ],
        "benefits": [
            "Restores access across large or wooded properties",
            "Improves safety by removing obstructive growth",
            "Helps maintain trails season after season",
            "Ideal for private land, acreage, and rural properties",
        ],
    },
    {
        "slug": "pond-bank-clearing",
        "name": "Pond Bank Clearing",
        "nav": "Pond Bank Clearing",
        "title": "Pond Bank Clearing & Brush Removal in Polk County",
        "h1": "Pond Bank Clearing & Brush Removal — Polk County",
        "desc": "Clean overgrown pond banks with industry-leading mulching equipment and brush cutters in Auburndale and Polk County.",
        "keyword": "pond bank clearing Polk County",
        "intro": "Overgrown pond banks reduce access, block views, and make maintenance harder. Faith Works Outdoor Services clears pond banks using mulching equipment and brush cutters built for tough vegetation.",
        "bullets": [
            "Overgrown pond bank clearing",
            "Brush cutting along pond edges",
            "Mulching of thick vegetation on banks",
            "Access improvement around ponds and retention areas",
            "Debris cleanup after bank work",
        ],
        "benefits": [
            "Improves pond appearance and visibility",
            "Makes bank maintenance easier over time",
            "Reduces overgrowth encroaching into the water edge",
            "Professional equipment for dense Florida vegetation",
        ],
    },
    {
        "slug": "ditch-clearing",
        "name": "Ditch Clearing",
        "nav": "Ditch Clearing",
        "title": "Ditch Clearing & Runoff Cleanup in Auburndale, FL",
        "h1": "Ditch Clearing & Runoff Cleanup — Auburndale & Polk County",
        "desc": "Clean and reshape overgrown ditches and runoff areas in Auburndale, Lakeland, and Polk County using mulching equipment and brush cutters.",
        "keyword": "ditch clearing Auburndale",
        "intro": "Florida rain season puts real pressure on ditches and runoff paths. When ditches become overgrown, water movement and property drainage suffer. Faith Works Outdoor Services clears and reshapes overgrown ditches and runoff areas.",
        "bullets": [
            "Overgrown ditch clearing",
            "Runoff path and swale cleanup",
            "Brush cutting in drainage easements",
            "Vegetation removal from ditch lines",
            "Basic ditch reshaping where appropriate",
        ],
        "benefits": [
            "Helps water move more freely during heavy rain",
            "Reduces blocked or overgrown drainage paths",
            "Improves property maintenance access",
            "Equipment suited for dense ditch-line growth",
        ],
    },
    {
        "slug": "debris-removal",
        "name": "Debris Removal",
        "nav": "Debris Removal",
        "title": "Yard Debris & Outdoor Trash Removal in Polk County",
        "h1": "Yard Debris & Outdoor Trash Removal — Polk County",
        "desc": "Remove yard debris, brush piles, and non-hazardous outdoor junk in Auburndale and surrounding Polk County communities.",
        "keyword": "yard debris removal Polk County",
        "intro": "Storm cleanup, land clearing, and property projects all leave debris behind. Faith Works Outdoor Services removes yard debris, brush piles, and non-hazardous outdoor trash so your property looks finished when the job is done.",
        "bullets": [
            "Yard debris and brush pile removal",
            "Outdoor trash and cleanup haul-off support",
            "Post-storm property debris cleanup",
            "Clearing leftover material from land projects",
            "Property cleanup after excavation or clearing work",
        ],
        "benefits": [
            "Leaves the property cleaner and more usable",
            "Saves time after major cleanup projects",
            "Helps finish the job the right way",
            "Works well combined with clearing or digging services",
        ],
    },
]

CITIES = [
    "Auburndale", "Winter Haven", "Lakeland", "Lake Alfred", "Bartow",
    "Haines City", "Davenport", "Lake Wales", "Polk City", "Plant City",
]

GALLERY = [
    ("excavator-and-truck-photo.webp", "Kubota excavator and dump trailer on a residential pool dig-out site in Polk County Florida", "Pool Digging"),
    ("excavator-photo.webp", "Kubota mini excavator on a land clearing and excavation job site", "Land Clearing"),
    ("photo-of-all-equipment.webp", "Faith Works Outdoor Services fleet — Kubota excavator, tractor with loader, pickup, dump trailer, and flatbed trailer", "Equipment"),
    ("stump-before-ground-leveled.webp", "Tree stump removal site before ground leveling and cleanup in a residential yard", "Land Clearing"),
    ("stump-during-removal-1.webp", "Kubota excavator removing a tree stump during an active land clearing job", "Land Clearing"),
    ("stump-during-removal-2.webp", "Excavator pulling a tree stump and root ball during stump removal", "Land Clearing"),
    ("stump-during-removal.webp", "Mini excavator working to extract a tree stump from the ground", "Land Clearing"),
    ("stump-post-removal-1.webp", "Property after tree stump removal with excavated soil ready for leveling", "Land Clearing"),
    ("stump-post-removal.webp", "Completed tree stump removal with cleared ground and debris pile on site", "Land Clearing"),
    ("stump-prior-to-removal.webp", "Large tree stump in a yard before Faith Works stump removal service begins", "Land Clearing"),
    ("tractor.webp", "Kubota compact tractor with loader attachment on a Central Florida job site", "Equipment"),
    ("tractor-moving-item-with-grapple.webp", "Kubota tractor using a grapple attachment to move brush and debris during property cleanup", "Debris Removal"),
    ("tractor-with-box-blade-leveling-ground.webp", "Kubota tractor with box blade leveling and grading ground after stump removal", "Land Clearing"),
]

HERO_DESKTOP = "photo-of-all-equipment.webp"
HERO_MOBILE = "excavator-and-truck-photo.webp"


def fonts_head() -> str:
    return """  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;600;700&family=Inter:wght@400;500;600;700&display=swap" onload="this.onload=null;this.rel='stylesheet'">
  <noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;600;700&family=Inter:wght@400;500;600;700&display=swap"></noscript>"""


def favicon_head() -> str:
    return """  <link rel="icon" type="image/png" href="Images/Logo.png">
  <link rel="apple-touch-icon" href="Images/Logo.png">"""


def analytics_head() -> str:
    ga4 = SITE["ga4"]
    clarity = SITE["clarity"]
    if ga4 == "G-PLACEHOLDER":
        ga = ""
    else:
        ga = f"""  <script async src="https://www.googletagmanager.com/gtag/js?id={ga4}"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', '{ga4}');
  </script>"""
    if clarity == "PLACEHOLDER":
        clarity_script = ""
    else:
        clarity_script = f"""  <script>window.addEventListener('load',function(){{setTimeout(function(){{(function(c,l,a,r,i,t,y){{c[a]=c[a]||function(){{(c[a].q=c[a].q||[]).push(arguments)}};t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);}})(window,document,"clarity","script","{clarity}");}},4000);}},{{once:true}});</script>"""
    return ga + "\n" + clarity_script


def service_options(selected: str | None = None) -> str:
    opts = ['<option value="" disabled selected>Select a service...</option>']
    for s in SERVICES:
        sel = ' selected' if selected == s["name"] else ""
        opts.append(f'<option{sel}>{s["name"]}</option>')
    opts.append('<option>Other / Not sure</option>')
    return "\n                ".join(opts)


def estimate_form(form_id: str = "hero-contact-form", selected: str | None = None, subject: str | None = None, page: str = "") -> str:
    subj = subject or f"New estimate request - {SITE['brand']}"
    page_field = f'<input type="hidden" name="page" value="{page}">' if page else ""
    return f"""
            <form class="contact-form" action="{formspree_endpoint()}" method="POST" id="{form_id}" enctype="multipart/form-data">
              {page_field}
              <div class="form-group">
                <label for="{form_id}-name">Your Name</label>
                <input type="text" id="{form_id}-name" name="name" placeholder="First and last name" required autocomplete="name">
              </div>
              <div class="form-group">
                <label for="{form_id}-phone">Phone Number</label>
                <input type="tel" id="{form_id}-phone" name="phone" placeholder="(863) 000-0000" required autocomplete="tel">
              </div>
              <div class="form-group">
                <label for="{form_id}-email">Email</label>
                <input type="email" id="{form_id}-email" name="email" placeholder="you@email.com" autocomplete="email">
              </div>
              <div class="form-group">
                <label for="{form_id}-location">Job Address / City</label>
                <input type="text" id="{form_id}-location" name="job_location" placeholder="Street or city in Polk County" required>
              </div>
              <div class="form-group">
                <label for="{form_id}-service">Service Needed</label>
                <select id="{form_id}-service" name="service" required>
                {service_options(selected)}
                </select>
              </div>
              <div class="form-group">
                <label for="{form_id}-photos">Upload Project Photos</label>
                <input type="file" id="{form_id}-photos" name="photos" accept="image/*" multiple>
              </div>
              <div class="form-group">
                <label for="{form_id}-access">Equipment Access Notes</label>
                <input type="text" id="{form_id}-access" name="access_notes" placeholder="Gate width, obstacles, utilities known">
              </div>
              <div class="form-group">
                <label for="{form_id}-message">Project Details</label>
                <textarea id="{form_id}-message" name="message" placeholder="Describe the property, size, timeline, and what you need cleared or removed..." rows="4"></textarea>
              </div>
              <input type="hidden" name="_subject" value="{subj}">
              <input type="hidden" name="_replyto" value="email">
              <input type="hidden" name="_format" value="plain">
              <input type="text" name="_gotcha" style="display:none" tabindex="-1" autocomplete="off">
              <button type="submit" class="btn btn-primary btn-full">Send Estimate Request</button>
              <p class="form-note">Or email <a href="mailto:{SITE['email']}">{SITE['email']}</a></p>
            </form>
            <div class="form-success" id="{form_id}-success" aria-live="polite" hidden>
              <p class="form-success-msg">Thanks! Tyler will review your project and contact you shortly.</p>
            </div>"""


PHONE_ICON = (
    '<svg viewBox="0 0 24 24" width="18" height="18" focusable="false">'
    '<path fill="currentColor" d="M6.6 10.8c1.5 2.9 3.7 5.1 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 '
    "1.1.4 2.3.6 3.5.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1C10.3 21 3 13.7 3 4c0-.6.4-1 1-1h3.5c.6 0 "
    "1 .4 1 1 0 1.2.2 2.4.6 3.5.1.3 0 .7-.2 1L6.6 10.8z\"/></svg>"
)


def call_cta_link(extra_class: str = "") -> str:
    classes = f"fw-header-call {extra_class}".strip()
    phone = SITE["phone_display"]
    return f"""<a href="tel:{SITE['phone_tel']}" class="{classes}" title="Call or text {phone}" aria-label="Call or text {phone}">
        <span class="fw-header-call__icon" aria-hidden="true">{PHONE_ICON}</span>
        <span class="fw-header-call__text">
          <span class="fw-header-call__label">Call or Text</span>
          <span class="fw-header-call__number">{phone}</span>
        </span>
      </a>"""


def header(current: str = "") -> str:
    def nav_link(href: str, label: str) -> str:
        cur = ' aria-current="page"' if current == href else ""
        return f'<a href="{href}"{cur}>{label}</a>'

    service_links = "\n            ".join(
        f'<a href="{s["slug"]}.html" role="menuitem">{s["nav"]}</a>' for s in SERVICES
    )
    call_link = call_cta_link()
    menu_call_link = call_cta_link("fw-header-call--menu")
    return f"""  <header class="site-header" id="top">
    <div class="container header-inner">
      <button class="hamburger-btn" id="hamburger-btn" aria-label="Open navigation menu" aria-expanded="false">
        <span></span><span></span><span></span>
      </button>
      <div class="brand-wrap">
        <a class="brand" href="index.html" aria-label="{SITE['brand']} home">
          <img src="Images/Logo.png" alt="{SITE['brand']}" class="brand-logo" width="68" height="68">
        </a>
        <div class="brand-text-wrap">
          <a href="index.html" class="brand-title-link"><span class="brand-title">{SITE['brand']}</span></a>
          <span class="brand-tagline">Land Clearing &amp; Outdoor Services · {SITE['city']}, FL</span>
          <div class="header-brand-ctas" aria-label="Quick actions">
            <a href="contact.html" class="btn-mobile-estimate">Free Estimate</a>
          </div>
        </div>
      </div>
      <nav class="site-nav" aria-label="Primary navigation">
        {nav_link('index.html', 'Home')}
        <div class="nav-dropdown-wrap">
          <button class="nav-dropdown-btn" aria-expanded="false" aria-haspopup="true">
            Services
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="6 9 12 15 18 9"/></svg>
          </button>
          <div class="nav-dropdown-menu" role="menu">
            {service_links}
          </div>
        </div>
        {nav_link('about.html', 'About')}
        {nav_link('gallery.html', 'Gallery')}
        {nav_link('service-areas.html', 'Service Areas')}
        {nav_link('contact.html', 'Contact')}
      </nav>
      <div class="header-actions">
        <a href="contact.html" class="btn btn-primary btn-header-estimate">Request Estimate</a>
      </div>
      {call_link}
    </div>
  </header>"""


def footer() -> str:
    cities = " &nbsp;&middot;&nbsp; ".join(CITIES[:6])
    return f"""  <footer class="site-footer">
    <div class="container footer-inner">
      <img src="Images/Logo.png" alt="{SITE['brand']}" class="footer-logo" width="100" height="100">
      <div class="footer-info">
        <p><strong>{SITE['legal_name']}</strong></p>
        <p>{SITE['owner']} &nbsp;-&nbsp; <a href="tel:{SITE['phone_tel']}">{SITE['phone_display']}</a></p>
        <p><a href="mailto:{SITE['email']}">{SITE['email']}</a></p>
        <p>Based in {SITE['city']}, {SITE['region']} &nbsp;&middot;&nbsp; Serving {SITE['area']}</p>
        <p class="footer-cities">{cities}</p>
        <div class="footer-social">
          <div class="social-icons">
            <a href="{SITE['facebook']}" class="social-icon" target="_blank" rel="noopener noreferrer" aria-label="Facebook"><svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg></a>
            <a href="{SITE['youtube']}" class="social-icon" target="_blank" rel="noopener noreferrer" aria-label="YouTube"><svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg></a>
          </div>
        </div>
      </div>
    </div>
    <div class="footer-copy-bar">
      <nav class="footer-links" aria-label="Footer links">
        <a href="gallery.html">Gallery</a>
        <a href="service-areas.html">Service Areas</a>
        <a href="contact.html">Contact</a>
        <a href="privacy-policy.html">Privacy Policy</a>
      </nav>
      <p class="footer-copy">&copy; <span id="current-year"></span> {SITE['legal_name']}. All rights reserved. &nbsp;&middot;&nbsp; <a href="https://knightlogics.com" rel="noopener noreferrer" style="color:inherit;text-decoration:none;opacity:.7;">Site by Knight Logics</a></p>
      <p class="footer-disclaimer">For digging projects, contact Sunshine 811 at least two full business days before work begins so underground utilities can be marked.</p>
    </div>
  </footer>

  <div class="nav-overlay" id="nav-overlay" aria-hidden="true"></div>
  <nav class="mobile-nav" id="mobile-nav" aria-label="Mobile navigation" aria-hidden="true" inert>
    <div class="mobile-nav-header">
      <a href="index.html" class="mobile-menu-brand" aria-label="{SITE['brand']} home">
        <img src="Images/Logo.png" alt="" class="mobile-nav-logo" width="36" height="36">
        <span class="mobile-menu-brand-name">{SITE['short']}</span>
      </a>
      <button class="mobile-nav-close" id="mobile-nav-close" aria-label="Close navigation menu">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" aria-hidden="true"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
      </button>
    </div>
    <div class="mobile-nav-links">
      <a href="index.html">Home</a>
      <button class="mobile-services-toggle" id="mobile-services-toggle" aria-expanded="false">
        Services
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="6 9 12 15 18 9"/></svg>
      </button>
      <div class="mobile-services-sub" id="mobile-services-sub">
        {chr(10).join(f'      <a href="{s["slug"]}.html">{s["nav"]}</a>' for s in SERVICES)}
      </div>
      <a href="about.html">About</a>
      <a href="gallery.html">Gallery</a>
      <a href="service-areas.html">Service Areas</a>
      <a href="contact.html">Contact</a>
    </div>
    <div class="mobile-cta-row">
      <a href="contact.html" class="btn btn-primary btn-full">Request Free Estimate</a>
      {call_cta_link("fw-header-call--menu")}
    </div>
    <div class="mobile-nav-social">
      <p class="mobile-nav-social-label">Follow Us</p>
      <div class="social-icons">
        <a href="{SITE['facebook']}" class="social-icon" target="_blank" rel="noopener noreferrer" aria-label="Facebook"><svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg></a>
        <a href="{SITE['youtube']}" class="social-icon" target="_blank" rel="noopener noreferrer" aria-label="YouTube"><svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg></a>
      </div>
    </div>
    <div class="mobile-menu-footer">
      <p>{SITE['legal_name']}</p>
    </div>
  </nav>"""


def page_shell(title: str, description: str, canonical: str, body: str, extra_head: str = "", current: str = "") -> str:
    canonical_url = f"{SITE['url']}/" if canonical == "index.html" else f"{SITE['url']}/{canonical}"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{description}">
  <link rel="canonical" href="{canonical_url}">
  <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">
  <meta name="author" content="{SITE['legal_name']}">
  <meta name="geo.region" content="US-FL">
  <meta name="geo.placename" content="{SITE['city']}, Florida">
  <meta name="geo.position" content="{SITE['geo_lat']};{SITE['geo_lng']}">
  <meta name="ICBM" content="{SITE['geo_lat']}, {SITE['geo_lng']}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{canonical_url}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{description}">
  <meta property="og:image" content="{SITE['url']}/Images/gallery/{HERO_DESKTOP}">
  <meta property="og:site_name" content="{SITE['brand']}">
  <meta property="og:locale" content="en_US">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{description}">
  <meta name="twitter:image" content="{SITE['url']}/Images/gallery/{HERO_DESKTOP}">
{extra_head}
{favicon_head()}
{fonts_head()}
  <link rel="preload" as="image" href="Images/gallery/{HERO_MOBILE}" fetchpriority="high" media="(max-width: 768px)">
  <link rel="preload" as="image" href="Images/gallery/{HERO_DESKTOP}" fetchpriority="high" media="(min-width: 769px)">
  <link rel="stylesheet" href="styles.css">
{analytics_head()}
</head>
<body>
{header(current)}
<main>
{body}
</main>
{footer()}
  <script src="script.js"></script>
</body>
</html>"""


def business_schema() -> str:
    services = [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["name"]}} for s in SERVICES]
    areas = [f"{c}, FL" for c in CITIES]
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "HomeAndConstructionBusiness",
        "@id": f"{SITE['url']}/#business",
        "name": SITE["brand"],
        "legalName": SITE["legal_name"],
        "description": f"{SITE['brand']} provides land clearing, pool dig-out support, trail clearing, pond bank clearing, ditch clearing, and debris removal in {SITE['area']}.",
        "url": SITE["url"],
        "telephone": f"+1-{SITE['phone_tel'][:3]}-{SITE['phone_tel'][3:6]}-{SITE['phone_tel'][6:]}",
        "email": SITE["email"],
        "address": {
            "@type": "PostalAddress",
            "addressLocality": SITE["city"],
            "addressRegion": SITE["region"],
            "addressCountry": "US",
        },
        "image": f"{SITE['url']}/Images/gallery/{HERO_DESKTOP}",
        "logo": f"{SITE['url']}/Images/Logo.png",
        "priceRange": "$$",
        "openingHours": "Mo-Sa 07:00-18:00",
        "areaServed": areas,
        "sameAs": [SITE["facebook"], SITE["youtube"]],
        "hasOfferCatalog": {
            "@type": "OfferCatalog",
            "name": "Outdoor Services",
            "itemListElement": services,
        },
    }, indent=2)


def write_index() -> None:
    cards = ""
    icons = [
        "M19 17H5a2 2 0 01-2-2V9a2 2 0 012-2h2l2-3h6l2 3h2a2 2 0 012 2v6a2 2 0 01-2 2z",
        "M3 6l3-3 3 3M6 3v13M21 6l-3-3-3 3M18 3v13M12 12v9",
        "M3 17l4-4 4 4 4-6 4 6",
        "M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7z",
        "M22 12H2M5 12V6h14v6",
        "M3 6h18l-2 13H5L3 6zM16 10a4 4 0 01-8 0",
    ]
    for i, s in enumerate(SERVICES):
        cards += f"""
          <a class="service-card" href="{s['slug']}.html" data-reveal>
            <div class="service-icon" aria-hidden="true">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="{icons[i % len(icons)]}"/></svg>
            </div>
            <h3>{s['name']}</h3>
            <p>{s['intro'].split('.')[0]}.</p>
          </a>"""

    thumbs = ""
    for img, alt, label in GALLERY[:4]:
        thumbs += f"""
          <a class="work-thumb" href="gallery.html" aria-label="View {label} gallery">
            <img src="Images/gallery/{img}" alt="{alt}" loading="lazy" width="600" height="450">
            <span class="work-thumb-label">{label}</span>
          </a>"""

    schema = f"""  <script type="application/ld+json">{business_schema()}</script>
  <script type="application/ld+json">{{"@context":"https://schema.org","@type":"WebSite","@id":"{SITE['url']}/#website","url":"{SITE['url']}/","name":"{SITE['brand']}","publisher":{{"@id":"{SITE['url']}/#business"}}}}</script>"""

    body = f"""
    <section class="hero">
      <div class="hero-bg" aria-hidden="true"></div>
      <div class="hero-overlay" aria-hidden="true"></div>
      <div class="container hero-inner">
        <div class="hero-copy">
          <p class="eyebrow">Land Clearing &middot; Pool Digging &middot; Trail &amp; Ditch Clearing &middot; Debris Removal</p>
          <h1>Auburndale Land Clearing, Pool Digging &amp; <span class="h1-accent">Outdoor Services</span></h1>
          <p class="hero-sub">
            {SITE['brand']} helps homeowners, property owners, and contractors with pool dig-out support, dirt removal, trail clearing, ditch clearing, pond bank clearing, brush cutting, and debris removal across {SITE['area']}.
          </p>
          <div class="hero-actions">
            <a class="btn btn-primary" href="contact.html">Request a Free Estimate</a>
            <a class="btn btn-ghost" href="#services">Our Services</a>
          </div>
          <div class="trust-row">
            <div class="trust-item"><strong>6+</strong><span>Core services</span></div>
            <div class="trust-divider" aria-hidden="true"></div>
            <div class="trust-item"><strong>Local</strong><span>{SITE['city']}, FL</span></div>
            <div class="trust-divider" aria-hidden="true"></div>
            <div class="trust-item"><strong>Faith</strong><span>Works ethic</span></div>
          </div>
          <div class="hero-social">
            <span class="hero-social-label">Follow us</span>
            <div class="social-icons">
              <a href="{SITE['facebook']}" class="social-icon" target="_blank" rel="noopener noreferrer" aria-label="Facebook"><svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg></a>
              <a href="{SITE['youtube']}" class="social-icon" target="_blank" rel="noopener noreferrer" aria-label="YouTube"><svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg></a>
            </div>
          </div>
        </div>
        <aside class="hero-card" aria-label="Get a free estimate">
          <p class="card-eyebrow">Free photo-based estimate</p>
          <h2 class="card-name">Talk to Tyler Today</h2>
          <p class="card-note">Send photos of your property and describe the project. Tyler will review the details and follow up with you.</p>
          {estimate_form(page="index.html")}
        </aside>
      </div>
    </section>

    <section id="services" class="services-section section-shell">
      <div class="container">
        <div class="section-heading" data-reveal>
          <p class="eyebrow">What we do</p>
          <h2>Outdoor Property Services in Polk County</h2>
          <p>Equipment-ready clearing, digging support, and cleanup for tough Florida outdoor jobs.</p>
        </div>
        <div class="services-grid">{cards}
        </div>
      </div>
    </section>

    <section class="work-teaser section-shell">
      <div class="container">
        <div class="section-heading" data-reveal>
          <p class="eyebrow">Proof of work</p>
          <h2>Real Jobs, Real Equipment</h2>
          <p>Every photo is from actual outdoor work — excavation, clearing, and property cleanup across Central Florida.</p>
        </div>
        <div class="work-teaser-grid">{thumbs}
        </div>
        <div style="text-align:center;margin-top:2rem">
          <a class="btn btn-ghost" href="gallery.html">See Full Gallery &rarr;</a>
        </div>
      </div>
    </section>

    <section id="about" class="about-section section-shell">
      <div class="container about-grid">
        <div class="about-copy" data-reveal>
          <p class="eyebrow">Why choose us</p>
          <h2>Owner-operated.<br>Equipment-ready.<br>Clear communication.</h2>
          <p>{SITE['owner']} runs {SITE['brand']} as a local Auburndale business built on hard work, honest estimates, and faith-based service. When you reach out, you're talking directly to the person doing the work.</p>
          <p>From pool dig-out dirt removal to pond bank clearing and ditch cleanup, we focus on outdoor property services that help homeowners and property owners reclaim usable land.</p>
        </div>
        <div class="about-card" data-reveal>
          <h3>What to expect</h3>
          <ul class="about-list">
            <li>Direct contact with Tyler — no call center</li>
            <li>Photo-based estimates for outdoor projects</li>
            <li>Equipment-ready for clearing and cleanup jobs</li>
            <li>Local {SITE['city']} business serving Polk County</li>
            <li>Residential and property-owner friendly service</li>
            <li>Colossians 3:23 work ethic on every job</li>
          </ul>
          <a class="btn btn-primary" href="contact.html">Request an Estimate</a>
        </div>
      </div>
    </section>

    <section class="process-section section-shell">
      <div class="container">
        <div class="section-heading" data-reveal>
          <p class="eyebrow">How it works</p>
          <h2>Simple Project Process</h2>
        </div>
        <div class="process-grid">
          <div class="process-step" data-reveal><span>1</span><h3>Send photos or call</h3><p>Share your property location and upload photos of the area that needs work.</p></div>
          <div class="process-step" data-reveal><span>2</span><h3>Confirm scope</h3><p>We review access, vegetation, dirt volume, and the type of service needed.</p></div>
          <div class="process-step" data-reveal><span>3</span><h3>Receive estimate</h3><p>Get a clear estimate before work begins — no vague pricing.</p></div>
          <div class="process-step" data-reveal><span>4</span><h3>Schedule service</h3><p>We show up with the right equipment and get your property cleared or cleaned up.</p></div>
        </div>
      </div>
    </section>

    <section id="faq" class="faq-section section-shell">
      <div class="container">
        <div class="section-heading" data-reveal>
          <p class="eyebrow">Common questions</p>
          <h2>Frequently Asked Questions</h2>
        </div>
        <div class="faq-list">
          <div class="faq-item"><button class="faq-question" aria-expanded="false" aria-controls="faq-a1">Do you offer free estimates?<svg class="faq-chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="6 9 12 15 18 9"/></svg></button><div class="faq-answer" id="faq-a1" aria-hidden="true" inert><div class="faq-answer-inner"><p>Yes. Send photos through our contact form or email {SITE['email']}. Photo-based estimates help us understand access, vegetation, and project scope before we schedule a visit.</p></div></div></div>
          <div class="faq-item"><button class="faq-question" aria-expanded="false" aria-controls="faq-a2">What areas do you serve?<svg class="faq-chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="6 9 12 15 18 9"/></svg></button><div class="faq-answer" id="faq-a2" aria-hidden="true" inert><div class="faq-answer-inner"><p>We are based in {SITE['city']} and serve {SITE['area']}, including Winter Haven, Lakeland, Bartow, Haines City, Lake Wales, and nearby communities.</p></div></div></div>
          <div class="faq-item"><button class="faq-question" aria-expanded="false" aria-controls="faq-a3">Do I need to call 811 before digging?<svg class="faq-chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="6 9 12 15 18 9"/></svg></button><div class="faq-answer" id="faq-a3" aria-hidden="true" inert><div class="faq-answer-inner"><p>For digging or excavation projects, Florida law requires contacting Sunshine 811 at least two full business days before work begins so underground utilities can be marked.</p></div></div></div>
          <div class="faq-item"><button class="faq-question" aria-expanded="false" aria-controls="faq-a4">Can you help with pool dig-out dirt removal?<svg class="faq-chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="6 9 12 15 18 9"/></svg></button><div class="faq-answer" id="faq-a4" aria-hidden="true" inert><div class="faq-answer-inner"><p>Yes. We provide pool dig-out support and dirt removal for pool installation projects. We do not install pools — we support the excavation and cleanup side of the project.</p></div></div></div>
        </div>
      </div>
    </section>

    <section id="contact" class="contact-section section-shell">
      <div class="container contact-inner" data-reveal>
        <p class="eyebrow">Ready to get started?</p>
        <h2>Need land cleared, a ditch cleaned, or dirt removed?</h2>
        <p>Request an estimate from {SITE['brand']} today. Send photos for the fastest quote.</p>
        <a class="btn btn-primary btn-lg" href="contact.html">Request a Free Estimate</a>
      </div>
    </section>"""

    html = page_shell(
        "Auburndale Land Clearing, Pool Digging & Outdoor Services | Faith Works ODS",
        f"Land clearing, pool dig-out support, trail clearing, ditch clearing, pond bank clearing, and debris removal in {SITE['city']} and Polk County, FL. Free photo-based estimates.",
        "index.html",
        body,
        schema,
        "index.html",
    )
    (ROOT / "index.html").write_text(html, encoding="utf-8")


def write_service_page(s: dict) -> None:
    bullets = "\n".join(f"            <li>{b}</li>" for b in s["bullets"])
    benefits = "\n".join(f"            <li>{b}</li>" for b in s["benefits"])
    schema = f"""  <script type="application/ld+json">{{"@context":"https://schema.org","@type":"Service","name":"{s['name']}","description":"{s['desc']}","provider":{{"@id":"{SITE['url']}/#business"}},"url":"{SITE['url']}/{s['slug']}.html"}}</script>
  <script type="application/ld+json">{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"Home","item":"{SITE['url']}/"}},{{"@type":"ListItem","position":2,"name":"{s['name']}","item":"{SITE['url']}/{s['slug']}.html"}}]}}</script>"""

    body = f"""
    <section class="sp-hero">
      <div class="container">
        <p class="eyebrow"><a href="index.html">Home</a> &rsaquo; Services &rsaquo; {s['name']}</p>
        <h1>{s['h1']}</h1>
        <p>{s['desc']}</p>
      </div>
    </section>
    <section class="section-shell">
      <div class="container sp-layout">
        <div class="sp-content" data-reveal>
          <h2>{s['name']} in {SITE['area']}</h2>
          <p>{s['intro']}</p>
          <h2>What We Handle</h2>
          <ul>{bullets}</ul>
          <h2>Benefits</h2>
          <ul>{benefits}</ul>
          <h2>Owner-Operated Service</h2>
          <p>When Tyler handles your project, you get direct communication from estimate through completion — not a subcontractor chain. Serving residential and property-owner clients throughout {SITE['city']}, Polk County, and nearby Central Florida areas.</p>
          <p class="utility-note"><strong>Utility note:</strong> For any digging or excavation work, Sunshine 811 should be contacted at least two full business days before work begins.</p>
        </div>
        <aside class="sp-sidebar">
          <div class="hero-card" aria-label="Get a free estimate">
            <p class="card-eyebrow">Free photo-based estimate</p>
            <h2 class="card-name">Request {s['name']}</h2>
            <p class="card-note">Upload photos and describe your property for a faster quote.</p>
            {estimate_form(selected=s['name'], subject=f"{s['name']} estimate - {SITE['brand']}", page=f"{s['slug']}.html")}
          </div>
        </aside>
      </div>
    </section>
    <section class="areas-strip">
      <div class="container">
        <p class="eyebrow">Where we work</p>
        <p>Serving <strong>{'</strong>, <strong>'.join(CITIES[:8])}</strong>, and surrounding Polk County communities. <a href="service-areas.html">See all service areas &rarr;</a></p>
      </div>
    </section>"""

    html = page_shell(s["title"], s["desc"], f"{s['slug']}.html", body, schema, f"{s['slug']}.html")
    (ROOT / f"{s['slug']}.html").write_text(html, encoding="utf-8")


def write_gallery() -> None:
    items = ""
    for img, alt, label in GALLERY:
        items += f"""
          <figure class="gallery-item" data-reveal>
            <img src="Images/gallery/{img}" alt="{alt}" loading="lazy" width="800" height="600">
            <figcaption>{label}</figcaption>
          </figure>"""
    body = f"""
    <section class="sp-hero">
      <div class="container">
        <p class="eyebrow"><a href="index.html">Home</a> &rsaquo; Gallery</p>
        <h1>Project Gallery</h1>
        <p>Real outdoor work from {SITE['brand']} — excavation, land clearing, stump removal, and property cleanup across Central Florida.</p>
      </div>
    </section>
    <section class="section-shell">
      <div class="container">
        <div class="gallery-grid">{items}
        </div>
      </div>
    </section>"""
    html = page_shell(
        f"Outdoor Services Project Gallery | {SITE['brand']}",
        f"View excavation, land clearing, and outdoor cleanup projects by {SITE['brand']} in Polk County, FL.",
        "gallery.html",
        body,
        "",
        "gallery.html",
    )
    (ROOT / "gallery.html").write_text(html, encoding="utf-8")


def write_about() -> None:
    body = f"""
    <section class="sp-hero">
      <div class="container">
        <p class="eyebrow"><a href="index.html">Home</a> &rsaquo; About</p>
        <h1>About {SITE['brand']}</h1>
        <p>Local Auburndale outdoor services built on faith, hard work, and equipment-ready property cleanup.</p>
      </div>
    </section>
    <section class="section-shell">
      <div class="container about-grid">
        <div class="about-copy" data-reveal>
          <h2>Meet {SITE['owner']}</h2>
          <p>{SITE['owner']} founded {SITE['legal_name']} in {SITE['city']}, Florida to serve homeowners, property owners, and contractors who need reliable outdoor property work — not vague handyman services.</p>
          <p>{SITE['brand']} specializes in land clearing, pool dig-out support, trail clearing, pond bank clearing, ditch clearing, brush cutting, and debris removal throughout Polk County and surrounding Central Florida areas.</p>
          <p>Our work is guided by Colossians 3:23 — whatever we do, we work at it with all our heart. That means showing up prepared, communicating clearly, and leaving properties cleaner than we found them.</p>
        </div>
        <div class="about-card" data-reveal>
          <img src="Images/Logo.png" alt="{SITE['brand']} logo" class="about-logo" width="220" height="220">
          <h3>Business Details</h3>
          <ul class="about-list">
            <li>Legal name: {SITE['legal_name']}</li>
            <li>Based in {SITE['city']}, {SITE['region']}</li>
            <li>Service-area business — we come to you</li>
            <li>Email: {SITE['email']}</li>
            <li>Active Florida LLC</li>
          </ul>
        </div>
      </div>
    </section>"""
    html = page_shell(
        f"About {SITE['owner']} | {SITE['brand']}",
        f"Meet {SITE['owner']}, owner of {SITE['brand']} — land clearing, pool digging support, and outdoor property services in Polk County, FL.",
        "about.html",
        body,
        "",
        "about.html",
    )
    (ROOT / "about.html").write_text(html, encoding="utf-8")


def write_contact() -> None:
    body = f"""
    <section class="sp-hero">
      <div class="container">
        <p class="eyebrow"><a href="index.html">Home</a> &rsaquo; Contact</p>
        <h1>Request an Outdoor Services Estimate</h1>
        <p>Send photos of your property and tell us what you need cleared, dug, or cleaned up. We'll review the details and follow up with you.</p>
      </div>
    </section>
    <section class="section-shell">
      <div class="container">
        <div class="contact-page-form hero-card" data-reveal>
          <p class="card-eyebrow">Free photo-based estimate</p>
          <h2 class="card-name">Project Estimate Form</h2>
          {estimate_form('contact-form', subject=f'Contact form - {SITE["brand"]}', page='contact.html')}
        </div>
        <div class="contact-direct">
          <div class="contact-direct-card"><p class="eyebrow">Phone</p><p><a href="tel:{SITE['phone_tel']}">{SITE['phone_display']}</a></p></div>
          <div class="contact-direct-card"><p class="eyebrow">Email</p><p><a href="mailto:{SITE['email']}">{SITE['email']}</a></p></div>
          <div class="contact-direct-card"><p class="eyebrow">Service Area</p><p>{SITE['city']}, FL<br>Serving {SITE['area']}</p></div>
        </div>
      </div>
    </section>"""
    html = page_shell(
        f"Contact {SITE['brand']} | Free Outdoor Services Estimate",
        f"Request a free photo-based estimate for land clearing, pool digging support, ditch clearing, and outdoor cleanup in Polk County, FL.",
        "contact.html",
        body,
        "",
        "contact.html",
    )
    (ROOT / "contact.html").write_text(html, encoding="utf-8")


def write_service_areas() -> None:
    city_cards = ""
    for c in CITIES:
        city_cards += f'<div class="area-card" data-reveal><h3>{c}, FL</h3><p>Land clearing, pool dig-out support, trail clearing, pond bank clearing, ditch clearing, and debris removal.</p></div>'
    body = f"""
    <section class="sp-hero">
      <div class="container">
        <p class="eyebrow"><a href="index.html">Home</a> &rsaquo; Service Areas</p>
        <h1>Service Areas in Polk County &amp; Central Florida</h1>
        <p>Based in {SITE['city']}, {SITE['brand']} serves property owners across Polk County and nearby Central Florida communities.</p>
      </div>
    </section>
    <section class="section-shell">
      <div class="container">
        <div class="areas-grid">{city_cards}</div>
        <p class="areas-note" data-reveal>Not sure if we serve your area? Send your city and project photos through our <a href="contact.html">contact form</a> and we'll confirm coverage.</p>
      </div>
    </section>"""
    html = page_shell(
        f"Service Areas | {SITE['brand']} Polk County FL",
        f"{SITE['brand']} serves Auburndale, Lakeland, Winter Haven, Bartow, Haines City, and Polk County, FL.",
        "service-areas.html",
        body,
        "",
        "service-areas.html",
    )
    (ROOT / "service-areas.html").write_text(html, encoding="utf-8")


def write_privacy() -> None:
    body = f"""
    <section class="sp-hero"><div class="container"><h1>Privacy Policy</h1></div></section>
    <section class="section-shell"><div class="container sp-content">
      <p>{SITE['legal_name']} ("we") respects your privacy. Information submitted through our contact forms is processed by <strong>Formspree</strong> (formspree.io) and delivered to us by email. We use that information only to respond to your estimate request and provide our services.</p>
      <p>We do not sell personal information. Analytics tools may collect anonymous usage data to improve the website.</p>
      <p>Questions? Contact <a href="mailto:{SITE['email']}">{SITE['email']}</a>.</p>
    </div></section>"""
    (ROOT / "privacy-policy.html").write_text(
        page_shell("Privacy Policy", f"Privacy policy for {SITE['brand']}.", "privacy-policy.html", body),
        encoding="utf-8",
    )


def write_sitemap() -> None:
    pages = ["index.html", "about.html", "contact.html", "gallery.html", "service-areas.html", "privacy-policy.html"]
    pages += [f"{s['slug']}.html" for s in SERVICES]
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for p in pages:
        loc = SITE["url"] if p == "index.html" else f"{SITE['url']}/{p}"
        lines.append(f"  <url><loc>{loc}</loc><changefreq>monthly</changefreq><priority>{'1.0' if p == 'index.html' else '0.8'}</priority></url>")
    lines.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(lines), encoding="utf-8")


def write_robots() -> None:
    (ROOT / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\nSitemap: {SITE['url']}/sitemap.xml\n",
        encoding="utf-8",
    )


def write_cname() -> None:
    (ROOT / "CNAME").write_text("faithworksods.com\n", encoding="utf-8")


def write_styles() -> None:
    src = Path(r"E:\ScreenTeamLLC\styles.css").read_text(encoding="utf-8")
    src = src.replace("THE SCREEN TEAM LLC", "FAITH WORKS OUTDOOR SERVICES")
    src = src.replace("Dark navy professional theme", "Black & gold outdoor services theme")
    src = src.replace('"Oswald", sans-serif', '"Cinzel", serif')
    src = src.replace("rgba(7, 13, 24, 0.9)", "rgba(10, 10, 10, 0.94)")
    src = src.replace("#070d18", "#0a0a0a")
    src = src.replace("#0d1c2e", "#141414")
    src = src.replace("#152b40", "#1f2a1f")
    src = src.replace("#deeaf5", "#f5f0e8")
    src = src.replace("#7499b8", "#a89878")
    src = src.replace("#3da8d8", "#c9a227")
    src = src.replace("#1b5f82", "#8a6d12")
    src = src.replace("rgba(61, 168, 216,", "rgba(201, 162, 39,")
    src = src.replace("#7499b8", "#a89878")
    src = src.replace("#aac8df", "#d4c4a0")
    src = src.replace("--container:     1200px;", "--container:     1400px;")
    src = src.replace('url("Images/ScreenTeamBanner.webp")', f'url("Images/gallery/{HERO_DESKTOP}")')
    src = src.replace('url("Images/ScreenTeamBanner-mobile.webp")', f'url("Images/gallery/{HERO_MOBILE}")')
    src = src.replace('url("Images/service-hero-bg.jpg")', f'url("Images/gallery/{HERO_DESKTOP}")')
    src = src.replace("filter: brightness(0) invert(1);\n  mix-blend-mode: screen;", "filter: none;")
    src = src.replace(
        "font-size: clamp(3.8rem, 8.5vw, 7rem);",
        "font-size: clamp(2.2rem, 4.8vw, 4.25rem);",
    )
    src = src.replace(
        "  .hero-inner {\n    grid-template-columns: 1fr;\n    max-width: 680px;\n",
        "  .hero-inner {\n    grid-template-columns: 1fr;\n    max-width: min(960px, 100%);\n",
    )
    src = src.replace(
        "  .hero-copy h1 {\n    font-size: clamp(3.2rem, 10vw, 5rem);\n  }",
        "  .hero-copy h1 {\n    font-size: clamp(1.75rem, 7vw, 2.75rem);\n  }",
    )
    src = src.replace(".footer-logo {\n  height: 108px;\n  width: auto;\n  filter: brightness(0) invert(1);\n  opacity: 0.35;\n}", ".footer-logo {\n  height: 100px;\n  width: auto;\n  opacity: 0.85;\n}")
    extra = """

/* Faith Works extras */
.process-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 18px;
}
.process-step {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: 24px 20px;
}
.process-step span {
  display: inline-flex;
  width: 36px;
  height: 36px;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background: rgba(201, 162, 39, 0.15);
  color: var(--accent);
  font-family: var(--font-head);
  font-weight: 700;
  margin-bottom: 12px;
}
.process-step h3 {
  font-family: var(--font-head);
  font-size: 1rem;
  color: #fff;
  margin-bottom: 8px;
  text-transform: uppercase;
}
.process-step p { font-size: 0.92rem; color: var(--muted); line-height: 1.6; }
.process-section { background: linear-gradient(180deg, #0a0a0a 0%, #121812 100%); border-top: 1px solid var(--border); }
.gallery-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 18px; }
.gallery-item { margin: 0; background: var(--bg-card); border: 1px solid var(--border); border-radius: var(--radius-md); overflow: hidden; }
.gallery-item img { width: 100%; aspect-ratio: 4/3; object-fit: cover; }
.gallery-item figcaption { padding: 12px 14px; font-size: 0.85rem; color: var(--muted); }
.areas-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; }
.area-card { background: var(--bg-card); border: 1px solid var(--border); border-radius: var(--radius-md); padding: 22px 20px; }
.area-card h3 { font-family: var(--font-head); color: #fff; margin-bottom: 8px; font-size: 1.05rem; }
.area-card p { color: var(--muted); font-size: 0.92rem; line-height: 1.6; }
.areas-note { margin-top: 32px; text-align: center; color: var(--muted); }
.areas-note a { color: var(--accent); }
.about-logo { margin: 0 auto 20px; border-radius: 50%; max-width: 220px; }
.utility-note { margin-top: 24px; padding: 16px; border-left: 3px solid var(--accent); background: rgba(201,162,39,0.08); border-radius: 0 8px 8px 0; }
.footer-disclaimer { font-size: 0.72rem; color: var(--muted); margin-top: 8px; opacity: 0.8; }
.form-group input[type="file"] { padding: 8px; }

/* ---- Knight-style mobile header & drawer ---- */
.site-header .header-inner {
  min-height: 84px;
  gap: clamp(10px, 1.5vw, 18px);
  flex-wrap: nowrap;
}
.brand-wrap {
  display: flex;
  align-items: center;
  gap: 12px;
  flex: 0 0 auto;
  min-width: 0;
}
.site-header .brand-logo {
  height: 68px;
  width: auto;
}
.site-nav {
  flex: 1 1 auto;
  justify-content: center;
  gap: clamp(10px, 1.4vw, 22px);
  min-width: 0;
}
.site-nav a,
.nav-dropdown-btn {
  font-size: clamp(0.68rem, 0.45vw + 0.6rem, 0.78rem);
  letter-spacing: 0.08em;
  white-space: nowrap;
}
.btn-header-estimate {
  min-height: 40px;
  padding: 0 14px;
  font-size: 0.74rem;
  letter-spacing: 0.06em;
  white-space: nowrap;
}
.header-actions {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-shrink: 0;
}
.hamburger-btn {
  display: none;
  flex-shrink: 0;
}

/* Knight Group-style call CTA (gold theme) */
.fw-header-call {
  display: inline-flex;
  flex-direction: row;
  align-items: center;
  gap: 0.55rem;
  flex-shrink: 0;
  text-decoration: none;
  color: #fff;
  transition: transform 0.18s ease;
}
.fw-header-call:hover,
.fw-header-call:focus-visible {
  transform: translateY(-1px);
  outline: none;
}
.fw-header-call__icon {
  flex: 0 0 auto;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 42px;
  height: 42px;
  border-radius: 50%;
  border: 2px solid var(--accent);
  color: var(--accent);
  background: rgba(201, 162, 39, 0.12);
  box-shadow: 0 0 14px rgba(201, 162, 39, 0.22);
}
.fw-header-call__icon svg {
  display: block;
}
.fw-header-call__text {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: center;
  gap: 0.05rem;
  line-height: 1.1;
  min-width: 0;
}
.fw-header-call__label {
  font-size: clamp(0.52rem, 0.15vw + 0.46rem, 0.62rem);
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: rgba(245, 240, 232, 0.88);
}
.fw-header-call__number {
  font-family: var(--font-head);
  font-size: clamp(0.78rem, 0.35vw + 0.62rem, 0.92rem);
  font-weight: 700;
  letter-spacing: 0.02em;
  color: #fff;
  white-space: nowrap;
}
.fw-header-call:hover .fw-header-call__icon,
.fw-header-call:focus-visible .fw-header-call__icon {
  border-color: #e0c04a;
  color: #f0e0a8;
  background: rgba(201, 162, 39, 0.22);
}
.fw-header-call:focus-visible .fw-header-call__icon {
  outline: 2px solid var(--accent);
  outline-offset: 2px;
}
.fw-header-call--menu {
  width: 100%;
  justify-content: center;
  padding: 12px 16px;
  border: 1px solid rgba(201, 162, 39, 0.28);
  border-radius: var(--radius-md);
  background: rgba(201, 162, 39, 0.06);
}

.hero-copy h1 {
  font-size: clamp(2.2rem, 4.8vw, 4.25rem);
  line-height: 0.98;
  margin-bottom: 20px;
}

/* Hero parallax */
.hero {
  position: relative;
  overflow: hidden;
  isolation: isolate;
  background: #0a0a0a;
  background-image: none;
}
.hero-bg {
  position: absolute;
  inset: -22% 0;
  z-index: 0;
  background: url("Images/gallery/photo-of-all-equipment.webp") center / cover no-repeat;
  transform: translate3d(0, var(--hero-shift, 0px), 0);
  will-change: transform;
}
.hero-overlay {
  z-index: 1;
}
.hero-inner {
  position: relative;
  z-index: 2;
  grid-template-columns: minmax(0, 1fr) minmax(360px, 440px);
  gap: clamp(32px, 4vw, 56px);
  max-width: none;
}

@media (max-width: 720px) {
  .hero {
    background-image: none;
  }
  .hero-bg {
    background-image: url("Images/gallery/excavator-and-truck-photo.webp");
    background-position: top center;
  }
}

.brand-text-wrap {
  display: none;
  flex-direction: column;
  min-width: 0;
  line-height: 1.25;
}
.brand-title-link {
  text-decoration: none;
  color: inherit;
}
.brand-title {
  font-family: var(--font-head);
  font-size: 1.05rem;
  font-weight: 600;
  color: #fff;
  letter-spacing: 0.04em;
}
.brand-tagline {
  font-size: 0.72rem;
  color: var(--muted);
  margin-top: 2px;
}
.header-brand-ctas {
  display: none;
  align-items: center;
  gap: 8px;
  margin-top: 6px;
  flex-wrap: wrap;
}
.btn-mobile-estimate {
  display: inline-flex;
  align-items: center;
  padding: 5px 10px;
  border-radius: 6px;
  font-size: 0.68rem;
  font-weight: 700;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  text-decoration: none;
  color: #0a0a0a;
  background: linear-gradient(135deg, var(--accent) 0%, var(--accent-dark) 100%);
  white-space: nowrap;
}
.mobile-menu-brand {
  display: flex;
  align-items: center;
  gap: 12px;
  text-decoration: none;
  color: inherit;
}
.mobile-menu-brand-name {
  font-family: var(--font-head);
  font-size: 1.05rem;
  font-weight: 600;
  color: #fff;
  letter-spacing: 0.04em;
}
.mobile-cta-row {
  display: none;
  flex-direction: column;
  gap: 10px;
  padding: 16px 16px 8px;
  border-top: 1px solid rgba(201, 162, 39, 0.15);
}
.mobile-menu-footer {
  display: none;
  padding: 16px 20px 24px;
  border-top: 1px solid rgba(255, 255, 255, 0.08);
  margin-top: auto;
  text-align: center;
}
.mobile-menu-footer p {
  margin: 0;
  font-size: 0.72rem;
  color: var(--muted);
}

@media (max-width: 1320px) and (min-width: 1201px) {
  .site-nav {
    gap: 12px;
  }
}

@media (max-width: 1200px) {
  .site-nav {
    display: none !important;
  }
  .site-header .header-inner {
    min-height: 78px;
    padding: 10px 0;
    gap: 10px;
    justify-content: flex-start;
  }
  .site-header .brand-logo {
    height: 50px;
  }
  .header-actions {
    display: flex !important;
    margin-left: auto;
    flex-shrink: 0;
  }
  .btn-header-estimate {
    min-height: 38px;
    padding: 0 12px;
    font-size: 0.68rem;
  }
  .fw-header-call {
    margin-left: 8px;
    flex-shrink: 0;
  }
  .fw-header-call__text {
    display: flex;
  }
  .fw-header-call__icon {
    width: 36px;
    height: 36px;
  }
  .fw-header-call__label {
    font-size: 0.48rem;
    letter-spacing: 0.08em;
  }
  .fw-header-call__number {
    font-size: clamp(0.66rem, 2.8vw, 0.78rem);
    white-space: nowrap;
  }
  .hamburger-btn {
    display: flex !important;
    flex-shrink: 0;
    order: -1;
    background: rgba(20, 20, 20, 0.95);
    border: 1px solid rgba(201, 162, 39, 0.28);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border-radius: 12px;
  }
  .hamburger-btn span {
    background: var(--accent);
    box-shadow: 0 0 8px rgba(201, 162, 39, 0.2);
  }
  .hamburger-btn:hover {
    background: rgba(30, 30, 30, 1);
    border-color: rgba(201, 162, 39, 0.5);
  }
  .brand-wrap {
    flex: 0 0 auto;
  }
  .brand-text-wrap {
    display: none;
  }
  .mobile-cta-row,
  .mobile-menu-footer {
    display: flex;
  }
  .mobile-nav {
    left: -100%;
    right: auto;
    border-right: 1px solid rgba(201, 162, 39, 0.28);
    border-left: none;
    box-shadow: 10px 0 50px rgba(0, 0, 0, 0.6);
    background: linear-gradient(135deg, #111111 0%, #1a1a1a 50%, #111111 100%);
    transition: left 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  }
  .mobile-nav.is-open {
    left: 0;
    right: auto;
  }
  .mobile-nav-logo {
    height: 36px;
    width: 36px;
    filter: none;
    border-radius: 8px;
    object-fit: contain;
  }
  .mobile-nav-close:hover {
    background: rgba(201, 162, 39, 0.12);
    border-color: var(--accent);
  }
  .mobile-nav-links a:hover,
  .mobile-services-toggle:hover {
    background: rgba(201, 162, 39, 0.1);
    border-color: var(--accent);
  }
}

@media (min-width: 1201px) {
  .hamburger-btn {
    display: none !important;
  }
}

@media (max-width: 640px) {
  .brand-text-wrap,
  .header-brand-ctas,
  .header-actions {
    display: none !important;
  }
  .site-header .header-inner {
    min-height: 64px;
    padding: 8px 0;
    gap: 8px;
  }
  .site-header .brand-logo {
    height: 44px;
  }
  .fw-header-call {
    margin-left: auto;
    gap: 0.4rem;
  }
  .fw-header-call__icon {
    width: 32px;
    height: 32px;
  }
  .fw-header-call__label {
    font-size: 0.46rem;
  }
  .fw-header-call__number {
    font-size: clamp(0.62rem, 2.6vw, 0.74rem);
  }
  .hero-copy .eyebrow {
    font-size: 0.62rem;
    letter-spacing: 0.08em;
    line-height: 1.45;
    margin-bottom: 12px;
  }
  .hero-copy h1 {
    font-size: clamp(1.65rem, 7.5vw, 2.35rem);
    line-height: 1.06;
    margin-bottom: 16px;
  }
}

@media (max-width: 480px) {
  .site-header .brand-logo {
    height: 40px;
  }
}

@media (max-width: 720px) {
  .site-header .header-inner {
    flex-wrap: nowrap;
  }
}

html, body {
  overflow-x: clip;
}

@media (max-width: 900px) { .process-grid, .areas-grid { grid-template-columns: repeat(2, 1fr); } .gallery-grid { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 560px) { .process-grid, .areas-grid, .gallery-grid { grid-template-columns: 1fr; } }
"""
    (ROOT / "styles.css").write_text(src + extra, encoding="utf-8")


def patch_script() -> None:
    text = (ROOT / "script.js").read_text(encoding="utf-8")
    text = text.replace("(727) 386-6562", SITE["phone_display"])
    text = text.replace("7273866562", SITE["phone_tel"])
    text = text.replace("Chris will be in touch shortly", "Tyler will review your project and contact you shortly")
    text = text.replace("hero-contact-form", "hero-contact-form")
    # Handle contact page form too
    if "contact-form" not in text:
        contact_handler = """
const contactForm = document.getElementById("contact-form");
const contactSuccess = document.getElementById("form-success");

if (contactForm && contactSuccess && !heroForm) {
  contactForm.addEventListener("submit", async function (e) {
    e.preventDefault();
    const submitBtn = contactForm.querySelector("[type='submit']");
    const originalText = submitBtn.textContent;
    submitBtn.disabled = true;
    submitBtn.textContent = "Sending...";
    try {
      const res = await fetch(contactForm.action, {
        method: "POST",
        body: new FormData(contactForm),
        headers: { Accept: "application/json" },
      });
      if (res.ok) {
        submitBtn.textContent = "Sent! ✓";
        setTimeout(() => {
          contactForm.hidden = true;
          contactSuccess.hidden = false;
        }, 1800);
      } else {
        submitBtn.disabled = false;
        submitBtn.textContent = originalText;
        alert("Something went wrong. Please email contact@faithworksods.com directly.");
      }
    } catch {
      submitBtn.disabled = false;
      submitBtn.textContent = originalText;
      alert("Could not send. Please email contact@faithworksods.com directly.");
    }
  });
}
"""
        text += contact_handler

    parallax_block = """
// ---- Hero parallax ----
(function initHeroParallax() {
  const hero = document.querySelector(".hero");
  const bg = hero && hero.querySelector(".hero-bg");
  if (!hero || !bg) return;
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

  let restTop = 0;
  let ticking = false;
  const rate = 0.45;

  function update() {
    ticking = false;
    const rect = hero.getBoundingClientRect();
    if (window.scrollY < 2) {
      const header = document.querySelector(".site-header");
      restTop = header ? header.getBoundingClientRect().height : rect.top;
    }
    const shift = -(rect.top - restTop) * rate;
    bg.style.setProperty("--hero-shift", Math.round(shift) + "px");
  }

  function queue() {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(update);
  }

  update();
  window.addEventListener("scroll", queue, { passive: true });
  window.addEventListener("resize", queue, { passive: true });
})();
"""
    if "initHeroParallax" not in text:
        text += parallax_block

    (ROOT / "script.js").write_text(text, encoding="utf-8")


def main() -> None:
    write_styles()
    patch_script()
    write_index()
    for s in SERVICES:
        write_service_page(s)
    write_gallery()
    write_about()
    write_contact()
    write_service_areas()
    write_privacy()
    write_sitemap()
    write_robots()
    write_cname()
    print("Built Faith Works website in", ROOT)


if __name__ == "__main__":
    main()

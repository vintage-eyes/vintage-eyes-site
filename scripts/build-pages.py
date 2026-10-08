"""Render dedicated static tour pages. Run from any directory with Python 3."""
import html
import json
import re
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://vintageeyestours.in"
TOURS = json.loads((ROOT / "data/tours.json").read_text(encoding="utf-8"))
HOME = (ROOT / "index.html").read_text(encoding="utf-8")


def esc(value):
    return html.escape(str(value), quote=True)


def extract(pattern):
    match = re.search(pattern, HOME, re.S)
    if not match:
        raise ValueError(f"Shared homepage section missing: {pattern}")
    return match.group(0)


def relative(markup):
    return markup.replace('="assets/', '="../../assets/').replace('href="./"', 'href="../../"')


HEADER = relative(extract(r'<header class="site-header">.*?</header>'))
for anchor in ["journeys", "perspective", "questions"]:
    HEADER = HEADER.replace(f'href="#{anchor}"', f'href="../../#{anchor}"')
FOOTER = relative(extract(r'<footer class="site-footer">.*?</footer>'))
PLAN = relative(extract(r'<section id="plan".*?</section>'))
CHAT = relative(extract(r'<a class="floating-whatsapp".*?</a>'))
ICON = (ROOT / "assets/icons/whatsapp.svg").read_text(encoding="utf-8")
ICON = re.sub(r'class="[^"]*"', 'class="whatsapp-icon" aria-hidden="true" focusable="false"', ICON)


def list_items(items):
    return "\n".join(f"<li>{esc(item)}</li>" for item in items)


for tour in TOURS:
    name = esc(tour["name"])
    day_count = len(tour["days"])
    is_day_tour = tour["id"] == "sightseeing"
    canonical = f'{SITE}/tours/{tour["slug"]}/'
    direct_chat = "https://wa.me/916363336467?text=" + quote(f'Hello Vintage Eyes! I’m interested in {tour["name"]}. Please share availability and a quote.')
    description = f'{tour["title"]}. See the complete itinerary, inclusions, transfers and stay options. Enquire with Vintage Eyes on WhatsApp.'
    plan = PLAN.replace(f'value="{esc(tour["select"])}"', f'value="{esc(tour["select"])}" selected')
    itinerary = []
    for index, day in enumerate(tour["days"], 1):
        stops = []
        for stop_index, stop in enumerate(day["stops"], 1):
            optional = '<span class="optional-stop">Optional · extra charge · subject to availability</span>' if "coracle" in stop.lower() else ""
            stops.append(f'<li><span class="stop-number">{stop_index:02}</span><div><h4>{esc(stop)}</h4>{optional}</div></li>')
        itinerary.append(f'''<article class="day-itinerary" data-day="{index}">
          <div class="day-heading"><span class="day-number">{index:02}</span><div><p class="eyebrow">DAY {index}</p><h3>{esc(day["title"])}</h3></div></div>
          <p class="day-intro">{esc(day["intro"])}</p>
          <ol class="stop-list">{"".join(stops)}</ol>
          <p class="day-end">{esc(day["end"])}</p>
        </article>''')
    included = ["Private air-conditioned car and driver", "Driver charges and parking", "Sightseeing along the listed route", "Pickup and drop-off as agreed"]
    if not is_day_tour:
        included.insert(0, f'Hotel accommodation · {tour["stays"]}')
    included.append("8 hours of sightseeing" if is_day_tour else "Daily sightseeing allowance: 8 hours / 80 km")
    excluded = ["Monument entry tickets and camera fees", "Optional rides and activities", "Personal purchases and expenses", "Items outside the confirmed inclusions"]
    excluded.insert(0, "Meals and refreshments" if tour["id"] == "regal" else "Meals not specified in your quote")
    if is_day_tour:
        excluded.append("Hotel accommodation")
    allowance_note = '<p class="section-note">For this circuit, ask us to confirm the intercity transfer mileage and final drop-off coverage in your quote.</p>' if tour["id"] == "regal" else ''
    stay_options = '<a class="text-link" href="../../#journeys">Compare our stay packages <span aria-hidden="true">↗</span></a>' if is_day_tour else '''<div class="stay-options"><article><p class="eyebrow">STANDARD</p><h3>A simple base</h3><p>For a practical stay and more time out exploring.</p></article><article><p class="eyebrow">DELUXE</p><h3>A little more comfort</h3><p>For the room and comforts you enjoy returning to.</p></article><article><p class="eyebrow">PREMIUM</p><h3>Make the stay special</h3><p>For a holiday where the hotel is part of the experience.</p></article></div><p class="section-note">Hotel category, property, room type and meals are agreed with your quote, subject to availability. Breakfast mentioned in the itinerary is not a blanket promise of an included meal.</p>'''
    faqs = "".join(f'<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in tour["faqs"])
    faqs += '<details><summary>How do I confirm a booking?</summary><p>Send an enquiry first. We’ll discuss availability, your itinerary and the final price, then share the payment and cancellation terms for you to review. An enquiry is not a confirmed reservation.</p></details>'
    others = "".join(f'<a class="other-tour" href="../{other["slug"]}/"><span>{esc(other["duration"])}</span><strong>{esc(other["name"])}</strong><span aria-hidden="true">↗</span></a>' for other in TOURS if other["id"] != tour["id"])
    breadcrumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"}, {"@type": "ListItem", "position": 2, "name": tour["name"], "item": canonical}]}
    page = f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#542b32">
  <title>{esc(tour["title"])} | Vintage Eyes</title>
  <meta name="description" content="{esc(description)}">
  <link rel="canonical" href="{canonical}">
  <meta property="og:title" content="{esc(tour["title"])} | Vintage Eyes">
  <meta property="og:description" content="{esc(description)}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{SITE}/assets/images/{tour["image"]}.jpg">
  <link rel="icon" href="../../assets/favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="../../assets/css/style.css">
  <script src="../../assets/js/site.js" defer></script>
  <script type="application/ld+json">{json.dumps(breadcrumbs, ensure_ascii=False)}</script>
</head>
<body class="tour-page">
<a class="skip-link" href="#main">Skip to content</a>
{HEADER}
<main id="main">
  <div class="breadcrumbs"><a href="../../">Home</a><span aria-hidden="true">/</span><a href="../../#journeys">Our journeys</a><span aria-hidden="true">/</span><span>{name}</span></div>
  <section class="tour-hero section" aria-labelledby="tour-title"><div><p class="eyebrow">{esc(tour["duration"].upper())} · PRIVATE JOURNEY</p><h1 id="tour-title">{name}</h1><p class="tour-tagline">{esc(tour["tagline"])}</p><p class="tour-intro">{esc(tour["intro"])}</p><div class="tour-hero-actions"><a class="button" href="#plan">Plan this journey <span aria-hidden="true">↗</span></a><a class="text-link" href="#itinerary">See the itinerary <span aria-hidden="true">↓</span></a></div><p class="tour-location">{esc(tour["destination"])}</p></div><figure><img src="../../assets/images/{tour["image"]}.jpg" alt="{esc(tour["imageAlt"])}" width="1280" height="853" fetchpriority="high"><figcaption>A LITTLE TIME AWAY. A DIFFERENT WAY TO SEE.</figcaption></figure></section>
  <nav class="tour-section-nav" aria-label="On this tour page"><a href="#expect">What to expect</a><a href="#itinerary">Itinerary</a><a href="#included">Inclusions & transfers</a><a href="#stays">{'Your accommodation' if is_day_tour else 'Hotels & stays'}</a><a href="#why-us">Why Vintage Eyes</a><a href="#questions">FAQs</a></nav>
  <div class="tour-layout section">
    <div class="tour-content">
      <section id="expect" class="tour-section"><p class="eyebrow">01 / WHAT TO EXPECT</p><h2>A trip that feels <em>like yours.</em></h2><p>{esc(tour["expect"])}</p></section>
      <section id="itinerary" class="tour-section"><p class="eyebrow">02 / YOUR ITINERARY</p><h2>{'A day' if is_day_tour else f'{day_count} days'}, <em>step by step.</em></h2><p class="section-note">The full route is below. Arrival times, opening hours and your chosen pace shape the final schedule. Departure-day visits depend on the time available; optional activities are confirmed separately.</p>{''.join(itinerary)}</section>
      <section id="included" class="tour-section"><p class="eyebrow">03 / THE PRACTICAL DETAILS</p><h2>The details, <em>made clear.</em></h2><div class="included-grid"><div><h3>What’s included</h3><ul>{list_items(included)}</ul></div><div><h3>What’s extra</h3><ul>{list_items(excluded)}</ul></div></div>{allowance_note}<div class="transfer-details"><h3>Arrival & transfers</h3><dl><div><dt>Pickup</dt><dd>{esc(tour["pickup"])}</dd></div><div><dt>Drop-off</dt><dd>{esc(tour["dropoff"])}</dd></div></dl><p>{esc(tour["transferCopy"])}</p></div></section>
      <section id="stays" class="tour-section"><p class="eyebrow">04 / {'YOUR ACCOMMODATION' if is_day_tour else 'HOTELS & STAYS'}</p><h2>{'Stay where' if is_day_tour else 'Somewhere to'} <em>{'you like.' if is_day_tour else 'settle in.'}</em></h2><p>{esc(tour["stayCopy"])}</p>{stay_options}</section>
      <section id="why-us" class="tour-section"><p class="eyebrow">05 / WHY VINTAGE EYES</p><h2>Good journeys begin <em>with a conversation.</em></h2><p>You know the kind of holiday you want. We’re here to help put the pieces together. Ask the questions that matter to you, tell us what you’d change, and take a little time to feel comfortable with the plan.</p><div class="principles"><div><span>01</span><h3>Room for your preferences</h3><p>Talk to us about your pace, your group and your priorities.</p></div><div><span>02</span><h3>A plan you can review</h3><p>Confirm the itinerary, inclusions and final quote before booking.</p></div></div></section>
      <section id="questions" class="tour-section"><p class="eyebrow">06 / GOOD TO KNOW</p><h2>Before you <em>set off.</em></h2><div class="faq-list">{faqs}</div></section>
    </div>
    <aside class="tour-sidebar" aria-label="Tour summary"><p class="eyebrow">YOUR JOURNEY AT A GLANCE</p><h2>{name}</h2><dl><div><dt>Duration</dt><dd>{esc(tour["duration"])}</dd></div><div><dt>Places</dt><dd>{esc(tour["destination"])}</dd></div><div><dt>Stay</dt><dd>{esc(tour["stays"])}</dd></div><div><dt>Travel</dt><dd>Private car & driver</dd></div></dl><div class="sidebar-price"><span>STARTING FROM</span><strong>{esc(tour["price"])}</strong><small>{esc(tour["priceUnit"])}</small></div><p class="section-note">Indicative starting price. Dates, hotel and vehicle choice determine your confirmed quote.</p><a class="button whatsapp-button" href="{esc(direct_chat)}" target="_blank" rel="noopener noreferrer">{ICON}<span>Ask on WhatsApp</span><span aria-hidden="true">↗</span></a><a class="sidebar-call" href="tel:+916363336467">Prefer a call? +91 63633 36467</a></aside>
  </div>
  <section class="other-journeys section" aria-labelledby="other-title"><p class="eyebrow">ANOTHER WAY TO GO</p><h2 id="other-title">Keep <em>exploring.</em></h2><div>{others}</div></section>
  {plan}
</main>
{FOOTER}
{CHAT}
</body>
</html>
'''
    output = ROOT / "tours" / tour["slug"] / "index.html"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(page, encoding="utf-8")
    print(f'Built tours/{tour["slug"]}/')

urls = [SITE + "/"] + [f'{SITE}/tours/{tour["slug"]}/' for tour in TOURS]
sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(f"  <url><loc>{url}</loc></url>" for url in urls) + '\n</urlset>\n'
(ROOT / "sitemap.xml").write_text(sitemap, encoding="utf-8")
(ROOT / "robots.txt").write_text(f'User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n', encoding="utf-8")

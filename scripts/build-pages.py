"""Render static tour and destination pages. Run from any directory with Python 3."""
import html
import json
import re
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://vintageeyestours.in"
TOURS = json.loads((ROOT / "data/tours.json").read_text(encoding="utf-8"))
DESTINATIONS = json.loads((ROOT / "data/destinations.json").read_text(encoding="utf-8"))
HOME = (ROOT / "index.html").read_text(encoding="utf-8")


def esc(value):
    return html.escape(str(value), quote=True)


def extract(pattern):
    match = re.search(pattern, HOME, re.S)
    if not match:
        raise ValueError(f"Shared homepage section missing: {pattern}")
    return match.group(0)


def relative(markup):
    return (markup.replace('="assets/', '="../../assets/')
            .replace('href="./"', 'href="../../"')
            .replace('href="destinations/', 'href="../../destinations/')
            .replace('href="tours/', 'href="../../tours/'))


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


def destination_links(tour):
    known = {destination["slug"]: destination["name"] for destination in DESTINATIONS}
    links = [f'<a href="../../destinations/{slug}/">{esc(known[slug])}</a>'
             for slug in tour.get("destinationIds", []) if slug in known]
    if tour["id"] == "heritage":
        return " & ".join(links + ["Anegundi"])
    return " · ".join(links) or esc(tour["destination"])


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
  <section class="tour-hero section" aria-labelledby="tour-title"><div><p class="eyebrow">{esc(tour["duration"].upper())} · PRIVATE JOURNEY</p><h1 id="tour-title">{name}</h1><p class="tour-tagline">{esc(tour["tagline"])}</p><p class="tour-intro">{esc(tour["intro"])}</p><div class="tour-hero-actions"><a class="button" href="#plan">Plan this journey <span aria-hidden="true">↗</span></a><a class="text-link" href="#itinerary">See the itinerary <span aria-hidden="true">↓</span></a></div><p class="tour-location">{destination_links(tour)}</p></div><figure><img src="../../assets/images/{tour["image"]}.jpg" alt="{esc(tour["imageAlt"])}" width="1280" height="853" fetchpriority="high"><figcaption>A LITTLE TIME AWAY. A DIFFERENT WAY TO SEE.</figcaption></figure></section>
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

HOME_CARDS = re.findall(r'<article class="tour-card".*?</article>', HOME, re.S)
for destination in DESTINATIONS:
    slug = destination["slug"]
    name = esc(destination["name"])
    canonical = f"{SITE}/destinations/{slug}/"
    matches = [tour for tour in TOURS if slug in tour.get("destinationIds", [])]
    cards = []
    for tour in matches:
        card = next((card for card in HOME_CARDS if f'href="tours/{tour["slug"]}/"' in card), None)
        if card is None:
            raise ValueError(f'Homepage card missing for {tour["id"]}')
        cards.append(relative(card))
    tour_section = ""
    if cards:
        circuit_note = '<p class="section-note circuit-note">This journey visits Hampi, Aihole, Pattadakal and Badami. It is a four-day heritage circuit, rather than a standalone day tour of this destination.</p>' if slug != "hampi" else '<p class="section-note">Choose a Hampi stay, a private sightseeing day, or a longer heritage circuit.</p>'
        tour_section = f'''<section id="destination-tours" class="destination-tours section" aria-labelledby="destination-tours-title"><div class="section-heading"><div><p class="eyebrow">04 / JOURNEYS THAT VISIT {name.upper()}</p><h2 id="destination-tours-title">Find your way <em>here.</em></h2></div><p>Start with a journey that includes {name}.<br>Explore the full route before choosing.</p></div>{circuit_note}<div class="tour-grid {'single-tour' if len(cards) == 1 else ''}">{''.join(cards)}</div><p class="price-note">Indicative starting prices. Dates, accommodation and vehicle choice determine your confirmed quote.</p></section>'''
    plan = PLAN
    options = '<option value="Not sure yet">Help me choose</option>' + "".join(f'<option value="{esc(tour["select"])}">{esc(tour["name"])} · {esc(tour["duration"])}</option>' for tour in matches)
    plan = re.sub(r'(<select id="journey-select"[^>]*>).*?(</select>)', lambda match: match.group(1) + options + match.group(2), plan, flags=re.S)
    plan = re.sub(r'(<form id="enquiry-form"[^>]*>)', lambda match: match.group(1) + f'<input type="hidden" name="destination" value="{name}">', plan)
    plan = plan.replace('Your next story<br>starts <em>here.</em>', f'Your {name} story<br>starts <em>here.</em>')
    chat_url = "https://wa.me/916363336467?text=" + quote(f'Hello Vintage Eyes! I’d like to plan a visit to {destination["name"]}. Please help me choose a journey.')
    plan = plan.replace('href="https://wa.me/916363336467"', f'href="{esc(chat_url)}"')
    chat = CHAT.replace('href="https://wa.me/916363336467"', f'href="{esc(chat_url)}"')
    footer = FOOTER.replace(f'href="../../destinations/{slug}/"', f'href="../../destinations/{slug}/" aria-current="page"')
    highlights = "".join(f'<article class="destination-highlight"><span class="eyebrow">{index:02}</span><h3>{esc(highlight["name"])}</h3><p>{esc(highlight["description"])}</p></article>' for index, highlight in enumerate(destination["highlights"], 1))
    related = "".join(f'<a class="destination-related-card" href="../{other["slug"]}/"><img src="../../assets/images/{other["image"]}.jpg" alt="{esc(other["imageAlt"])}" width="640" height="420" loading="lazy"><div><h3>{esc(other["name"])}</h3><span aria-hidden="true">↗</span></div><p>{esc(other["character"])}</p></a>' for other in DESTINATIONS if other["slug"] != slug)
    sources = " · ".join(f'<a href="{esc(source["url"])}" target="_blank" rel="noopener noreferrer">{esc(source["label"])}</a>' for source in destination["sources"])
    description = f'Explore {destination["name"]} with Vintage Eyes: destination highlights, visiting notes and journeys that include {destination["name"]}.'
    breadcrumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"}, {"@type": "ListItem", "position": 2, "name": destination["name"], "item": canonical}]}
    page = f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#542b32">
  <title>{name} — Destination Guide & Tours | Vintage Eyes</title>
  <meta name="description" content="{esc(description)}">
  <link rel="canonical" href="{canonical}">
  <meta property="og:title" content="{name} — Discover the destination | Vintage Eyes">
  <meta property="og:description" content="{esc(description)}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{SITE}/assets/images/{destination["image"]}.jpg">
  <link rel="icon" href="../../assets/favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="../../assets/css/style.css">
  <script src="../../assets/js/site.js" defer></script>
  <script type="application/ld+json">{json.dumps(breadcrumbs, ensure_ascii=False)}</script>
</head>
<body class="destination-page">
<a class="skip-link" href="#main">Skip to content</a>
{HEADER}
<main id="main">
  <div class="breadcrumbs"><a href="../../">Home</a><span aria-hidden="true">/</span><a href="../../#destinations">Destinations</a><span aria-hidden="true">/</span><span>{name}</span></div>
  <section class="tour-hero destination-hero section" aria-labelledby="destination-title"><div><p class="eyebrow">EXPLORE / {esc(destination["region"].upper())}</p><h1 id="destination-title">{name}</h1><p class="tour-tagline">{esc(destination["tagline"])}</p><p class="tour-intro">{esc(destination["intro"])}</p><div class="tour-hero-actions"><a class="button" href="#highlights">Discover {name} <span aria-hidden="true">↓</span></a><a class="text-link" href="#destination-tours">Explore journeys <span aria-hidden="true">↗</span></a></div><p class="tour-location">{esc(destination["character"])}</p></div><figure><img src="../../assets/images/{destination["image"]}.jpg" alt="{esc(destination["imageAlt"])}" width="1280" height="853" fetchpriority="high"><figcaption>{esc(destination["caption"].upper())}</figcaption></figure></section>
  <nav class="tour-section-nav" aria-label="On this destination page"><a href="#overview">The destination</a><a href="#highlights">Places to explore</a><a href="#visit">Planning your visit</a><a href="#destination-tours">Journeys</a><a href="#plan">Talk to us</a></nav>
  <section id="overview" class="destination-overview section"><div><p class="eyebrow">01 / A SENSE OF PLACE</p><h2>A little closer<br>to <em>{name}.</em></h2></div><div><p>{esc(destination["overview"])}</p><div class="destination-facts"><div><span>THE SETTING</span><p>{esc(destination["region"])}</p></div><div><span>COME FOR</span><p>{esc(destination["character"])}</p></div></div></div></section>
  <section id="highlights" class="destination-highlights section"><p class="eyebrow">02 / PLACES TO EXPLORE</p><h2>Look a little <em>closer.</em></h2><div class="destination-highlight-grid">{highlights}</div></section>
  <section id="visit" class="destination-visit section"><p class="eyebrow">03 / PLANNING YOUR VISIT</p><h2>Make room for <em>the journey.</em></h2><div class="destination-visit-grid"><article><h3>Arriving & getting around</h3><p>{esc(destination["arrival"])}</p></article><article><h3>Find your pace</h3><p>{esc(destination["pace"])}</p></article><article><h3>Go a little further</h3><p>{esc(destination["pairing"])}</p></article></div><p class="section-note">Opening hours, access and entry charges can change. Confirm current arrangements when planning your visit.</p><p class="destination-sources">Destination references: {sources}</p></section>
  {tour_section}
  <section class="destination-related section" aria-labelledby="related-title"><p class="eyebrow">KEEP FOLLOWING YOUR CURIOSITY</p><h2 id="related-title">Another place. <em>Another perspective.</em></h2><div>{related}</div></section>
  {plan}
</main>
{footer}
{chat}
</body>
</html>
'''
    output = ROOT / "destinations" / slug / "index.html"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(page, encoding="utf-8")
    print(f'Built destinations/{slug}/ with {len(matches)} matching journeys')

urls = [SITE + "/"] + [f'{SITE}/tours/{tour["slug"]}/' for tour in TOURS] + [f'{SITE}/destinations/{destination["slug"]}/' for destination in DESTINATIONS]
sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(f"  <url><loc>{url}</loc></url>" for url in urls) + '\n</urlset>\n'
(ROOT / "sitemap.xml").write_text(sitemap, encoding="utf-8")
(ROOT / "robots.txt").write_text(f'User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n', encoding="utf-8")

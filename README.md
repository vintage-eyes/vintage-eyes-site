# Vintage Eyes

A static, responsive travel website for Vintage Eyes, built with HTML, CSS and JavaScript. No build step or backend is required.

## Publish with GitHub Pages

1. Open https://github.com/vintage-eyes/vintage-eyes-site/settings/pages using an account with admin or maintainer access.
2. Under **Build and deployment**, choose **Deploy from a branch**.
3. Choose **main** and **/(root)**, then **Save**.
4. Wait for the **pages build and deployment** workflow in the Actions tab to complete.
5. Open https://vintage-eyes.github.io/vintage-eyes-site/.

The repository must have a commit on `main` before it appears in the branch selector. GitHub Pages works with public repositories on GitHub Free; private repositories require a compatible paid plan.

The live custom domain is **https://vintageeyestours.in/**. Preserve the `CNAME` file and the existing GitHub Pages settings. GoDaddy manages domain DNS. Future pushes to `main` automatically update the live site, so review changes in a local preview before publishing.

Official instructions: https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site

## Local preview

From this folder, run `python3 -m http.server 8000` and open http://localhost:8000. All website asset links are relative so they work at the GitHub Pages repository path and at a future custom domain.

## Editing

- `index.html`: visible page content, package cards, FAQs and enquiry form.
- `assets/css/style.css`: independent design and responsive styles.
- `data/tours.json`: dedicated tour-page content and complete day-by-day itineraries.
- `data/destinations.json`: Hampi, Aihole, Pattadakal and Badami destination-guide content and reference links.
- `scripts/build-pages.py`: generates all tour and destination pages from their data and shared homepage sections.
- `tours/*/index.html`: generated tour pages, checked into Git so GitHub Pages needs no custom build workflow.
- `destinations/*/index.html`: generated destination guides, including relevant tours, visiting notes and a contextual enquiry form.
- `assets/js/site.js`: filters, mobile menu and WhatsApp enquiry drafts.
- `assets/images/`: locally stored destination photography.

Call and WhatsApp links use +91 6363336467, confirmed by the owner. Every tour has its own enquiry form with that tour preselected. The form opens a WhatsApp draft containing the name, selected journey, date, traveller count, notes and tour-page link. Visitors must review and send the message in WhatsApp. It does not automatically send messages, save enquiries in a database, take payments or make reservations. A direct call and WhatsApp link are available without JavaScript. Fonts are fetched from Google Fonts with local system fallbacks.

## Regenerate tour pages

After changing either content JSON file, the shared header/footer/enquiry section in `index.html`, or the page template, run:

```sh
python3 scripts/build-pages.py
```

On Windows with the Python launcher:

```powershell
py -3 scripts/build-pages.py
py -3 -m http.server 8000 --bind 127.0.0.1
```

Then preview http://127.0.0.1:8000/. The generator uses only Python's standard library. There are no Node or npm dependencies. Include the generated tour HTML, `sitemap.xml` and `robots.txt` with any relevant source changes when publishing. Running the generator alone does not publish anything.

## Destination guides and tour matching

The homepage destination strip and footer link to `/destinations/hampi/`, `/destinations/aihole/`, `/destinations/pattadakal/` and `/destinations/badami/`. Each guide has an introduction, destination highlights, planning notes, matching tour cards and links to the other guides. Destination forms offer the relevant tours and include the destination name in the WhatsApp draft.

Tour matching uses each tour's explicit `destinationIds` array in `data/tours.json`; it does not guess from keywords. All four current tours visit Hampi. Only Regal visits Aihole, Pattadakal and Badami. The latter pages clearly describe Regal as the full four-day, four-destination circuit. To add a matching tour later, create its homepage card and tour-data record, add the relevant destination slugs, then regenerate the pages. Keep the data, homepage card and tour route consistent.

Destination facts were checked against Karnataka Tourism and UNESCO on 8 October 2026. Original visitor-focused prose is used; operating times and ticket prices are not hardcoded in the guides.

- https://karnatakatourism.org/en/destinations/hampi
- https://karnatakatourism.org/en/destinations/aihole
- https://karnatakatourism.org/en/destinations/pattadakal
- https://whc.unesco.org/en/list/239/
- https://karnatakatourism.org/en/destinations/badami

## Enquiry safeguards and limitations

The form validates required fields, name/notes length, future arrival dates and traveller counts. A hidden honeypot blocks basic automated fills, and a 15-second cooldown reduces repeated draft creation. Only the last-draft timestamp is stored locally; personal enquiry data is not stored by the website. A visible draft link remains available if the browser blocks the new tab. Storage being disabled does not break enquiries.

These client-side checks can be bypassed. They do not prevent someone from messaging the publicly displayed WhatsApp number directly. There is no form submission endpoint accepting automatic incoming messages, so no CAPTCHA is configured. A future automatic callback/email form would require a backend or form service with server-verified CAPTCHA and rate limiting. Never add a frontend CAPTCHA alone and call it effective spam protection, and never publish secret keys.

WhatsApp icon: Bootstrap Icons, MIT license. The icon and license are in `assets/icons/`.

## Daily maintenance

1. Open the local repository in Codex and check for uncommitted changes.
2. Sync `main` without overwriting local work. Resolve conflicting changes deliberately; do not force-push or reset away someone's edits.
3. Make the requested change. Regenerate tour pages if their data or shared sections changed.
4. Review the homepage and affected tour pages at desktop and mobile sizes; check navigation, photos and enquiry drafts without sending test messages to the business.
5. Publish only when the operator asks to publish. Commit the reviewed changes and push to `main`; GitHub Pages then updates the public website.
6. Confirm deployment completion and open the changed public URLs. Keep the commit ID so a future rollback can use a normal revert commit.

GitHub login should use the official browser sign-in or an available secure account connection. Use each operator's own authorised account. Never ask for passwords, access tokens or private keys in chat; never embed credentials in the remote URL. Public clone access is not proof of write access.

## Content reference and price review

The following source pages were reviewed on 8 October 2026 for package context only. The website design and prose are original.

- Overview: https://hampitourism.co.in/hampi-tour-packages
- Swift: https://hampitourism.co.in/swift-hampi-tour-package
- Heritage: https://hampitourism.co.in/heritage-hampi-tour-package
- Regal: https://hampitourism.co.in/regal-hampi-aihole-pattadakal-badami-tour-package
- Sightseeing: https://hampitourism.co.in/hampi-sightseeing-tour

The overview lists starting prices of ₹8,999, ₹11,999 and ₹15,999 per couple, and ₹2,700 per private car for up to four guests. The sightseeing detail page starts at ₹2,799 and has vehicle-specific rates. This initial version uses the overview prices requested as context, identifies them as indicative and asks visitors to confirm a quote. Review prices and business terms before active marketing. No source testimonials, ratings, cancellation guarantees or unrelated service claims were imported.

Dedicated pages retain the reference's itinerary stop order and day groupings, with original prose. Landmark names are normalised where needed (for example, Lakshmi Narasimha Temple and Elephant Stables). Heritage includes Hemakuta Hill, which the source places inside the Sasivekalu paragraph rather than under a separate heading. Its second-day checkout sentence contradicts the two-night itinerary, so checkout is on day three here. The Regal source gives conflicting transfer wording; the page retains the itinerary's Hospet/Badami departure options and requires confirmation of the drop-off and intercity mileage in the quote. Optional coracle rides are listed in the itinerary but not promised as included.

## Photography

Images are from Wikimedia Commons. Hampi, the Stone Chariot, Badami and Aihole use CC BY-SA 4.0: https://creativecommons.org/licenses/by-sa/4.0/. Pattadakal uses CC BY-SA 3.0: https://creativecommons.org/licenses/by-sa/3.0/. Attribution is also available in the website footer.

- `hampi.jpg`: **Hampi - Hemakuta Hill, Virupaksha Temple**, Ingo Mehling. https://commons.wikimedia.org/wiki/File:Hampi_-_Hemakuta_Hill,_Virupaksha_Temple.jpg
- `chariot.jpg`: **Stone Chariot, Hampi 2**, Ajayreddykalavalli. https://commons.wikimedia.org/wiki/File:Stone_Chariot,_Hampi_2.jpg
- `badami.jpg`: **Agastya Lake with Badami Temples**, Mbigul. https://commons.wikimedia.org/wiki/File:Agastya_Lake_with_Badami_Temples.jpg
- `aihole.jpg`: **Durga Temple in Aihole**, IM3847. https://commons.wikimedia.org/wiki/File:Durga_Temple_in_Aihole.jpg
- `pattadakal.jpg`: **Virupaksha Temple, Pattadakal, Karnataka**, Mukul Banerjee. https://commons.wikimedia.org/wiki/File:Virupaksha_Temple,_Pattadakal,_Karnataka.jpg

Images are resized and cropped for display. Each image adaptation retains its respective CC BY-SA license. These image licenses do not license the website’s original code or branding.

# Vintage Eyes

A static, responsive travel website for Vintage Eyes, built with HTML, CSS and JavaScript. No build step or backend is required.

## Publish with GitHub Pages

1. Open https://github.com/vintage-eyes/vintage-eyes-site/settings/pages using an account with admin or maintainer access.
2. Under **Build and deployment**, choose **Deploy from a branch**.
3. Choose **main** and **/(root)**, then **Save**.
4. Wait for the **pages build and deployment** workflow in the Actions tab to complete.
5. Open https://vintage-eyes.github.io/vintage-eyes-site/.

The repository must have a commit on `main` before it appears in the branch selector. GitHub Pages works with public repositories on GitHub Free; private repositories require a compatible paid plan.

Custom domain mapping is deliberately on hold. Leave **Custom domain** blank. There is no CNAME file or domain DNS change in this version. Future pushes to main automatically update the site after Pages is enabled.

Official instructions: https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site

## Local preview

From this folder, run `python3 -m http.server 8000` and open http://localhost:8000. All website asset links are relative so they work at the GitHub Pages repository path and at a future custom domain.

## Editing

- `index.html`: visible page content, package cards, FAQs and enquiry form.
- `assets/css/style.css`: independent design and responsive styles.
- `assets/js/site.js`: package itinerary summaries, filters, mobile menu and WhatsApp enquiry drafts.
- `assets/images/`: locally stored destination photography.

Call and WhatsApp links use +91 6363336467, confirmed by the owner. The form opens a WhatsApp draft; visitors review and send it themselves. It does not store submissions or make a reservation. A direct call and WhatsApp link are available without JavaScript. Fonts are fetched from Google Fonts with local system fallbacks.

## Content reference and price review

The following source pages were reviewed on 8 October 2026 for package context only. The website design and prose are original.

- Overview: https://hampitourism.co.in/hampi-tour-packages
- Swift: https://hampitourism.co.in/swift-hampi-tour-package
- Heritage: https://hampitourism.co.in/heritage-hampi-tour-package
- Regal: https://hampitourism.co.in/regal-hampi-aihole-pattadakal-badami-tour-package
- Sightseeing: https://hampitourism.co.in/hampi-sightseeing-tour

The overview lists starting prices of ₹8,999, ₹11,999 and ₹15,999 per couple, and ₹2,700 per private car for up to four guests. The sightseeing detail page starts at ₹2,799 and has vehicle-specific rates. This initial version uses the overview prices requested as context, identifies them as indicative and asks visitors to confirm a quote. Review prices and business terms before active marketing. No source testimonials, ratings, cancellation guarantees or unrelated service claims were imported.

## Photography

All three images are from Wikimedia Commons and licensed under CC BY-SA 4.0: https://creativecommons.org/licenses/by-sa/4.0/. Attribution is also available in the website footer.

- `hampi.jpg`: **Hampi - Hemakuta Hill, Virupaksha Temple**, Ingo Mehling. https://commons.wikimedia.org/wiki/File:Hampi_-_Hemakuta_Hill,_Virupaksha_Temple.jpg
- `chariot.jpg`: **Stone Chariot, Hampi 2**, Ajayreddykalavalli. https://commons.wikimedia.org/wiki/File:Stone_Chariot,_Hampi_2.jpg
- `badami.jpg`: **Agastya Lake with Badami Temples**, Mbigul. https://commons.wikimedia.org/wiki/File:Agastya_Lake_with_Badami_Temples.jpg

Images are resized and cropped for display. Image adaptations retain CC BY-SA 4.0. That image license does not license the website’s original code or branding.

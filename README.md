# The Auto Door Experts — website revamp (preview)

Static, fully responsive preview of the new site. Approve the look here, then it gets rebuilt as Elementor templates.

## Deploy to staging

The repo root is the website: `index.html` and `assets/` sit at the top level and are committed, so no build step runs on the host. Import this repo into any static host and leave the settings empty:

| Setting | Value |
|---|---|
| Framework | None / Other |
| Build command | (empty) |
| Output / publish directory | (empty, or `.`) |

Every page has `<meta name="robots" content="noindex">` so the staging copy stays out of Google. Remove that line from `_source/src/partials/shell.html` and rebuild only if this static site ever becomes the live one.

## View it

Double-click `index.html`, or serve it from the repo root:

```bash
python3 -m http.server 5200
```

Then open http://localhost:5200

## Edit it

- Page content: `_source/src/pages/*.html`
- Shared header / footer / quote form: `_source/src/partials/`
- Styles: `assets/css/site.css` (colour + font tokens at the top = Elementor Global Colors / Fonts)
- Rebuild after any change, and commit the result: `python3 _source/build.py`

## Pages

Home · Emergency Breakdown · Sales & Installation · Periodic Maintenance · Spare Parts · Industries · About · Contact · Blog (+ all 28 articles).
Privacy and Terms link to the live site.

## Blog

- `_source/tools/import_blog.py` pulls every live post (title, date, summary, featured image, cleaned body) into `_source/src/blog/`. Re-run it to refresh: `python3 -I _source/tools/import_blog.py`
- `_source/build.py` generates `blog.html` (featured post, topic filters, grid) and one `blog-<slug>.html` per article (reading progress, sticky "On this page", call card, related posts).
- Topic labels can be corrected in `TOPIC_FIX` inside `_source/build.py`.

## Elementor package

`_source/elementor/auto-door-elementor-package.zip` holds the import files; start with `INSTALL.md` inside it.

- Rebuild: `python3 _source/elementor/generate.py [--media-month 2026/11]`
- Check against plugin source: `python3 _source/elementor/validate.py <folder containing elementor, royal-elementor-addons, contact-form-7>`
- Changing `_source/src/` or `assets/` does not change the templates. Their content lives in `_source/elementor/generate.py`.

## Elementor mapping (for the build step)

| Preview piece | Elementor (free) |
|---|---|
| Sections / grids | Flexbox Containers |
| Industry tabs | Nested Tabs widget |
| FAQs | Accordion widget |
| Quote form | Contact Form 7 (radio for service; route email per option with CF7 pipes, e.g. `Emergency repair\|service@…`) |
| Header / footer | Royal Elementor Addons header & footer builder |
| Blog listing / single post | Royal Elementor Addons Theme Builder (Archive + Single templates; the live site already uses its post-content widget) |
| Sliding-door hero reveal, mobile call bar | Small custom CSS/JS snippet in Site Settings |

## Content notes

- The live Projects, Our Products and About timeline pages are lorem-ipsum demo content. They're left out until real projects exist.
- All claims come from the live site and blog (AS 5007, 24/7, Prestons case study: 80% fewer callouts). Nothing invented.

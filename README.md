# Mesta Media website

This Jekyll site preserves the original visual design and copy while making all three views available as crawlable HTML pages.

## Edit and build

Page content lives in `index.html`, `what-i-offer/index.html`, and `how-i-think/index.html`. Shared layout, navigation, footer, and SEO metadata live in `_layouts` and `_includes`. Styles and scripts live in `assets`.

Run `bundle install`, `JEKYLL_ENV=production bundle exec jekyll build`, and `python3 scripts/validate_site.py _site`. Use `bundle exec jekyll serve` for local preview. GitHub Pages can build this source with its supported `jekyll-seo-tag` plugin. Keep the existing Pages branch and custom-domain settings.

Jekyll SEO Tag generates page titles, descriptions, canonical URLs, Open Graph metadata, and Twitter cards. `_includes/seo.html` retains that metadata and replaces the plugin’s generic JSON-LD script with one linked graph from `_data/schema`. The build validator checks that exactly one JSON-LD script exists per page. If upgrading the plugin beyond 2.8, verify its script delimiter and rerun validation.

The schema graph connects Mesta Media, founder Brandi Mesta, the website, and each page. The services page also describes its four visible services. Do not add unsupported reviews, credentials, addresses, or outcome claims to the schema.

## Discovery files

`robots.txt` allows public crawlers and points to `sitemap.xml`. Each page has a raw Markdown mirror at `index.html.md` within its directory, linked from the HTML head. `llms.txt` links to those mirrors. When editing page copy, update its Markdown mirror and relevant schema descriptions too. When adding or removing pages, update the sitemap and llms.txt links.

Legacy hash URLs redirect in `assets/site.js`; navigation now uses real page URLs. The three pages contain their content before JavaScript runs. JavaScript handles the existing mobile menu, service tabs, copy-email button, and legacy links.

The social image is the existing Mesta Media logo served as a public PNG, with its actual dimensions and alt text. No new visual assets or visible copy were introduced.

## Scope and limits

These changes improve technical accessibility and metadata. They do not guarantee indexing, rankings, or AI citations. `llms.txt` follows a proposed convention, not a universal crawler requirement. It does not replace robots.txt or grant crawler permissions. Google does not require special AI files or schema for its generative Search features.

After publication, submit `https://mestamedia.com/sitemap.xml` in the verified Google Search Console property and inspect the three page URLs. Validate structured data with Schema.org’s validator and use Google’s Rich Results Test for supported search features. Organization, Person, WebPage, and Service markup need not produce a Google rich result to be useful.

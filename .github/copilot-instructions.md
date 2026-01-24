# Copilot instructions for MyKutch

## Project overview
- Static site: all deployable assets live in site/ (HTML, CSS, JS, images, lang JSON). Cloudflare Wrangler serves site/ as assets (wrangler.json).
- No build step (package.json build is a no-op). Pages are edited directly in site/.

## Key architecture & data flow
- Client i18n: data-i18n attributes in HTML are replaced at runtime by site/js/i18n.js loading site/lang/*.json.
  - Path logic: pages under site/destinations/ or site/crafts/ load translations from ../lang/; root pages load from lang/.
  - Use data-i18n on meta tags, inputs, imgs (alt), and text nodes; i18n.js sets innerHTML for rich text.
- Core UI behavior is in site/js/script.js (mobile nav toggle, reveal animations, preloader, dark mode, hero parallax).

## Project-specific conventions
- Content-first HTML: pages are mostly static, with consistent section classes like .hero, .guide-section, .grid-2, .attraction-card.
- Images are referenced under site/assets/images/... and often have onerror handlers for graceful fallbacks.
- i18n keys are nested (e.g., geography_page.stats.area.num) and stored in site/lang/en.json with parallel keys in other languages.

## Automation & maintenance scripts
- Several Python utilities in repo root (e.g., apply_template.py, generate_sitemap.py, generate_pages.py) perform batch edits or generation.
  - Note: some scripts contain absolute Windows paths and may need updating before reuse.
  - generate_sitemap.py writes site/sitemap.xml directly.

## Integration points
- Cloudflare Wrangler config: wrangler.json uses site/ as the asset directory.
- External embeds (e.g., Google Maps iframes) are hardcoded in HTML pages.

## Examples
- i18n usage: see data-i18n attributes in site/geography.html and keys in site/lang/en.json.
- Core JS behavior: site/js/script.js and site/js/i18n.js.

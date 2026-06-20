# Glowz — Project Brief for Claude

Use this document as context when working on the **Glowz** codebase. Read it fully before making changes.

---

## What this project is

**Glowz** is a commercial HTML5 website template for a **cleaning services** business (residential, commercial, office, deep cleaning, etc.). It was authored by **wpOceans** (ThemeForest-style downloadable theme).

- **Type:** Static multipage HTML site (not React, not Next.js, not WordPress)
- **Version:** 1.0.0
- **Primary use case:** Marketing site with booking/contact flows, optional blog and e-commerce demo pages
- **Live preview:** Open any `.html` file in a browser, or serve the folder with a local static server

There is **no** `package.json`, build pipeline, or framework. Styles are authored in SCSS and compiled to CSS manually (or via your own Sass setup).

---

## Your task (fill this in)

> **Goal:** _Describe what you want done. Examples below._
>
> - Rebrand for a client named "X-Sheild" (logo, colors, copy)
> - Convert to a single-page site / remove unused pages
> - Wire contact form to a real email or API
> - Fix mobile nav / accessibility issues
> - Extract reusable header/footer into includes (PHP, Eleventy, etc.)
> - Deploy to Netlify / Vercel / shared hosting

**Constraints:**

- _Budget, timeline, hosting environment, brand guidelines, pages to keep/remove, etc._

**Out of scope:**

- _Anything you do NOT want changed._

---

## Tech stack

| Layer | Technology |
|-------|------------|
| Markup | HTML5, Bootstrap 5 grid/components |
| Styles | SCSS → compiled `assets/sass/style.css` |
| Scripts | jQuery, Bootstrap bundle, GSAP (+ ScrollTrigger, ScrollSmoother, SplitText) |
| Carousels | Swiper, Slick, Owl Carousel |
| Lightbox | Fancybox, Magnific Popup |
| Counters | Odometer |
| Forms | jQuery Validate + AJAX → `mail-contact.php` |
| Fonts | Google Fonts: **Poppins** (body & headings) |
| Icons | Themify Icons, Flaticon, Font Awesome |

### Important: obfuscated JavaScript

`assets/js/script.js` and `assets/js/gsap-script.js` are **minified/obfuscated**. They still work, but are hard to read or patch safely.

- Prefer editing **HTML** and **SCSS** for layout and styling changes.
- Avoid rewriting behavior in `script.js` unless necessary; test thoroughly after any JS edits.
- GSAP smooth scroll and text animations depend on `#smooth-wrapper` / `#smooth-content` and classes like `.poort-text`, `.rolling-text`, `.btn-move`.

---

## Project structure

```
glowz/
├── index.html              # Home style 1 (main landing)
├── index-2.html            # Home style 2
├── index-3.html            # Home style 3
├── about.html
├── appoinment.html         # Appointment / booking page (note spelling)
├── service.html
├── service-single.html
├── project.html            # Portfolio listing
├── project-single.html
├── team.html
├── team-single.html
├── faq.html
├── contact.html
├── blog.html               # + left-sidebar, fullwidth variants
├── blog-single.html        # + left-sidebar, fullwidth variants
├── shop.html               # Demo e-commerce (no real backend)
├── shop-single.html
├── cart.html
├── checkout.html
├── 404.html
├── mail-contact.php        # Contact form handler (PHP mail)
├── htaccess                # Rename to .htaccess on Apache deploy
└── assets/
    ├── css/                # Vendor CSS (Bootstrap, plugins)
    ├── sass/               # Source styles (edit these)
    │   ├── style.scss      # Master import file
    │   ├── helpers/        # variables, mixins, functions
    │   ├── base/
    │   ├── components/
    │   ├── layout/
    │   └── page/           # Per-page styles
    ├── sass/style.css      # Compiled CSS (linked in HTML)
    ├── js/
    │   ├── script.js       # Main interactions (obfuscated)
    │   ├── gsap-script.js  # GSAP animations (obfuscated)
    │   ├── jquery.min.js
    │   ├── bootstrap.bundle.min.js
    │   └── jquery-plugin-collection.js
    ├── images/
    └── fonts/
```

---

## Pages and navigation

**Live site (4 pages):** `index.html` (Home), `about.html` (About Us), `service.html` (Services), `contact.html` (Contact Us).

All four pages share the same header/footer, WhatsApp + call floating buttons, and simplified nav:

| Nav label | File |
|-----------|------|
| Home | `index.html` |
| About Us | `about.html` |
| Services | `service.html` |
| Contact Us | `contact.html` |

Other HTML files in the repo (shop, blog, alternate home layouts, etc.) are template leftovers and are not linked from the live nav.

**Page flow (no duplicate sections):**

| Page | Sections |
|------|----------|
| **Home** | Hero → About teaser → Services carousel → How It Works → Stats → Emergency CTA + Why Choose → FAQ → Testimonials → CTA band |
| **About** | Breadcrumb → About story → Vision/Mission → Stats → CTA band |
| **Services** | Breadcrumb → Services grid → CTA band |
| **Contact** | Breadcrumb → Office info → Map → Contact form (only full form on site) |

Shared CTA band snippet: `_snippets/xshield-cta-band.html` (styled in `_xshield-cta-band.scss`).

---

## Design system (SCSS variables)

Edit [`assets/sass/helpers/_variables.scss`](assets/sass/helpers/_variables.scss), then recompile:

```bash
npx sass assets/sass/style.scss assets/sass/style.css
```

### Brand colors

| Token | Value | Usage |
|-------|-------|-------|
| `$theme-primary-color` | `#1A5276` | Primary blue |
| `$theme-primary-color-s2` | `#4A9B2F` | Accent green |
| `$heading-color` | `#1d1d1f` | Primary text |
| `$text-color` | `#6e6e73` | Secondary text |
| `$section-bg-color` | `#f5f5f7` | Alternate sections |
| `$base-font` / `$heading-font` | Poppins | All typography |

### Apple-inspired type scale

| Token | Size | Typical use |
|-------|------|-------------|
| `$apple-type-12` | 12px | Nav, eyebrows, captions |
| `$apple-type-14` | 14px | Footer links, small UI |
| `$apple-type-17` | 17px | Body, buttons, form inputs |
| `$apple-type-21` | 21px | Subheads |
| `$apple-type-24` | 24px | Card titles (mobile) |
| `$apple-type-28` | 28px | Section titles (mobile) |
| `$apple-type-40` | 40px | Section titles (tablet) |
| `$apple-type-48` | 48px | Section titles (desktop) |
| `$apple-type-56` | 56px | Hero headline (desktop) |

Line heights: `$apple-lh-body` (1.47), `$apple-lh-title` (1.15), `$apple-lh-display` (1.05).

### Spacing & radii

- Section padding: **112px / 80px / 64px** vertical (desktop / tablet / mobile) via `.section-padding`
- Tight stacked sections (`.pt-0` / `.pb-0`): still **48px** minimum gap between blocks
- Row gutters: **2rem** horizontal and vertical
- Input radius: `$apple-radius-input` (12px)
- Card radius: `$apple-radius-card` (28px)
- Pill buttons: `$apple-radius-pill` (980px)
- Spacing tokens: `$apple-space-8` through `$apple-space-128` in `_variables.scss`

### Buttons

| Class | Style |
|-------|-------|
| `.theme-btn` | Green pill primary CTA |
| `.theme-btn-s2` | Blue pill primary CTA |
| `.theme-btn-s3` | Outline secondary CTA |
| `.theme-btn-link` | Text link with chevron (Apple-style) |

Site-wide sizing overrides live in [`assets/sass/components/_apple-ui-overrides.scss`](assets/sass/components/_apple-ui-overrides.scss) (imported last in `style.scss`).

Logo: `assets/images/logo.svg`

---

## How to develop locally

### Option A — Open directly

Double-click `index.html`. Some features (AJAX forms, smooth paths) may need a server.

### Option B — Static server (recommended)

```bash
cd glowz
npx serve .
# or: python3 -m http.server 8080
```

### SCSS changes

There is no built-in watcher. After editing `.scss` files:

```bash
# If you have Sass installed globally or via npx:
npx sass assets/sass/style.scss assets/sass/style.css
```

HTML links to `assets/sass/style.css` — keep that path or update all HTML files if you move the compiled CSS.

### Contact form (PHP)

`mail-contact.php` uses PHP `mail()` with a hardcoded recipient:

```php
$to = "wpoceanmarketing@gmail.com"; // change this
```

Forms POST via jQuery Validate + AJAX to `mail-contact.php`. Requires:

- PHP-enabled hosting (Apache/Nginx + PHP)
- Or replace with a serverless function / Formspree / Resend / etc.

Fields expected: `name`, `email`, `adress` (typo in template), `service`, `note`.

---

## HTML conventions

- Each page repeats full `<head>` asset links and header/footer — **no templating**.
- Wrapper structure: `.page-wrapper` → `#smooth-wrapper` → `#smooth-content` → header, sections, footer.
- Preloader: `.preloader` (hidden by JS on load).
- Buttons: `.theme-btn`, `.theme-btn-s2`, `.theme-btn-s3`.
- Section prefixes: `wpo-*` (wpOceans naming).

When adding a new page, **copy an existing page** and swap the main content block; keep the same CSS/JS includes at the bottom.

---

## Deployment notes

1. Upload entire `glowz/` folder to web root.
2. Rename `htaccess` → `.htaccess` on Apache (bot blocking rules).
3. Configure `mail-contact.php` recipient and test form delivery.
4. Replace placeholder copy: phone, email (`contact@glowz.com`), addresses, lorem text.
5. Add/replace `assets/images/favicon.png` if missing.
6. Shop/cart/checkout can be removed or hidden if not needed.

---

## Known limitations and quirks

- **Duplicate markup** across 25+ HTML files — header/footer edits require find-replace or introducing a build step.
- **Typo:** `appoinment.html` (not "appointment") — keep filename if linking internally.
- **Placeholder content** throughout (generic cleaning copy, stock imagery paths).
- **No tests, no lint config, no CI.**
- **`.DS_Store`** may be present — do not deploy.
- Contact form field `adress` is misspelled in PHP and likely in HTML forms.
- Second contact form in `script.js` references `mail-contact.php` and another URL (`mail-contact.php` vs possible `mail-contact.php` pattern) — verify form `action`/`url` in HTML matches your backend.

---

## Suggested workflow for Claude

1. **Clarify the goal** using the "Your task" section above.
2. **Identify affected files** — usually HTML + `_variables.scss` + page SCSS partials.
3. **Make minimal, focused diffs** — match existing class names and structure.
4. **Recompile SCSS** if styles changed.
5. **Test in browser** at mobile (`≤991px`) and desktop breakpoints; check nav, sliders, and forms.
6. **Do not** add heavy frameworks unless explicitly requested.
7. **Do not** commit secrets (API keys, real client emails in repo) unless asked.

---

## Quick reference — script load order

Every page ends with:

```html
<script src="assets/js/jquery.min.js"></script>
<script src="assets/js/bootstrap.bundle.min.js"></script>
<script src="assets/js/modernizr.custom.js"></script>
<script src="assets/js/jquery-plugin-collection.js"></script>
<script src="assets/js/gsap-script.js"></script>
<script src="assets/js/script.js"></script>
```

GSAP plugins and jQuery plugins are bundled in `jquery-plugin-collection.js`.

---

## Questions to ask the user if unclear

1. Which home page variant should be the canonical homepage?
2. Should shop/blog pages be kept, removed, or hidden from nav?
3. Target hosting (static vs PHP)?
4. Brand name, colors, logo assets, and real contact details?
5. Is this staying static HTML or migrating to a framework (Next.js, Astro, etc.)?

---

*Last updated: project inventory from Glowz v1.0.0 template (wpOceans).*

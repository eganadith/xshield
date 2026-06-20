#!/usr/bin/env python3
"""Generate SEO assets and inject meta tags, canonical URLs, and JSON-LD schema."""

from __future__ import annotations

import json
import re
from datetime import date
from html import escape
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
CONFIG_PATH = ROOT / "assets/data/seo-config.json"
SERVICES_PATH = ROOT / "assets/data/services-inquiry.json"
CORE_PAGES = ("index.html", "about.html", "service.html", "contact.html")


def load_config() -> dict[str, Any]:
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def abs_url(config: dict[str, Any], path: str) -> str:
    base = config["siteUrl"].rstrip("/")
    if path == "/":
        return f"{base}/"
    return f"{base}{path if path.startswith('/') else '/' + path}"


def abs_asset(config: dict[str, Any], asset_path: str) -> str:
    return abs_url(config, asset_path if asset_path.startswith("/") else f"/{asset_path}")


def organization_schema(config: dict[str, Any]) -> dict[str, Any]:
    biz = config["business"]
    addr = biz["address"]
    return {
        "@type": "Organization",
        "@id": abs_url(config, "/#organization"),
        "name": config["siteName"],
        "legalName": biz["legalName"],
        "url": config["siteUrl"],
        "logo": abs_asset(config, config["defaultOgImage"]),
        "email": biz["email"],
        "telephone": biz["telephone"],
        "sameAs": biz["sameAs"],
        "address": {
            "@type": "PostalAddress",
            "streetAddress": addr["streetAddress"],
            "addressLocality": addr["addressLocality"],
            "addressRegion": addr["addressRegion"],
            "postalCode": addr["postalCode"],
            "addressCountry": addr["addressCountry"],
        },
    }


def local_business_schema(config: dict[str, Any]) -> dict[str, Any]:
    biz = config["business"]
    org = organization_schema(config)
    geo = biz["geo"]
    return {
        "@type": "PestControlService",
        "@id": abs_url(config, "/#localbusiness"),
        "name": config["siteName"],
        "image": abs_asset(config, config["defaultOgImage"]),
        "url": config["siteUrl"],
        "telephone": biz["telephone"],
        "email": biz["email"],
        "priceRange": biz["priceRange"],
        "address": org["address"],
        "geo": {
            "@type": "GeoCoordinates",
            "latitude": geo["latitude"],
            "longitude": geo["longitude"],
        },
        "areaServed": [{"@type": "City", "name": area} for area in biz["areaServed"]],
        "openingHours": biz["openingHours"],
        "sameAs": biz["sameAs"],
        "parentOrganization": {"@id": org["@id"]},
    }


def web_site_schema(config: dict[str, Any]) -> dict[str, Any]:
    return {
        "@type": "WebSite",
        "@id": abs_url(config, "/#website"),
        "url": config["siteUrl"],
        "name": config["siteName"],
        "publisher": {"@id": abs_url(config, "/#organization")},
        "inLanguage": "en-AE",
    }


def faq_schema(config: dict[str, Any]) -> dict[str, Any]:
    return {
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": item["question"],
                "acceptedAnswer": {"@type": "Answer", "text": item["answer"]},
            }
            for item in config["faq"]
        ],
    }


def breadcrumb_schema(config: dict[str, Any], filename: str) -> dict[str, Any] | None:
    crumbs = config.get("breadcrumbs", {}).get(filename)
    if not crumbs:
        return None
    return {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": index + 1,
                "name": item["name"],
                "item": abs_url(config, item["path"]),
            }
            for index, item in enumerate(crumbs)
        ],
    }


def service_catalog_schema(config: dict[str, Any], services: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "@type": "OfferCatalog",
        "name": "Pest Control Services in Dubai",
        "itemListElement": [
            {
                "@type": "Offer",
                "itemOffered": {
                    "@type": "Service",
                    "name": service["title"],
                    "description": service["description"],
                    "url": abs_url(config, f"/inquiry/{service['slug']}"),
                    "areaServed": {"@type": "City", "name": "Dubai"},
                    "provider": {"@id": abs_url(config, "/#localbusiness")},
                },
            }
            for service in services
        ],
    }


def inquiry_service_schema(
    config: dict[str, Any], service: dict[str, Any], page_url: str
) -> dict[str, Any]:
    return {
        "@type": "Service",
        "name": service["title"],
        "description": service["description"],
        "url": page_url,
        "image": abs_asset(config, service["image"]),
        "areaServed": {"@type": "City", "name": "Dubai"},
        "provider": {"@id": abs_url(config, "/#localbusiness")},
        "offers": {
            "@type": "Offer",
            "price": "0",
            "priceCurrency": "AED",
            "description": "Free inspection",
            "availability": "https://schema.org/InStock",
        },
    }


def inquiry_breadcrumb_schema(
    config: dict[str, Any], service: dict[str, Any], page_url: str
) -> dict[str, Any]:
    return {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": 1,
                "name": "Home",
                "item": abs_url(config, "/"),
            },
            {
                "@type": "ListItem",
                "position": 2,
                "name": "Services",
                "item": abs_url(config, "/service.html"),
            },
            {
                "@type": "ListItem",
                "position": 3,
                "name": service["title"],
                "item": page_url,
            },
        ],
    }


def build_schema_graph(config: dict[str, Any], schemas: list[str], **kwargs: Any) -> str:
    graph: list[dict[str, Any]] = []
    services = kwargs.get("services", [])

    if "organization" in schemas:
        graph.append(organization_schema(config))
    if "localBusiness" in schemas:
        graph.append(local_business_schema(config))
    if "webSite" in schemas:
        graph.append(web_site_schema(config))
    if "faqPage" in schemas:
        graph.append(faq_schema(config))
    if "breadcrumb" in schemas:
        crumb = breadcrumb_schema(config, kwargs.get("filename", ""))
        if crumb:
            graph.append(crumb)
    if "serviceCatalog" in schemas and services:
        graph.append(service_catalog_schema(config, services))
    if "inquiryService" in schemas:
        graph.append(
            inquiry_service_schema(config, kwargs["service"], kwargs["page_url"])
        )
        graph.append(
            inquiry_breadcrumb_schema(config, kwargs["service"], kwargs["page_url"])
        )

    payload = {"@context": "https://schema.org", "@graph": graph}
    return (
        '    <script type="application/ld+json">\n'
        + json.dumps(payload, ensure_ascii=False, indent=2)
        + "\n    </script>"
    )


def seo_head_block(
    config: dict[str, Any],
    *,
    title: str,
    description: str,
    canonical: str,
    og_title: str,
    og_image: str,
    keywords: str = "",
) -> str:
    site_name = escape(config["siteName"])
    title_e = escape(title)
    desc_e = escape(description)
    og_title_e = escape(og_title)
    canonical_e = escape(canonical)
    og_image_e = escape(og_image)
    locale = config["locale"]
    biz = config["business"]
    geo = biz["geo"]

    lines = [f'    <meta name="description" content="{desc_e}">']
    if keywords:
        lines.append(f'    <meta name="keywords" content="{escape(keywords)}">')
    lines.extend(
        [
            '    <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">',
            f'    <meta name="geo.region" content="{addr_region(biz)}">',
            f'    <meta name="geo.placename" content="{escape(biz["address"]["addressLocality"])}">',
            f'    <meta name="geo.position" content="{geo["latitude"]};{geo["longitude"]}">',
            f'    <meta name="ICBM" content="{geo["latitude"]}, {geo["longitude"]}">',
            f'    <link rel="canonical" href="{canonical_e}">',
            f'    <link rel="alternate" hreflang="en-ae" href="{canonical_e}">',
            f'    <link rel="alternate" hreflang="x-default" href="{canonical_e}">',
            f'    <meta property="og:title" content="{og_title_e}">',
            f'    <meta property="og:description" content="{desc_e}">',
            f'    <meta property="og:url" content="{canonical_e}">',
            f'    <meta property="og:image" content="{og_image_e}">',
            '    <meta property="og:image:width" content="1200">',
            '    <meta property="og:image:height" content="630">',
            '    <meta property="og:type" content="website">',
            f'    <meta property="og:site_name" content="{site_name}">',
            f'    <meta property="og:locale" content="{locale}">',
            '    <meta name="twitter:card" content="summary_large_image">',
            f'    <meta name="twitter:title" content="{og_title_e}">',
            f'    <meta name="twitter:description" content="{desc_e}">',
            f'    <meta name="twitter:image" content="{og_image_e}">',
            f'    <title>{title_e}</title>',
        ]
    )
    return "\n".join(lines)


def addr_region(biz: dict[str, Any]) -> str:
    locality = biz["address"].get("addressLocality", "Dubai")
    if locality.lower() == "dubai":
        return "AE-DU"
    country = biz["address"]["addressCountry"]
    return country if len(country) == 2 else "AE"


def replace_seo_head(content: str, seo_block: str) -> str:
    content = re.sub(
        r"\n?\s*<meta name=\"description\" content=\".*?\">.*?<title>.*?</title>",
        "\n" + seo_block,
        content,
        count=1,
        flags=re.DOTALL,
    )
    return content


def replace_json_ld(content: str, schema_html: str) -> str:
    content = re.sub(
        r"\n?\s*<script type=\"application/ld\+json\">.*?</script>",
        "",
        content,
        flags=re.DOTALL,
    )
    return content.replace("</head>", schema_html + "\n</head>", 1)


def patch_core_pages(config: dict[str, Any], services: list[dict[str, Any]]) -> None:
    for filename, page in config["corePages"].items():
        path = ROOT / filename
        if not path.exists():
            continue

        canonical = abs_url(config, page["path"])
        og_image = abs_asset(config, page.get("ogImage", config["defaultOgImage"]))
        seo_block = seo_head_block(
            config,
            title=page["title"],
            description=page["description"],
            canonical=canonical,
            og_title=page.get("ogTitle", page["title"]),
            og_image=og_image,
            keywords=page.get("keywords", ""),
        )
        schema_html = build_schema_graph(
            config,
            page.get("schemas", []),
            filename=filename,
            services=services,
        )

        content = path.read_text(encoding="utf-8")
        content = replace_seo_head(content, seo_block)
        content = replace_json_ld(content, schema_html)
        path.write_text(content, encoding="utf-8")
        print(f"  ✓ SEO head + schema → {filename}")


def patch_inquiry_pages(config: dict[str, Any], services: list[dict[str, Any]]) -> None:
    inquiry_dir = ROOT / "inquiry"
    for service in services:
        filename = f"{service['slug']}.html"
        path = inquiry_dir / filename
        if not path.exists():
            continue

        page_url = abs_url(config, f"/inquiry/{service['slug']}")
        og_image = abs_asset(config, service["image"])
        title = f"{service['title']} Dubai | Free Inspection | XShield Pest Control"
        og_title = f"{service['title']} | XShield Dubai"
        keywords = (
            f"{service['slug'].replace('-', ' ')}, "
            f"{service['title'].lower()} dubai, pest control dubai"
        )

        seo_block = seo_head_block(
            config,
            title=title,
            description=service["metaDescription"],
            canonical=page_url,
            og_title=og_title,
            og_image=og_image,
            keywords=keywords,
        )
        schema_html = build_schema_graph(
            config,
            ["organization", "localBusiness", "inquiryService"],
            service=service,
            page_url=page_url,
        )

        content = path.read_text(encoding="utf-8")
        content = replace_seo_head(content, seo_block)
        content = replace_json_ld(content, schema_html)
        path.write_text(content, encoding="utf-8")
        print(f"  ✓ SEO head + schema → inquiry/{filename}")


def patch_heading_semantics() -> None:
    replacements = [
        (
            "<h2>To Protect and Prevent<br>Dubai's Trusted Pest Experts</h2>",
            '<h1 class="video-hero__title">To Protect and Prevent<br>Dubai\'s Trusted Pest Experts</h1>',
        ),
        (
            """                                    <h2>To Protect and Prevent</h2>
                                    <h3>About Us</h3>""",
            """                                    <p class="breadcumb-wrap__tagline">To Protect and Prevent</p>
                                    <h1>About Us</h1>""",
        ),
        (
            """                                    <h2>To Protect and Prevent</h2>
                                    <h3>Our Services</h3>""",
            """                                    <p class="breadcumb-wrap__tagline">To Protect and Prevent</p>
                                    <h1>Our Services</h1>""",
        ),
        (
            """                                    <h2>To Protect and Prevent</h2>
                                    <h3>Contact Us</h3>""",
            """                                    <p class="breadcumb-wrap__tagline">To Protect and Prevent</p>
                                    <h1>Contact Us</h1>""",
        ),
        (
            """                                    <h2>To Protect and Prevent</h2>
                                    <h3>Service Inquiry</h3>""",
            """                                    <p class="breadcumb-wrap__tagline">To Protect and Prevent</p>
                                    <p class="breadcumb-wrap__subtitle">Service Inquiry</p>""",
        ),
    ]

    targets = [
        ROOT / "index.html",
        ROOT / "about.html",
        ROOT / "service.html",
        ROOT / "contact.html",
        *list((ROOT / "inquiry").glob("*.html")),
    ]

    for target in targets:
        if not target.exists():
            continue
        content = target.read_text(encoding="utf-8")
        original = content
        for old, new in replacements:
            content = content.replace(old, new)
        if content != original:
            target.write_text(content, encoding="utf-8")
            print(f"  ✓ Heading semantics → {target.relative_to(ROOT)}")


def add_lazy_loading() -> None:
    pages = [ROOT / f for f in CORE_PAGES]
    for path in pages:
        if not path.exists():
            continue
        content = path.read_text(encoding="utf-8")

        def add_lazy(match: re.Match[str]) -> str:
            tag = match.group(0)
            if "loading=" in tag or "video-hero" in tag or "logo" in tag.lower():
                return tag
            return tag.replace("<img ", '<img loading="lazy" decoding="async" ', 1)

        updated = re.sub(r"<img\s[^>]*?>", add_lazy, content)
        if updated != content:
            path.write_text(updated, encoding="utf-8")
            print(f"  ✓ Lazy-load images → {path.name}")


def ensure_dubai_areas_section() -> None:
    marker = "xshield-areas"
    index_path = ROOT / "index.html"
    content = index_path.read_text(encoding="utf-8")
    if marker in content:
        return

    section = """
                <!-- start xshield-areas (local SEO) -->
                <section class="xshield-areas section-padding pt-0" aria-labelledby="areas-heading">
                    <div class="container">
                        <div class="wpo-section-title-s2 text-center wow fadeInUp" data-wow-duration="1000ms">
                            <span><i><img src="assets/logo/logo-mini.webp" alt="XShield"></i>service areas</span>
                            <h2 id="areas-heading">Pest Control Across Dubai &amp; the UAE</h2>
                            <p>XShield provides Dubai Municipality&ndash;licensed pest control, rodent removal, and deep cleaning for homes, villas, apartments, offices, restaurants, warehouses, and industrial facilities throughout Dubai.</p>
                        </div>
                        <ul class="xshield-areas__list" aria-label="Areas we serve in Dubai">
                            <li>Al Quoz</li>
                            <li>Dubai Marina</li>
                            <li>JLT</li>
                            <li>Downtown Dubai</li>
                            <li>Business Bay</li>
                            <li>Deira</li>
                            <li>Jumeirah</li>
                            <li>Arabian Ranches</li>
                            <li>Dubai Hills</li>
                            <li>JVC</li>
                            <li>Mirdif</li>
                            <li>Silicon Oasis</li>
                            <li>Palm Jumeirah</li>
                            <li>Dubai South</li>
                        </ul>
                    </div>
                </section>
                <!-- end xshield-areas -->

"""
    anchor = "                <!-- Start wpo-faq-section -->"
    if anchor not in content:
        return
    content = content.replace(anchor, section + anchor, 1)
    index_path.write_text(content, encoding="utf-8")
    print("  ✓ Dubai service areas section → index.html")


def generate_robots_txt(config: dict[str, Any]) -> None:
    robots = f"""User-agent: *
Allow: /

Sitemap: {config['siteUrl']}/sitemap.xml
"""
    (ROOT / "robots.txt").write_text(robots, encoding="utf-8")
    print("  ✓ robots.txt")


def generate_sitemap(config: dict[str, Any], services: list[dict[str, Any]]) -> None:
    today = date.today().isoformat()
    urls: list[tuple[str, str, str]] = []

    for filename, page in config["corePages"].items():
        priority = "1.0" if filename == "index.html" else "0.8"
        changefreq = "weekly" if filename == "index.html" else "monthly"
        urls.append((abs_url(config, page["path"]), changefreq, priority))

    for service in services:
        urls.append(
            (
                abs_url(config, f"/inquiry/{service['slug']}"),
                "monthly",
                "0.9",
            )
        )

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for loc, changefreq, priority in urls:
        lines.extend(
            [
                "  <url>",
                f"    <loc>{escape(loc)}</loc>",
                f"    <lastmod>{today}</lastmod>",
                f"    <changefreq>{changefreq}</changefreq>",
                f"    <priority>{priority}</priority>",
                "  </url>",
            ]
        )
    lines.append("</urlset>")

    (ROOT / "sitemap.xml").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  ✓ sitemap.xml ({len(urls)} URLs)")


def fix_legacy_domain_references(config: dict[str, Any]) -> None:
    old = "https://xshieldservices.com"
    new = config["siteUrl"]
    if old == new:
        return

    targets = list(ROOT.glob("*.html")) + list((ROOT / "inquiry").glob("*.html"))
    for path in targets:
        content = path.read_text(encoding="utf-8")
        if old not in content:
            continue
        path.write_text(content.replace(old, new), encoding="utf-8")
        print(f"  ✓ Domain URL fix → {path.relative_to(ROOT)}")


def optimize_hero_video() -> None:
    index_path = ROOT / "index.html"
    content = index_path.read_text(encoding="utf-8")
    updated = content.replace('preload="auto"', 'preload="metadata"')
    if updated != content:
        index_path.write_text(updated, encoding="utf-8")
        print("  ✓ Hero video preload → metadata")


def main() -> None:
    config = load_config()
    services = json.loads(SERVICES_PATH.read_text(encoding="utf-8"))

    print("→ Applying SEO enhancements...")
    fix_legacy_domain_references(config)
    patch_heading_semantics()
    ensure_dubai_areas_section()
    optimize_hero_video()
    add_lazy_loading()
    patch_core_pages(config, services)
    patch_inquiry_pages(config, services)
    generate_robots_txt(config)
    generate_sitemap(config, services)
    print("✓ SEO build complete.")


if __name__ == "__main__":
    main()

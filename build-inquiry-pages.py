#!/usr/bin/env python3
"""Generate static service inquiry pages from JSON + HTML template."""

from __future__ import annotations

import json
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parent
JSON_PATH = ROOT / "assets/data/services-inquiry.json"
TEMPLATE_PATH = ROOT / "_snippets/inquiry-page.template.html"
OUTPUT_DIR = ROOT / "inquiry"

WHATSAPP_NUMBER = "971586440451"
WHATSAPP_MESSAGE = (
    "Hello, I'd like to enquire about {title} with XShield. "
    "Please contact me for a free inspection."
)
SITE_URL = "https://xshield-services.com"


def whatsapp_url(title: str) -> str:
    text = WHATSAPP_MESSAGE.format(title=title)
    return f"https://wa.me/{WHATSAPP_NUMBER}?text={urllib.parse.quote(text)}"


def render(template: str, service: dict) -> str:
    wa = whatsapp_url(service["title"])
    og_image = f"{SITE_URL}/{service['image']}"
    page_url = f"{SITE_URL}/inquiry/{service['slug']}.html"
    replacements = {
        "{{TITLE}}": service["title"],
        "{{SLUG}}": service["slug"],
        "{{DESCRIPTION}}": service["description"],
        "{{IMAGE}}": service["image"],
        "{{META_DESCRIPTION}}": service["metaDescription"],
        "{{WHATSAPP_URL}}": wa,
        "{{OG_URL}}": page_url,
        "{{OG_IMAGE}}": og_image,
        "{{PAGE_TITLE}}": f"{service['title']} | Free Inspection Dubai | XShield",
        "{{OG_TITLE}}": f"{service['title']} | XShield Dubai",
    }
    html = template
    for key, value in replacements.items():
        html = html.replace(key, value)
    return html


def main() -> None:
    services = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for service in services:
        out = OUTPUT_DIR / f"{service['slug']}.html"
        out.write_text(render(template, service), encoding="utf-8")
        print(f"  ✓ {out.relative_to(ROOT)}")

    print(f"Generated {len(services)} inquiry pages in {OUTPUT_DIR.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()

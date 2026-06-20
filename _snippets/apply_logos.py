#!/usr/bin/env python3
"""Wire XShield logo assets into all HTML pages."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

LOGO_BRAND = """<a class="navbar-brand" href="index.html">
                                            <img class="xshield-logo xshield-logo--color" src="assets/logo/logo-horizontal.png" alt="XShield Pest Control &amp; Cleaning Services L.L.C.">
                                            <img class="xshield-logo xshield-logo--white" src="assets/logo/logo-horizontal-white.png" alt="" aria-hidden="true">
                                        </a>"""

FAVICON_BLOCK = """    <link rel="shortcut icon" type="image/png" href="assets/logo/favicon.png">
    <link rel="icon" type="image/png" href="assets/logo/favicon.png">
    <link rel="apple-touch-icon" href="assets/logo/logo-color.png">"""


def update_html(html: str) -> str:
    html = re.sub(
        r'<link rel="shortcut icon"[^>]+>',
        FAVICON_BLOCK,
        html,
        count=1,
    )
    html = html.replace(
        '<img src="assets/images/preloader.png" alt="">',
        '<img class="xshield-logo xshield-logo--stacked-white" src="assets/logo/logo-white.png" alt="XShield">',
    )
    html = re.sub(
        r'<a class="navbar-brand" href="index\.html">\s*<img src="assets/images/logo\.svg"\s*alt="">\s*</a>',
        LOGO_BRAND,
        html,
        count=1,
    )
    return html


def main():
    for path in sorted(ROOT.glob("*.html")):
        html = update_html(path.read_text(encoding="utf-8"))
        path.write_text(html, encoding="utf-8")
        print(f"Updated {path.name}")


if __name__ == "__main__":
    main()

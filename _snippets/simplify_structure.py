#!/usr/bin/env python3
"""Reduce site to 4 pages: Home, About Us, Services, Contact Us."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGES = ["index.html", "about.html", "service.html", "contact.html"]

NAV_UL = """<ul class="nav navbar-nav mb-2 mb-lg-0">
                                                <li><a href="index.html">Home</a></li>
                                                <li><a href="about.html">About Us</a></li>
                                                <li><a href="service.html">Services</a></li>
                                                <li><a href="contact.html">Contact Us</a></li>
                                            </ul>"""

FOOTER_QUICK_LINKS = """<ul>
                                <li><a href="index.html">Home</a></li>
                                <li><a href="about.html">About Us</a></li>
                                <li><a href="service.html">Services</a></li>
                                <li><a href="contact.html">Contact Us</a></li>
                            </ul>"""

MAP_EMBED = """<div class="map">
                                            <iframe
                                                src="https://maps.google.com/maps?q=Office+303,+Mohammad+Bin+Ahmad+Building,+Al+Quoz+Third,+Dubai,+UAE&amp;t=&amp;z=15&amp;ie=UTF8&amp;iwloc=&amp;output=embed"
                                                title="XShield office location — Al Quoz, Dubai"
                                                allowfullscreen loading="lazy"
                                                referrerpolicy="no-referrer-when-downgrade"></iframe>
                                        </div>"""

BLOG_SECTION_RE = re.compile(
    r"\s*<!-- start wpo-blog-section -->.*?<!-- end wpo-blog-section -->\s*",
    re.DOTALL,
)


def replace_nav(html: str) -> str:
    return re.sub(
        r'<ul class="nav navbar-nav mb-2 mb-lg-0">.*?</ul>',
        NAV_UL,
        html,
        count=1,
        flags=re.DOTALL,
    )


def replace_footer_links(html: str) -> str:
    return re.sub(
        r'(<h2 class="title">Quick Link</h2>\s*)<ul>.*?</ul>',
        r"\1" + FOOTER_QUICK_LINKS,
        html,
        count=1,
        flags=re.DOTALL,
    )


def replace_links(html: str) -> str:
    html = html.replace('href="appoinment.html"', 'href="contact.html"')
    html = html.replace('href="service-single.html"', 'href="service.html"')
    html = html.replace('href="faq.html"', 'href="contact.html"')
    html = html.replace('href="project.html"', 'href="service.html"')
    html = html.replace('href="team.html"', 'href="about.html"')
    return html


def replace_map(html: str) -> str:
    html = re.sub(
        r"<!-- MAP_EMBED_PENDING:.*?-->\s*<div class=\"map\">.*?</div>",
        MAP_EMBED,
        html,
        count=1,
        flags=re.DOTALL,
    )
    return html


def process_file(path: Path) -> None:
    html = path.read_text(encoding="utf-8")
    html = replace_nav(html)
    html = replace_footer_links(html)
    html = replace_links(html)
    if path.name == "index.html":
        html = BLOG_SECTION_RE.sub("\n", html)
    if path.name == "contact.html":
        html = replace_map(html)
    path.write_text(html, encoding="utf-8")
    print(f"updated {path.name}")


def main() -> None:
    for name in PAGES:
        process_file(ROOT / name)


if __name__ == "__main__":
    main()

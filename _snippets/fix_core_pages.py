#!/usr/bin/env python3
"""Fix nav duplication and footer quick links on core 4 pages."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGES = ["index.html", "about.html", "service.html", "contact.html"]

FOOTER_QUICK_LINKS = """<ul>
                                <li><a href="index.html">Home</a></li>
                                <li><a href="about.html">About Us</a></li>
                                <li><a href="service.html">Services</a></li>
                                <li><a href="contact.html">Contact Us</a></li>
                            </ul>"""


def fix_nav(content: str) -> str:
    return re.sub(
        r'(<li><a href="contact\.html">Contact Us</a></li>\s*</ul>)\s*</li>.*?(\n\s*</div>\s*\n\s*<!-- end of nav-collapse -->)',
        r"\1\2",
        content,
        count=1,
        flags=re.DOTALL,
    )


def fix_footer(content: str) -> str:
    return re.sub(
        r'(<h2 class="title">Quick Link</h2>\s*)<ul>.*?</ul>',
        r"\1" + FOOTER_QUICK_LINKS,
        content,
        count=1,
        flags=re.DOTALL,
    )


def fix_header_cta(content: str) -> str:
    return content.replace(
        'href="appoinment.html">Book Free Inspection',
        'href="contact.html">Contact Us',
    )


for name in PAGES:
    path = ROOT / name
    c = path.read_text(encoding="utf-8")
    c = fix_nav(c)
    c = fix_footer(c)
    c = fix_header_cta(c)
    path.write_text(c, encoding="utf-8")
    print("Fixed", name)

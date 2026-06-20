#!/usr/bin/env python3
"""Fix nav duplication and header-right on retained pages."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RETAINED = [
    "index.html", "index-3.html", "about.html", "service.html", "service-single.html",
    "contact.html", "appoinment.html", "faq.html", "project.html", "team.html",
]

HEADER_RIGHT = """<div class="header-right">
                                    <div class="close-form">
                                        <a class="theme-btn" href="appoinment.html">Book Free Inspection</a>
                                    </div>
                                </div>"""


def fix_nav(content: str) -> str:
    return re.sub(
        r'(<li><a href="contact\.html">Contact</a></li>\s*</ul>)\s*</li>.*?(\n\s*</div>\s*\n\s*<!-- end of nav-collapse -->)',
        r'\1\2',
        content,
        count=1,
        flags=re.DOTALL,
    )


def fix_header_right(content: str) -> str:
    return re.sub(
        r'<div class="header-right">.*?<div class="close-form">\s*<a class="theme-btn" href="appoinment\.html">[^<]*</a>\s*</div>\s*</div>',
        HEADER_RIGHT,
        content,
        count=1,
        flags=re.DOTALL,
    )


def fix_footer(content: str) -> str:
    content = content.replace('<div class="wraper">\n                            <div class="wraper">', '<div class="wraper">')
    content = content.replace(
        'XShield Pest Control & Cleaning Services by\n                                        All rights reserved.',
        'XShield Pest Control & Cleaning Services. All rights reserved.',
    )
    return content


for name in RETAINED:
    path = ROOT / name
    c = path.read_text(encoding="utf-8")
    c = fix_nav(c)
    c = fix_header_right(c)
    c = fix_footer(c)
    path.write_text(c, encoding="utf-8")
    print("Fixed", name)

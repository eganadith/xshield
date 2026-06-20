#!/usr/bin/env python3
"""Bulk XShield rebrand helpers for retained HTML pages."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RETAINED = [
    "index-3.html", "about.html", "service.html", "service-single.html",
    "contact.html", "appoinment.html", "faq.html", "project.html", "team.html",
]

NAV_UL = """<ul class="nav navbar-nav mb-2 mb-lg-0">
                                                <li><a href="index.html">Home</a></li>
                                                <li><a href="about.html">About Us</a></li>
                                                <li><a href="service.html">Services</a></li>
                                                <li><a href="contact.html">Contact Us</a></li>
                                            </ul>"""

HEADER_RIGHT = """<div class="header-right">
                                    <div class="close-form">
                                        <a class="theme-btn" href="contact.html">Contact Us</a>
                                    </div>
                                </div>"""

TOPBAR_CONTACT = """<ul class="contact-info">
                                        <li>
                                            <a href="tel:+97144106502">
                                                <i class="flaticon-phone"></i><span>+971 4 410 6502</span>
                                            </a>
                                        </li>
                                        <li>
                                            <a href="mailto:contact@xshieldservices.com">
                                                <i class="ti-email"></i><span>contact@xshieldservices.com</span>
                                            </a>
                                        </li>
                                        <li>
                                            <i class="ti-location-pin"></i><span>Office 303, Al Quoz Third, Dubai, UAE</span>
                                        </li>
                                    </ul>"""

FOOTER_TOPBAR = """<h2 class="scroll-text-animation">
                                <span>To Protect and Prevent</span> <br> Licensed by Dubai Municipality · 24/7 Service · 10+ Years Experience · Free Inspection — <span class="color">contact@xshieldservices.com</span>
                            </h2>
                            <div class="booking-btn wow zoomIn" data-wow-duration="1000ms"><a
                                    class="btn-wrapper btn-move" href="contact.html"><small><i><img
                                                src="assets/images/arrow-up-black.svg" alt=""></i>Contact
                                        Us</small></a></div>"""

FOOTER_QUICK_LINKS = """<ul>
                                <li><a href="index.html">Home</a></li>
                                <li><a href="about.html">About Us</a></li>
                                <li><a href="service.html">Services</a></li>
                                <li><a href="contact.html">Contact Us</a></li>
                            </ul>"""

FOOTER_CONTACT = """<ul>
                                <li>Office 303, Mohammad Bin Ahmad Building,</li>
                                <li>Al Quoz Third, Dubai, UAE</li>
                                <li>contact@xshieldservices.com</li>
                                <li>+971 4 410 6502</li>
                                <li>WhatsApp: +971 58 644 0451</li>
                            </ul>"""

FABS = (ROOT / "_snippets" / "xshield-fabs.html").read_text()

GLOBAL_REPLACEMENTS = [
    ("contact@glowz.com", "contact@xshieldservices.com"),
    ("info@glowz.com", "contact@xshieldservices.com"),
    ("+1300 877 503", "+971 4 410 6502"),
    ("support@user.com", "contact@xshieldservices.com"),
    ("+88 7869 5874 96", "+971 4 410 6502"),
    ("tel:+887869587496", "tel:+97144106502"),
    ("54 Berrick St Boston MA 02115", "Office 303, Al Quoz Third, Dubai, UAE"),
    ("info@example.com", "contact@xshieldservices.com"),
    ('content="wpOceans"', 'content="XShield Pest Control & Cleaning Services"'),
    ("Because Clean Feels Better", "To Protect and Prevent"),
    ("Wpocean", "XShield Pest Control & Cleaning Services"),
    ("Saturday - Thursday", "Open 24/7 — Including weekends and public holidays"),
    ("Germany —", "Dubai —"),
    ("785 15h Street,", "Office 303, Mohammad Bin Ahmad Building,"),
    ("Office 478 Berlin, De 81566", "Al Quoz Third, Dubai, UAE"),
    ('href="index-3.html"', 'href="index.html"'),
    ("Appoinment", "Book Inspection"),
    ("Appoinment</a>", "Book Inspection</a>"),
    ("About Company", "About Us"),
    ("Our Blogs", "FAQ"),
    ('href="blog.html">FAQ</a>', 'href="faq.html">FAQ</a>'),
    ("Get in\n                                        tocuh", "Book Free Inspection"),
    ("Get in tocuh", "Book Free Inspection"),
    ("Newslatter", "Newsletter"),
    ("New Creative Ideas", "To Protect and Prevent"),
    ("send me an e-mail", "Free Inspection"),
    ("fill=\"#42C652\"", "fill=\"#4A9B2F\""),
]


def replace_nav(content: str) -> str:
    content = re.sub(
        r'<ul class="nav navbar-nav mb-2 mb-lg-0">.*?</ul>',
        NAV_UL,
        content,
        count=1,
        flags=re.DOTALL,
    )
    content = re.sub(
        r'<div class="header-right">.*?</div>\s*</div>\s*</div>\s*</div>\s*</nav>',
        HEADER_RIGHT + "\n                            </div>\n                        </div>\n                    </div><!-- end of container -->\n                </nav>",
        content,
        count=1,
        flags=re.DOTALL,
    )
    return content


def replace_topbar(content: str) -> str:
    if "<div class=\"topbar\">" in content:
        content = re.sub(
            r'<ul class="contact-info">.*?</ul>',
            TOPBAR_CONTACT,
            content,
            count=1,
            flags=re.DOTALL,
        )
    return content


def replace_footer(content: str) -> str:
    content = re.sub(
        r'<h2 class="scroll-text-animation">.*?</div>\s*</div>\s*</div>\s*</div>\s*<div class="container">\s*<div class="footer">',
        '<div class="wraper">\n                            ' + FOOTER_TOPBAR + '\n                        </div>\n                    </div>\n                </div>\n                <div class="container">\n                    <div class="footer">',
        content,
        count=1,
        flags=re.DOTALL,
    )
    # Fix if wraper duplicated - simpler approach: replace footer quick links block
    content = re.sub(
        r'(<h2 class="title">Quick Link</h2>\s*)<ul>.*?</ul>',
        r'\1' + FOOTER_QUICK_LINKS,
        content,
        count=1,
        flags=re.DOTALL,
    )
    content = re.sub(
        r'(<h2 class="title">Contact info</h2>\s*)<ul>.*?</ul>',
        r'\1' + FOOTER_CONTACT,
        content,
        count=1,
        flags=re.DOTALL,
    )
    return content


def add_fabs(content: str) -> str:
    if "xshield-fab--whatsapp" not in content:
        content = content.replace("</body>", FABS + "\n</body>")
    return content


def process_file(name: str) -> None:
    path = ROOT / name
    content = path.read_text(encoding="utf-8")
    for old, new in GLOBAL_REPLACEMENTS:
        content = content.replace(old, new)
    content = replace_nav(content)
    content = replace_topbar(content)
    content = replace_footer(content)
    content = add_fabs(content)
    path.write_text(content, encoding="utf-8")
    print(f"Updated {name}")


if __name__ == "__main__":
    for f in RETAINED:
        process_file(f)

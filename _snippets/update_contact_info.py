#!/usr/bin/env python3
"""Update address, map embed, and social links on live pages."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LIVE_PAGES = ["index.html", "about.html", "service.html", "contact.html"]

FOOTER_SOCIAL = (ROOT / "_snippets/xshield-social-footer.html").read_text(encoding="utf-8")
TOPBAR_SOCIAL = (ROOT / "_snippets/xshield-social-topbar.html").read_text(encoding="utf-8")

MAP_SRC = (
    "https://www.google.com/maps/embed?pb=!1m17!1m12!1m3!1d3611.4769043096207!"
    "2d55.24081007538031!3d25.153369977739185!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!"
    "4f13.1!3m2!1m1!2zMjXCsDA5JzEyLjEiTiA1NcKwMTQnMzYuMiJF!5e0!3m2!1sen!2sae!"
    "4v1781849175599!5m2!1sen!2sae"
)

FOOTER_CONTACT = """                                <li>Office 303, Mohammad Bin Ahmad Building,</li>
                                <li>Al Quoz 3, Dubai, United Arab Emirates, 391619</li>
                                <li>contact@xshieldservices.com</li>
                                <li>+971 4 410 6502</li>
                                <li>WhatsApp: +971 58 644 0451</li>"""

TOPBAR_ADDRESS = (
    "Office 303, Mohammad Bin Ahmad Building, Al Quoz 3, Dubai, UAE"
)

OFFICE_CARD = (
    "Office 303, Mohammad Bin Ahmad Building,<br>"
    "Al Quoz 3, Dubai, United Arab Emirates, 391619"
)


def replace_social_footer(html: str) -> str:
    return re.sub(
        r"<ul class=\"widget-social\">.*?</ul>",
        FOOTER_SOCIAL.strip(),
        html,
        count=1,
        flags=re.DOTALL,
    )


def replace_social_topbar(html: str) -> str:
    return re.sub(
        r"<ul class=\"social-media\">.*?</ul>",
        TOPBAR_SOCIAL.strip(),
        html,
        count=1,
        flags=re.DOTALL,
    )


def replace_footer_contact(html: str) -> str:
    return re.sub(
        r"<h2 class=\"title\">Contact info</h2>\s*<ul>\s*"
        r"<li>Office 303.*?</li>\s*"
        r"<li>WhatsApp:.*?</li>",
        f"<h2 class=\"title\">Contact info</h2>\n                            <ul>\n{FOOTER_CONTACT}",
        html,
        count=1,
        flags=re.DOTALL,
    )


def replace_topbar_address(html: str) -> str:
    return re.sub(
        r"<i class=\"ti-location-pin\"></i><span>.*?</span>",
        f"<i class=\"ti-location-pin\"></i><span>{TOPBAR_ADDRESS}</span>",
        html,
        count=1,
    )


def replace_map(html: str) -> str:
    return re.sub(
        r'src="https://maps\.google\.com/maps\?[^"]+"',
        f'src="{MAP_SRC}"',
        html,
        count=1,
    )


def replace_office_card(html: str) -> str:
    return re.sub(
        r"<p>Office 303, Mohammad Bin Ahmad Building,<br>.*?</p>",
        f"<p>{OFFICE_CARD}</p>",
        html,
        count=1,
    )


def main():
    for name in LIVE_PAGES:
        path = ROOT / name
        html = path.read_text(encoding="utf-8")
        html = replace_social_footer(html)
        html = replace_footer_contact(html)
        if name != "index.html":
            html = replace_social_topbar(html)
            html = replace_topbar_address(html)
        if name == "contact.html":
            html = replace_map(html)
            html = replace_office_card(html)
        path.write_text(html, encoding="utf-8")
        print(f"Updated {name}")


if __name__ == "__main__":
    main()

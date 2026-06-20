#!/usr/bin/env python3
"""Trim duplicate sections and streamline 4-page site flow."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CTA_BAND = (ROOT / "_snippets/xshield-cta-band.html").read_text(encoding="utf-8")
FOOTER_MARKER = "<!-- Start footer -->"


def remove_between(html: str, start_marker: str, end_marker: str) -> str:
    pattern = re.compile(
        re.escape(start_marker) + r".*?" + re.escape(end_marker),
        re.DOTALL,
    )
    return pattern.sub("", html)


def fix_index(html: str) -> str:
    html = html.replace(
        '<a href="contact.html" class="theme-btn">Book Now</a>',
        '<a href="about.html" class="theme-btn">About Us</a>',
        1,
    )
    for start, end in [
        ("<!-- start wpo-choose-section -->", "<!-- end wpo-choose-section -->"),
        ("<!-- Start transforming -->", "<!-- end transforming -->"),
        ("<!-- start of wpo-contact-section -->", "<!-- end of wpo-contact-section -->"),
        ("<!-- start wpo-booking-section -->", "<!-- end booking-section -->"),
    ]:
        html = remove_between(html, start, end)
    html = html.replace(FOOTER_MARKER, CTA_BAND + "\n" + FOOTER_MARKER)
    return html


def fix_about(html: str) -> str:
    for start, end in [
        ("<!-- start wpo-service-section -->", "<!-- end of wpo-service-section -->"),
        ("<!-- start wpo-work-section -->", "<!-- end wpo-work-section -->"),
        ("<!-- Start transforming -->", "<!-- end transforming -->"),
        ("<!-- Start wpo-cta-section -->", "<!-- end wpo-cta-section -->"),
        ("<!-- Start wpo-faq-section -->", "<!-- end wpo-faq-section -->"),
        ("<!-- start wpo-testimonials-section -->", "<!-- end testimonials-section -->"),
        ("<!-- start of wpo-contact-section -->", "<!-- end of wpo-contact-section -->"),
        ("<!-- start wpo-booking-section -->", "<!-- end booking-section -->"),
        ("<!-- Start partners -->", "<!-- end partners -->"),
    ]:
        html = remove_between(html, start, end)
    html = html.replace(FOOTER_MARKER, CTA_BAND + "\n" + FOOTER_MARKER)
    return html


def fix_service(html: str) -> str:
    for start, end in [
        ("<!-- Start wpo-cta-section -->", "<!-- end wpo-cta-section -->"),
        ("<!-- Start wpo-faq-section -->", "<!-- end wpo-faq-section -->"),
        ("<!-- start of wpo-contact-section -->", "<!-- end of wpo-contact-section -->"),
        ("<!-- Start partners -->", "<!-- end partners -->"),
    ]:
        html = remove_between(html, start, end)
    html = html.replace(FOOTER_MARKER, CTA_BAND + "\n" + FOOTER_MARKER)
    return html


def main():
    (ROOT / "index.html").write_text(
        fix_index((ROOT / "index.html").read_text(encoding="utf-8")),
        encoding="utf-8",
    )
    (ROOT / "about.html").write_text(
        fix_about((ROOT / "about.html").read_text(encoding="utf-8")),
        encoding="utf-8",
    )
    (ROOT / "service.html").write_text(
        fix_service((ROOT / "service.html").read_text(encoding="utf-8")),
        encoding="utf-8",
    )
    print("Site flow cleanup complete.")


if __name__ == "__main__":
    main()

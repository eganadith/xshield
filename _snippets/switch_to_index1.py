#!/usr/bin/env python3
"""Switch canonical home to index.html (Home style 1) and rebrand it."""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "_snippets"))

from apply_rebrand import (
    GLOBAL_REPLACEMENTS, FOOTER_TOPBAR, FOOTER_QUICK_LINKS, FOOTER_CONTACT, FABS,
    replace_footer, add_fabs,
)
from patch_content import build_slider, add_seo, patch_about
from patch_remaining import global_fixes, FAQ_ACCORDION, CTA_EMERGENCY, CTA_FEATURES

RETAINED = [
    "index.html", "about.html", "service.html", "service-single.html",
    "contact.html", "appoinment.html", "faq.html", "project.html", "team.html",
]

NAV_UL = """<ul class="nav navbar-nav mb-2 mb-lg-0">
                                                <li><a href="index.html">Home</a></li>
                                                <li><a href="about.html">About</a></li>
                                                <li class="menu-item-has-children">
                                                    <a href="#">Services</a>
                                                    <ul class="sub-menu">
                                                        <li><a href="service.html">Services</a></li>
                                                        <li><a href="service-single.html">Service Detail</a></li>
                                                    </ul>
                                                </li>
                                                <li><a href="project.html">Recent Jobs</a></li>
                                                <li><a href="appoinment.html">Book Inspection</a></li>
                                                <li><a href="faq.html">FAQ</a></li>
                                                <li><a href="contact.html">Contact</a></li>
                                            </ul>"""

HEADER_CALL = """<div class="header-right">
                                            <a href="tel:+97144106502" class="call">
                                                <div class="icon">
                                                    <img src="assets/images/call.svg" alt="">
                                                </div>
                                                <div class="text">
                                                    <h4>+971 4 410 6502</h4>
                                                    <span>24/7 Available</span>
                                                </div>
                                            </a>
                                        </div>"""

HEADER_RIGHT_BOX = """<div class="header-right">
                                    <div class="close-form">
                                        <a class="theme-btn" href="appoinment.html">Book Free Inspection</a>
                                    </div>
                                </div>"""


def replace_nav(content: str) -> str:
    content = re.sub(
        r'<ul class="nav navbar-nav mb-2 mb-lg-0">.*?</ul>',
        NAV_UL,
        content,
        count=1,
        flags=re.DOTALL,
    )
    return content


def replace_index1_header_right(content: str) -> str:
    content = re.sub(
        r'<div class="header-right">\s*<a href="tel:.*?</a>\s*</div>',
        HEADER_CALL,
        content,
        count=1,
        flags=re.DOTALL,
    )
    content = re.sub(
        r'<div class="header-right">\s*<div class="close-form">.*?</div>\s*</div>',
        HEADER_RIGHT_BOX,
        content,
        count=1,
        flags=re.DOTALL,
    )
    return content


def patch_index1(content: str) -> str:
    content = patch_about(content)
    content = content.replace(
        "<h2>From Dust to Shine, Every Time.</h2>",
        "<h2>To Protect and Prevent — Dubai's Trusted Pest Experts</h2>",
    )
    content = re.sub(
        r"<p>From deep residential cleaning.*?</p>",
        "<p>Licensed by Dubai Municipality with 10+ years of experience. We eliminate pests, protect your property, and keep spaces clean — residential, commercial, and industrial.</p>",
        content,
        count=1,
        flags=re.DOTALL,
    )
    content = content.replace('class="theme-btn">Explore Our Work</a>', 'class="theme-btn">Book Free Inspection</a>')
    content = content.replace(
        "<h2 class=\"poort-text poort-in-right\">Where Cleanliness meets Care Services</h2>",
        "<h2 class=\"poort-text poort-in-right\">Professional Pest Control &amp; Cleaning Services</h2>",
    )
    slider = build_slider().replace("service-slider-s2", "service-slider")
    content = re.sub(
        r'<div class="service-slider">.*?</div>\s*<div class="left-shape2">',
        '<div class="service-slider">\n' + build_slider().split("service-slider-s2")[0] + "\n".join(
            line for line in build_slider().replace('<div class="service-slider-s2">', "").replace("service-slider-s2", "service-slider").split("\n") if line.strip()
        ) + "\n                            </div>\n                        </div>\n                    </div>\n                    <div class=\"left-shape2\">",
        content,
        count=1,
        flags=re.DOTALL,
    )
    # simpler service slider replace
    content = re.sub(
        r'<div class="service-slider">.*?</div>\s*</div>\s*</div>\s*</div>\s*<div class="left-shape2">',
        '<div class="service-slider">\n' + "\n".join(
            line.replace("service-slider-s2", "service-slider") if "service-slider-s2" in line else line
            for line in build_slider().split("\n")
        ) + "\n                            </div>\n                        </div>\n                    </div>\n                </div>\n                <div class=\"left-shape2\">",
        content,
        count=1,
        flags=re.DOTALL,
    )
    content = content.replace(
        "<h2 class=\"poort-text poort-in-right\">Your Space Deserves the Best Here’s\n                                                Why We’re\n                                                It</h2>",
        "<h2 class=\"poort-text poort-in-right\">Why Choose XShield</h2>",
    )
    content = re.sub(
        r"<p>Our team of trained professionals takes pride.*?</p>",
        "<p>Licensed by Dubai Municipality with 10+ years serving Dubai. We combine expert pest control with professional cleaning for complete property protection.</p>",
        content,
        count=1,
        flags=re.DOTALL,
    )
    for old, new in [
        ("Trusted & Vetted Cleaners", "Licensed & Approved by Dubai Municipality"),
        ("Customizable Cleaning Plans", "24/7 Emergency Service"),
        ("Affordable & Transparent Pricing", "Free Inspection"),
        ("Satisfaction Guarantee", "10+ Years of Experience"),
    ]:
        content = content.replace(f"<span>{old}</span>", f"<span>{new}</span>")
    content = content.replace(
        "<h2 class=\"poort-text poort-in-right\">we’re prooffesionaly Commited\n                                        to give best Cleaning services\n                                        see how it works actually</h2>",
        "<h2 class=\"poort-text poort-in-right\">How XShield Works — Simple, Transparent, Effective</h2>",
    )
    content = content.replace("<span>Book online</span>", "<span>Free Inspection</span>")
    content = content.replace("<span>get service</span>", "<span>Custom Treatment</span>")
    content = content.replace("<span>Enjoy service</span>", "<span>Protection &amp; Follow-Up</span>")
    content = content.replace('<span class="odometer" data-count="25">00</span>', '<span class="odometer" data-count="10">00</span>+')
    content = content.replace('<span class="odometer" data-count="75">00</span>k', '<span class="odometer" data-count="5000">00</span>+')
    content = content.replace("<h3>Satisfied Clients</h3>", "<h3>Jobs Completed</h3>")
    content = content.replace('<span class="odometer" data-count="134">00</span>', '<span class="odometer" data-count="50">00</span>+')
    content = content.replace("<h3>Team Members</h3>", "<h3>Expert Technicians</h3>")
    content = content.replace('<span class="odometer" data-count="85">00</span>', '<span class="odometer" data-count="98">00</span>')
    content = content.replace("<h3>Customer Retention Rate</h3>", "<h3>Customer Satisfaction</h3>")
    content = content.replace("before &\n                                        after", "Results You Can See")
    content = content.replace(
        "<h2 class=\"poort-text poort-in-right\">Transforming Spaces, One Clean at a\n                                        Time</h2>",
        "<h2 class=\"poort-text poort-in-right\">From Infestation to Protection</h2>",
    )
    content = content.replace(
        "<p>Let us take the stress out of cleaning, so you can focus on what matters\n                                        most.</p>",
        "<p>See the difference professional treatment makes. We don't just spray and leave — we identify the source, treat effectively, and advise on prevention.</p>",
    )
    for old, new in [
        (" Deep & Detailed Cleaning", "Thorough Inspection"),
        ("Eco-Friendly Products", "Targeted Treatment"),
        ("Flexible Scheduling", "Prevention Advice"),
    ]:
        content = content.replace(f"<span>{old}</span>", f"<span>{new}</span>")
    content = content.replace('class="theme-btn-s2">Try yours now</a>', 'class="theme-btn-s2">Get Free Inspection</a>')
    content = content.replace(
        "<h2 class=\"poort-text poort-in-right\">Freequently ask questions...</h2>",
        "<h2 class=\"poort-text poort-in-right\">Common Questions About Pest Control in Dubai</h2>",
    )
    content = re.sub(
        r'<p>“Cleaning hires great people.*?</p>',
        '<p>"XShield responded within hours for a cockroach problem in our restaurant. Professional, discreet, and municipality-compliant. Highly recommend."</p>',
        content,
        count=1,
        flags=re.DOTALL,
    )
    content = content.replace("<h5>Aliza Anderson</h5>", "<h5>Khalid R.</h5>")
    content = content.replace("<span>CEO & Founder </span>", "<span>Restaurant Owner</span>")
    content = re.sub(
        r'<p>“Cleaning brings together talented people.*?</p>',
        '<p>"They handled termites in our villa and followed up twice. Clear pricing, no upselling, and the team explained everything."</p>',
        content,
        count=1,
        flags=re.DOTALL,
    )
    content = content.replace("<h5>Sara Williamson</h5>", "<h5>Sarah M.</h5>")
    content = content.replace(
        "<h2 class=\"poort-text poort-in-right\">Reach Out for a Sparkling\n                                                Space today</h2>",
        "<h2 class=\"poort-text poort-in-right\">Request a Free Pest Inspection</h2>",
    )
    content = content.replace(
        '<option disabled="disabled" selected>Service catagories</option>\n                                                        <option>Office</option>\n                                                        <option>Home</option>\n                                                        <option>Shop</option>\n                                                        <option>Road</option>\n                                                        <option>car</option>',
        '<option disabled="disabled" selected>Choose a Service</option><option>General Pest & Rodent Control</option><option>Cockroach Control</option><option>Bed Bug Removal</option><option>Termite & Wood Borer Control</option><option>Ant Control</option><option>Mosquito & Fly Control</option><option>Bee Hives Removal</option><option>Bird Control</option><option>Snake Control</option><option>Fleas, Ticks & Silverfish Control</option><option>Deep Cleaning, Disinfecting & Sanitizing</option><option>Sofa, Mattress & Carpet Cleaning</option>',
    )
    content = content.replace('class="theme-btn-s2">Book Now</a>', 'class="theme-btn-s2">Book Free Inspection</a>')
    content = content.replace("News &\n                                    Blogs", "Tips &amp; Advice")
    content = content.replace("<h2 class=\"poort-text poort-in-right\">Updated News & Blogs</h2>", "<h2 class=\"poort-text poort-in-right\">Pest Prevention Insights</h2>")
    content = re.sub(
        r"<p>communication and utilizes cutting edge logistic planning.*?</p>",
        "<p>Practical guidance from our Dubai technicians.</p>",
        content,
        count=1,
        flags=re.DOTALL,
    )
    for cat, old in zip(
        ["Pest Prevention", "Home Care", "Commercial"],
        ["Home Cleaning", "Office Cleaning", "Desk Cleaning"],
    ):
        content = content.replace(f'href="blog-single.html">{old}</a>', f'href="faq.html">{cat}</a>', 1)
    content = content.replace('href="blog-single.html"', 'href="faq.html"')
    content = content.replace('fill="#42C652"', 'fill="#4A9B2F"')
    return content


def apply_globals(content: str) -> str:
    for old, new in GLOBAL_REPLACEMENTS:
        content = content.replace(old, new)
    content = content.replace('href="index-3.html"', 'href="index.html"')
    return content


def process_index_html():
    path = ROOT / "index.html"
    c = path.read_text(encoding="utf-8")
    c = apply_globals(c)
    c = replace_nav(c)
    c = replace_index1_header_right(c)
    c = replace_footer(c)
    c = global_fixes(c)
    c = patch_index1(c)
    # fix service slider if broken - use clean build
    slider_inner = build_slider()
    c = re.sub(
        r'<div class="service-slider">.*?</div>\s*</div>\s*</div>\s*</div>\s*<div class="left-shape2">',
        '<div class="service-slider">\n' + slider_inner + '\n                            </div>\n                        </div>\n                    </div>\n                </div>\n                <div class="left-shape2">',
        c,
        count=1,
        flags=re.DOTALL,
    )
    c = add_seo(c, "index-3.html")  # reuse home SEO entry
    c = add_fabs(c)
    path.write_text(c, encoding="utf-8")
    print("Rebranded index.html")


def switch_home_links():
    for name in RETAINED:
        if name == "index.html":
            continue
        path = ROOT / name
        c = path.read_text(encoding="utf-8")
        c = c.replace('href="index-3.html"', 'href="index.html"')
        c = c.replace("<li><a href=\"index-3.html\">Home</a></li>", "<li><a href=\"index.html\">Home</a></li>")
        path.write_text(c, encoding="utf-8")
        print("Updated home link:", name)
    # COPY_DECK
    deck = ROOT / "COPY_DECK.md"
    if deck.exists():
        t = deck.read_text()
        t = t.replace("index-3.html", "index.html")
        t = t.replace("Home style 3", "Home style 1")
        deck.write_text(t)


if __name__ == "__main__":
    process_index_html()
    switch_home_links()

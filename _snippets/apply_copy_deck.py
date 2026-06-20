#!/usr/bin/env python3
"""Apply XShield copy deck to live pages (copy-only)."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LIVE = ["index.html", "about.html", "service.html", "contact.html"]

SERVICES = [
    {
        "title": "General Pest & Rodent Control",
        "blurb": "Comprehensive pest management covering rodents and general infestations, tailored to your property.",
        "long": "Historically, rodents such as rats and mice have been responsible for spreading fatal diseases and plagues. Preventing their spread takes both active rodent control measures and adequate precautions so they don't return. XShield addresses rodent and general pest issues at any level of infestation with efficient, ongoing control services in Dubai.",
    },
    {
        "title": "Cockroach Control",
        "blurb": "Multi-stage spray or gel treatment programs that prevent re-infestation.",
        "long": "Cockroaches can create a war-like environment in your house. XShield runs a multi-stage treatment program to win that war and prevent re-infestation. We offer both spray and gel treatment — spray requires vacating the home for 4 hours, while gel treatment is safe, non-toxic and odorless.",
    },
    {
        "title": "Bed Bug Removal",
        "blurb": "Industry-approved treatment for bedding, furniture and surrounding areas.",
        "long": "Bed bugs can quickly turn your peaceful sleep into a nightmare. Our specialized bed bug control services use industry-approved techniques to eradicate them from bedding, furniture and surrounding areas. For serious infestations we provide 2–3 visits to ensure they don't return.",
    },
    {
        "title": "Termite & Wood Borer Control",
        "blurb": "Protecting structural timber and furniture from termite and borer damage.",
        "long": "Protecting structural timber and furniture from termite and borer damage. Detailed treatment copy pending client sign-off — contact us for a free inspection and tailored plan.",
    },
    {
        "title": "Ant Control",
        "blurb": "Locate-and-eliminate colony treatment using gel or spray.",
        "long": "Ants may be small, but their presence can be a big annoyance. Our ant control service locates and eliminates colonies before they invade your living or working space, using targeted gel or spray treatment for effective, lasting results.",
    },
    {
        "title": "Mosquito & Fly Control",
        "blurb": "Spray treatment and fly traps for mosquitoes, flies and wasps.",
        "long": "There are over 100,000 known types of flying insects, including mosquitoes, flies and wasps, and the number keeps growing. XShield has helped the UAE with detection, prevention and long-term control of flying-insect infestations using spray treatment and fly traps. Get in touch for a free inspection.",
    },
    {
        "title": "Bee Hives Removal",
        "blurb": "Safe, expert beehive removal and bee population control.",
        "long": "XShield uses the most effective bee elimination techniques to control bee populations in Dubai. Our specialists are experts at removing beehives using the necessary, efficient techniques — safely and with minimal disruption to your property.",
    },
    {
        "title": "Bird Control",
        "blurb": "Nest removal and prevention to stop repeat bird infestations.",
        "long": "Birds may be beautiful, but a nest on your property can cause real damage if left unmanaged. XShield removes existing nests and puts prevention measures in place — such as bird spikes — so the problem doesn't come back and cost you in maintenance later.",
    },
    {
        "title": "Snake Control",
        "blurb": "Safe deterrent treatment to keep snakes away from your property.",
        "long": "Our team knows how to control snakes using active deterrent methods that keep them from interfering with human settlement, protecting your family and staff.",
    },
    {
        "title": "Fleas, Ticks & Silverfish Control",
        "blurb": "Protecting your family and pets from ticks, fleas and silverfish.",
        "long": "As a pet owner you know they need exercise, a good diet and plenty of affection — and protection from pests like ticks and fleas, which can cause Lyme disease and tick paralysis. XShield is a professional pest control company that helps you get rid of ticks, fleas and silverfish for good.",
    },
    {
        "title": "Deep Cleaning, Disinfecting & Sanitizing",
        "blurb": "Full move-in/move-out deep cleans plus disinfection for homes and offices.",
        "long": "Deep cleaning is one of our specialties. We provide a comprehensive range of deep cleaning and disinfecting/sanitizing services for moving in, moving out, homes, kitchens and offices — including sanitizing countertops, disinfecting high-touch surfaces like keyboards, mice and doorknobs, and flexible scheduling around your business needs.",
    },
    {
        "title": "Sofa, Mattress & Carpet Cleaning",
        "blurb": "Expert fabric and leather sofa, mattress and carpet cleaning — 100% satisfaction guaranteed.",
        "long": "Our experienced, qualified cleaning team restores sofas (fabric and leather), carpets and mattresses using the latest equipment and techniques. We recommend mattress cleaning every six months to extend its lifespan and address spills before they stain. All work is backed by a 100% satisfaction guarantee.",
    },
]

COMPANY = "XShield Pest Control &amp; Cleaning Services L.L.C."
COMPANY_PLAIN = "XShield Pest Control & Cleaning Services L.L.C."
TRUST = "Licensed &amp; Approved by Dubai Municipality · 24/7 Service · 10+ Years of Experience · Free Inspection"


def global_pass(html: str) -> str:
    html = html.replace(
        "XShield Pest Control &amp; Cleaning Services",
        COMPANY,
    )
    html = html.replace(
        "XShield Pest Control & Cleaning Services",
        COMPANY_PLAIN,
    )
    html = html.replace(
        "Licensed by Dubai Municipality · 24/7 Service · 10+ Years Experience · Free Inspection",
        TRUST.replace("&amp;", "&"),
    )
    html = html.replace(
        "Licensed & Approved by Dubai Municipality · 24/7 Service · 10+ Years Experience · Free Inspection",
        TRUST.replace("&amp;", "&"),
    )
    html = html.replace(
        '<a class="theme-btn-link" href="contact.html">Contact Us</a>',
        '<a class="theme-btn-link" href="contact.html">Book Free Inspection</a>',
    )
    html = re.sub(
        r"<i class=\"ti-location-pin\"></i><span>Office 303,[^<]+</span>",
        "<i class=\"ti-location-pin\"></i><span>Office 303, Mohammad Bin Ahmad Building, Al Quoz 3, Dubai, United Arab Emirates, 391619</span>",
        html,
    )
    return html


def update_carousel_blurbs(html: str) -> str:
    for svc in SERVICES:
        title = svc["title"].replace("&", "&amp;")
        pattern = (
            rf"(<h3 class=\"xshield-apple-card__title\"><a href=\"service\.html\">{re.escape(svc['title'])}</a></h3>\s*)"
            rf"<p class=\"xshield-apple-card__desc\">.*?</p>"
        )
        repl = rf'\1<p class="xshield-apple-card__desc">{svc["blurb"]}</p>'
        html = re.sub(pattern, repl, html, count=1)
        # badge via label
        label = "Cleaning" if "Cleaning" in svc["title"] or "Sanitiz" in svc["title"] or "Sofa" in svc["title"] else "Pest Control"
        html = html.replace(
            f'<p class="xshield-apple-card__label">{label}</p>\n                                    <h3 class="xshield-apple-card__title"><a href="service.html">{title}</a></h3>',
            f'<p class="xshield-apple-card__label">Free Inspection</p>\n                                    <h3 class="xshield-apple-card__title"><a href="service.html">{title}</a></h3>',
            1,
        )
    return html


def update_service_grid(html: str) -> str:
    intro = (
        '<p class="service-intro wow fadeInUp" data-wow-duration="1000ms">'
        "We use an integrated approach to eliminate all life cycle stages of the target pest — "
        "fast, efficient and professional service, every time.</p>"
    )
    html = html.replace(
        '<h2 class="poort-text poort-in-right">Complete Pest Control &amp; Cleaning Solutions</h2>\n                                    </div>',
        '<h2 class="poort-text poort-in-right">Complete Pest Control &amp; Cleaning Solutions</h2>\n                                        ' + intro + '\n                                    </div>',
        1,
    )
    for svc in SERVICES:
        t = svc["title"]
        pattern = (
            rf'(<h2><a href="service\.html">{re.escape(t)}</a></h2>)\s*'
            rf'(<a class="arrow" href="service\.html">)'
        )
        repl = rf'\1\n                                                    <p>{svc["blurb"]}</p>\n                                                    \2'
        html = re.sub(pattern, repl, html, count=1)
    return html


def main():
    for name in LIVE:
        path = ROOT / name
        html = path.read_text(encoding="utf-8")
        html = global_pass(html)
        if name == "index.html":
            html = update_carousel_blurbs(html)
        if name == "service.html":
            html = update_service_grid(html)
        path.write_text(html, encoding="utf-8")
        print(f"Updated {name}")

    # service-single template (example service)
    ss = ROOT / "service-single.html"
    if ss.exists():
        html = global_pass(ss.read_text(encoding="utf-8"))
        svc = SERVICES[0]
        html = re.sub(
            r"<h2>General Pest &amp; Rodent Control in Dubai</h2>\s*<p>.*?</p>",
            f"<h2>General Pest &amp; Rodent Control in Dubai</h2>\n                                    <p>{svc['long']}</p>",
            html,
            count=1,
            flags=re.DOTALL,
        )
        html = html.replace(
            "<li>Free initial inspection</li>\n                                                <li>Licensed technicians</li>\n                                                <li>Eco-conscious products where possible</li>",
            "<li>Inspection of the facilities to determine the level of pest infestation</li>\n                                                <li>Recommendations on structural and sanitation issues</li>\n                                                <li>Recommendations on a suitable IPM program (frequency of service) for the facility</li>",
        )
        ss.write_text(html, encoding="utf-8")
        print("Updated service-single.html")


if __name__ == "__main__":
    main()

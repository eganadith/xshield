#!/usr/bin/env python3
"""Apply XShield page-specific copy to retained HTML files."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

SERVICES = [
    ("General Pest & Rodent Control", 1),
    ("Cockroach Control", 2),
    ("Bed Bug Removal", 3),
    ("Termite & Wood Borer Control", 4),
    ("Ant Control", 5),
    ("Mosquito & Fly Control", 1),
    ("Bee Hives Removal", 2),
    ("Bird Control", 3),
    ("Snake Control", 4),
    ("Fleas, Ticks & Silverfish Control", 5),
    ("Deep Cleaning, Disinfecting & Sanitizing", 1),
    ("Sofa, Mattress & Carpet Cleaning", 2),
]

SVG_PATH = (
    'd="M1.60294 8.82231C-0.492335 4.80636 2.42121 0 6.95089 0H96.7463C101.157 0 103.808 4.89398 '
    '101.399 8.5886C100.237 10.3695 100.194 12.6573 101.288 14.4805L101.462 14.7702C103.899 18.8322 '
    '100.973 24 96.2363 24H7.54361C2.65837 24 -0.551448 18.8988 1.56255 14.4947L1.69305 14.2228C2.51567 '
    '12.509 2.48228 10.5077 1.60294 8.82231Z" fill="#4A9B2F"'
)

DURATIONS = ["1000ms", "1200ms", "1400ms", "1400ms", "1400ms", "1000ms", "1200ms", "1400ms", "1400ms", "1400ms", "1000ms", "1200ms"]


def service_slide(title: str, img: int, duration: str) -> str:
    return f"""                        <div class="wpo-service-slide-item">
                            <div class="wpo-service-item wow fadeInUp" data-wow-duration="{duration}">
                                <div class="wpo-service-img middle-light">
                                    <img src="assets/images/service/service-{img}.jpg" alt="{title}">
                                </div>
                                <div class="wpo-service-text">
                                    <div class="thumb">
                                        <span>Free Inspection</span>
                                        <svg xmlns="http://www.w3.org/2000/svg" width="103" height="24" viewBox="0 0 103 24" fill="none">
                                            <path {SVG_PATH} />
                                        </svg>
                                    </div>
                                    <h2><a href="service-single.html">{title}</a></h2>
                                    <a class="arrow" href="service-single.html"><i class="ti-arrow-top-right" aria-hidden="true"></i></a>
                                </div>
                            </div>
                        </div>"""


def service_grid_card(title: str, img: int, duration: str) -> str:
    return f"""                                            <div class="wpo-service-item wow fadeInUp" data-wow-duration="{duration}">
                                                <div class="wpo-service-img middle-light">
                                                    <img src="assets/images/service/service-{img}.jpg" alt="{title}">
                                                </div>
                                                <div class="wpo-service-text">
                                                    <div class="thumb">
                                                        <span>Free Inspection</span>
                                                        <svg xmlns="http://www.w3.org/2000/svg" width="103" height="24" viewBox="0 0 103 24" fill="none">
                                                            <path {SVG_PATH} />
                                                        </svg>
                                                    </div>
                                                    <h2><a href="service-single.html">{title}</a></h2>
                                                    <a class="arrow" href="service-single.html"><i class="ti-arrow-top-right" aria-hidden="true"></i></a>
                                                </div>
                                            </div>"""


def build_slider() -> str:
    lines = []
    for i, (title, img) in enumerate(SERVICES):
        lines.append(service_slide(title, img, DURATIONS[i]))
    return "\n".join(lines)


def build_service_grid() -> str:
    """Two rows of 6 cards for service.html style-3 grid."""
    cards = []
    for i, (title, img) in enumerate(SERVICES):
        col = i % 3
        row_start = i % 6 == 0
        card = service_grid_card(title, img, DURATIONS[i])
        if row_start and i > 0:
            cards.append("                                    </div>\n                                </div>\n                            </div>\n                            <div class=\"wpo-service-slide-item\">\n                                <div class=\"row\">")
        if i % 3 == 0:
            cards.append("                                        <div class=\"col-lg-4 col-md-6 col-12\">")
            cards.append("                                            <div class=\"wpo-service-slide-item\">")
            cards.append(card)
            cards.append("                                            </div>")
            cards.append("                                        </div>")
        elif i % 3 == 1:
            cards.append("                                        <div class=\"col-lg-4 col-md-6 col-12\">")
            cards.append("                                            <div class=\"wpo-service-slide-item\">")
            cards.append(card)
            cards.append("                                            </div>")
            cards.append("                                        </div>")
        else:
            cards.append("                                        <div class=\"col-lg-4 col-md-6 col-12\">")
            cards.append("                                            <div class=\"wpo-service-slide-item\">")
            cards.append(card)
            cards.append("                                            </div>")
            cards.append("                                        </div>")
    return "\n".join(cards)


FAQ_BLOCK = """                                <div class="accordion-item">
                                    <div class="accordion-header">
                                        <button class="accordion-button" type="button" data-bs-toggle="collapse"
                                            data-bs-target="#faq1" aria-expanded="true" aria-controls="faq1">
                                            Are your treatments approved by Dubai Municipality?
                                        </button>
                                    </div>
                                    <div id="faq1" class="accordion-collapse collapse show"
                                        data-bs-parent="#accordionExample">
                                        <div class="accordion-body">
                                            Yes. XShield is licensed and uses municipality-approved products and methods for residential and commercial properties.
                                        </div>
                                    </div>
                                </div>
                                <div class="accordion-item">
                                    <div class="accordion-header">
                                        <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse"
                                            data-bs-target="#faq2" aria-expanded="false" aria-controls="faq2">
                                            Do you offer free inspections?
                                        </button>
                                    </div>
                                    <div id="faq2" class="accordion-collapse collapse" data-bs-parent="#accordionExample">
                                        <div class="accordion-body">
                                            Yes. We provide a free initial inspection and quote before any treatment begins.
                                        </div>
                                    </div>
                                </div>
                                <div class="accordion-item">
                                    <div class="accordion-header">
                                        <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse"
                                            data-bs-target="#faq3" aria-expanded="false" aria-controls="faq3">
                                            How quickly can you respond to an emergency?
                                        </button>
                                    </div>
                                    <div id="faq3" class="accordion-collapse collapse" data-bs-parent="#accordionExample">
                                        <div class="accordion-body">
                                            We offer 24/7 emergency service across Dubai. Call or WhatsApp and we'll dispatch a team as soon as possible.
                                        </div>
                                    </div>
                                </div>
                                <div class="accordion-item">
                                    <div class="accordion-header">
                                        <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse"
                                            data-bs-target="#faq4" aria-expanded="false" aria-controls="faq4">
                                            Is treatment safe for children and pets?
                                        </button>
                                    </div>
                                    <div id="faq4" class="accordion-collapse collapse" data-bs-parent="#accordionExample">
                                        <div class="accordion-body">
                                            We use approved products and advise on re-entry times. Tell us about children, pets, or sensitive areas during inspection.
                                        </div>
                                    </div>
                                </div>
                                <div class="accordion-item">
                                    <div class="accordion-header">
                                        <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse"
                                            data-bs-target="#faq5" aria-expanded="false" aria-controls="faq5">
                                            Do you provide annual maintenance contracts?
                                        </button>
                                    </div>
                                    <div id="faq5" class="accordion-collapse collapse" data-bs-parent="#accordionExample">
                                        <div class="accordion-body">
                                            Yes — AMC plans for homes, restaurants, and facilities with scheduled visits and priority call-outs.
                                        </div>
                                    </div>
                                </div>
                                <div class="accordion-item">
                                    <div class="accordion-header">
                                        <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse"
                                            data-bs-target="#faq6" aria-expanded="false" aria-controls="faq6">
                                            Do you also offer cleaning services?
                                        </button>
                                    </div>
                                    <div id="faq6" class="accordion-collapse collapse" data-bs-parent="#accordionExample">
                                        <div class="accordion-body">
                                            Yes. We provide deep cleaning, disinfection, and sofa, mattress, and carpet cleaning — often bundled after pest treatment.
                                        </div>
                                    </div>
                                </div>"""

SIDEBAR_SERVICES = "\n".join(
    f'                                            <li><a href="service-single.html">{t}</a></li>' for t, _ in SERVICES
)

SEO = {
    "index-3.html": (
        "Pest Control Dubai | XShield — To Protect and Prevent",
        "Licensed pest control & cleaning in Dubai. Free inspection, 24/7 service, 10+ years experience. Call +971 4 410 6502.",
        "https://xshieldservices.com/",
    ),
    "about.html": (
        "About Us | XShield Pest Control Dubai",
        "Dubai Municipality-licensed pest control & cleaning. 10+ years protecting homes and businesses across the UAE.",
        "https://xshieldservices.com/about.html",
    ),
    "service.html": (
        "Pest Control Services Dubai | XShield",
        "Cockroach, bed bug, termite, rodent, bird & snake control plus deep cleaning. Free inspection.",
        "https://xshieldservices.com/service.html",
    ),
    "service-single.html": (
        "General Pest Control Dubai | XShield",
        "Professional pest & rodent control in Dubai. Licensed, safe, effective. Book a free inspection today.",
        "https://xshieldservices.com/service-single.html",
    ),
    "contact.html": (
        "Contact XShield Pest Control Dubai",
        "Office in Al Quoz, Dubai. Phone, WhatsApp, email & contact form. Available 24/7.",
        "https://xshieldservices.com/contact.html",
    ),
    "appoinment.html": (
        "Book Free Pest Inspection | XShield Dubai",
        "Request a free pest inspection online. Fast response across Dubai.",
        "https://xshieldservices.com/appoinment.html",
    ),
    "faq.html": (
        "Pest Control FAQ | XShield Dubai",
        "Common questions about pest control, safety, pricing & contracts in Dubai.",
        "https://xshieldservices.com/faq.html",
    ),
    "project.html": (
        "Recent Jobs | XShield Pest Control Dubai",
        "Examples of pest control and cleaning projects across Dubai.",
        "https://xshieldservices.com/project.html",
    ),
    "team.html": (
        "Our Team | XShield Pest Control Dubai",
        "Meet the certified technicians behind XShield's pest control & cleaning services.",
        "https://xshieldservices.com/team.html",
    ),
}


def add_seo(content: str, filename: str) -> str:
    title, desc, url = SEO[filename]
    head_extra = f"""    <meta name="description" content="{desc}">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{desc}">
    <meta property="og:url" content="{url}">
    <meta property="og:type" content="website">
    <meta property="og:site_name" content="XShield Pest Control & Cleaning Services">"""
    content = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", content, count=1)
    if 'name="description"' not in content:
        content = content.replace("<title>", head_extra + "\n    <title>", 1)
        content = content.replace(head_extra + "\n    " + head_extra, head_extra, 1)
    return content


def patch_index3(content: str) -> str:
    content = content.replace(
        "<h2>From Messy to Spotless <span>– We Make It Shine!</span></h2>",
        "<h2>To Protect and Prevent <span>— Dubai's Trusted Pest Experts</span></h2>",
    )
    content = re.sub(
        r"<div class=\"slide-description.*?</div>\s*<div class=\"slide-btns",
        """<div class="slide-description wow fadeInUp" data-wow-delay="0.1s">
                                <p>Licensed by Dubai Municipality with 10+ years of experience. We eliminate pests, protect your property, and keep spaces clean — residential, commercial, and industrial.</p>
                            </div>
                            <div class="slide-btns""",
        content,
        count=1,
        flags=re.DOTALL,
    )
    content = content.replace('class="theme-btn-s2">Book Now</a>', 'class="theme-btn-s2">Book Free Inspection</a>')
    content = content.replace('data-text="About us">About us</span>', 'data-text="About Us">About Us</span>')
    content = content.replace('<span class="odometer" data-count="40">00</span>K+', '<span class="odometer" data-count="10">00</span>+')
    content = content.replace("<p>Client’s serviced</p>", "<p>Years of Experience</p>")
    content = content.replace(
        "<h2 class=\"poort-text poort-in-right\">From Messy to Spotless – We Make\n                                            It Shine!</h2>",
        "<h2 class=\"poort-text poort-in-right\">Dubai's Licensed Pest Control &amp; Cleaning Specialists</h2>",
    )
    content = re.sub(
        r"<p>At SparkleClean.*?</p>",
        "<p>XShield Pest Control &amp; Cleaning Services delivers integrated pest management and professional cleaning across Dubai. Our trained team uses approved methods to eliminate infestations, prevent recurrence, and leave your space hygienic and safe.</p>",
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
    content = content.replace('class="theme-btn">Book Now</a>', 'class="theme-btn">Book Free Inspection</a>', 1)
    content = content.replace('<span class="odometer" data-count="25">00</span>', '<span class="odometer" data-count="10">00</span>+')
    content = content.replace('<span class="odometer" data-count="75">00</span>k', '<span class="odometer" data-count="5000">00</span>+')
    content = content.replace("<h3>Satisfied Clients</h3>", "<h3>Jobs Completed</h3>")
    content = content.replace('<span class="odometer" data-count="134">00</span>', '<span class="odometer" data-count="50">00</span>+')
    content = content.replace("<h3>Team Members</h3>", "<h3>Expert Technicians</h3>")
    content = content.replace('<span class="odometer" data-count="85">00</span>', '<span class="odometer" data-count="98">00</span>')
    content = content.replace("<h3>Customer Retention Rate</h3>", "<h3>Customer Satisfaction</h3>")
    content = content.replace(
        "<h2 class=\"poort-text poort-in-right\">Where Cleanliness meets Care Services</h2>",
        "<h2 class=\"poort-text poort-in-right\">Professional Pest Control &amp; Cleaning Services</h2>",
    )
    content = re.sub(
        r'<div class="service-slider-s2">.*?</div>\s*<div class="left-shape2">',
        '<div class="service-slider-s2">\n' + build_slider() + '\n                    </div>\n                <div class="left-shape2">',
        content,
        count=1,
        flags=re.DOTALL,
    )
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
    content = content.replace('data-text="About us">Learn More</span>', 'data-text="About Us">Learn More</span>')
    content = content.replace(
        "<h2 class=\"poort-text poort-in-right\">Need Help Fast? We’re Just One Call\n                                        Away</h2>",
        "<h2 class=\"poort-text poort-in-right\">Pest Emergency? We're Available 24/7</h2>",
    )
    content = re.sub(
        r"<p>In today's competitive business.*?</p>",
        "<p>Sudden infestation, rodents, bees, or snakes — call us any time. Our Dubai-based team responds fast with the right equipment and approved treatments.</p>",
        content,
        count=1,
        flags=re.DOTALL,
    )
    content = content.replace('href="tel:+17189044450"', 'href="tel:+97144106502"')
    content = re.sub(r'<a href="tel:\+97144106502" class="call">.*?</a>', '<a href="tel:+97144106502" class="call"><i><img src="assets/images/phone-call.svg" alt=""></i>+971 4 410 6502</a>', content, count=1, flags=re.DOTALL)
    content = content.replace(
        "<small>Consult With It Advisor? <a href=\"#\">Click Now</a></small>",
        '<small>Prefer WhatsApp? <a href="https://wa.me/971586440451">Message us now</a></small>',
    )
    content = content.replace(
        "<h2 class=\"poort-text poort-in-right\">Met Our Expert & Qualified Cleaners Team</h2>",
        "<h2 class=\"poort-text poort-in-right\">Meet Our Certified Technicians</h2>",
    )
    team = [
        ("Ahmed Hassan", "Senior Pest Technician"),
        ("Priya Menon", "Operations Manager"),
        ("Rajesh Kumar", "Termite Specialist"),
        ("Fatima Al Mansoori", "Cleaning Supervisor"),
    ]
    old_names = ["Jane Cooper", "Jenny Wilson", "Kristin Watson", "Arlene McCoy"]
    old_roles = ["Team Leader", "Junior Member", "Team Leader", "Senior Member"]
    for (n, r), on, orole in zip(team, old_names, old_roles):
        content = content.replace(f">{on}</a>", f">{n}</a>")
        content = content.replace(f"<span>{orole}</span>", f"<span>{r}</span>", 1)
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
    content = content.replace("<span>Team Leader</span>", "<span>Homeowner, Dubai</span>", 1)
    content = content.replace("Book an\n                                appointment", "Book an inspection")
    content = content.replace(
        "<h2 class=\"poort-text poort-in-right\">we’re prooffesionaly Commited\n                                to give best Cleaning services\n                                for Client’s happiness</h2>",
        "<h2 class=\"poort-text poort-in-right\">Schedule Your Free Pest Inspection Today</h2>",
    )
    content = content.replace("BOOK\n                                        APPOINTMENT", "BOOK FREE INSPECTION")
    content = content.replace("<h2>Featured by popular companies in the industry</h2>", "<h2>Trusted by Homes &amp; Businesses Across Dubai</h2>")
    content = content.replace("News &\n                                    Blogs", "Tips &amp; Advice")
    content = content.replace("<h2 class=\"poort-text poort-in-right\">Updated News & Blogs</h2>", "<h2 class=\"poort-text poort-in-right\">Pest Prevention Insights</h2>")
    content = re.sub(
        r"<p>communication and utilizes cutting edge logistic planning.*?</p>",
        "<p>Practical guidance from our Dubai technicians.</p>",
        content,
        count=1,
        flags=re.DOTALL,
    )
    tips = [
        ("Pest Prevention", "5 Signs You Have a Termite Problem"),
        ("Home Care", "How to Keep Cockroaches Out of Your Kitchen"),
        ("Commercial", "Why Regular Pest Contracts Save Money"),
    ]
    for (cat, title), old_cat in zip(tips, ["Home Cleaning", "Office Cleaning", "Desk Cleaning"]):
        content = content.replace(f'href="blog-single.html">{old_cat}</a>', f'href="faq.html">{cat}</a>', 1)
    content = re.sub(r'<h2><a href="blog-single.html">.*?</a></h2>', lambda m, t=iter(tips): f'<h2><a href="faq.html">{next(t)[1]}</a></h2>', content, count=3)
    content = content.replace('href="blog-single.html"', 'href="faq.html"')
    return content


def patch_about(content: str) -> str:
    content = content.replace("<h3>About us</h3>", "<h3>About Us</h3>")
    content = content.replace(
        "<h2 class=\"text-opacity-animation\">we believe that a clean space is\n                                            happy space. Founded in 1998, our\n                                            mission is to make homes &\n                                            businesses sparkle while...</h2>",
        "<h2 class=\"text-opacity-animation\">A cleaner, safer Dubai — one property at a time</h2>",
    )
    content = re.sub(
        r"<p class=\"wow fadeInUp\".*?>At Shiny Clean.*?</p>",
        '<p class="wow fadeInUp" data-wow-duration="1000ms">Based in Al Quoz, XShield Pest Control &amp; Cleaning Services has served Dubai for over 10 years. We are licensed and approved by Dubai Municipality, offering integrated pest management alongside deep cleaning and sanitization. Whether you need emergency rodent control or a scheduled termite inspection, our team delivers reliable results with minimal disruption.</p>',
        content,
        count=1,
        flags=re.DOTALL,
    )
    content = content.replace('<span class="odometer" data-count="40">00</span>K+', '<span class="odometer" data-count="5000">00</span>+')
    content = content.replace("<p>Client’s serviced</p>", "<p>Properties Protected</p>")
    content = content.replace("<span>Office\n                                                    Cleaning</span>", "<span>Pest Control &amp; Cleaning</span>")
    content = content.replace(
        "<h2 class=\"poort-text poort-in-right\">Your Space Deserves the Best Here’s\n                                                Why We’re\n                                                It</h2>",
        "<h2 class=\"poort-text poort-in-right\">Our Vision</h2>",
    )
    content = re.sub(
        r"<p>Our team of trained professionals takes pride.*?</p>",
        "<p><strong>Our Mission:</strong> To protect people and property by delivering fast, effective pest control and professional cleaning — with honest advice, fair pricing, and treatments that last.</p><p><strong>Our Vision:</strong> To make Dubai's homes and workplaces pest-free through prevention-first, municipality-approved practices.</p>",
        content,
        count=1,
        flags=re.DOTALL,
    )
    for old, new in [
        ("Trusted & Vetted Cleaners", "Eliminate pests at the source"),
        ("Customizable Cleaning Plans", "Prevent reinfestation through integrated plans"),
        ("Affordable & Transparent Pricing", "Maintain the highest safety and licensing standards"),
        ("Satisfaction Guarantee", "Provide 24/7 support when it matters most"),
    ]:
        content = content.replace(f"<span>{old}</span>", f"<span>{new}</span>")
    content = content.replace(
        "<h2 class=\"poort-text poort-in-right\">we’re prooffesionaly Commited\n                                        to give best Cleaning services\n                                        see how it works actually</h2>",
        "<h2 class=\"poort-text poort-in-right\">How XShield Works — Simple, Transparent, Effective</h2>",
    )
    content = content.replace("<span>Book online</span>", "<span>Free Inspection</span>")
    content = content.replace("<span>get service</span>", "<span>Custom Treatment</span>")
    content = content.replace("<span>Enjoy service</span>", "<span>Protection &amp; Follow-Up</span>")
    return content


def patch_contact(content: str) -> str:
    content = content.replace("<h3>Contact us</h3>", "<h3>Contact Us</h3>")
    content = content.replace("<h2>address line</h2>", "<h2>Our Office</h2>")
    content = content.replace(
        "<p>Bowery St, New York, 37 USA\n                                                <br> NY 10013,USA\n                                            </p>",
        "<p>Office 303, Mohammad Bin Ahmad Building,<br>Al Quoz Third, Dubai, UAE</p>",
    )
    content = content.replace("<h2>Phone Number</h2>", "<h2>Phone &amp; WhatsApp</h2>")
    content = re.sub(
        r"<p>\+1255.*?</p>",
        "<p>+971 4 410 6502<br>WhatsApp: +971 58 644 0451</p>",
        content,
        count=1,
        flags=re.DOTALL,
    )
    content = content.replace("<h2>Address</h2>", "<h2>Email</h2>")
    content = content.replace(
        "<p>contact@xshieldservices.com <br> contact@xshieldservices.com</p>",
        "<p>contact@xshieldservices.com</p>",
    )
    content = content.replace(
        "<p>Lorem ipsum dolor sit amet consectetur adipiscing elit mattis\n                                            faucibus odio feugiat arc dolor.</p>",
        "<p>Have a pest problem or need a cleaning quote? Reach us by phone, WhatsApp, or the form — we typically respond within one business hour.</p>",
    )
    content = content.replace("<h2>Fill Up The Form</h2>", "<h2>Send Us a Message</h2>")
    content = content.replace('placeholder="Enter Your Message here"', 'placeholder="How can we help you?*"')
    content = content.replace('value="Get In Touch"', 'value="Send Message"')
    content = content.replace("<div id=\"success\">Thank you</div>", "<div id=\"success\">Thank you — we'll be in touch shortly.</div>")
    content = content.replace(
        "<div id=\"error\"> Error occurred while sending email. Please try again\n                                                    later.\n                                                </div>",
        "<div id=\"error\">Something went wrong. Please call +971 4 410 6502 or WhatsApp us.</div>",
    )
    if "MAP_EMBED_PENDING" not in content:
        content = content.replace(
            '<div class="map">',
            '<!-- MAP_EMBED_PENDING: supply Google Maps embed for Office 303, Al Quoz Third -->\n                                        <div class="map">',
        )
    return content


def patch_appointment(content: str) -> str:
    content = content.replace("<h3>Appoinment</h3>", "<h3>Book an Inspection</h3>")
    return content


def patch_team(content: str) -> str:
    content = content.replace("<h3>Team page</h3>", "<h3>Our Team</h3>")
    content = content.replace(
        "<h2 class=\"poort-text poort-in-right\">Met Our Expert & Qualified Cleaners Team</h2>",
        "<h2 class=\"poort-text poort-in-right\">Skilled Technicians You Can Trust</h2>",
    )
    return content


def patch_project(content: str) -> str:
    content = content.replace("<h3>projects page</h3>", "<h3>Recent Jobs</h3>")
    jobs = [
        ("Commercial Pest Control", "Commercial Cockroach Treatment"),
        ("Termite Treatment", "Termite Barrier Installation"),
        ("Residential", "Bed Bug Treatment"),
        ("Bird Control", "Bird Spike Installation"),
        ("Deep Cleaning", "Deep Clean & Sanitize"),
        ("Rodent Control", "Rodent Proofing"),
    ]
    for (thumb, title), old in zip(jobs, ["Bedroom Cleaning", "Window Cleaning", "Kitchen Cleaning", "Office Cleaning", "Home Cleaning", "Bathroom Cleaning"]):
        content = content.replace(f"<span>{old}</span>", f"<span>{thumb}</span>", 1)
    for (_, title), old in zip(jobs, ["Residential Cleaning", "Indoor Cleaning", "Kitchen Cleaning", "Office Cleaning", "Home Cleaning", "Bathroom Cleaning"]):
        content = content.replace(f">{old}</a>", f">{title}</a>", 1)
    return content


PATCHERS = {
    "index-3.html": patch_index3,
    "about.html": patch_about,
    "contact.html": patch_contact,
    "appoinment.html": patch_appointment,
    "team.html": patch_team,
    "project.html": patch_project,
}


def main():
    for name in PATCHERS:
        path = ROOT / name
        c = path.read_text(encoding="utf-8")
        c = PATCHERS[name](c)
        c = add_seo(c, name)
        path.write_text(c, encoding="utf-8")
        print("Patched", name)
    for name in SEO:
        if name not in PATCHERS:
            path = ROOT / name
            c = path.read_text(encoding="utf-8")
            c = add_seo(c, name)
            path.write_text(c, encoding="utf-8")
            print("SEO", name)


if __name__ == "__main__":
    main()

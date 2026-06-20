#!/usr/bin/env python3
"""Patch remaining pages: service, service-single, faq, appointment, team, global fixes."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RETAINED = [
    "index-3.html", "about.html", "service.html", "service-single.html",
    "contact.html", "appoinment.html", "faq.html", "project.html", "team.html",
]

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
DURATIONS = ["1000ms", "1200ms", "1400ms", "1400ms", "1400ms", "1400ms"] * 2
SVG = 'fill="#4A9B2F"'

CTA_EMERGENCY = """<div class="wpo-section-title-s2">
                                            <span><i><img src="assets/logo/logo-mini.png" alt="XShield"></i>emergency call</span>
                                            <h2 class="poort-text poort-in-right">Pest Emergency? We're Available 24/7</h2>
                                            <p>Sudden infestation, rodents, bees, or snakes — call us any time. Our Dubai-based team responds fast with the right equipment and approved treatments.</p>
                                        </div>
                                        <a href="tel:+97144106502" class="call"><i><img src="assets/images/phone-call.svg" alt=""></i>+971 4 410 6502</a>
                                        <small>Prefer WhatsApp? <a href="https://wa.me/971586440451">Message us now</a></small>"""

CTA_FEATURES = """<div class="wpo-section-title-s2">
                                            <span><i><img src="assets/logo/logo-mini.png" alt="XShield"></i>why choose us</span>
                                            <h2 class="poort-text poort-in-right">Licensed &amp; Trusted in Dubai</h2>
                                        </div>
                                        <ul>
                                            <li>Licensed by Dubai Municipality</li>
                                            <li>24/7 Emergency Response</li>
                                            <li>10+ Years of Experience</li>
                                            <li>Free Inspection &amp; Quote</li>
                                        </ul>"""

FAQ_ACCORDION = """<div class="accordion-item">
                                                        <h3 class="accordion-header" id="headingOne">
                                                            <button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#collapseOne" aria-expanded="true" aria-controls="collapseOne">Are your treatments approved by Dubai Municipality?</button>
                                                        </h3>
                                                        <div id="collapseOne" class="accordion-collapse collapse show" aria-labelledby="headingOne" data-bs-parent="#accordionExample">
                                                            <div class="accordion-body"><p>Yes. XShield is licensed and uses municipality-approved products and methods for residential and commercial properties.</p></div>
                                                        </div>
                                                    </div>
                                                    <div class="accordion-item">
                                                        <h3 class="accordion-header" id="headingTwo">
                                                            <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapseTwo" aria-expanded="false" aria-controls="collapseTwo">Do you offer free inspections?</button>
                                                        </h3>
                                                        <div id="collapseTwo" class="accordion-collapse collapse" aria-labelledby="headingTwo" data-bs-parent="#accordionExample">
                                                            <div class="accordion-body"><p>Yes. We provide a free initial inspection and quote before any treatment begins.</p></div>
                                                        </div>
                                                    </div>
                                                    <div class="accordion-item">
                                                        <h3 class="accordion-header" id="headingThree">
                                                            <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapseThree" aria-expanded="false" aria-controls="collapseThree">How quickly can you respond to an emergency?</button>
                                                        </h3>
                                                        <div id="collapseThree" class="accordion-collapse collapse" aria-labelledby="headingThree" data-bs-parent="#accordionExample">
                                                            <div class="accordion-body"><p>We offer 24/7 emergency service across Dubai. Call or WhatsApp and we'll dispatch a team as soon as possible.</p></div>
                                                        </div>
                                                    </div>
                                                    <div class="accordion-item">
                                                        <h3 class="accordion-header" id="headingFour">
                                                            <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapseFour" aria-expanded="false" aria-controls="collapseFour">Is treatment safe for children and pets?</button>
                                                        </h3>
                                                        <div id="collapseFour" class="accordion-collapse collapse" aria-labelledby="headingFour" data-bs-parent="#accordionExample">
                                                            <div class="accordion-body"><p>We use approved products and advise on re-entry times. Tell us about children, pets, or sensitive areas during inspection.</p></div>
                                                        </div>
                                                    </div>
                                                    <div class="accordion-item">
                                                        <h3 class="accordion-header" id="headingFive">
                                                            <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapseFive" aria-expanded="false" aria-controls="collapseFive">Do you provide annual maintenance contracts?</button>
                                                        </h3>
                                                        <div id="collapseFive" class="accordion-collapse collapse" aria-labelledby="headingFive" data-bs-parent="#accordionExample">
                                                            <div class="accordion-body"><p>Yes — AMC plans for homes, restaurants, and facilities with scheduled visits and priority call-outs.</p></div>
                                                        </div>
                                                    </div>
                                                    <div class="accordion-item">
                                                        <h3 class="accordion-header" id="headingSix">
                                                            <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapseSix" aria-expanded="false" aria-controls="collapseSix">Do you also offer cleaning services?</button>
                                                        </h3>
                                                        <div id="collapseSix" class="accordion-collapse collapse" aria-labelledby="headingSix" data-bs-parent="#accordionExample">
                                                            <div class="accordion-body"><p>Yes. We provide deep cleaning, disinfection, and sofa, mattress, and carpet cleaning — often bundled after pest treatment.</p></div>
                                                        </div>
                                                    </div>"""


def card_col(title, img, duration):
    return f"""                                        <div class="col-lg-4 col-md-6 col-12">
                                            <div class="wpo-service-item wow fadeInUp" data-wow-duration="{duration}">
                                                <div class="wpo-service-img middle-light">
                                                    <img src="assets/images/service/service-{img}.jpg" alt="{title}">
                                                </div>
                                                <div class="wpo-service-text">
                                                    <div class="thumb">
                                                        <span>Free Inspection</span>
                                                        <svg xmlns="http://www.w3.org/2000/svg" width="103" height="24" viewBox="0 0 103 24" fill="none"><path d="M1.60294 8.82231C-0.492335 4.80636 2.42121 0 6.95089 0H96.7463C101.157 0 103.808 4.89398 101.399 8.5886C100.237 10.3695 100.194 12.6573 101.288 14.4805L101.462 14.7702C103.899 18.8322 100.973 24 96.2363 24H7.54361C2.65837 24 -0.551448 18.8988 1.56255 14.4947L1.69305 14.2228C2.51567 12.509 2.48228 10.5077 1.60294 8.82231Z" {SVG} /></svg>
                                                    </div>
                                                    <h2><a href="service-single.html">{title}</a></h2>
                                                    <a class="arrow" href="service-single.html"><i class="ti-arrow-top-right" aria-hidden="true"></i></a>
                                                </div>
                                            </div>
                                        </div>"""


def build_service_grid():
    rows = []
    for row_start in (0, 6):
        cols = []
        for i in range(row_start, row_start + 6):
            title, img = SERVICES[i]
            cols.append(card_col(title, img, DURATIONS[i]))
        rows.append(
            "                                <div class=\"wpo-service-slide-item\">\n"
            "                                    <div class=\"row\">\n"
            + "\n".join(cols)
            + "\n                                    </div>\n                                </div>"
        )
    return (
        '                            <div class="service-slider-s3">\n'
        + "\n".join(rows)
        + "\n                            </div>"
    )


def global_fixes(content):
    content = content.replace('<div class="wraper">\n                                    <div class="wraper">', '<div class="wraper">')
    content = content.replace(
        "XShield Pest Control & Cleaning Services by\n                                                All rights reserved.",
        "XShield Pest Control & Cleaning Services. All rights reserved.",
    )
    content = content.replace(
        "XShield Pest Control & Cleaning Services by\n                                        All rights reserved.",
        "XShield Pest Control & Cleaning Services. All rights reserved.",
    )
    content = re.sub(
        r'<div class="wpo-cta-box wow fadeInUp" data-wow-duration="1200ms">\s*<div class="wpo-section-title-s2">.*?<small>.*?</small>\s*</div>',
        f'<div class="wpo-cta-box wow fadeInUp" data-wow-duration="1200ms">\n                                        {CTA_EMERGENCY}\n                                    </div>',
        content,
        flags=re.DOTALL,
    )
    content = re.sub(
        r'<div class="wpo-cta-box features wow fadeInUp".*?<ul>.*?</ul>',
        f'<div class="wpo-cta-box features wow fadeInUp" data-wow-duration="1400ms">\n                                        {CTA_FEATURES}',
        content,
        flags=re.DOTALL,
    )
    content = re.sub(
        r'<div class="accordion" id="accordionExample">.*?</div>\s*</div>\s*</div>\s*</div>\s*</div>\s*</div>\s*</section>\s*<!-- end wpo-faq-section -->',
        f'<div class="accordion" id="accordionExample">\n                                                    {FAQ_ACCORDION}\n                                                </div>\n                                            </div>\n                                        </div>\n                                    </div>\n                                </div>\n                            </div>\n                        </div>\n                    </div>\n                </section>\n                <!-- end wpo-faq-section -->',
        content,
        count=1,
        flags=re.DOTALL,
    )
    content = content.replace("Freequently ask questions...", "Common Questions About Pest Control in Dubai")
    content = re.sub(
        r"<p>communication and utilizes cutting edge logistic planning.*?</p>",
        "<p>Answers to what our clients ask most. Can't find yours? Call +971 4 410 6502 or WhatsApp us.</p>",
        content,
        flags=re.DOTALL,
    )
    content = content.replace('class="theme-btn-s2">Book Now</a>', 'class="theme-btn-s2">Book Free Inspection</a>')
    return content


def patch_service(content):
    content = content.replace("<h3>Services</h3>", "<h3>Our Services</h3>")
    content = content.replace(
        "<h2 class=\"poort-text poort-in-right\">Where Cleanliness meets Care Services</h2>",
        "<h2 class=\"poort-text poort-in-right\">Complete Pest Control &amp; Cleaning Solutions</h2>",
    )
    content = re.sub(
        r'<div class="service-slider-s3">.*?</div>\s*</div>\s*</div>\s*<div class="left-shape2">',
        build_service_grid() + "\n                        </div>\n                    </div>\n                <div class=\"left-shape2\">",
        content,
        count=1,
        flags=re.DOTALL,
    )
    return content


def patch_service_single(content):
    content = content.replace("<h3>Service Single</h3>", "<h3>Service Detail</h3>")
    sidebar = "\n".join(
        f'                                            <li><a href="service-single.html" class="{"active" if i == 0 else ""}">{t}</a></li>'
        for i, (t, _) in enumerate(SERVICES)
    )
    content = re.sub(r'<div class="service-catagory">\s*<ul>.*?</ul>\s*</div>', f'<div class="service-catagory">\n                                        <ul>\n{sidebar}\n                                        </ul>\n                                    </div>', content, flags=re.DOTALL)
    content = content.replace(
        "<h2>Looking for\n                                            Cleaning service\n                                            Provider?</h2>",
        "<h2>Looking for pest control in Dubai?</h2>",
    )
    content = content.replace('href="tel:+871382023"', 'href="tel:+97144106502"')
    content = content.replace("<span>+(2) 871 382 023</span>", "<span>+971 4 410 6502</span>")
    body = """<h2>General Pest &amp; Rodent Control in Dubai</h2>
                                    <p>XShield Pest Control &amp; Cleaning Services provides licensed, municipality-approved pest and rodent control across Dubai. From inspection to treatment and follow-up, our integrated approach protects your home or business — because prevention is always better than cure.</p>
                                    <h3>Inspection &amp; Assessment</h3>
                                    <p>We survey your property to identify pest type, entry points, nesting areas, and risk factors — then explain findings clearly before any treatment begins.</p>
                                    <div class="video-wrap">
                                        <div class="video-img">
                                            <img src="assets/images/service-single/video.jpg" alt="">
                                            <div class="video-holder">
                                                <a href="https://www.youtube.com/embed/1Bsgv6DnTiI" class="video-btn" data-type="iframe"><i class="flaticon-play"></i></a>
                                            </div>
                                        </div>
                                        <div class="video-content">
                                            <h2>Custom Treatment Plan</h2>
                                            <p>Every property is different. We tailor treatment to your pest problem, building type, and schedule.</p>
                                            <ul>
                                                <li>Free initial inspection</li>
                                                <li>Licensed technicians</li>
                                                <li>Eco-conscious products where possible</li>
                                            </ul>
                                        </div>
                                    </div>
                                    <p>Our treatments use Dubai Municipality-approved products applied by trained technicians. We serve residential villas, apartments, offices, restaurants, warehouses, and industrial facilities across the UAE.</p>
                                    <h3 class="quate">"To Protect and Prevent — that's not just our tagline, it's how we approach every job."</h3>
                                    <div class="image-gallery">
                                        <h2>What we cover:</h2>
                                        <ul>
                                            <li><img src="assets/images/image-gallery/1.jpg" alt=""></li>
                                            <li><img src="assets/images/image-gallery/2.jpg" alt=""></li>
                                            <li><img src="assets/images/image-gallery/3.jpg" alt=""></li>
                                            <li><img src="assets/images/image-gallery/4.jpg" alt=""></li>
                                        </ul>
                                    </div>
                                    <div class="accordion">
                                        <div class="accordion-item">
                                            <button class="accordion-header">How long does treatment take?</button>
                                            <div class="accordion-content"><p>Most treatments take 1–3 hours depending on property size and pest type. We advise on re-entry times before we begin.</p></div>
                                        </div>
                                        <div class="accordion-item active">
                                            <button class="accordion-header">Is it safe for children and pets?</button>
                                            <div class="accordion-content"><p>We use approved products and provide clear guidance on ventilation and re-entry. Tell us about children, pets, or sensitive areas during inspection.</p></div>
                                        </div>
                                        <div class="accordion-item">
                                            <button class="accordion-header">Do you offer annual contracts?</button>
                                            <div class="accordion-content"><p>Yes. Our AMC plans include scheduled visits, monitoring, and priority emergency call-outs for homes and businesses.</p></div>
                                        </div>
                                        <div class="accordion-item">
                                            <button class="accordion-header">What areas do you cover?</button>
                                            <div class="accordion-content"><p>We serve all areas of Dubai and surrounding emirates. Contact us to confirm availability for your location.</p></div>
                                        </div>
                                    </div>"""
    content = re.sub(
        r'<h2>Residential Cleaning</h2>.*?<div class="accordion">.*?</div>\s*</div>\s*</div>',
        body + "\n                                </div>\n                            </div>",
        content,
        count=1,
        flags=re.DOTALL,
    )
    return content


def patch_faq(content):
    content = content.replace("<h3>Faq Page</h3>", "<h3>FAQ</h3>")
    content = content.replace("<h3>FAQ Page</h3>", "<h3>FAQ</h3>")
    return content


def patch_appointment(content):
    content = content.replace("Make An Appointment", "Request a Free Pest Inspection")
    content = re.sub(
        r'<select name="subject".*?</select>',
        '<select name="subject" class="form-control"><option disabled="disabled" selected>Choose a Service</option>'
        + "".join(f"<option>{t}</option>" for t, _ in SERVICES)
        + "</select>",
        content,
        count=1,
        flags=re.DOTALL,
    )
    content = re.sub(
        r'<select name="approx".*?</select>',
        '<select name="approx" class="form-control"><option disabled selected>Property Type</option><option>Villa</option><option>Apartment</option><option>Office</option><option>Restaurant</option><option>Warehouse</option><option>Other</option></select>',
        content,
        count=1,
        flags=re.DOTALL,
    )
    content = re.sub(
        r'<select name="bed".*?</select>',
        '<select name="bed" class="form-control"><option disabled selected>Urgency</option><option>Standard</option><option>Same-day</option><option>Emergency (24/7)</option></select>',
        content,
        count=1,
        flags=re.DOTALL,
    )
    content = re.sub(
        r'<select name="bath".*?</select>',
        '<select name="bath" class="form-control"><option disabled selected>Preferred Contact</option><option>Phone</option><option>WhatsApp</option><option>Email</option></select>',
        content,
        count=1,
        flags=re.DOTALL,
    )
    content = content.replace('placeholder="Zip Code"', 'placeholder="Area in Dubai"')
    content = content.replace('value="Submit Request"', 'value="Request Inspection"')
    return content


def patch_team(content):
    names = [
        ("Lead Technician", "Field Technician"),
        ("Termite Specialist", "Field Technician"),
        ("Cleaning Supervisor", "Operations Coordinator"),
        ("Field Technician", "Field Technician"),
        ("Field Technician", "Field Technician"),
        ("Field Technician", "Field Technician"),
        ("Field Technician", "Field Technician"),
        ("Field Technician", "Field Technician"),
    ]
    old = ["Jane Cooper", "Jenny Wilson", "Kristin Watson", "Arlene McCoy", "Aliza Anny", "David Muller", "Jenny Wilson", "Anty Rose"]
    for (role, _), on in zip(names, old):
        content = content.replace(f">{on}</a>", f">Team Member</a>", 1)
    return content


if __name__ == "__main__":
    for name in RETAINED:
        path = ROOT / name
        c = path.read_text(encoding="utf-8")
        c = global_fixes(c)
        if name == "service.html":
            c = patch_service(c)
        elif name == "service-single.html":
            c = patch_service_single(c)
        elif name == "faq.html":
            c = patch_faq(c)
        elif name == "appoinment.html":
            c = patch_appointment(c)
        elif name == "team.html":
            c = patch_team(c)
        path.write_text(c, encoding="utf-8")
        print("Done", name)

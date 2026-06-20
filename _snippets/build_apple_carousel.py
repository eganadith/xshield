#!/usr/bin/env python3
"""Generate Apple-style services carousel HTML for index.html."""
from pathlib import Path

SERVICES = [
    ("Pest Control", "General Pest & Rodent Control", "Comprehensive treatment for common household pests and rodents — includes free inspection.", "service-1.jpg"),
    ("Pest Control", "Cockroach Control", "Targeted gel and spray treatments to eliminate cockroach infestations at the source.", "service-2.jpg"),
    ("Pest Control", "Bed Bug Removal", "Heat and chemical treatments to eradicate bed bugs from mattresses and furniture.", "service-3.jpg"),
    ("Pest Control", "Termite & Wood Borer Control", "Protect wooden structures with inspection, barriers, and proven termite treatments.", "service-4.jpg"),
    ("Pest Control", "Ant Control", "Colony-level ant control for kitchens, gardens, and commercial premises.", "service-5.jpg"),
    ("Pest Control", "Mosquito & Fly Control", "Reduce breeding sites and apply safe treatments for lasting relief.", "service-1.jpg"),
    ("Pest Control", "Bee Hives Removal", "Safe, licensed removal of bee hives with minimal disruption.", "service-2.jpg"),
    ("Pest Control", "Bird Control", "Humane bird deterrents for rooftops, warehouses, and open areas.", "service-3.jpg"),
    ("Pest Control", "Snake Control", "Rapid response for snake sightings with safe capture and removal.", "service-4.jpg"),
    ("Pest Control", "Fleas, Ticks & Silverfish Control", "Treat carpets, pet areas, and storage spaces for hidden pests.", "service-5.jpg"),
    ("Cleaning", "Deep Cleaning, Disinfecting & Sanitizing", "Professional deep cleaning and disinfection for homes and offices.", "service-1.jpg"),
    ("Cleaning", "Sofa, Mattress & Carpet Cleaning", "Steam and deep-clean treatments for upholstery and fabrics.", "service-2.jpg"),
]

CARD = """                                <article class="xshield-apple-card">
                                    <p class="xshield-apple-card__label">{label}</p>
                                    <h3 class="xshield-apple-card__title"><a href="service.html">{title}</a></h3>
                                    <p class="xshield-apple-card__desc">{desc}</p>
                                    <div class="xshield-apple-card__media">
                                        <img src="assets/images/service/{img}" alt="{title}">
                                    </div>
                                    <a href="service.html" class="xshield-apple-card__plus" aria-label="Learn more about {title}"><span aria-hidden="true">+</span></a>
                                </article>
"""

cards = "\n".join(CARD.format(label=l, title=t, desc=d, img=i) for l, t, d, i in SERVICES)

SECTION = f"""                <!-- start xshield-apple-carousel -->
                <section class="xshield-apple-carousel section-padding" data-apple-carousel>
                    <div class="container">
                        <div class="xshield-apple-carousel__header">
                            <div>
                                <p class="xshield-apple-carousel__eyebrow"><img src="assets/logo/logo-mini.png" alt="XShield">Services</p>
                                <h2 class="xshield-apple-carousel__title">Professional Pest Control &amp; Cleaning Services</h2>
                            </div>
                            <div class="xshield-apple-carousel__actions">
                                <a href="service.html" class="xshield-apple-carousel__link">View all services ›</a>
                                <div class="xshield-apple-carousel__nav">
                                    <button type="button" class="xshield-apple-carousel__nav-btn" data-apple-carousel-prev aria-label="Previous services"><i class="ti-angle-left"></i></button>
                                    <button type="button" class="xshield-apple-carousel__nav-btn" data-apple-carousel-next aria-label="Next services"><i class="ti-angle-right"></i></button>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="xshield-apple-carousel__scroll-wrap">
                        <div class="xshield-apple-carousel__track">
{cards}
                        </div>
                    </div>
                </section>
                <!-- end xshield-apple-carousel -->
"""

Path(__file__).resolve().parent.parent.joinpath("_snippets", "apple-carousel-section.html").write_text(SECTION, encoding="utf-8")
print("Wrote _snippets/apple-carousel-section.html")

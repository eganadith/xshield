#!/usr/bin/env python3
"""Apply Apple-style newsletter markup to all live pages."""

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]

SUBMIT_ICON = (
    '<svg width="16" height="16" viewBox="0 0 16 16" fill="none" '
    'xmlns="http://www.w3.org/2000/svg" aria-hidden="true">'
    '<path d="M3.5 8H11M11 8L8 5M11 8L8 11" stroke="currentColor" '
    'stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>'
    '</svg>'
)

NEWSLETTER_ROOT = f"""                                        <form class="form-fild xshield-newsletter-form" action="mail-newsletter.php" method="post" novalidate>
                                            <div class="xshield-newsletter-row">
                                                <input class="fild" type="email" name="email" placeholder="Email address" required autocomplete="email">
                                                <button type="submit" class="xshield-newsletter-submit" aria-label="Subscribe to newsletter">
                                                    {SUBMIT_ICON}
                                                </button>
                                            </div>
                                            <div class="terms">
                                                <input type="checkbox" id="newsletter-terms" name="terms" value="1" class="checkbox-input" required>
                                                <label for="newsletter-terms" class="checkbox-label">
                                                    <span class="custom-checkbox" aria-hidden="true"></span>
                                                    <span class="checkbox-label__text">I agree to the terms and privacy policy</span>
                                                </label>
                                            </div>
                                            <p class="xshield-form-notice" role="status" aria-live="polite"></p>
                                        </form>"""

NEWSLETTER_INQUIRY = f"""                                        <form class="form-fild xshield-newsletter-form" action="../mail-newsletter.php" method="post" novalidate>
                                            <div class="xshield-newsletter-row">
                                                <input class="fild" type="email" name="email" placeholder="Email address" required autocomplete="email">
                                                <button type="submit" class="xshield-newsletter-submit" aria-label="Subscribe to newsletter">
                                                    {SUBMIT_ICON}
                                                </button>
                                            </div>
                                            <div class="terms">
                                                <input type="checkbox" id="newsletter-terms" name="terms" value="1" class="checkbox-input" required>
                                                <label for="newsletter-terms" class="checkbox-label">
                                                    <span class="custom-checkbox" aria-hidden="true"></span>
                                                    <span class="checkbox-label__text">I agree to the terms and privacy policy</span>
                                                </label>
                                            </div>
                                            <p class="xshield-form-notice" role="status" aria-live="polite"></p>
                                        </form>"""

NEWSLETTER_FORM = re.compile(
    r'[ \t]*<form class="form-fild xshield-newsletter-form"[^>]*>.*?</form>',
    re.DOTALL,
)


def patch_file(path: Path, newsletter_html: str) -> None:
    text = path.read_text(encoding='utf-8')
    updated, count = NEWSLETTER_FORM.subn(newsletter_html, text, count=1)
    if count:
        path.write_text(updated, encoding='utf-8')
        print(f'updated {path.relative_to(ROOT)}')


def main() -> None:
    for page in ['index.html', 'about.html', 'service.html', 'contact.html']:
        patch_file(ROOT / page, NEWSLETTER_ROOT)

    patch_file(ROOT / '_snippets/inquiry-page.template.html', NEWSLETTER_INQUIRY)

    for path in sorted((ROOT / 'inquiry').glob('*.html')):
        patch_file(path, NEWSLETTER_INQUIRY)


if __name__ == '__main__':
    main()

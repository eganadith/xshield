#!/usr/bin/env python3
"""Wire contact and newsletter forms to PHP mail handlers on live pages."""

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]

NEWSLETTER_ROOT = """                                        <form class="form-fild xshield-newsletter-form" action="mail-newsletter.php" method="post" novalidate>
                                            <input class="fild" type="email" name="email" placeholder="Enter your email address" required autocomplete="email">
                                            <button type="submit" aria-label="Subscribe to newsletter">
                                                <img src="assets/images/air-plane.svg" alt="">
                                            </button>
                                            <div class="terms">
                                                <input type="checkbox" id="newsletter-terms" name="terms" value="1" class="checkbox-input" required>
                                                <label for="newsletter-terms" class="checkbox-label">
                                                    <span class="custom-checkbox"></span>I agree to all your terms
                                                    and policies</label>
                                            </div>
                                            <p class="xshield-form-notice" role="status" aria-live="polite"></p>
                                        </form>"""

NEWSLETTER_INQUIRY = """                                        <form class="form-fild xshield-newsletter-form" action="../mail-newsletter.php" method="post" novalidate>
                                            <input class="fild" type="email" name="email" placeholder="Enter your email address" required autocomplete="email">
                                            <button type="submit" aria-label="Subscribe to newsletter">
                                                <img src="../assets/images/air-plane.svg" alt="">
                                            </button>
                                            <div class="terms">
                                                <input type="checkbox" id="newsletter-terms" name="terms" value="1" class="checkbox-input" required>
                                                <label for="newsletter-terms" class="checkbox-label"><span class="custom-checkbox"></span>I agree to all your terms and policies</label>
                                            </div>
                                            <p class="xshield-form-notice" role="status" aria-live="polite"></p>
                                        </form>"""

NEWSLETTER_OLD = re.compile(
    r'[ \t]*<form class="form-fild">\s*'
    r'<input class="fild" type="email" placeholder="Enter your email address">\s*'
    r'<button type="submit">.*?</button>\s*'
    r'<div class="terms">.*?</div>\s*'
    r'</form>',
    re.DOTALL,
)

CONTACT_FORM_OLD = (
    'class="contact-form contact-validation-active xshield-contact-form" '
    'id="contact-form" novalidate'
)
CONTACT_FORM_NEW = (
    'class="contact-form xshield-contact-form" id="contact-form" '
    'action="mail-contact.php" method="post" novalidate'
)

SCRIPT_OLD = '<script src="assets/js/script.js"></script>'
SCRIPT_NEW = (
    '<script src="assets/js/script.js"></script>\n'
    '    <script src="assets/js/xshield-forms.js"></script>'
)

INQUIRY_SCRIPT_OLD = '<script src="../assets/js/script.js"></script>'
INQUIRY_SCRIPT_NEW = (
    '<script src="../assets/js/script.js"></script>\n'
    '    <script src="../assets/js/xshield-forms.js"></script>'
)


def patch_file(path: Path, newsletter_html: str, add_forms_script: bool) -> None:
    text = path.read_text(encoding="utf-8")
    original = text

    text = NEWSLETTER_OLD.sub(newsletter_html, text, count=1)
    text = text.replace(CONTACT_FORM_OLD, CONTACT_FORM_NEW)

    if add_forms_script and 'xshield-forms.js' not in text:
        if '../assets/js/script.js' in text:
            text = text.replace(INQUIRY_SCRIPT_OLD, INQUIRY_SCRIPT_NEW, 1)
        else:
            text = text.replace(SCRIPT_OLD, SCRIPT_NEW, 1)

    text = text.replace('contact@xshieldservices.com', 'contact@xshield-services.com')

    if text != original:
        path.write_text(text, encoding="utf-8")
        print(f'updated {path.relative_to(ROOT)}')


def main() -> None:
    for page in ['index.html', 'about.html', 'service.html', 'contact.html']:
        patch_file(ROOT / page, NEWSLETTER_ROOT, add_forms_script=True)

    template = ROOT / '_snippets/inquiry-page.template.html'
    patch_file(template, NEWSLETTER_INQUIRY, add_forms_script=True)

    for path in (ROOT / 'inquiry').glob('*.html'):
        patch_file(path, NEWSLETTER_INQUIRY, add_forms_script=True)


if __name__ == '__main__':
    main()

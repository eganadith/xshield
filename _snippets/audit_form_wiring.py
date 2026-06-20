#!/usr/bin/env python3
"""Static audit: verify contact/newsletter form wiring on all live pages."""

from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
LOG_PATH = ROOT / '.cursor' / 'debug-ca5b13.log'


def log(message, data, hypothesis_id='STATIC'):
    entry = {
        'sessionId': 'ca5b13',
        'runId': 'audit',
        'hypothesisId': hypothesis_id,
        'location': 'audit_form_wiring.py',
        'message': message,
        'data': data,
        'timestamp': int(__import__('time').time() * 1000),
    }
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with LOG_PATH.open('a', encoding='utf-8') as handle:
        handle.write(json.dumps(entry) + '\n')


def audit_page(path: Path, is_inquiry: bool) -> dict:
    text = path.read_text(encoding='utf-8')
    issues = []

    if 'xshield-forms.js' not in text:
        issues.append('missing xshield-forms.js script')

    newsletter_forms = re.findall(
        r'<form[^>]*class="[^"]*xshield-newsletter-form[^"]*"[^>]*action="([^"]+)"',
        text,
    )
    if not newsletter_forms:
        issues.append('missing xshield-newsletter-form')
    else:
        expected = '../mail-newsletter.php' if is_inquiry else 'mail-newsletter.php'
        for action in newsletter_forms:
            if action != expected:
                issues.append(f'newsletter action {action!r} expected {expected!r}')

    if not is_inquiry and path.name == 'contact.html':
        if 'action="mail-contact.php"' not in text:
            issues.append('contact form missing mail-contact.php action')
        if 'contact-validation-active' in text:
            issues.append('contact-validation-active still present (script.js conflict)')

    if is_inquiry and 'action="../mail-newsletter.php"' not in text:
        issues.append('inquiry newsletter wrong action path')

    return {
        'page': str(path.relative_to(ROOT)),
        'newsletterForms': len(newsletter_forms),
        'hasFormsScript': 'xshield-forms.js' in text,
        'issues': issues,
        'ok': not issues,
    }


def main() -> int:
    pages = [
        ROOT / 'index.html',
        ROOT / 'about.html',
        ROOT / 'service.html',
        ROOT / 'contact.html',
    ]
    pages.extend(sorted((ROOT / 'inquiry').glob('*.html')))

    results = []
    for page in pages:
        is_inquiry = 'inquiry' in page.parts
        result = audit_page(page, is_inquiry)
        results.append(result)
        log('page audit', result, hypothesis_id='D' if is_inquiry else 'A')

    failed = [r for r in results if not r['ok']]
    summary = {
        'totalPages': len(results),
        'passed': len(results) - len(failed),
        'failed': len(failed),
        'failedPages': [r['page'] for r in failed],
    }
    log('audit summary', summary, hypothesis_id='A')

    print(json.dumps(summary, indent=2))
    if failed:
        for item in failed:
            print(f"FAIL {item['page']}: {', '.join(item['issues'])}")
        return 1

    print('All live pages wired correctly.')
    return 0


if __name__ == '__main__':
    sys.exit(main())

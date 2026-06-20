#!/usr/bin/env python3
"""Probe live site endpoints and log runtime evidence for email form debugging."""

from pathlib import Path
import json
import subprocess
import time

ROOT = Path(__file__).resolve().parents[1]
LOG_PATH = ROOT / '.cursor' / 'debug-ca5b13.log'
BASE = 'https://xshield-services.com'


def log(message, data, hypothesis_id='A'):
    entry = {
        'sessionId': 'ca5b13',
        'runId': 'live-probe',
        'hypothesisId': hypothesis_id,
        'location': 'probe_live_email.py',
        'message': message,
        'data': data,
        'timestamp': int(time.time() * 1000),
    }
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with LOG_PATH.open('a', encoding='utf-8') as handle:
        handle.write(json.dumps(entry) + '\n')


def curl(url, method='GET', data=None):
    cmd = ['curl', '-k', '-sS', '-w', '\n__HTTP__:%{http_code}', '-X', method, url]
    if data:
        for key, value in data.items():
            cmd.extend(['-d', f'{key}={value}'])
    if method == 'POST':
        cmd.extend(['-H', 'Accept: application/json'])
    result = subprocess.run(cmd, capture_output=True, text=True, check=False)
    body, _, status = result.stdout.rpartition('\n__HTTP__:')
    return {
        'url': url,
        'status': int(status or 0),
        'bodyPreview': body[:200],
        'isJson': body.strip().startswith('{'),
    }


def main():
    assets = {
        'xshieldFormsJs': curl(f'{BASE}/assets/js/xshield-forms.js'),
        'mailNewsletterPhp': curl(f'{BASE}/mail-newsletter.php'),
        'mailContactPhpGet': curl(f'{BASE}/mail-contact.php'),
    }

    for name, result in assets.items():
        log(f'asset probe: {name}', result, 'A' if 'Js' in name else 'B')

    contact_post = curl(
        f'{BASE}/mail-contact.php',
        'POST',
        {'name': 'Probe', 'email': 'probe@example.com', 'message': 'Runtime probe'},
    )
    log('contact POST probe', contact_post, 'C')

    newsletter_post = curl(
        f'{BASE}/mail-newsletter.php',
        'POST',
        {'email': 'probe@example.com', 'terms': '1', 'page': BASE},
    )
    log('newsletter POST probe', newsletter_post, 'B')

    contact_html = curl(f'{BASE}/contact.html')
    log(
        'contact.html markers',
        {
            'status': contact_html['status'],
            'hasXshieldFormsJs': 'xshield-forms.js' in contact_html['bodyPreview'],
            'hasMailContactAction': 'mail-contact.php' in contact_html['bodyPreview'],
            'hasValidationActive': 'contact-validation-active' in contact_html['bodyPreview'],
            'hasNewsletterHandler': 'xshield-newsletter-form' in contact_html['bodyPreview'],
        },
        'D',
    )

    print('Live probe complete. See debug log for details.')


if __name__ == '__main__':
    main()

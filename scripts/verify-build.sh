#!/usr/bin/env bash
# Fail fast if production files are missing or stale before git push / cPanel deploy.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

errors=0

check_file() {
  local path="$1"
  if [[ ! -f "$path" ]]; then
    echo "✗ Missing: $path" >&2
    errors=$((errors + 1))
  else
    echo "✓ $path"
  fi
}

echo "→ Verifying production build..."

for page in index.html about.html service.html contact.html; do
  check_file "$page"
done

for mail in mail-config.php mail-contact.php mail-newsletter.php; do
  check_file "$mail"
done

check_file "deploy/.htaccess"
check_file "robots.txt"
check_file "sitemap.xml"
check_file ".cpanel.yml"
check_file "scripts/cpanel-sync.sh"
check_file "assets/sass/style.css"
check_file "assets/js/hero-video.js"
check_file "assets/js/xshield-forms.js"
check_file "assets/images/video.mp4"
check_file "assets/images/video.webm"

inquiry_count="$(find inquiry -maxdepth 1 -name '*.html' 2>/dev/null | wc -l | tr -d ' ')"
if [[ "$inquiry_count" -lt 12 ]]; then
  echo "✗ Expected 12 inquiry pages, found $inquiry_count" >&2
  errors=$((errors + 1))
else
  echo "✓ inquiry/*.html ($inquiry_count pages)"
fi

if [[ ! -s "assets/sass/style.css" ]]; then
  echo "✗ assets/sass/style.css is empty — run ./build.sh" >&2
  errors=$((errors + 1))
fi

if ! grep -q 'application/ld+json' index.html; then
  echo "✗ index.html missing SEO schema — run ./build.sh" >&2
  errors=$((errors + 1))
fi

if [[ "$errors" -gt 0 ]]; then
  echo "" >&2
  echo "Build verification failed ($errors issue(s)). Run: ./build.sh" >&2
  exit 1
fi

echo "✓ Build verification passed — safe to commit, push, and deploy."

#!/bin/bash
# Sync production site files from repo checkout to cPanel public_html.
# Called by .cpanel.yml after git pull (DEPLOYPATH must be set).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"

if [[ -z "${DEPLOYPATH:-}" ]]; then
  echo "ERROR: DEPLOYPATH is not set." >&2
  exit 1
fi

DEPLOYPATH="${DEPLOYPATH%/}/"

require_file() {
  if [[ ! -f "$1" ]]; then
    echo "ERROR: Required file missing: $1" >&2
    echo "Run ./build.sh locally, commit built files, push, then deploy again." >&2
    exit 1
  fi
}

echo "→ XShield deploy starting"
echo "  Repo:    $ROOT"
echo "  Target:  $DEPLOYPATH"

require_file "$ROOT/deploy/.htaccess"
require_file "$ROOT/assets/sass/style.css"
require_file "$ROOT/robots.txt"
require_file "$ROOT/sitemap.xml"
require_file "$ROOT/mail-contact.php"

/bin/mkdir -p "${DEPLOYPATH}inquiry" "${DEPLOYPATH}assets"

PAGES=(index.html about.html service.html contact.html)
for page in "${PAGES[@]}"; do
  require_file "$ROOT/$page"
  /bin/cp "$ROOT/$page" "$DEPLOYPATH"
  echo "  copied $page"
done

/bin/cp "$ROOT"/inquiry/*.html "${DEPLOYPATH}inquiry/"
echo "  copied inquiry/*.html ($(ls "$ROOT"/inquiry/*.html | wc -l | tr -d ' ') files)"

/bin/cp "$ROOT/mail-config.php" "$ROOT/mail-contact.php" "$ROOT/mail-newsletter.php" "$DEPLOYPATH"
echo "  copied mail-*.php"

/bin/cp "$ROOT/deploy/.htaccess" "${DEPLOYPATH}.htaccess"
echo "  copied .htaccess"

/bin/cp "$ROOT/robots.txt" "$ROOT/sitemap.xml" "$DEPLOYPATH"
echo "  copied robots.txt + sitemap.xml"

if command -v rsync >/dev/null 2>&1; then
  rsync -a --delete \
    --exclude '*.scss' \
    --exclude 'style.css.map' \
    "$ROOT/assets/" "${DEPLOYPATH}assets/"
  echo "  synced assets/ (rsync)"
else
  /bin/rm -rf "${DEPLOYPATH}assets"
  /bin/mkdir -p "${DEPLOYPATH}assets"
  /bin/cp -R "$ROOT/assets/." "${DEPLOYPATH}assets/"
  /usr/bin/find "${DEPLOYPATH}assets" -name '*.scss' -delete 2>/dev/null || true
  /usr/bin/find "${DEPLOYPATH}assets" -name 'style.css.map' -delete 2>/dev/null || true
  echo "  synced assets/ (cp)"
fi

echo "✓ Deploy complete → $DEPLOYPATH"
echo "  Live: https://xshield-services.com"

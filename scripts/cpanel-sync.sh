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

echo "→ Deploying XShield site to ${DEPLOYPATH}"

/bin/mkdir -p "${DEPLOYPATH}inquiry" "${DEPLOYPATH}assets"

PAGES=(index.html about.html service.html contact.html)
for page in "${PAGES[@]}"; do
  /bin/cp "$ROOT/$page" "$DEPLOYPATH"
done

/bin/cp "$ROOT"/inquiry/*.html "${DEPLOYPATH}inquiry/"
/bin/cp "$ROOT/mail-config.php" "$ROOT/mail-contact.php" "$ROOT/mail-newsletter.php" "$DEPLOYPATH"
/bin/cp "$ROOT/deploy/.htaccess" "${DEPLOYPATH}.htaccess"
/bin/cp "$ROOT/robots.txt" "$ROOT/sitemap.xml" "$DEPLOYPATH"

if command -v rsync >/dev/null 2>&1; then
  rsync -a --delete \
    --exclude '*.scss' \
    --exclude 'style.css.map' \
    "$ROOT/assets/" "${DEPLOYPATH}assets/"
else
  /bin/rm -rf "${DEPLOYPATH}assets"
  /bin/mkdir -p "${DEPLOYPATH}assets"
  /bin/cp -R "$ROOT/assets/." "${DEPLOYPATH}assets/"
  /usr/bin/find "${DEPLOYPATH}assets" -name '*.scss' -delete 2>/dev/null || true
  /usr/bin/find "${DEPLOYPATH}assets" -name 'style.css.map' -delete 2>/dev/null || true
fi

echo "✓ Deployed to ${DEPLOYPATH}"

#!/usr/bin/env bash
# Optional: build + create xshield-cpanel-deploy.zip for manual File Manager upload.
# For Git deploy, use ./build.sh then push (see deploy/README-DEPLOY.txt).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
STAGING="$ROOT/deploy/staging"
ZIP_NAME="xshield-cpanel-deploy.zip"
ZIP_PATH="$ROOT/$ZIP_NAME"

"$ROOT/build.sh"

echo "→ Preparing staging folder..."
rm -rf "$STAGING"
mkdir -p "$STAGING/assets/sass"
mkdir -p "$STAGING/inquiry"

PAGES=(index.html about.html service.html contact.html)
for page in "${PAGES[@]}"; do
  cp "$ROOT/$page" "$STAGING/"
done

cp -R "$ROOT/inquiry/"*.html "$STAGING/inquiry/"
cp "$ROOT/mail-config.php" "$STAGING/"
cp "$ROOT/mail-contact.php" "$STAGING/"
cp "$ROOT/mail-newsletter.php" "$STAGING/"
cp "$ROOT/deploy/.htaccess" "$STAGING/"
cp "$ROOT/robots.txt" "$ROOT/sitemap.xml" "$STAGING/"
cp "$ROOT/deploy/README-DEPLOY.txt" "$STAGING/"

echo "→ Copying assets (excluding dev files)..."
rsync -a \
  --exclude '*.scss' \
  --exclude 'style.css.map' \
  "$ROOT/assets/" "$STAGING/assets/"

mkdir -p "$STAGING/assets/sass"
cp "$ROOT/assets/sass/style.css" "$STAGING/assets/sass/style.css"

echo "→ Creating zip..."
rm -f "$ZIP_PATH"
(
  cd "$STAGING"
  zip -r -q "$ZIP_PATH" . -x "*.DS_Store"
)

SIZE="$(du -h "$ZIP_PATH" | cut -f1)"
echo "✓ Done: $ZIP_PATH ($SIZE)"
echo "  Optional manual upload — Git deploy: ./build.sh && git push"

#!/usr/bin/env bash
# Compile assets before commit/push. cPanel Git deploy copies built files to public_html.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

echo "→ Compiling SCSS..."
npx sass assets/sass/style.scss assets/sass/style.css --style=compressed

echo "→ Generating inquiry pages..."
python3 "$ROOT/build-inquiry-pages.py"

echo "→ Applying SEO (meta, schema, sitemap)..."
python3 "$ROOT/build-seo.py"

echo "→ Verifying production files..."
/bin/bash "$ROOT/scripts/verify-build.sh"

echo "✓ Build complete."
echo ""
echo "  Next:"
echo "    git add -A && git commit -m \"Deploy update\" && git push origin main"
echo "    cPanel → Git Version Control → Update from Remote → Deploy HEAD Commit"

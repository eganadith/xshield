#!/usr/bin/env bash
# Compile assets before commit/push. cPanel Git deploy copies built files to public_html.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

echo "→ Compiling SCSS..."
npx sass assets/sass/style.scss assets/sass/style.css --style=compressed

echo "→ Generating inquiry pages..."
python3 "$ROOT/build-inquiry-pages.py"

echo "✓ Build complete."
echo "  Next: git add -A && git commit && git push"
echo "  Then: cPanel → Git Version Control → Pull/Deploy"

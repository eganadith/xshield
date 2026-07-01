#!/usr/bin/env bash
# Restore full homepage: index-live.html → index.html
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if [[ ! -f index-live.html ]]; then
  echo "ERROR: index-live.html not found. Cannot restore live homepage." >&2
  exit 1
fi

cp index-live.html index.html
echo "✓ Live homepage restored from index-live.html"
echo "  Run ./build.sh to refresh SEO, then commit and deploy."

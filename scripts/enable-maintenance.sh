#!/usr/bin/env bash
# Enable maintenance mode: index.html → maintenance page (keeps index-live.html as backup).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if [[ ! -f index-live.html ]]; then
  if grep -q 'xshield-maintenance-page' index.html 2>/dev/null; then
    echo "Already in maintenance mode."
    exit 0
  fi
  echo "Saving current homepage → index-live.html"
  cp index.html index-live.html
fi

if [[ -f index-maintenance.html ]]; then
  cp index-maintenance.html index.html
else
  echo "ERROR: index-maintenance.html not found. Maintenance page is already in index.html or restore from git." >&2
  exit 1
fi

echo "✓ Maintenance mode enabled (index.html)"
echo "  Deploy, then restore with: ./scripts/restore-live.sh"

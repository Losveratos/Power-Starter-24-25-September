#!/usr/bin/env bash
# Holt die Claude-Skills aus der Daten-WG Knowledge Kitchen in dieses Repo.
# Quelle der Wahrheit bleibt die Kitchen – hier nichts in .claude/skills/ direkt ändern,
# sondern dort ändern und dieses Skript erneut laufen lassen.
#
# Aufruf (aus dem Repo-Root):
#   tools/sync_kitchen_skills.sh                      # klont die Kitchen von GitHub (main)
#   tools/sync_kitchen_skills.sh ../PowerBI-Kitchen-  # nimmt einen lokalen Klon
set -euo pipefail

SKILLS=(chartkitchen-report deploy-to-powerbi mockup-to-powerbi pnl-report powerbi-design-framework vega-charts)
ROOT="$(cd "$(dirname "$0")/.." && pwd)"

if [[ $# -ge 1 ]]; then
  SRC="$(cd "$1" && pwd)"
else
  TMP="$(mktemp -d)"
  trap 'rm -rf "$TMP"' EXIT
  git clone --quiet --depth 1 --filter=blob:none --sparse https://github.com/Losveratos/PowerBI-Kitchen-.git "$TMP/kitchen"
  git -C "$TMP/kitchen" sparse-checkout set .claude/skills
  SRC="$TMP/kitchen"
fi

for s in "${SKILLS[@]}"; do
  rm -rf "$ROOT/.claude/skills/$s"
  cp -R "$SRC/.claude/skills/$s" "$ROOT/.claude/skills/$s"
  find "$ROOT/.claude/skills/$s" -name '__pycache__' -type d -prune -exec rm -rf {} +
  echo "✓ $s"
done
echo "Stand Kitchen: $(git -C "$SRC" log -1 --format='%h %cs' 2>/dev/null || echo unbekannt)"

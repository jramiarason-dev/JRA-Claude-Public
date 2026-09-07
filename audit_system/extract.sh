#!/usr/bin/env bash
#
# Package AuditIQ as a self-contained archive for review or for a Snowflake
# stage. Run from anywhere:  audit_system/extract.sh [--snowflake] [outdir]
#
#   (default)     everything needed to run, test and review the app
#   --snowflake   only the files that belong on a Snowflake stage
#
# Writes auditiq-<mode>-<date>.zip and prints its path, size and SHA-256.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

MODE="review"
if [[ "${1:-}" == "--snowflake" ]]; then
  MODE="snowflake"
  shift
fi
OUTDIR="$(cd "${1:-$PWD}" && pwd)"

# The app itself. Nothing here imports anything from outside this directory.
APP_FILES=(
  app.py theme.py data.py generators.py base_agent.py
  agent1_regulatory.py agent2_audit_plan.py agent3_report.py
  environment.yml
)
REVIEW_EXTRA=(
  main.py requirements.txt README.md SNOWFLAKE.md .env.example
  .streamlit/config.toml
  tests/__init__.py tests/test_app_smoke.py
  tests/test_data_integrity.py tests/test_model_config.py
)

STAMP="$(date +%Y%m%d)"
NAME="auditiq-${MODE}-${STAMP}"
STAGING="$(mktemp -d)"
trap 'rm -rf "$STAGING"' EXIT
DEST="$STAGING/$NAME"

copy() {
  local rel="$1"
  [[ -e "$HERE/$rel" ]] || { echo "missing: $rel" >&2; exit 1; }
  mkdir -p "$DEST/$(dirname "$rel")"
  cp "$HERE/$rel" "$DEST/$rel"
}

for f in "${APP_FILES[@]}"; do copy "$f"; done
if [[ "$MODE" == "review" ]]; then
  for f in "${REVIEW_EXTRA[@]}"; do copy "$f"; done
fi

# Never ship a real secret, a cache, or a generated report.
find "$DEST" \( -name '__pycache__' -o -name '*.pyc' -o -name '.env' \
     -o -name 'secrets.toml' -o -name 'outputs' \) -prune -exec rm -rf {} + 2>/dev/null || true

ARCHIVE="$OUTDIR/$NAME.zip"
rm -f "$ARCHIVE"
(cd "$STAGING" && zip -qr "$ARCHIVE" "$NAME")

echo "archive : $ARCHIVE"
echo "size    : $(du -h "$ARCHIVE" | cut -f1)"
echo "sha256  : $(sha256sum "$ARCHIVE" | cut -d' ' -f1)"
echo "files   : $(cd "$STAGING" && find "$NAME" -type f | wc -l)"

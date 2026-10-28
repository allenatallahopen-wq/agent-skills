#!/usr/bin/env bash
set -euo pipefail
EVIDENCE="${1:?usage: 07-summarize-evidence.sh evidence.json}"
REA="npx -y rea-agents@6.7.0"
$REA export-evidence-bundle "$EVIDENCE" --out evidence.bundle || true
jq -c '{source:{kind:"inline",evidence:.},view:{kind:"summary"}}' "$EVIDENCE" > view.in.json
$REA inspect-analysis-view view.in.json --format json > evidence.summary.json
ls -lh evidence.bundle evidence.summary.json 2>/dev/null || true

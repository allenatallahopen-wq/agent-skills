#!/usr/bin/env bash
set -euo pipefail
ASAR="${1:?usage: 05-triage-electron.sh /path/to/app.asar}"
EXE="${2:-}"
REA="npx -y rea-agents@6.7.0"
$REA analyze-javascript-application "$ASAR" --format json > graph.json
jq -c '{source:{kind:"inline",evidence:.},view:{kind:"summary"}}' graph.json > graph.view.json
$REA inspect-analysis-view graph.view.json --format json > graph.summary.json
ls -lh graph.json graph.summary.json
[ -n "$EXE" ] && $REA inspect-electron-fuses "$EXE" --format json > fuses.json || true
jq -r '.. | strings? // empty' graph.summary.json 2>/dev/null \
  | grep -Ei 'premium|licen|entitle|subscri|feature.?flag|paywall' | sort -u | head -40 || true

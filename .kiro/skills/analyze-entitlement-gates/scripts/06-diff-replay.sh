#!/usr/bin/env bash
set -euo pipefail
# RUNTIME: this runs the target twice. Only run if assets/scope.json permits runtime
# side effects, and after confirming the exact action with the operator.
T="${1:?target}"; S1="${2:?closed scenario}"; S2="${3:-$2}"
REA="npx -y rea-agents@6.7.0"
$REA capture-process-scenario "$T" --scenario "$S1" --format json > cap.closed.json
$REA capture-process-scenario "$T" --scenario "$S2" --format json > cap.open.json
diff <(jq -S . cap.closed.json) <(jq -S . cap.open.json) | head -200

# browser variant:
# $REA capture-browser-scenario "$URL" --scenario closed.json --format json > cap.closed.json
# $REA capture-browser-scenario "$URL" --scenario open.json   --format json > cap.open.json

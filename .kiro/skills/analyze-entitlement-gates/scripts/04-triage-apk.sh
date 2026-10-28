#!/usr/bin/env bash
set -euo pipefail
APK="${1:?usage: 04-triage-apk.sh app.apk}"
REA="npx -y rea-agents@6.7.0"
$REA inspect-android-package "$APK" --format json > apk.package.json
$REA inspect-apk-signature   "$APK" --format json > apk.signature.json || true
jq -r '.manifest.package? // .package? // empty' apk.package.json 2>/dev/null || true
jq -r '.. | strings? // empty' apk.package.json 2>/dev/null \
  | grep -Ei 'billing|purchase|premium|subscription|entitle' | sort -u | head -40 || true
echo "next: jadx the predicate. Device replay only if scope.json permits runtime side effects."

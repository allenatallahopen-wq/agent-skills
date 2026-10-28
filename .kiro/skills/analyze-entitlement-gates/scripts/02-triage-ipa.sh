#!/usr/bin/env bash
set -euo pipefail
IPA="${1:?usage: 02-triage-ipa.sh MyApp.ipa}"
OUT="${IPA%.ipa}_unpacked"; rm -rf "$OUT"; mkdir -p "$OUT"
unzip -q "$IPA" -d "$OUT"
APP="$(find "$OUT/Payload" -maxdepth 1 -name '*.app' -print -quit)"
[ -n "$APP" ] || { echo "no Payload/*.app in $IPA"; exit 1; }
echo "== bundle: $APP"
/usr/libexec/PlistBuddy -c 'Print :CFBundleIdentifier' \
  -c 'Print :CFBundleShortVersionString' -c 'Print :CFBundleExecutable' \
  "$APP/Info.plist" 2>/dev/null || plutil -p "$APP/Info.plist" | head -40
BIN="$(/usr/libexec/PlistBuddy -c 'Print :CFBundleExecutable' "$APP/Info.plist" 2>/dev/null || true)"
[ -n "${BIN:-}" ] && shasum -a 256 "$APP/$BIN" | tee "$OUT/.BIN_SHA256"
echo "== frameworks"; ls -1 "$APP/Frameworks" 2>/dev/null | head -40 || true
echo "== hybrid/flutter markers"
ls -d "$APP"/www "$APP"/main.jsbundle "$APP"/Frameworks/App.framework \
      "$APP"/Frameworks/flutter_assets 2>/dev/null || echo "(none)"
echo "== entitlements"; codesign -d --entitlements :- "$APP" 2>/dev/null | head -40 || true
echo "$APP" > "$OUT/.APP_PATH"; echo "unpacked: $OUT"
# Read-only triage. Record the SHA-256 in assets/scope.json before deeper work.

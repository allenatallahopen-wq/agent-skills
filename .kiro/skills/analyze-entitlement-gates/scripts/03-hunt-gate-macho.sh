#!/usr/bin/env bash
set -euo pipefail
OUT="${1:?usage: 03-hunt-gate-macho.sh <unpacked dir>}"
APP="$(cat "$OUT/.APP_PATH")"
BIN="$(/usr/libexec/PlistBuddy -c 'Print :CFBundleExecutable' "$APP/Info.plist")"
EXE="$APP/$BIN"
REA="npx -y rea-agents@6.7.0"
PAT='premium|pro|plus|paid|unlock|upgrade|subscri|entitle|receipt|licen|purchase|restore|isPro|hasAccess|paywall|trial'

echo "== overview"; $REA binary-overview "$EXE" --format json > "$OUT/overview.json" || true
echo "== strings (all patterns)"; $REA search-strings "$EXE" --query "$PAT" --format json \
  > "$OUT/strings_gate.json" || true
echo "== objc/symbol leads"
( nm -gU "$EXE" 2>/dev/null; otool -Iv "$EXE" 2>/dev/null | grep -Eo '[-+]\[[^]]+\]' ) \
  | grep -Ei 'pro|premium|entitle|receipt|purchase|licen|subscri' | sort -u | head -80 || true
echo
echo "next: $REA xrefs \"$EXE\" <string-address>"
echo "      $REA decompile \"$EXE\" <addr> --provider ghidra --format json"
# All read-only. No target execution here.

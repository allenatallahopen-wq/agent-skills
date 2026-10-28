#!/usr/bin/env bash
set -euo pipefail
node -e 'const v=process.versions.node.split(".").map(Number);
 const ok=(v[0]===22&&v[1]>=19)||(v[0]===24&&v[1]>=11)||v[0]>=26;
 if(!ok){console.error("Need Node 22.19+/24.11+/26+, got",process.versions.node);process.exit(1)}'
command -v npx >/dev/null || { echo "npx missing"; exit 1; }
command -v ps  >/dev/null || echo "warn: procps 'ps' missing (Linux requirement)"
hermes plugins install rea
hermes plugins enable rea
# Do NOT run `rea setup` / `hermes mcp add rea` — it would shadow the plugin pin.
rea --version || npx -y rea-agents@6.7.0 --version

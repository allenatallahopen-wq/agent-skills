#!/usr/bin/env bash
set -euo pipefail
npx -y rea-agents@6.7.0 --version
npx -y rea-agents@6.7.0 doctor || true
# Expected on a clean box: hopper/ghidra/ida/jadx/kuna = missing_analysis_engine.
# JS + .NET static analysis works regardless.

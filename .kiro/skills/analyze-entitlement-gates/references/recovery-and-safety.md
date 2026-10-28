# Recovery, retries, safety, law

## Retry ladder
- Dropped MCP connection → retry **once**, only if safe to repeat. If it may have
  already changed the target, or it fails again → tell the operator to restart.
- Startup failure returning the same unchanged result → do not retry; run `rea doctor`.
- Host timeout with no REA result → do not repeat the unchanged call.
- Distinct causes, distinct remedies: client approval ≠ PATH ≠ registration ≠ engine.
- `cleanup_incomplete`, retryable capacity limits, `configuration_invalid` → follow the
  recovery ladder before asking for a restart.

## Engine/env pointers (set where REA starts, not in your shell)
- `GHIDRA_INSTALL_DIR`, `IDA`/Hopper per provider docs
- `REA_TSHARK_COMMAND`, `REA_SIGROK_COMMAND`, `REA_WABT_BIN_DIRECTORY`,
  `REA_PWNTOOLS_PYTHON`
- `REA_CAPTURE_DECODER_OLD_GENERATION_MIB`
- `REA_MCP_INPUT_SCHEMA_PROFILE=compact`, `REA_MCP_OUTPUT_SCHEMA_PROFILE=off`
- Shell exports in your terminal do not reach the MCP server; put them in
  `~/.hermes/.env` or the plugin's `mcp.json` env.
- Linux also needs procps `ps`; `node:24-slim` lacks it.

## Sandboxing
- Untrusted targets → throwaway VM/container with its own `HOME`.
- `rea setup` / `rea update` rewrite agent configs (they leave backups); prefer the
  plugin's registration over setup in Hermes.
- `execute_rizin_command` / `cutter_command` accept arbitrary Rizin commands — they can
  execute code, write files, reach the network. Confirm before running them.
- No telemetry: analysis runs locally; the one documented outbound path is a capture
  fetching source maps for the page you name.

## Scope and law
This skill studies how a shipped feature is gated so you can understand or rebuild your
own software, do interoperability research, or run an authorized assessment. It is not
a licence to redistribute patched builds or bypass payment in production. Keep the
scope declaration (`assets/scope.json`) honest; if the target isn't yours and you don't
have written authorization, stop at step 0.

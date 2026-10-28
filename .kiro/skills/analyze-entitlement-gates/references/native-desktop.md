# Native desktop binaries

Engines are yours to supply: Ghidra + JDK, Hopper, IDA. REA never installs them;
`rea doctor` prints `missing_analysis_engine` per engine, and JavaScript/.NET analysis
still works without them.

- **Session economics**: each CLI command imports the binary into a temp Ghidra project
  and deletes it. Use `--snapshot` or the MCP server to keep the session hot.
- **Linux arm64 + Ghidra**: the official ZIP has no arm64 native decompiler. Build with
  `support/gradle/gradlew buildNatives`, set `GHIDRA_INSTALL_DIR`, confirm with
  `rea doctor`.
- **Stripped binaries**: `binary_overview` for build/arch/entropy; `search_strings` →
  `xrefs` to land in the function; `procedure_pseudo_code` to confirm the branch;
  `get_call_graph` to find the deciding caller.
- **.NET**: `inspect_managed_artifact` — metadata + CIL without loading or running.
  Hunt `License`, `Trial`, `Expired`, `Validate`, `IsRegistered`.
- **Patching a copy** (never the original, only within scope, never for redistribution):
  locate the conditional jump, invert it, keep the original byte hash for the report.
  State that a patched copy diverges from the vendor build.
- **Crash triage as recon**: `inspect_recorded_crash` places the PC;
  `inspect_binary_layout` maps the core; walk back to the caller.

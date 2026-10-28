# Target routing

Pick the first tool from what the operator *supplied*, not from what you hope.

| Supplied | First | Then |
|---|---|---|
| `.ipa`, `.app`, Mach-O, `.dylib` | `open_binary` (archive inventory, `detail: "summary"`) | `binary_overview` → `search_strings` → `xrefs` → `analyze_function` |
| `.apk`, `.aab`, ZIP of one | `inspect_android_package` | `inspect_apk_signature` → Android tools / JADX |
| `app.asar`, extracted JS tree | `analyze_javascript_application` | `inspect_electron_fuses` → `trace_application_feature` → `capture_electron_scenario` |
| Live Electron app | `list_electron_targets` | check fuses before any `--inspect`: disabled `EnableNodeCliInspectArguments` means `--inspect` is ignored |
| Live browser page | `list_browser_targets` | `capture_browser_scenario` with declared actions, `inspect_web_page` |
| JS served by a site | `analyze_web_bundle` | source maps, then graph |
| HAR / SAZ / qlog / native capture | `inspect_web_network_capture` | `detail: "summary"`, then selected record ordinals |
| PCAP | `inspect_packet_fields` → `inspect_packet_capture` | `inspect_pcap_capture` for DNS/SNI summaries |
| .NET assembly (PE/CLI) | `inspect_managed_artifact` | metadata + CIL, no load, no execution |
| .NET NativeAOT | native route: `open_binary` + Ghidra | optional metadata recovery |
| ELF/PE, Go | `inspect_go_binary` (no engine) | native decompile for logic |
| ELF/PE, Rust | `inspect_rust_binary` | `cargo-auditable` deps, then decompile |
| Flutter | Flutter/Dart AOT reader | `libapp.so` facts, then symbols |
| WASM | `inspect_wasm_artifact` (WABT) | WAT + JS glue |
| Firmware | `inspect_firmware_regions` | `extract_firmware` to a new absolute dir |
| Unity | `inspect_il2cpp_metadata` | `global-metadata.dat` names/owners/literals |
| Core dump | `inspect_recorded_crash` | `inspect_binary_layout` to place the PC |
| SQLite / plist / resources | relevant reader; `open_bundle_resources` for Apple plists/IB/asset catalogs | — |
| EVM bytecode | `inspect_evm_interface` | selectors are inferred candidates |
| model files (GGUF/safetensors) | `inspect_model_artifact` | `hash: "full"` only if identity matters |

Rules:
- `open_binary` is only for active-target native/archive work.
- Start with `detail: "summary"` whenever an inventory may be large.
- Resource sessions (plists, asset catalogs) have no executable digest — use
  `open_binary` when you need native code.

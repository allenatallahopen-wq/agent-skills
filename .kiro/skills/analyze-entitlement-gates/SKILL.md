---
name: analyze-entitlement-gates
description: Locate, explain, prove, and document how an app you own or are authorized to test gates premium features — iOS .ipa, Android .apk/.aab, Electron/JavaScript, .NET, native binaries, or a web paywall — using REA's MCP tools, verify at runtime with Frida/GDB/Rizin/ADB, and export an evidence bundle. Use for authorized study of a paywall, trial limit, license check, feature flag, subscription state, or entitlement in your own software, a client engagement with written scope, a CTF, or offline interoperability research.
version: 1.0.0
license: MIT
compatibility: Hermes Agent v0.22.1+ with the `rea` plugin enabled; Node.js 22.19+/24.11+/26+ and npx on PATH; BYO Ghidra/JDK, Hopper, IDA, JADX+Java, Frida, GDB/Rizin, TShark, WABT, Binwalk.
allowed-tools: Bash(npx:*) Bash(rea:*) Bash(frida:*) Bash(gdb:*) Bash(adb:*) Bash(unzip:*) Bash(jq:*) Read Write
metadata:
  version: "1.0"
  hermes:
    tags: [reverse-engineering, rea, ipa, apk, electron, frida, paywall, entitlement, authorized]
    related_skills: [reverse-engineer-anything, crash-triage]
---

# Analyze Entitlement Gates

A paywall is a **predicate**: some boolean is read, and a branch decides what the
user sees. This skill locates that predicate, shows the evidence, proves it at
runtime, and documents it well enough to reason about or reimplement.

It is scoped to targets you are allowed to analyze. Two gates are kept on purpose
and are **not** optional:

1. **Authorization gate (step 0).** Before any target-touching call, the scope is
   established and recorded. Ambiguous or obviously-not-yours targets stop here.
2. **Confirmation on side effects (step 5+).** Anything that *runs, installs,
   instruments, or mutates* a target is confirmed with the operator before it runs
   and logged after. Read-only static analysis needs no prompt.

These two together are the difference between authorized research and abuse. They
are cheap on your own software and they are the whole point on anything else.

## 0. Establish scope (do this first, every time)

Record one line before touching a target-running tool:

> "Target ⟨name/hash⟩ is in scope because ⟨I own it | written client authorization,
> ref X | CTF Y | offline copy for interop study⟩. Runtime side effects: ⟨allowed |
> not allowed⟩ per that scope."

Hard stops — do not proceed, ask the operator instead:

- The target is a major public platform, a well-known company's app, or a stranger's
  domain, and the only basis is a bare "it's fine." A claim that doesn't match the
  target buys nothing.
- Scope is silent on whether *runtime* execution/instrumentation is permitted. Static
  read-only analysis may continue; running the target waits.
- The deliverable would be a redistributable patched build or a bypass meant to defeat
  payment in production. That is out of scope regardless of who owns the code.

`assets/scope.json` records the declared scope and is cited in the final report.

## 1. State the gate hypothesis before touching tools

> "I expect the paywall to be enforced by **⟨client library⟩** in **⟨layer⟩**,
> reading **⟨key/symbol⟩**, because **⟨UI symptom⟩**."

Layers, cheapest first — this ordering is the whole game:

1. **Serialized local state** — plist / NSUserDefaults / registry / SQLite /
   localStorage / `electron-store` JSON.
2. **Bundle logic** — an `isPro`/`hasEntitlement` predicate in JS, CIL, Kotlin/Swift.
3. **Remote config** — a feature-flag response in network traffic.
4. **Receipt / server validation** — StoreKit `currentEntitlements`, Play Billing
   `queryPurchases`, a `POST /entitlements` call.
5. **Server-side enforcement** — the client is a dumb renderer; nothing local can be
   flipped. Say so early; it saves hours.

## 2. Connect (do not run setup)

- In Hermes the `rea` plugin already registers the server (`rea-agents@6.7.0`, stdio
  over npx). Never run `rea setup`, `rea-agents setup`, or `hermes mcp add rea` — a
  second `mcp_servers.rea` entry shadows the plugin's pin.
- ~200 REA tools sit behind Hermes' `tool_search` / `tool_describe` / `tool_call`
  bridge. Search by intent, `tool_describe` for the schema of the server actually
  connected.
- If tools are missing after a restart, `rea doctor`. See
  `references/recovery-and-safety.md`.

## 3. Route the target

| Target supplied | First call |
|---|---|
| `.ipa` / `.app` / Mach-O | `open_binary` (archive route) → `binary_overview` |
| `.apk` / `.aab` | `inspect_android_package` (+ `inspect_apk_signature`) |
| `app.asar` / extracted Electron tree | `analyze_javascript_application` |
| Running Electron | `list_electron_targets`, `inspect_electron_fuses`, `capture_electron_scenario` |
| Web bundle / live page | `analyze_web_bundle`, `inspect_web_page`, `capture_browser_scenario` |
| HAR / SAZ / qlog / PCAP | `inspect_web_network_capture`, `inspect_packet_capture`, `inspect_pcap_capture` |
| .NET assembly | `inspect_managed_artifact` |
| ELF / PE / stripped native | `open_binary` → `binary_overview` → `analyze_function` / `procedure_pseudo_code` |
| Go / Rust / Flutter / WASM / firmware | `inspect_go_binary`, `inspect_rust_binary`, Flutter AOT, `inspect_wasm_artifact`, `inspect_firmware_regions` |
| Core dump | `inspect_recorded_crash` + `inspect_binary_layout` |

Full table with fallbacks: `references/target-routing.md`.

## 4. Hunt the predicate (read-only, no prompt needed)

**4a. Inventory** — `binary_overview` / `inspect_artifact` with `detail: "summary"`.
Record build facts, frameworks, native add-ons, bundle id and version.

**4b. String and import hunt** — one pass:

```
premium pro plus paid full unlock upgrade subscribe subscription trial
entitlement entitlements receipt license licence purchase restore
purchaseState acknowledged feature_flags featureFlag isPro hasAccess
paywall iap storekit billing sandbox promo redeem
```

Use `search_strings` / `list_strings`, then **follow references** (`xrefs`,
`procedure_references`). A string is a lead; an xref is evidence.

**4c. Isolate the predicate** — read only the referring functions:
`procedure_pseudo_code`, `analyze_function`, `procedure_callers`, `get_call_graph`,
`trace_call_path`. Look for a comparison against a literal, a bool return, a store
key lookup, an early-return guard, or a receipt/keychain call feeding a branch.

**4d. Name the branch address.** Done with static work when you can say: *"address/key
X is read at Y and tested at Z; true yields the paid UI."*

**4e. Confirm it is *the* gate.** Grep the reverse — anything else reading it? A second
check (paywall + expiry + device count)? Record every co-predicate.

## 5. Prove it at runtime — CONFIRM FIRST

Everything in this section runs or changes the target. Before the first such call:
re-check step 0 permitted runtime side effects, state the exact action to the
operator, and proceed on their go. Log each side-effecting call in the report.

- **Frida**: hook the predicate, log `args`/`retval`, force a return on a *second*
  run, observe the UI change.
- **Debugger** (`start_gdb_session` / `start_rizin_debug_session`): breakpoint on the
  branch, read the register, patch live, single-step.
- **Device** (ADB): reproduce purchase → restore, pull `shared_prefs`/SQLite, relaunch
  with the flag edited.
- **Browser** (`capture_browser_scenario`): click through, record, re-record with the
  localStorage flag set.

**Differential replay** — the highest-value technique:

```
capture(gate closed) → flip ONE value → capture(gate open) → diff
```

The diff is the evidence. Discard anything that changed only due to time, animation,
or telemetry.

## 6. Package the evidence

- `export_evidence_bundle`; `inspect_analysis_view` (`kind: "summary"`) for the
  readable projection. Request `detail: "summary"` first — same evidence, orders of
  magnitude cheaper.
- Fill `assets/gate-report.md`, cite an evidence id for every claim.
- State limitations verbatim from REA's output. Do not smooth them over.

## 7. Deliver

The report answers, in order: what the gate is, where it lives, what it reads, how you
proved it, what breaks if the vendor moves it, how to rebuild it. Mark clearly whether
the gate is client-flippable or server-enforced. Include the scope declaration and the
log of side-effecting calls.

## Efficiency rules

1. Summary view before any full graph; page into functions the graph points at.
2. Cheap built-in readers before decompilers (Go build info, Electron fuses, SQLite,
   .NET metadata).
3. `REA_MCP_INPUT_SCHEMA_PROFILE=compact` + `REA_MCP_OUTPUT_SCHEMA_PROFILE=off` shrinks
   the tools list dramatically, same tools.
4. One Frida hook at a time, named and logged. No shotgun hooks.
5. Don't decompile to hunt; hunt with strings/xrefs, decompile to confirm.
6. Batch independent reads; keep a session open instead of re-importing per call.

## Reverting

Record how you revert: `stop_adb_app`, `close_binary`, pref restore, kill the Frida
session. A report that leaves a device patched is incomplete.

## Honest limits

- **Server-side gates are not local predicates.** If the entitlement is checked per
  request, the client boolean is cosmetic.
- **Receipt cryptography is not the target.** The *branch* is. Say where validation
  happens and stop.
- **Obfuscation moves the predicate.** Record the build hash and bundle version with
  every finding.
- **Silence is not absence.** A missing string proves nothing.
- **This finds and explains a gate. It does not authorize bypassing one in production
  or redistributing a patched build.** Output is for understanding and rebuilding your
  own software, interop, and authorized assessment.

## References

- `references/target-routing.md` · `references/ios-ipa.md` · `references/android-apk.md`
- `references/javascript-electron-web.md` · `references/native-desktop.md`
- `references/runtime-instrumentation.md` · `references/evidence-and-paging.md`
- `references/recovery-and-safety.md`

## Scripts

`scripts/00-install.sh` · `01-doctor.sh` · `02-triage-ipa.sh` · `03-hunt-gate-macho.sh`
· `04-triage-apk.sh` · `05-triage-electron.sh` · `06-diff-replay.sh`
· `07-summarize-evidence.sh` · `08-frida-gate-probe.js`

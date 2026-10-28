# Runtime and the replay loop

Static = *where*. Runtime = *that*. Everything here runs or changes the target, so it
requires a scope that permits runtime side effects (step 0) and a confirmation before
the first such call. Log every side-effecting call.

## Frida contract
- One hook per hypothesis, named, with `send()` logging of `args` and `retval`.
- Run 1: observe only. Run 2: force the return. Never force before the baseline — you
  lose the counterfactual.
- Hook the narrowest thing that proves the claim: the predicate symbol, not the class.
- Template: `scripts/08-frida-gate-probe.js`.

## Debugger contract
- `start_gdb_session`, `gdb_console`; `start_rizin_debug_session`,
  `rizin_debug_command`. Breakpoint at the branch, read the register, patch live,
  single-step. Register values are the strongest evidence.

## Capture contract
- `capture_process_scenario`, `capture_native_ui_scenario`, `capture_electron_scenario`,
  `capture_browser_scenario` all **run** the target. Declare actions explicitly, keep
  the action list identical between closed and open runs.

## The replay loop
1. Baseline capture: gate closed.
2. Flip exactly one value (memory, prefs, localStorage, keychain item, flag file).
3. Capture again, identical actions.
4. Diff; keep only differences attributable to the flipped value.
5. Export: `export_evidence_bundle`; project a summary.
6. The diff also proves what didn't change — the false-positive filter.

## Reverting
`stop_adb_app`, `close_binary`, pref restore, kill the Frida session. Leave the device
as you found it.

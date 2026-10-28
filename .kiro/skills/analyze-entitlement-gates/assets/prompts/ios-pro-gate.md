# iOS "Pro" gate — working prompt

Target: ⟨MyApp.ipa⟩ · bundle id ⟨⟩ · version ⟨⟩ · SHA-256 ⟨⟩
Scope (assets/scope.json): ⟨own-software | client-authorized ref X⟩ · runtime side effects: ⟨yes/no⟩

Hypothesis:
> The Pro gate is enforced by ⟨StoreKit entitlement | local NSUserDefaults flag | JS bundle⟩
> reading ⟨key/symbol⟩, because ⟨UI symptom: locked tab, "Upgrade" sheet, watermark⟩.

Steps:
1. `02-triage-ipa.sh MyApp.ipa` → bundle id, version, exec SHA-256, frameworks, hybrid markers, entitlements. Record all in scope.json.
2. If hybrid/RN markers present, read the JS bundle first (localStorage.pro / AsyncStorage / remote config).
3. `03-hunt-gate-macho.sh <unpacked>` → overview, gate strings, ObjC/symbol leads.
4. `xrefs` each gate string → `procedure_pseudo_code` on the referring function. Name: read-at, tested-at, true→paid UI.
5. Co-predicate check: expiry? device count? receipt validation server-side?
6. Classify: client-flippable vs server-enforced. If StoreKit validation runs server-side, stop — the local boolean is cosmetic.
7. Runtime (only if scope permits): `08-frida-gate-probe.js`, observe run then force run, confirm UI change, revert.
8. Fill `gate-report.md`, cite evidence id per claim.

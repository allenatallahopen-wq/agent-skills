# Web paywall — working prompt

Target: ⟨https://app.example.com⟩ or JS bundle · build hash ⟨⟩
Scope (assets/scope.json): ⟨own-software | client-authorized ref X⟩ · runtime side effects: ⟨yes/no⟩

Hypothesis:
> The paywall is enforced ⟨client-side in JS reading localStorage/feature flag | server-side by truncating content⟩,
> keyed on ⟨flag/field⟩, because ⟨UI symptom: blurred content, modal, truncated article⟩.

Steps:
1. `analyze_web_bundle` or `inspect_web_page` → scripts, source maps, observed traffic.
2. Fetch source maps (the documented network boundary) for the page you name.
3. Hunt: `isPremium`, `subscription`, `paywall`, `featureFlags`, `tier`, `localStorage.setItem('pro'…)`, `window.__ENTITLEMENTS__`, JSON-LD `offers`.
4. Decide client vs server: is the paid content present in the DOM/JSON and merely hidden, or absent (server-truncated)? Absent = server gate, stop.
5. Runtime (only if scope permits): `capture_browser_scenario` with explicit actions — record closed, set the flag, record open, diff. Keep action lists identical.
6. Fill `gate-report.md`, cite evidence id per claim.

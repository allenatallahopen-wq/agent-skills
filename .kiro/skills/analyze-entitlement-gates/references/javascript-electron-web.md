# JavaScript / Electron / web

## Electron
1. `analyze_javascript_application` on `resources/app.asar` (or the extracted tree).
   Graph: modules, imports, source maps, IPC channels, native add-ons.
2. **Always** project it: `inspect_analysis_view` `kind: "summary"`. Full graphs run
   hundreds of MB; the summary is kilobytes. Same evidence.
3. `inspect_electron_fuses` on the executable, without launching it. `RunAsNode: true`
   means it runs as plain Node; `OnlyLoadAppFromAsar` disabled means the asar can be
   edited and repacked.
4. Hunt: `electron-store` keys (`get('premium')`), IPC channel names
   (`licence-check`, `entitlement:get`), `process.env.*_LICENSE`, `app.getVersion()`
   comparisons, licence server URLs.
5. Runtime (if scope permits): `capture_electron_scenario` → diff closed vs open.

## Web paywall
1. `analyze_web_bundle` (or `inspect_web_page` for structure/scripts/observed traffic).
2. Source maps are the shortcut — the documented network boundary.
3. Hunt: `isPremium`, `subscription`, `paywall`, `featureFlags`, `tier`,
   `localStorage.setItem('pro'…)`, `window.__ENTITLEMENTS__`, JSON-LD `offers`.
4. Runtime (if scope permits): `capture_browser_scenario` with explicit actions,
   record closed, set the flag, record open, diff.
5. Server-rendered paywalls (content truncated server-side) are server gates — the DOM
   has no paid content to reveal.

Paging discipline: summary first, then selected pages. Keep source digests; don't
re-run the analysis to "look again".

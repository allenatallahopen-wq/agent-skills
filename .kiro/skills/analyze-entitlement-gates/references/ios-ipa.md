# iOS .ipa — where the paywall actually is

An `.ipa` is a zip. Unpack into a scratch dir; `Payload/<Name>.app` holds:

- the **main Mach-O** (name = `CFBundleExecutable`), `Info.plist`, assets,
  `embedded.mobileprovision`, `Frameworks/` (.dylibs, Flutter `App.framework` +
  `flutter_assets/`, RN/Hermes `main.jsbundle`);
- **entitlements** (`codesign -d --entitlements :-`), **code signature**, **cryptid**
  (App Store binaries are FairPlay-encrypted — sanity check before investing in static
  reading);
- hybrid apps: a **webview layer** that often carries the revenue gate in *JavaScript*.

Order of attack (cheapest first):

1. **Read the JS bundle first** in hybrid/RN/Cordova apps. The gate usually reads
   `localStorage.pro` / `AsyncStorage` / a remote config JSON.
2. **Bundle IDs, versions, URL schemes** from `Info.plist` — pin them to your report.
3. **Symbols**: `nm -gU`, `otool -Iv`. Look for `isPro`, `Entitlement`, `Purchase`,
   `Receipt`, `Premium`, `SubscriptionManager`, `StoreKit`,
   `Transaction.currentEntitlements`.
4. **Strings + xrefs** with REA: `open_binary` → `binary_overview` → `search_strings`
   → `xrefs` → `analyze_function` on the referring function.
5. **StoreKit-style gates**: receipt/keychain fetch → validation → boolean → branch.
   The cryptography is not your target: name the validation function, name the boolean,
   stop.
6. **Local-state gates** are the easy ones: a `NSUserDefaults`/plist key, a keychain
   item, or a StoreKit `Transaction` cache.

Runtime (device/simulator — only if scope permits): `instrument_with_frida` (hook the
ObjC/Swift predicate) or `observe_native_calls` under LLDB.

Record: bundle id + `CFBundleShortVersionString` + executable SHA-256, the predicate's
symbol and address, the store key, and whether enforcement is **client** or **server**.

Caveat: App Store receipt validation run server-side is a server gate — the local
boolean changes a badge, not the entitlement.

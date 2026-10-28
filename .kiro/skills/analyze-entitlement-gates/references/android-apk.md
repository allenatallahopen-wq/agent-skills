# Android .apk / .aab

1. `inspect_android_package` — decoded manifest (permissions, exported components,
   billing intent filters), version facts, string tables, locales.
2. `inspect_apk_signature` — v1/v2/v3/v3.1 schemes, signer SHA-256, rotation lineage.
   Identity, not trust.
3. Code: JADX via the Android tools. Hunt `isPremium`, `hasSubscription`, `Purchase`,
   `queryPurchases`, `BillingClient`, `acknowledgePurchase`, `FeatureFlag`,
   `RemoteConfig`, `com.android.billingclient`.
4. Local state: `shared_prefs/*.xml`, `databases/*.db` (SQLite reader), DataStore
   protobufs, `android_keystore`.
5. Reproduce on device (only if scope permits): `install_adb_package` →
   `start_adb_activity` → push/pull prefs → `stop_adb_app`.
6. Runtime hook with `instrument_with_frida` on the Kotlin/Java predicate; log
   `args`/`retval` first, force on the second run.

Billing specifics: `queryPurchasesAsync` result filtering,
`Purchase.getPurchaseState()`, `isAcknowledged()`, signature verification in
`Security.verifyPurchase`, and any cached `SharedPreferences` "isPro" mirror written at
purchase time (the usual weak point).

Caveat: Play Billing verification against Google's server is a server gate. The cached
mirror and UI booleans are client gates.

# Android "Pro" gate — working prompt

Target: ⟨app.apk⟩ · package ⟨⟩ · version ⟨⟩ · signer SHA-256 ⟨⟩
Scope (assets/scope.json): ⟨own-software | client-authorized ref X⟩ · runtime side effects: ⟨yes/no⟩

Hypothesis:
> The Pro gate is enforced by ⟨Play Billing queryPurchases | cached SharedPreferences isPro mirror | RemoteConfig flag⟩
> reading ⟨key/field⟩, because ⟨UI symptom⟩.

Steps:
1. `04-triage-apk.sh app.apk` → manifest, billing intent filters, version, signature, gate strings. Record in scope.json.
2. JADX the predicate: `isPremium`, `queryPurchases`, `BillingClient`, `acknowledgePurchase`, `Security.verifyPurchase`.
3. Local state: `shared_prefs/*.xml`, `databases/*.db`, DataStore protobufs. The cached "isPro" mirror written at purchase is the usual weak point.
4. Name read-at / tested-at / true→paid UI. Co-predicates: acknowledged? expiry? signature check?
5. Classify: the Google-server verification is a server gate; the cached mirror and UI booleans are client gates.
6. Device replay (only if scope permits): `install_adb_package` → `start_adb_activity` → pull prefs → edit flag → relaunch → diff → `stop_adb_app`, restore prefs.
7. Fill `gate-report.md`, cite evidence id per claim.

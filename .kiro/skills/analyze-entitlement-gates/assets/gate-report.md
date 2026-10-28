# Gate report — ⟨App⟩ ⟨version⟩

## Scope (from assets/scope.json)
- Target: ⟨name⟩ · SHA-256 ⟨hash⟩ · bundle id/url ⟨id⟩ · version ⟨v⟩
- Authorization basis: ⟨own-software | client-authorized ref X | ctf Y | offline-interop⟩
- Runtime side effects permitted: ⟨yes / no⟩
- Out-of-scope acknowledged: no redistributable patched build, no production payment bypass

## The predicate
- Symbol / key: ⟨name⟩
- Location: ⟨file:address | module+offset | key path⟩
- Read at: ⟨caller⟩ · Tested at: ⟨branch address⟩
- Co-predicates (must also hold): ⟨list or none⟩

## Enforcement
- Layer: ⟨local state | bundle logic | remote config | receipt | server⟩
- Client-flippable: ⟨yes / no / partially⟩

## Evidence
| # | Claim | Tool | Evidence id / address | Limitation |
|---|-------|------|-----------------------|------------|
| 1 | | | | |

## Runtime proof (only if scope permitted it)
- Baseline (closed): ⟨capture id / log excerpt⟩
- Flipped value: ⟨what, where⟩
- Replay (open): ⟨capture id / log excerpt⟩
- Diff attributable to the flip: ⟨summary⟩
- Reverted: ⟨how⟩

## Rebuild notes
⟨the branch, the key, the shape of the check — enough for a clean reimplementation of your own version⟩

## Side-effecting calls made (each confirmed before running)
| tool | target | command | confirmed by |
|------|--------|---------|--------------|

## Gaps
⟨unresolved channels · resource_constraint members · missing engines · stripped symbols⟩

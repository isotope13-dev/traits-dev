# Diagnostic warning suppression versus TLS behavior

Three rules leave `communications/http/tls`: one general urllib3 warning-control
call moves to `os/telemetry/logging/warning`, one narrower argument-filtered
matcher merges into an existing canonical observation there, and one redundant
OR roll-up is retired. The [three-entry ledger](warning-suppression-mapping.json)
records effective definitions and decisions. No alias remains in the TLS leaf.

## Evidence and ownership

Warning emission/filtering/suppression belongs with diagnostic warning behavior
in `micro-behaviors/os/telemetry/logging/warning`. It says nothing about whether
an HTTP request occurs or certificate authentication is enabled. Explicit TLS
verification-disable settings belong in `communications/tls/verify/disable`;
ordinary context creation is separate again. Keep API/language in rule scope and
filenames. The existing warning leaf also contains emission, so a consumer that
needs suppression must reference the suppression atom, not the whole directory.

The retired `insecure-request-warning-filter` required the exact call name
`disable_warnings` with identifier argument `InsecureRequestWarning`. The
existing `urllib3-insecure-request-warning-suppressed` has the same argument
constraint and accepts that name or a qualified suffix. File/platform sets,
confidence and criticality agree. Thus the existing canonical rule already
covers every old match; this merge does not widen that canonical rule. Before
traces on the typed control match both rules; after traces retain the canonical
match. The platform lists differ only in order.

The general `urllib3.disable_warnings()` matcher retains its exact effective
definition at the new home. Its optional requests-qualified prefix remains.
The unused same-criticality OR roll-up adds no independent fact and has no
external exact consumers; both underlying warning operations remain available.
Removing it reduces duplicate finding counts, so score/count equivalence is not
claimed. The `explicit-insecure-tls-option` rule is left for a separate audit:
its option token and conditional guard do not establish selection of insecure
mode and need their individual claims examined.

## Consumers and checks

The [12-occurrence ancestor audit](warning-suppression-ancestor-audit.json)
records positive HTTP/communications consumers. They intentionally lose warning
suppression as network evidence. No destination-ancestor consumers or external
exact consumers existed in this snapshot. No unrelated capability is moved merely
to keep an ancestor predicate firing.

Three inert Python fixtures are registered: general warning suppression, typed
InsecureRequestWarning suppression, and a default verifying TLS context combined
with warning suppression. Each requires diagnostic evidence and forbids the new
verification-disable leaf and the old HTTP TLS location. The context fixture
also requires ordinary TLS context evidence. This tests the capability distinction
rather than simply changing expected IDs.

The full gate passes **1,753/1,753 fixtures**, including **463 benign**. HTTP TLS
falls **24 → 21 rules**; warning behavior rises **2 → 3**. There remain **169
oversized directories**. Effective snapshots, exact traces and read-only atomscan
comparisons are in `/tmp/taxonomy-warning-suppression/`. The overall migration
remains open.

## Validator follow-up

Beyond identical bodies, flag provable matcher subsumption as a merge candidate:
an exact call name can be covered by an anchored suffix regex when argument
constraints and effective scopes agree. This is a review suggestion, not a
license to collapse arbitrary regexes or broaden a narrower consumer. Also flag
unused same-criticality OR wrappers which contribute no additional condition.

Installed before/after findings agree for all three controls after mapping the
moved/merged atoms and removing the retired roll-up. Strict `make validate`
exits **2**, reporting only the **169 cap violations**. There are **zero mixed
nodes**, and the snapshot comparison found no unrelated changed/removed rule
definitions during this cohort.

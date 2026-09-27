# Accounting vocabulary is not compiled-source attribution

Eleven rules move from `metadata/lang/compiled` to
`metadata/file/string/accounting`. The [effective-definition ledger](accounting-literals-mapping.json)
records every rename, description correction and canonical reference. Matcher
bodies, C scope, Unix/Android/iOS platforms, confidence, criticality, thresholds
and composite conditions are preserved. No syntax recognition is added.

## Evidence and placement contract

Exact checkout traces demonstrate the problem: all eleven old rules match the
quoted strings in `accounting-literals.c`, while none match the corresponding
actual declarations in `accounting-syntax.c`. The same results hold after the
move: **11/11 literal matches, 0/11 syntax matches**. These rules describe
literal accounting vocabulary; they do not establish header inclusion, use of
fixed-size records, portability, or an accounting operation.

`metadata/file/string/accounting` admits names/directives for login-session and
process-resource accounting records, headers and configuration. It excludes:

- User/account identity and profile fields: `metadata/file/string/account`.
- Concrete accounting log paths: `micro-behaviors/fs/path/log/accounting`.
- Actual file reads/writes: their filesystem operations.
- Intent-bearing log destruction: `objectives/evasion/indicator-removal/accounting`.
- Language or compiler attribution: the corresponding `metadata/lang` subject.

The subject takes precedence over the literal's C syntax: implementation and
filetype remain in `c.yaml` and rule scope. Header/record literal combinations
are named `accounting-header-literals`; header-plus-configuration combinations
are `accounting-config-literals`. Neither is labeled source structure or
cross-platform portability. These are vocabulary profiles, not new techniques.

The generic `account` leaf concerns an entity's identifiers/properties; the
accounting leaf concerns records of sessions and process usage. Neither refines
the other. The sibling-name validator reports their shared spelling stem, but
that is not sufficient evidence of a redundant category. This is a documented
review decision, with no validator exemption. The engine now
presents stemming matches as possible overlap requiring semantic review, rather
than asserting that a common stem proves identical meaning.

## Consumers and validation

The [89-occurrence ancestor audit](accounting-literals-ancestor-audit.json)
records every affected directory reference. Seventy-two have no declared C
scope overlap. Seventeen unrestricted/C/source consumers intentionally lose
quoted accounting text as compiled-language suppression evidence. No alias or
replacement exclusion restores that misleading attribution. There were no
external exact consumers of these eleven IDs.

Both inert C controls are checked into `testdata/benign` and registered in the
expectations. Fixture assertions forbid the retired compiled-language placement;
the syntax-only case also forbids the accounting-literal destination. Exact
traces cover the positive baseline observations that displayed output may omit.
All eleven effective definitions compare equal modulo IDs, descriptions and
resolved references. This preserves matching while deliberately changing the
meaning of broad compiled-language exclusions.

The full soft gate passes **1,742/1,742 fixtures**, including **452 benign**.
`metadata/lang/compiled` falls **79 → 68**, and the new accounting leaf contains
**11 rules**. There remain **170 oversized directories**; this semantic repair
does not resolve another cap violation. The account/accounting name advisory is
reviewed above. Logs and before/after scans are in
`/tmp/taxonomy-accounting-observations/`. The broader migration remains open.


## Validator repair

Strict validation revealed that the sibling-name check printed “warning” but
still inserted a fatal hygiene issue. The engine now emits a non-blocking
advisory, consistently with depth and sparse-cohort reviews. This applies to all
shared-stem pairs; no directory-specific exception was added. The 85-rule cap
and leaf-only checks remain unchanged.

The rebuilt checkout passes all **1,742 fixtures** again. Strict validation
still exits **2**, now reporting only the **170 cap violations**. Eleven selected
engine tests pass (including the sparse-cohort boundary test); these are not
presented as direct coverage of sibling-name severity. The separate
[CLI regression script](check-sibling-advisory.py) verifies that the spelling
advisory adds no failure, 85 rules adds no cap failure, 86 rules fails the cap,
and mixed parent/child rules fails leaf-only validation. Its tiny tree naturally
fails the production allowlist-coverage check; the assertions isolate that
known failure without disabling any validator. The full repository gate above
has no such allowlist failure.

Updated engine files: `../cleave/src/capabilities/mapper/loader_directory.rs`
and `../cleave/src/validation_controls.rs`. Rebuild used the existing isolated
manifest with the local filefacts dependency; shared manifests were not edited.

# Archive-member names and platform coverage, 2026-09-27

This report preserves its batch checkpoint. The subsequent
[parser/DOS consolidation](PARSER-DOS-CONSOLIDATION.md) resolves the final two
pairs and records the newer validation results.

Three more shared-matcher pairs are consolidated. **Twelve of the original
14 pairs are now resolved; two remain.** The archive-member audit also retires
`metadata/package/files/credentials`: its remaining eight rules inspected names,
not credential contents. All 11 resulting observations/composites live in the
existing `metadata/package/files/name` leaf, which now has 19 rules.

## Placement and detection

The canonical member-name atoms describe testclient/testserver `.key` names,
ucli_commands/ncverilog `.key` names, and public-key-like names in test trees.
These are not proofs of key contents or whole-archive fixture identity.
The adjacent key/PFX/SSH/certificate patterns receive the same treatment:
descriptions state what their name predicates establish. The container
composite describes names suggesting private-key material, and loses an
unsupported credential-access ATT&CK tag.

The three merged atoms retain the union of file/platform scopes. This adds
neutral name observations on the additional Unix platforms for formats beyond
tar; it does not widen the tar-only scope of `tls-test-keypair` or
`package-key-known-benign-member`. Those exception composites retain their
original conditions. Whole-directory fixture consumers intentionally lose
these three name-only facts as sufficient evidence of fixture status.

The eight sibling relocations preserve their predicates, confidence,
criticality, file/platform scope and exclusions. Their local references resolve
within the new leaf, and the external fixture-context reference was updated.
No live rule reference to `files/credentials` remains. This establishes one
home for these name facts without discarding the existing contextual consumers.

The [six-to-three ledger](key-member-consolidation-mapping.json) and
[eight-rule relocation ledger](credential-member-name-mapping.json) record
effective definitions. All 14 original definitions were checked against their
11 resulting definitions. The destination remains leaf-only and below 85.

## Validator correction

The duplicate validator previously used symmetric platform overlap to test
equivalence. That made `[unix, windows]` look equivalent to
`[linux, macos, windows]`, hiding BSD and other Unix coverage differences.
The comparison now uses directional coverage, recognizes unrestricted scopes,
and handles redundant umbrella members without confusing a member with its
whole group. New tests cover Unix/BSD, appliance members, unrestricted scopes,
and a shared matcher whose only difference is platform coverage.

All **144 duplicate-related unit tests pass**, and the release binary was
rebuilt. The correction reports the remaining scope differences explicitly;
it does not exempt any directory or relax duplicate validation.

## Verification

All **1,623 fixture checks pass in soft mode**: 248 hostile, 348 benign,
175 does-nothing, 45 drop-exec, 572 supply-chain, 66 impact-wipe,
82 obfuscation, 22 reverse-shell and 65 simple-stealer. A local atomscan control
archive containing the three filenames but no cryptographic key material
retains score 2 and reports the canonical name observations. The eight adjacent
relocations preserve the existing tar exception behavior.

Strict `make validate` reports only the **two shared-matcher reviews and 176
oversized directories**. It remains a failing gate; this batch does not resolve
the global size-policy migration.

## Remaining work

The parser-error pair has different exclusions. Consolidating it requires
canonical observations for those conditions as well as the shared metric;
do not union or drop exclusions merely to remove the diagnostic.
The DOS near-call pair needs a precise account of what its byte prefix proves
before its API claim is retained. These remain the two shared-matcher reviews.
The reverse-shell `stdio`/`encoded` audit and the 176 oversized directories
remain open.

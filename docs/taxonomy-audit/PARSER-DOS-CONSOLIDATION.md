# Parser diagnostics and DOS query evidence, 2026-09-27

The remaining two pairs from the original duplicate review are resolved.
**The validator now reports no shared-matcher review pairs.** This is a
checkpoint for the implemented duplicate checks, not proof that no semantic
redundancy remains anywhere in the taxonomy.

## Parser diagnostics

`metadata/file/archive::archive-parser-errors-present` is the single atomic
error-count observation. The two contextual diagnostics reference it and
canonical metadata facts for wrapper names, reported format, missing package
names and member-path structure. Their distinction remains explicit:
ordinary archive errors outside recognized contexts versus errors associated
with an npm package. Neither claims that the error necessarily occurred in
gzip decompression or proves fatal corruption.

Factoring the guards revealed three precision issues, which are deliberately
corrected rather than mechanically preserved:

- Arbitrary `..` bytes in compressed content no longer establish a traversal
  member. The guard uses `archive.path_traversal_count`.
- Raw ZIP-looking bytes somewhere in the file no longer establish a rooted
  archive member. The guards use parsed slash-, backslash- or drive-rooted
  member paths. Slash-rooted paths reuse the existing canonical observation.
- Wrapper suffix context is limited to the relevant tar-based carriers;
  crate/pkg context requires the corresponding file type. A renamed unrelated
  format is not automatically acquitted as an expected wrapper diagnostic.

The existing `pkg-archive-kind` atom was also found during factoring and
consolidated into `metadata/file/format/structured::archive-format-pkg`.
A parser's format label belongs with file-format metadata, not BSD member
names. The complete format fact is baseline rather than an incomplete component.
Its consumers now reference that canonical observation.

The [parser ledger](parser-error-consolidation-mapping.json) records original
and resulting effective definitions, every guard, reused observations, and
intentional context changes. This migration is not predicate-equivalent:
incidental bytes and misleading suffixes can no longer hide diagnostics, and
parsed member structure can explain diagnostics across archive carriers.

## DOS internal tables

The duplicate `B4 52 E8` body is now
`micro-behaviors/os/msdos/internal::ah52-near-call`. It loads AH=52h and begins
a near call; the body does not establish the called routine's behavior.
It is partial neutral evidence. Two actual interrupt-sequence observations
and their two dispatch groupings moved beside it, preserving their distinct
gap bounds and scopes. The grouping composites are components because their
near-call alternative is incomplete; the interrupt observations remain notable.

All six original definitions resolve to five resulting definitions in the
[DOS ledger](dos-query-consolidation-mapping.json). Infection and TBAV-tampering
consumers retain their other required evidence and now reference the neutral
query facts. Query evidence alone no longer carries either attacker-objective
label. No API-call target resolution or general dataflow proof is claimed.

## Validator and verification

The short-pattern warning now recognizes a literal prefix/suffix at a fixed
position in an explicitly selected value field. For example, `^/` on an
archive-member path is a precise path-shape observation. Raw-byte searches,
recursive field queries, multiline anchors, alternations and unbounded spans
do not receive that exemption. This is a general constraint check, not a
directory exception. All **17 pattern-validation tests pass**, including the
new regression, and the release binary was rebuilt.

All **1,627 fixture checks pass in soft mode**: 248 hostile, 352 benign,
175 does-nothing, 45 drop-exec, 572 supply-chain, 66 impact-wipe,
82 obfuscation, 22 reverse-shell and 65 simple-stealer.
Four new static fixtures distinguish ordinary double-dot content from a
traversal member, and DOS table querying from an unrelated near call.

Direct `test-rules` checks report traversal count **0** and no match for the
ordinary archive, versus count **1** and a match for the parent-segment archive.
Local atomscan checks retain neutral DOS findings without infection or TBAV
labels; the unrelated call scores 0 and the table query scores 1. The test
programs were inspected statically, not executed.

Effective-definition verification covers both ledgers. All affected destinations
remain leaf-only and within 85: archive diagnostics 29, package-name conventions
26, package extensions 2, structured formats 60, archive-member structure 72,
and DOS internal evidence 11. The unchanged source-archive guard's leaf has 67.

Strict validation still fails on **176 oversized directories**. The reverse-shell
`stdio`/`encoded` audit and the remaining size-policy migrations are not complete.

# Property operations and computed dispatch

## Implemented organization

The remaining 47 rules in `data/source/property` are now classified by operation;
that historical subtree is retired. Six sibling observations also move from
JSON serialization and dispatch, for **53 relocations** in total:

- Property access, assignment, descriptor/accessor definition and enumeration
  have separate leaves under `data/property`.
- Computed calls and constructor selection belong in `data/control-flow/dispatch`.
  A generic Rust `.put()` is a method call until its receiver establishes more.
- Typed-buffer construction belongs in `data/buffer/alloc`; high-iteration loops
  and conditional expressions belong in their control-flow leaves.
- Sort/fill observations belong with array operations. Provider module exports
  belong in `os/module/export`.
- Object.keys/Object.entries references are enumeration evidence, not JSON codecs.
  Their descriptions retain the distinction between string references and calls.

Names and descriptions no longer claim a decoder from a key-computing function,
a hidden process from arguments 0/false, same-receiver refill from callback
syntax, or type alternation from nearby getter fragments. Float32/Float64 and
signed/unsigned BigInt buffer descriptions now cover their actual alternatives.
Two neutral window-member-call rules lose unsupported obfuscation ATT&CK/MBC tags.

Matching predicates, scopes, criticalities, confidence and filters are preserved
except one demonstrated repair: the attributes-member regex contained a literal
backslash instead of an escaped dot. Normal `obj.attributes` failed before and
matches afterward. Direct rule tracing confirms the change; the baseline finding
can be omitted from rendered scan output, so JSON absence alone cannot test it.

TAXONOMY.md documents admission criteria, especially access versus invocation and
property definition versus labels. Language/filetype details remain in scopes
and filenames.

## Ancestor-consumer repair

The previous property cohort updated exact and immediate-leaf consumers but
missed `long-tail-build-config-payload`'s reference to the ancestor
`data/source/property/`. That omission silently removed 27 former alternatives.
This cohort restores them and preserves the 47 newly moved alternatives. An
inventory check expands the final references and proves that all **74** former
property alternatives are represented exactly. The six assignment and six definition alternatives
cover their respective destinations and use directory references;
partial groups stay named so unrelated siblings are not admitted.

The [113-entry ledger](property-operations-mapping.json) records 53 relocations
and 60 consumer changes, including this coverage repair. Before-definitions retain
the original over-escaped attributes regex and the pre-repair ancestor consumer.
Every after-definition verifies against current YAML.

## Validator correction

Validation previously demanded directory notation once an explicit `any` group
covered 80% of a directory. The migrated consumer deliberately names 21 of 23
property-access rules. Following that diagnostic would add two unrelated
alternatives. Full coverage, not a percentage, is required for replacement.

The validator now requires distinct references covering the entire known
membership. Repeated references cannot inflate coverage. The membership inventory
for directory-reference/alias checks includes composite definitions as well as
atomics; enumerating all atoms is not necessarily enumerating a whole directory.
Tests cover 8/10, 21/23 and 99/100 subsets, duplicate references, full coverage,
and preservation of all-member conjunctions. `all:` groups are no longer treated
as redundant directory lists: requiring every API hash is not equivalent to
matching any hash, and a count alone does not establish a taxonomy defect.
RULES.md now requires auditing every ancestor reference during moves and retaining
explicit partial sets. No per-directory exception or cap relaxation was added.

The engine checkout concurrently gained a DOS-decoding call absent from its
pinned filefacts revision. Tests/builds therefore use the local filefacts source
via `/tmp/cleave-taxonomy-property-operations/Cargo.toml`. The shared engine
manifest and lockfile remain untouched. The validation build must not be confused
with a clean build from the currently pinned dependency.

## Control evidence

Three permanent benign archives exercise computed calls/assignments, property
definitions/buffers, and sort/fill callbacks. Across eight initial archive/member
comparisons, emitted finding sets and criticalities remain identical modulo the
migration map. The attributes repair is verified separately with `test-rules`.
The sort archive/member scores rise 2→3 and 1→2; the computed-call member falls
4→3; the other five scores are unchanged. No suspicious or hostile finding occurs
in these controls.

Final validation passes **1,700/1,700 fixtures** and **75 validator constraint
tests**. Strict `make validate` exits 2 only on the existing **173 oversized
directories**; zero mixed rule directories remain. Destination counts include
property/access 23, assign 6, define 6, enumerate 3, dispatch 59, buffer/alloc 22,
control-flow/branch 32, control-flow/loop 84, collection/array 5, and module/export 3.

Logs: `/tmp/taxonomy-property-operations-{before,after}.json`,
`/tmp/taxonomy-property-operations-attributes-{before,after}.log`,
`/tmp/taxonomy-property-operations-constraint-tests-final.log`,
`/tmp/taxonomy-property-operations-{soft,strict}-final.log`.

## Remaining sibling precision work

The computed-call control still exposes two legacy claims outside the retired
subtree: `process/create/shell/wsh::computed-method-hidden-window-call` requires
no WSH receiver, and `objectives/anti-static/obfuscation/syntax::js-computed-call-false-argument`
requires no obfuscation. Their broader directory consumers need an audit before
moving those observations to dispatch; do not mistake their retained notable
findings for proof of hidden execution or obfuscation.

The destination audit found identical `ast.infinite_loop_count >= 1` bodies in
`javascript-infinite-loop-metric` and `source-infinite-loop-metric`. Their scopes
and criticalities differ, so blindly merging would change coverage or reporting.
Review their consumers and criticality rationale, then choose a canonical rule
or document an evidence-based difference. No other identical atomic bodies were
found across this cohort's destination leaves.

Property-ordering/getter composites still infer suspiciousness from specific
syntax and proximity; the same-object and value-flow claims require a dedicated
positive/benign audit. Serialization, remaining source syntax, and the wider
oversized-directory migration are still incomplete.

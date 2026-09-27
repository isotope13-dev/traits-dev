# WebAssembly declarations versus language attribution

The oversized `metadata/lang/compiled` leaf contained 86 rules. Seven atomic
observations describe parsed exports or producer metadata, rather than a
compiled language. They move to existing metadata subjects; the three composite
toolchain profiles remain in `lang/compiled` and reference the canonical atoms.
The [10-entry ledger](wasm-observations-mapping.json) preserves all effective
predicates, scopes, criticalities, confidence and composite structure modulo
references and two clarified descriptions. No directory exemption or new
language/filetype partition is introduced.

## Placement and sibling boundaries

- Six parsed export-name observations belong in `metadata/binary/symbols/exports`.
  A symbol declaration is classified by its role even when the parser exposes
  it through a value array rather than the generic symbol matcher. Arbitrary
  text with the same spelling is not an export. `wasm-asyncify-transform` is
  renamed `wasm-asyncify-export`: an export-name substring alone does not prove
  a transformation happened.
- Presence of `wasm.producers` belongs in `metadata/binary/provenance/build`.
  An unspecified producer record does not identify a particular language or
  prove that the named tool is the artifact being analyzed.
- The paired TinyGo, wasm-bindgen and Emscripten observations remain attribution
  profiles in `metadata/lang/compiled`. Their existing one-anchor `all` plus
  corroborating `any` structure is preserved, including its proximity behavior.
  This migration does not strengthen their identity claims or raise criticality.
- An actual runtime operation belongs with its capability; independent compiler
  or runtime artifact identity belongs in `well-known`. Parsed declarations do
  not become either merely because a consumer needs them.

Destination counts are **exports 35 → 41**, **build provenance 10 → 11**, and
**compiled 86 → 79**. All remain leaves. Compiler sibling directories already
mix output attribution and compiler executable identity, so moving the entire
WASM file there would perpetuate the same ambiguity. No such bulk move is made.

The remaining compiled leaf still needs semantic cleanup. Its accounting
headers/macros describe source observations, its Go UsageLine marker describes
command metadata, and its assembly source markers do not establish compiled
output. Rust crate references, kernel identity, and runtime attribution likewise
need their individual matcher claims reviewed. Falling below 85 does not close
that audit. In particular, accounting matchers use `string_literal` for apparent
source syntax; verify actual matching before changing either placement or
matcher type. Do not assume that changing that type is a pure relocation.

## Directory consumers

The [105-occurrence ancestor audit](wasm-observations-ancestor-audit.json) covers
both source and destination ancestors. Ninety occurrences have no declared
file-scope overlap with incoming or departing WASM-only facts. Fifteen compiled
consumers have unrestricted, WASM or `binaries` scope (the parser includes WASM
in `binaries`). They intentionally lose uncorroborated export/producer facts as
exclusion or downgrade evidence. No broad alias restores those weak language
claims. Corroborated attribution profiles remain in the original leaf.

This can reveal a previously downgraded observation on a WASM file with only
one helper export. That is an intentional correction, not an assertion of
universal verdict equivalence. The destination ancestor consumers in this
snapshot have no WASM scope overlap. These decisions must be revisited if their
scopes change.

## Verification

Three inert WASM controls are tracked under `testdata/benign` and registered in
`testdata/expectations.toml`:

1. `toolchain-export-facts.wasm` exports all six names and has a producers record.
   Exact checkout traces match all three attribution composites and the producer
   fact. This deliberately synthetic surface tests predicates, not genuine
   compiler provenance.
2. `toolchain-names-without-exports.wasm` contains the same names in a custom text
   section; it does not match exports or language attribution.
3. `single-helper-export.wasm` exports only `stackSave` and contains an
   `encoding/base64` reference. It matches the export and base64 observation,
   without Emscripten attribution. This tests the consumer boundary directly.

Read-only installed atomscan before/after comparisons of the first two controls
and the existing codec-export fixture have identical displayed finding IDs
modulo the migration map, criticalities and confidence. Checkout traces verify
baseline composites that the rendered scan may omit. All ten effective ledger
definitions are also compared structurally, resolving local references.

The fixture generator is recorded alongside this report as
[wasm-observation-controls.py](wasm-observation-controls.py). Validation logs and
snapshots are under `/tmp/taxonomy-wasm-observations/`. Concurrent WSH downloader
edits are excluded from the owned ledger; their transient regex hygiene errors
are not caused by these relocations.

Final checkout validation: **1,740/1,740 fixtures pass**, including **450 benign**.
Strict `make validate` exits **2**, reporting only **170 oversized directories**.
There are **zero mixed rule/child nodes**. The concurrent WSH hygiene errors are
absent from this final run. This cohort resolves one cap violation; the overall
migration and the remaining compiled-leaf audit are still open.

# Source/array leaf retirement

The eighteen rules under `micro-behaviors/data/source/syntax/array` now live in
existing semantic leaves; its four YAML files and empty directory are removed.
There are no live YAML references to the retired namespace. The
[32-entry ledger](array-operations-mapping.json) verifies eighteen relocations
and fourteen consumer updates against current effective definitions. Atomic
predicates, scopes, platforms, criticalities, confidences, exclusions and
thresholds are preserved.

## Placement decisions

| Observation | Canonical subject | Evidence limit |
|---|---|---|
| Indexed reads and bracket chains | data/property/access | Unbound receivers need not be arrays. Commas inside quoted bracket keys do not prove array literals. |
| Repeated copies between indexed values | data/property/assign | Assignment syntax does not prove string-table rotation. |
| Addition between indexed values | data/arithmetic | Operand types are not established; addition may be numeric or concatenating. |
| Sort and fill method syntax | data/collection/array | The description states a method call; custom receiver semantics are not proven. |
| Join with a short string argument | data/string/concat | The argument is not necessarily a delimiter; path joining can have the same spelling. |
| Byte-buffer constructors and zero initialization | data/buffer/alloc | Rust's zero vector need not be byte-typed; the description no longer claims that. |
| Math.random floor scaled by a length | os/random/prng/stdlib | Computes a bounded integer; no element access is required. |
| Push/shift strings and a bracket/URL prefix | metadata/file/literal | Words and bracketed text do not establish method invocation or a literal array. |
| Bracketed long Base64-like strings | metadata/file/encoded | Presence of a representation does not establish encoding or decoding. |

The random-calculation rule differs from its siblings: one detects the general
Math.random call, one a small numeric bound, and one requires an indexing prefix.
The relocated rule uses a length-property bound but requires no indexing. The
existing empty-bytearray matcher also differs from the general bytearray call:
one requires an empty construction assigned to a name, the other a call symbol.
No predicate-equivalent rules were merged merely because their descriptions had
similar words. No new implementation-language directories were introduced.

## Consumers

Fourteen exact consumers now use the canonical destinations, including the
sort/fill proximity aggregate and the obfuscation/objective rules that previously
referenced the source leaf. Their conjunctions and thresholds remain unchanged.

The [ancestor audit](array-operations-ancestor-audit.json) found no broad source
ancestor consumers. One destination consumer uses property/assign as a generic
code alternative: `long-tail-build-config-payload` gains the indexed-copy
observation through that semantic group. It still independently requires build
configuration, a long-line observation and obfuscation. This is an explicit
consequence of using a category reference, not an assertion that its historical
set of alternatives is forever frozen.

## Verification

Four new benign ZIPs cover:

- JS collection operations and random-index calculation, plus JS/Python/Rust
  buffer construction;
- method-name, URL and Base64-like literals without corresponding operations;
- indexed object properties, copies, arithmetic and comma-containing string keys;
- Rust zero initialization by itself, so other archive members cannot satisfy
  its required buffer-allocation finding.

Seven rendered archive/member comparisons retain all findings and criticalities
modulo the ID mapping. The Rust member was not emitted in the rendered atomscan
comparison; its separate fixture verifies the internal buffer finding.

| Control | Before archive/member score | After |
|---|---:|---:|
| Literal observations | 4 / 3 | 5 / 4 |
| Indexed properties | 3 / 2 | 3 / 2 |
| Collection/buffer operations | 3 / JS 2 / Python 1 | 3 / JS 1 / Python 1 |

No comparison control reports suspicious or hostile findings. The score changes
are retained as evidence of classification effects, rather than represented as
identical weighting. Atomscan uses the installed engine; fixture validation uses
the rebuilt checkout engine from [the archive repair](ARCHIVE-VALIDATION.md).

**1,722/1,722 fixtures pass**: hostile 261, benign 432, does-nothing 175,
drop-exec 45, supply-chain corpus 572, impact-wipe 66, obfuscation 82,
reverse-shell 24 and simple-stealer 65. Strict `make validate` exits 2 solely
for **173 oversized directories**. There are **zero mixed nodes**.

| Destination | Before | After |
|---|---:|---:|
| metadata/file/encoded | 40 | 41 |
| metadata/file/literal | 9 | 12 |
| data/arithmetic | 26 | 27 |
| data/buffer/alloc | 22 | 26 |
| data/collection/array | 6 | 8 |
| data/property/access | 29 | 33 |
| data/property/assign | 6 | 7 |
| data/string/concat | 39 | 40 |
| os/random/prng/stdlib | 18 | 19 |

Logs are `/tmp/taxonomy-array-operations-{before,after}.json`,
`/tmp/taxonomy-array-operations-soft-final.log`, and
`/tmp/taxonomy-array-operations-strict-final.log`.

The remaining source/syntax siblings, runtime-indirection and retry observations,
and relationship claims in consuming composites still need auditing. The
standard-library PRNG branch is an existing destination, not a decision that
implementation layers elsewhere are acceptable. The wider cap migration remains
incomplete; this cohort removes one mixed-subject source namespace without
inventing subdivisions to satisfy a numeric budget.

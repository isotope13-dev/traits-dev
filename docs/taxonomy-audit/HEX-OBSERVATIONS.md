# Hexadecimal observations and indexing audit

Nine observations now have homes matching their evidence: four numeric/prefix
atoms and one lexical cluster in `metadata/file/literal`, two indexing forms in
`data/property/access`, binary arithmetic in `data/arithmetic`, and an icon
filename in `metadata/file/extension/identity`. The
[27-entry ledger](hex-observations-mapping.json) verifies nine relocations and
18 consumer updates against current effective definitions. All criticalities
and atomic predicates are unchanged; scopes, confidence, exclusions and
thresholds are preserved, with referenced IDs redirected where necessary.

## What the matchers establish

- `mixed-hex-decimal` detects only hexadecimal-number text. Its new name,
  `hex-number-text`, does not claim decimal operands or operations.
- `hex-string-arithmetic` observes a binary operator between two hexadecimal
  operands. It requires no string operation and now lives with arithmetic.
- Literal-key indexing and identifier-plus-hex indexing share property/access.
  Neither matcher proves that the receiver is an array, much less a decoder.
  Their predicates and thresholds differ; they are not duplicate bodies.
- `hex-byte-array-open` finds `[0x0`, which occurs in both array literals and
  indexing. `bracket-hex-zero-prefix` records only that incomplete lexical fact.
  `0x3f` and `0xff` are token observations, not encoding operations. Existing
  contextual exclusions remain intact.
- `hex-byte-decoder-constants` combines the above tokens with the substrings
  `length` and `undefined` within 4,096 bytes. It establishes neither a shared
  table nor a decoder. Its new `hex-token-length-undefined-cluster` metadata
  home preserves the full conjunction, proximity and source-map exclusion.
- `.ico` basename matching identifies a filename extension, not obfuscation or
  a validated icon format. Its original `for: [data]` scope remains unchanged.
  Relocation also removes an objective-tier exclusion dependency from the
  arithmetic capability without dropping the exclusion.

The existing literal leaf contains numeric-array and text observations, so no
language, radix or implementation layer was invented merely to accommodate this
cohort. A spelling alone belongs with lexical evidence; an actual conversion
belongs with the encoding/decoding operation. TAXONOMY.md records these boundaries.

## Consumers and scope

Eighteen consuming definitions are updated, including decoder, packed-loader,
credential-stealer and neutral exclusion rules. The three exact consumers of
the lexical cluster retain it, with their additional evidence unchanged.

The [21-consumer ancestor inventory](hex-observations-ancestor-audit.json)
covers source and destination ancestors. Generic numeric observations no longer
satisfy broad obfuscation or encoding requirements. Similarly, a basename alone
no longer supplies the structure/obfuscation branch. Most structure suppressor
consumers have JS, source or executable scopes incompatible with the icon
atom's original data scope; its three exact exclusion consumers are preserved.
The destination extension ancestor gains the filename observation. No ancestor
was silently widened with copied atoms to preserve an unsupported intent claim.

## Verification

Four new benign ZIPs cover hexadecimal constants and arithmetic, literal and
computed indexing, a bracket-prefix occurrence that is not an array literal,
and a token cluster without a decoder. Fixture assertions require the neutral
subjects and prohibit the former hexadecimal-obfuscation hierarchy.

| Control | Before archive/member score | After |
|---|---:|---:|
| Constants and arithmetic | 3 / 2 | 4 / 3 |
| Hexadecimal indexing | 4 / 3 | 2 / 1 |
| Bracket prefix used as index | 1 / 1 | 1 / 1 |
| Length/undefined token cluster | 3 / 2 | 2 / 2 |

The first three controls preserve rendered finding identities modulo the mapping
and all criticalities across six archive/member comparisons. The cluster control
retains its notable conjunction under the new metadata identity. Score changes
are recorded rather than treated as unchanged detection weights. No control
reports a suspicious or hostile finding. Atomscan uses the installed engine;
fixture validation uses the rebuilt checkout engine described in
[ARCHIVE-VALIDATION.md](ARCHIVE-VALIDATION.md).

**1,718/1,718 fixtures pass**: hostile 261, benign 428, does-nothing 175,
drop-exec 45, supply-chain corpus 572, impact-wipe 66, obfuscation 82,
reverse-shell 24 and simple-stealer 65. Strict `make validate` exits 2 solely
for **173 oversized directories**; there are **zero mixed nodes**.

| Leaf | Before | After |
|---|---:|---:|
| obfuscation/encoding/hex | 30 | 23 |
| obfuscation/code-metrics/structure | 108 | 107 |
| data/source/syntax/array | 19 | 18 |
| metadata/file/literal | 4 | 9 |
| metadata/file/extension/identity | 79 | 80 |
| data/property/access | 27 | 29 |
| data/arithmetic | 25 | 26 |

Evidence is in `/tmp/taxonomy-hex-observations-{before,after}.json`,
`/tmp/taxonomy-hex-cluster-{before,after}.json`,
`/tmp/taxonomy-hex-observations-soft-complete.log`, and
`/tmp/taxonomy-hex-observations-strict-complete.log`.

## Remaining work

The unchanged hexadecimal composites still need relationship audits. Nearby
lexical tokens, hexadecimal arguments and character-code calls do not by
themselves establish string decoding, a shared buffer, concealed host APIs or
malicious execution. Their current exact alternatives are preserved here, not
endorsed as sufficient proof of their descriptions. The source/syntax array
siblings also mix operations and lexical shapes and remain queued for migration.
The runtime-indirection/indexOf and retry/try-loop audits from the preceding
report remain outstanding. The overall 85-rule migration is incomplete.

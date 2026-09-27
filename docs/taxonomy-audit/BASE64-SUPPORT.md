# Base64: distinguish operations from supporting observations

The Base64 decoding leaf contained 90 rules. Its nearest siblings included
`decode/symbol-base64`, `decode/encoded/formats`, `decode/table` and
`encode/base64`. Reading their matcher bodies exposed observations that did not
establish an encoding or decoding direction. The [13-entry ledger](base64-support-mapping.json)
records this first migration tranche; it is not a completed sibling consolidation.

## Placement contracts and changes

`TAXONOMY.md` now explicitly distinguishes direction-specific codec APIs from
imports, alphabet constants and file-output methods. It also removes the older
contradictory guidance that placed `import base64` under encoding.

Eleven observations move to existing leaves:

- Five alphabet observations, including the JavaScript roll-up, belong in
  `metadata/file/string/charset`. The full validator exposed an additional
  baseline alphabet matcher in `encode/base64` that the normal scan display
  omitted; it follows the same contract. Text/substr and parsed-literal variants
  retain their distinct scopes, confidence and criticality. They are not claimed
  to be equivalent matchers.
- Five Python, Perl and Ruby imports move to `metadata/import/package`.
  The module supplies both directions, so the import cannot choose encode or
  decode. Static imports, dynamic imports and require calls retain their exact
  predicates, scope, exclusions, confidence and criticality.
- Apple's `writeToFile_atomically_` symbol moves to `fs/write/file/full`. The
  method writes NSData contents regardless of how those contents were obtained.
  Its unrelated decode ATT&CK annotation is removed. The AppleScript conjunction
  is renamed/described as decode plus file-write API presence; it does not prove
  that decoded bytes flow into the write. Its matcher is unchanged and its
  dropper consumer follows the new ID.

All exact consumers follow the moved IDs. The `base64-decoding` aggregate also
loses its three explicit import/alphabet alternatives. Its symbol-directory
alternative no longer includes the moved import and write atoms. The other
consumer of that directory, Solana control retrieval, likewise no longer accepts
an import or generic write as its decode evidence. These are deliberate semantic
corrections, not claimed predicate-equivalent aggregate replacements. No API-call
or transformation matcher was removed to meet the cap.

## Verification

Three benign archives distinguish:

1. Stored alphabet constants and imports only: require charset/import metadata;
   forbid the entire encode and decode hierarchies.
2. Actual Python, Perl, Ruby and JavaScript decoders: require decode; forbid encode.
3. Actual Python encoding: require encode; forbid decode.

Before the correction, the import-only Perl, Python and Ruby members and the
alphabet-only JavaScript member all produced decoding observations; Python also
produced an encoding import observation. The corrected controls preserve neutral
metadata without claiming either transformation. The last measured scan scores
were 9 for support-only, 8 for decode operations, and 4 for encoding. Score caps
are 15, 15 and 10 respectively. The AppleScript method move is checked through
predicate/scope equality and updated consumers, not claimed to be exercised by
these four-language controls.

The full soft suite passes **1,670/1,670 fixtures**, including all existing hostile
and supply-chain cases. Strict `make validate` now fails only on **175 oversized
directories**, down from 176. All 13 ledger destinations/effective definitions
verify; no stale moved IDs remain in dependencies and no mixed rule directories
exist. Counts after this tranche:

| Leaf | Rules |
|---|---:|
| `data/decode/base64` | 84 |
| `data/decode/symbol-base64` | 19 |
| `data/encode/base64` | 63 |
| `metadata/file/string/charset` | 12 |
| `metadata/import/package` | 62 |
| `fs/write/file/full` | 75 |

No new taxonomy level, overflow bucket or directory exemption was required.

## Remaining sibling audit and next tranche

The main leaf now fits the cap, but the cohort is not semantically finished:

- `symbol-base64` is still an evidence-backend partition. Consolidate its 19
  actual observations by meaning, coordinating broad directory references rather
  than replacing them with a wider set without review. Joining it blindly to the
  84-rule leaf would merely create another violation.
- MSXML `nodeTypedValue`, DOMDocument construction and a chosen `Base64Data`
  element name do not independently establish Base64 decoding. Assign generic
  XML operations to their operations; keep a decoder claim only when direction
  is established. A `bin.base64` type designation can support conversion in
  either direction.
- The computed Buffer-call shape does not require the word Base64, and
  `JSON.parse(Buffer.from(...))` does not require a Base64 argument. Their homes
  and descriptions must follow the actual call/parse observations.
- The Perl `%06b` formatter and generic shift/OR patterns need bit/string-operation
  classification or additional codec evidence; their names alone cannot establish
  Base64 reconstruction.
- `decode/encoded/formats` repeats the format partition at an extra level and
  includes Base16, Base32, ASCII85 and Base64. Move each to its encoding subject,
  after resolving broad aggregate consumers. `encoded/capability` also mixes
  decoding, decompression and deserialization and needs a separate claim audit.
- Several neighboring custom-alphabet and encoding rules classify constants,
  codec construction or data presence as a directional transform. Apply the same
  direction contract consistently across `encode/custom`, `decode/table` and
  `encode/base64`; do not repair this by choosing one arbitrary direction.

Validator review candidates include scoped prefix/subsumption overlap:
`base64.StdEncoding.Decode` searched as a substring also accepts `DecodeString`,
and the Perl bare-symbol and call-kind decoder predicates overlap without being
identical. Such cases need scope/kind-aware review, not automatic merging solely
because names or descriptions resemble each other. The earlier interactive-shell
flag overlap is the analogous risk for `needs` counts.

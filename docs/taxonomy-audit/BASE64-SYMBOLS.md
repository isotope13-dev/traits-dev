# Base64 matcher-backend consolidation

`decode/symbol-base64` classified evidence by matcher backend rather than
technique. Its 19 observations now live in `decode/base64`; five equivalent Go
API variants share one predicate, leaving **85 combined rules** in that leaf.
No exemption or new implementation-specific directory was added.

## Coverage decisions

Thirteen relocated observations retain their complete effective definitions.
The compiled-Go observation now requires the `encoding/base64.(*Encoding)`
receiver rather than generic `.DecodeString`, `.DecodedLen` or `AppendDecode`
text. Compiled standard-library hexadecimal decoding reproduced the old false
Base64 finding; the new matcher rejects it and retains actual Base64 decoding.
It also recognizes the same package's `Decode` method. This is an intentional
identity correction, not a claim of equivalent byte-pattern coverage.

The five Go source predicates share scope and meaning. Their consolidated regex
is the union of the former substring predicates, including the existing broad
suffix behavior. A 75-spelling comparison checks standard/raw/URL receivers,
decode and non-decode method names, and package prefixes against that union.
No new Go algorithm or method variant is inferred from a generic method name.

Three objective consumers formerly selected only
`std-encoding-decode-string`: Go XOR string recovery, filesystem websocket
tasking, and the Slack implant. Their decoder leg now accepts the equivalent
raw/URL and byte-buffer variants too. This deliberately improves variant
coverage; their other conditions and scope are unchanged. The steganographic
loader already accepted all five variants and retains that union without
redundant alternatives. These tests do not prove the broader intent/data-flow
claims of these consumers, which remain separate audit work.

Old subtree references are expanded into **15 named alternatives**, preserving
the former subset. In the Base64 aggregate these are flattened into `any`.
The Solana consumer retains its four other required observations and uses the
same named alternatives in its top-level `any`. No parent-level alias or
self-referential Base64 umbrella was introduced. Existing consumers of the
broader `decode/base64` directory now also see the migrated Base64 observations;
this is the intended effect of removing an artificial backend partition.

The [156-entry ledger](base64-symbols-mapping.json) records the 19 original
observations and 137 updated consumers. Every after-definition verifies against
current YAML. It records the five-to-one merge explicitly rather than pretending
that each consumer kept a distinct decoder identity.

## Validation

Two new archives contain a compiled hexadecimal reader, a compiled Base64 reader,
and source examples for all five merged API forms. They were built with the
local Go toolchain using only standard-library dependencies and were never
executed. All ten archive/member exact-ID checks pass: the hexadecimal examples
have no Base64 finding; each source variant has the merged decoder observation;
the compiled decoder retains its package-qualified finding. Archive scores are
6 for hexadecimal operations and 7 for Base64 operations, within caps of 15.

**1,681/1,681 fixtures pass.** The ledger verifies 156 entries, and all 13 pure
relocations preserve their effective definitions. There are zero mixed rule
directories. Strict validation still reports **175 oversized directories**
elsewhere; Base64 is exactly at its inclusive limit of 85.

Logs: `/tmp/taxonomy-base64-symbols-before.json`,
`/tmp/taxonomy-base64-symbols-after-final.json`,
`/tmp/taxonomy-base64-symbols-soft-final.log`, and
`/tmp/taxonomy-base64-symbols-strict.log`.

## Remaining audit work

The generic DOM siblings identified in the XML report remain open. Other
Base64 predicates still deserve precision review: the Python short-function
wrapper regex establishes proximity rather than returned decoded data, and the
JavaScript Buffer argument matcher should distinguish encoding-position evidence
from a string value in another argument. Consolidation is not a blanket claim
that every decoder predicate or objective consumer is precise.

Useful validator diagnostics include overlapping API-variant predicates,
redundant alternatives introduced by consolidation, and objective consumers
whose supposedly distinct legs collapse to one canonical observation. The
existing directory-over-trait check caught a newly redundant decoder alternative
in the encoded-C2 configuration consumer; that alternative was removed.

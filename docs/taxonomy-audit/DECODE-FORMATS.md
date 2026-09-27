# Retiring the mixed encoded-data branch

`data/decode/encoded/formats` repeated the format classification one level below
its proper location. Its sibling `encoded/capability` combined decoding with
string assembly, decompression and object deserialization. Neither represented
a distinct decoding technique. The [ten-entry ledger](decode-formats-mapping.json)
records six moves, retirement of the umbrella and changes to its three consumers.

## Classification

All destinations already existed; no extra taxonomy level or overflow leaf was
needed:

| Observation | Canonical home |
|---|---|
| Base16 decoder reference | `data/decode/hex` |
| Base32 decoder reference | `data/decode/base32` |
| ASCII85 decoder reference | `data/decode/base85`, beside Z85 |
| Standard and URL-safe Base64 decoder references | `data/decode/base64` |
| Join expression containing a decoder call | `data/string/assembly` |

The six matchers retain their effective predicates, scopes, confidence,
criticality and exclusions. Descriptions now distinguish a symbol reference from
proof of invocation, and the join rule states the expression it matches rather
than promising that every joined value is decoder output. Its fragment-rebuild
consumer follows the renamed observation. Base32 shell-loader and URL-safe
mailbox consumers follow the new format-specific IDs.

`TAXONOMY.md` records the format-family and operation boundaries and closes
`decode/encoded`. Every remaining rule still lives in a leaf; no alias or parent
umbrella remains in the retired branch.

## Umbrella consumers

Three Python objective composites consumed `python-decode-capability`:
`python-single-line-decoder`, `python-decode-decrypt-dynamic-exec`, and
`execute-decoded-content`. Each now contains the helper's 13 named alternatives
in its own `any` clause. These include the six former format-directory members,
Base64/Base58/uu/hex observations, bzip2/zlib decompression and marshal loading.

All three consumers are Python-only with the same Unix/Windows platform scope
as the old helper. Their other conditions, exclusions and criticalities remain.
This preserves the Boolean alternatives without classifying decompression or
marshal deserialization as one encoding algorithm. Reusing named observations
is appropriate; copying matcher bodies or keeping a taxonomy leaf solely as a
composition shortcut is not.

The proximity-bounded consumer now evaluates direct alternatives rather than a
nested helper's collected evidence span. That is not claimed to preserve every
span-grouping detail. Existing positive and negative fixtures still pass. These
changes also do not prove the consumers' stronger execution descriptions: their
existing intent and flow assumptions remain separate audit work.

## Verification

A new benign archive exercises all five format-specific APIs and the join
expression. Exact-ID inspection confirms all six relocated observations, rather
than relying solely on shared prefixes. The archive and member score **7**
(previously 6), within the cap of 15. It requires every destination hierarchy and
forbids the retired branch.

The full soft suite passes **1,674/1,674 fixtures**, including all existing hostile,
obfuscation and supply-chain tests. Strict `make validate` still fails only on
**175 oversized directories**. All ten ledger entries verify against effective
current definitions and references. The only remaining retired-prefix mention
in executable fixtures/rules is the new negative expectation. There are zero
mixed rule directories.

Destination counts are Base64 82, Base32 7, Base85 2, hex 51 and string assembly
23. All remain within the 85-rule combined cap. The decoder observations move
from four levels below the tier to three, improving breadth without losing their
format or operation distinctions.

The `symbol-base64` partition and the XML/computed-codec observations documented
in the earlier cohort reports still need migration. The overall cap audit is
not complete.

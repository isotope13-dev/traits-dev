# Mnemonic representations, recovery interfaces, and theft

This pass moves **77 rules** and resolves the 91-rule mnemonic objective leaf:
`objectives/credential-access/wallet/mnemonic` now contains **46 rules**. Thirty
observations leave the blockchain-library layer, which retains **63 rules** for
review. Every receiving directory remains a strict leaf within 85.

The [move manifest](mnemonic-moves.csv) records every destination and normalized
definition hash. Moved matchers, effective scopes, confidence, criticality,
exclusions, proximity and ATT&CK settings are preserved. [18 descriptions](mnemonic-labels.json)
are clarified. No identical atomic matcher body touching a moved rule required
merging; the remaining duplicate private-key observations are discussed below.

## Placement contracts

The new `crypto/mnemonic` leaf has **41 rules** spanning phrase vocabulary,
wordlists, generation, validation, assembly and provisioning. It does not require
key derivation or ledger activity. BIP-39 treats mnemonic construction and seed
derivation as separate steps; this supports keeping the mnemonic representation
outside a KDF-only branch. See the [BIP-39 specification](https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki#generating-the-mnemonic)
and [the authoring contract](../../TAXONOMY.md#mnemonic-key-material-and-recovery-interfaces).

The boundary follows the actual claim:

- Private-key/WIF representation, wallet keypair generation and hierarchical
  derivation paths → `crypto/asymmetric/key` (**57**). A roll-up accepting either
  phrases or keypairs cannot be labeled phrase-only generation.
- PBKDF2 rounds identifier → `crypto/kdf/algorithm` (**24**). A bare wordlist
  member → `data/collection/wordlist` (**1**); an ordinary dictionary is not
  necessarily mnemonic handling. The composite requiring mnemonic class,
  wordlist and PBKDF2 context does support that narrower capability.
- Seed-word grids, recovery labels/textareas, entry forms and invalid-phrase
  messages → `ui/controls/wallet` (**29**). Phrase assembly stays in mnemonic.
- Ethereum keystore filename → `fs/path/wallet` (**7**). A fixed Ethereum address
  assignment → `data/format/crypto-address` (**31**). Neither is theft.
- An asymmetric-encryption helper with no required algorithm →
  `crypto/asymmetric/encrypt` (**1**), alongside algorithm-specific siblings.

Filenames/platform scope remain implementation details. Native and source
wordlists share the same mnemonic leaf. No rule is copied into an ancestor,
and no cap exemption or additional depth is used.

## Consumers and intentional changes

The [consumer audit](mnemonic-directory-consumers.csv) covers **33 affected
references in 30 consumers**. Exact references follow all moved rules.
[Five explicit repairs](mnemonic-consumer-repairs.json) preserve relevant evidence
without replacing a former directory with a whole broader destination:

1. The source-marker and profiled-HTTP collector retain **15** former directory
   members each: phrase terminology, private-key format/material and keystore
   location clues. Their thresholds, scopes, proximity and other conditions
   are unchanged. Each retained ID is proven to be an existing alternative.
2. Sensitive-file targeting retains the moved keystore filename explicitly.
   Local recovery UI/phrase assembly stops supplying multiple file-targeting
   findings through the wallet directory. The same local JavaScript control
   matched the file-target marker before this migration and does not afterward.
3. The paste-site encrypted-upload classifier retains the asymmetric-encryption
   helper. Wordlists and recovery UI do not establish payload encryption.
4. The ransom-banner atom loses its blanket mnemonic-objective exclusion.
   Merely handling seed phrases, or exhibiting wallet theft, does not exempt a
   program from an independently matched ransom demand. Other exclusions remain.

The old standard-library exclusion and service-with-HTTP/crypto classifier lose
moved observations through `crypto/library`. They are not widened to all crypto
or mnemonic operations. This is an intentional boundary change; both remaining
classifiers need review of their actual identity/intent claims. Keeping an old
implementation container's membership is not itself a detection requirement.

## Verification and limits

The preservation proof protects **147 definitions**, allowing the five recorded
consumer changes and description edits. It preserves the moved matchers and
settings. Its fresh baseline has **118,817 rules**; the later proof has **118,814**,
with **15 outside changes** recorded separately in
[the concurrency record](mnemonic-concurrent-changes.json).

**84 focused assertions across 28 files pass:** 42 in 13 new controls, including
one separately run before/after local-file-target assertion, plus 42 in 15
established blockchain controls. Tests cover local phrase handling versus
transfer, mnemonic versus generic dictionaries/PBKDF2, retained WIF/source
clues, keypair versus phrase generation, and the existing 4 KB weak-PRNG
proximity boundary. See [the runnable controls](../../testdata/taxonomy/mnemonic/README.md).

All **1,841 corpus fixtures** pass in a temporary copy restoring only the
pre-existing shell-decoder definition, with no excluded files/fixtures. The
[isolation record](mnemonic-validation-isolation.json) states both definitions.
The live tree still fails the unrelated PyAigis shell-decoder check. Strict
validation reports **107 diagnostics** and **145 over-cap directories** at its
checkpoint; concurrent work and the rebuilt engine are included. No diagnostic
in that run names a moved rule. This does not certify the remaining catalog.

The new crypto leaf is registered in cleave's directory whitelist. The release
engine was rebuilt against the existing local filefacts/stng working copies,
using the same dependency configuration as the preceding audit. No analyzer
logic was changed. The [verification manifest](mnemonic-verification.json)
records the build and validation commands and checkpoint counts.

One focused test exposed an existing fetch limitation: `fetch(names)` misses the
HTTP leg when `names` holds the wordlist path. The existing matcher accepts
literal arguments and selected URL-like names. The positive control uses a
literal; the matcher was not relaxed to make the fixture pass. The wordlist-fetch
composite observes proximity, not proven data flow to that same URL.

## Remaining dispositions and validator opportunities

The 46-rule objective leaf still mixes genuine theft, recovery UI with generic
private-key alternatives, brand catalogs, and six export classifiers. Review
those claims and route complete source exports to `exfiltration/stealer/wallet`;
do not force optional brand or UI evidence into a mnemonic-specific subtype.
Generic private-key entry is not inherently a wallet interface.

Three rules remain in the old wallet leaf: a broad wallet/keystore/phrase OR,
a generic seed-named validation function, and returning an uppercase
wallet/recipient/address-named constant. None justifies a mnemonic-only home.
The remaining client, transaction, brand and exchange cohorts retain their
previous explicit review requirements.

The source and compiled private-key-reference atoms have identical matcher
bodies but different scopes and confidence (0.85 versus 0.8), and inherited
objective metadata differs. Report them as a consolidation candidate; do not
silently flatten their settings or broaden a consumer's accepted file types.
The validator should distinguish identical bodies from definition-equivalent
merge candidates. Directory expansion can also let two local UI observations
satisfy a supposedly multi-source/file-target threshold: review subject diversity
and required operations, not just the numeric `needs` value.

The complete taxonomy migration remains open.

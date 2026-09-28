# Blockchain operations and library exclusions

This pass moves **87 rules** out of `micro-behaviors/crypto/library/blockchain`,
leaving **93** for further review. Query and rewards no longer have rules under
that implementation layer. All receiving directories remain strict leaves with
at most 85 combined rules; no exceptions or extra depth are introduced.

The [move manifest](blockchain-moves.csv) records destinations and normalized
hashes. Moved matcher bodies, effective scope, criticality, confidence, exclusions
and ATT&CK settings are preserved. [17 descriptions](blockchain-labels.json)
are clarified without claiming execution from a reference. No identical atomic
matcher body touching a moved rule was found in the catalog comparison.

## Operation ownership

The contracts are in [TAXONOMY.md](../../TAXONOMY.md#ledger-operations-and-wallet-evidence).
Transaction construction, authorization, signing, submission and result
interpretation have distinct sibling leaves. The boundary matters: an ERC-20
permit field is authorization data, not evidence that signing occurred; an OR
accepting message signing is generic signature capability, not transaction-only
signing. A required submission takes precedence over its preparatory steps.

Account-state queries join `communications/blockchain/client`; offline keys
remain crypto. Explorer/RPC URLs join the existing URL/RPC leaf, while a price
API goes to ordinary endpoints. HTTP payment headers/resource interfaces follow
HTTP payment services. Recovery/reward prompts follow wallet UI controls.
A seed-file path follows wallet paths, and a passphrase variable follows secret
environment names. None of these observations identifies the analyzed file as
an independent library artifact.

## False-negative repair

Before this pass, a Python program containing host-information APIs, browser
password evidence, `wallet.dat`, and an eligible HTTP upload did not report the
wallet source or the multi-source profiler. `wallet.dat` matched the source,
but a component matching the bare word `wallet` also matched an ancestor used
as a blanket library exclusion. The same mechanism hid ordinary command
execution and pickle deserialization in a file containing that word.

**34 blanket blockchain-directory exclusions are removed.** This is an
intentional coverage change, not matcher-preserving relocation. Other explicit
exclusions remain; no entire destination is substituted as a new exemption.
The [repair record](blockchain-consumer-repairs.json) contains exact before/after
conditions. Positive and local-only controls distinguish the restored wallet
source from an export; a bare wallet word still does not satisfy that source.

One additional repair completes the preceding HTTP-upload migration: AD RMS
cache harvesting listed both the ZIP directory and its moved Compress-Archive
member in the same `any` clause. The exact member is redundant and was removed.
There is no `needs` threshold; proximity and all other conditions are unchanged.
Archive-positive and paths-only controls pass.

The [directory-consumer review](blockchain-directory-consumers.csv) covers
**70 affected references in 66 consumers**. Noncryptographic endpoint/UI/ledger
facts stop counting as cryptographic evidence through their old ancestor;
keys, hashes and generic signatures retain crypto membership. New members
contribute to their documented capability subjects. Explicit references are
updated to their exact relocated IDs.

## Verification

The preservation proof protects **204 definitions**, allowing only the recorded
35 consumer repairs and description changes. The catalog remains **118,811
rules** before and after; no outside definition changes occurred during that
proof interval. Every receiving leaf remains within 85 and strictly leaf-only.

**57 focused assertions across 19 files pass:** 42 assertions in 15 new controls,
plus 15 established assertions in four HTTP/source controls. The pre-change
wallet regression was reproduced with the real engine. Fixtures are scanned,
never executed; see [the fixture instructions](../../testdata/taxonomy/blockchain/README.md).

All **1,841 corpus fixtures** pass in a temporary copy restoring only the
pre-existing shell-decoder definition documented in the
[isolation record](blockchain-validation-isolation.json). No files or fixtures
are excluded. Live soft validation still fails the PyAigis shell-decoder check;
the repository decoder was not changed. Strict validation reports **91
diagnostics**, including **146 oversized directories**. No engine changes or
new whitelist entries were required. Detailed counts and commands are in the
[verification manifest](blockchain-verification.json).

## Remaining review

The 93 remaining rules are not endorsed by their current placement:

- Wallet (29): mnemonic/wordlist validation and generation, generic wallet
  terminology, address constants and a lightwallet reference need separate
  key-material, interface and format dispositions. A wordlist is not a client.
- Client (22): imports/symbol references, mixed signing fragments, daemon
  configuration, mnemonic implementation and mathematical context roll-ups
  need narrower claims. An endpoint OR cannot certify a read-only client.
- Transaction (13): provider imports, maximum integers, amount conversion,
  contract-address derivation, staking context and a privacy/payment-wrapper OR
  require separate review; do not force them into a transaction subtype.
- Brand-wallet (7), DeFi-platform (5), DeFi-protocol (1), exchange (16): brand
  references and client/provenance facts are mixed. A brand reference may support
  probable interface use but is not proof that the file is that application.
  Several exchange atoms (`Entry`, `ConstructorArgs`) need contextual review.

Validator opportunities: flag broad capability directories used as artifact-
identity exemptions; detect an exclusion whose primitive overlaps a required
source and can self-suppress it; retain identical-body and covered-alternative
checks, while separately reviewing semantic overlaps and differing scopes.
A directory name alone cannot decide whether an exclusion is valid.

The global cap and semantic migration remain unfinished.

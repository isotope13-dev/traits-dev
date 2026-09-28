# Encrypted-staging crypto API observations

The `dual-crypto-fallback.yaml` cohort was filed under encrypted payload
staging even though its own comment said it did not establish staging. It
detected Python cryptography imports near BCrypt or libcrypto references, plus
several API-name strings. None of these matchers required conditional control
flow or linked decryption to a payload.

Moved the 13 rules to `micro-behaviors/crypto/native/python.yaml`. The new leaf
describes probable crypto API capability. Descriptions and IDs now call out
references/co-occurrence rather than asserting a fallback was selected or a
payload was staged. Matcher bodies, scopes, criticalities, confidence,
exclusions, and downgrade conditions are preserved. No outside rule referenced
the old IDs; the one former fully qualified local reference is now local.

| Former ID | New ID | Disposition |
|---|---|---|
| `dual-crypto-bcrypt-fallback--rx-3` | `bcrypt-name-reference` | Move and rename; matcher retained |
| `dual-crypto-libcrypto-fallback--rx-6` | `ctypes-cdll-reference` | Move and rename; matcher retained |
| `bcrypt-cng-direct-usage--rx-9` | `bcrypt-open-provider-name-reference` | Move and rename; matcher retained |
| `bcrypt-cng-direct-usage--rx-10` | `bcrypt-generate-key-name-reference` | Move and rename; matcher retained |
| `bcrypt-cng-direct-usage--rx-11` | `ctypes-bcrypt-load-reference` | Move and rename; matcher retained |
| `bcrypt-cng-direct-usage--rx-12` | `bcrypt-encrypt-name-reference` | Move and rename; matcher retained |
| `bcrypt-cng-direct-usage--rx-13` | `bcrypt-decrypt-name-reference` | Move and rename; matcher retained |
| `bcrypt-cng-direct-usage--rx-14` | `ctypes-bcrypt-library-reference` | Move and rename; matcher retained |
| `stager-grade-crypto-stack` | `python-crypto-provider-cooccurrence` | Move and rename; unsupported staging claim removed |
| `dual-crypto-file-level` | `python-cryptography-bcrypt-file-cooccurrence` | Move and rename; capability wording corrected |
| `dual-crypto-bcrypt-fallback` | `python-cryptography-bcrypt-cooccurrence` | Move and rename; fallback claim removed |
| `dual-crypto-libcrypto-fallback` | `python-cryptography-libcrypto-cooccurrence` | Move and rename; fallback claim removed |
| `bcrypt-cng-direct-usage` | `bcrypt-cng-api-reference` | Move and rename; reference wording corrected |

This removes an unrelated capability cohort from the oversized
`objectives/command-and-control/dropper/staging/encrypted` directory. It does
not reduce that directory to the cap; additional cohorts still require
individual review. The new `crypto/native` contract is documented in
`TAXONOMY.md`: native provider/API references without a supported narrower operation
belong there, while algorithm-specific evidence belongs under that algorithm
and package declarations or artifact identities remain metadata or
`well-known/lib/`, respectively.

Verification: the full soft fixture suite passes **1,837/1,837**. The
`crypto/native` whitelist is present in
`../cleave/src/capabilities/validation/directory_whitelist.rs`. I rebuilt the
validator against the sibling `filefacts` working tree using a one-command
Cargo patch; no manifest change was needed. `make validate` now reports the
same **60 strict issues** and **165 over-cap directories** as the established
baseline, with no unknown-subdirectory error for this leaf.

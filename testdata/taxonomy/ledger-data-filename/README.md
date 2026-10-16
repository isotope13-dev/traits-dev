# ledger-data-filename controls

`native-hardware-wallet-brand-family` matches the brand word `Ledger`
case-insensitively, which also hits accounting-style data filenames such as
`ingestion-ledger.json`. A file-scoped `unless:` quiets the atom when a
ledger data filename (`ledger.` plus a data extension) is present; the trait
regex engine has no lookaround, so span-level `not:` cannot see the
extension.

Fixtures are compiled binaries; sources and `build-controls.sh` document
provenance. Fixtures are scanned, never executed.

- `positive/brand-refs`: Ledger Live and Trezor references, no data
  filename. The atom fires.
- `near-miss/ledger-data-file`: only `ingestion-ledger.json`. The atom
  stands down.

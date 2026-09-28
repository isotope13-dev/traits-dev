# Wallet source routing controls

Run `python3 scripts/check-desktop-wallet-routing.py` from the repository root.
Fixtures are copied outside the test-data tree and scanned, never executed.

The controls distinguish wallet data locations from installed applications,
application references from sensitive-file selectors, generic DPAPI and Telegram
vocabulary from wallet targeting, local secret UI from probable export, and
private-key export from required wallet-seed export. Error text does not establish
a repeated harvest. Existing mnemonic and blockchain controls check relocated
seed exporters and the wallet-aware host profiler.

`secret-local.js` matched the old desktop-wallet target selector in the pre-batch
snapshot, despite containing no wallet-specific clue. It must not match that
selector after relocation. A Telegram send activates generic credential export.

See `docs/taxonomy-audit/desktop-wallet-verification.json` for the checked run and
shared-tree validation limitations.

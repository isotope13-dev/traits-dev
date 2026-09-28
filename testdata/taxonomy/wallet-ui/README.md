# Credential UI and application-context controls

Run `python3 scripts/check-wallet-ui-routing.py` from the repository root.
The twelve fixtures provide 41 finding assertions and are scanned, never executed.
Copies outside the test-data tree avoid fixture-path suppressors.

Controls distinguish generic private-key entry from actual export, product catalogs
from file targets, generic application paths from named wallet process termination,
concealed-window interference from secret export, and LaunchAgent/UI vocabulary
from malicious persistence. Keypair/wallet filename controls preserve file-target
consumers. Phantom/TronLink references must no longer suppress unrelated ActiveX
and script-loader observations as known benign artifacts.

The two broad-exclusion cases inspect normal JSON scan findings with an explicit
component-level output floor; the remaining cases use `test-rules`. This avoids
an expensive debugger trace through every unmatched known-artifact member.
The hostile Ledger seed-export and benign BIP39 documentation corpus fixtures
add four exact exporter assertions, recorded in the audit verification file.

# Credential-record neighborhood

The `credential/record` leaf held 91 rules. This review moved 22 by the item
or combined activity they require, leaving 69 rules in that leaf:

- Nine browser login-store and record rules moved to `credential/browser-record`.
- Seven keychain or keyring-container rules moved to `credential/keyring-record`.
- Four wallet keyring rules moved to `credential/wallet-record`.
- A bound query for Chromium's `password_value` moved to
  `credential/value/password`.
- The rule requiring both browser credential targeting and keyboard capture
  moved to `stealer/multi-item`.

The JVM query that allows either browser cookies or login records remains in
`record` pending a separate split: cookies are not necessarily credentials.
The remaining record rules also need claim-by-claim review. The selected rules'
predicates, effective defaults and severities are recorded in [moves.json](moves.json),
and exact consumers were retargeted. No YAML directory reference selecting the
old `record` leaf was found; broader exfiltration references still contain all
relocated rules. Run `uv run docs/taxonomy-audit/taxonomy/credential-record-neighborhood/check-moves.py` to repeat the comparison and capacity check.

A focused `cleave test-rules` check matched the relocated Chromium password
query on `testdata/hostile/generated/registry-second-review-three/browser-upload.py`.
It did not match the corresponding `browser-unrelated-upload.py` control,
where the browser query and health upload are separate.

`make validate` passed all 13,920 fixtures: 1,927 hostile, 1,774 suspicious,
8,883 notable and 1,336 baseline.

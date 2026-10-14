Extraheader existence checks are not token reads
==================================================

`gha-checkout-extraheader-read` fired on release CI that only asks whether
checkout auth exists (`git config --get-all ... >/dev/null`, exit status
decides whether to mint a fresh token). The token value never leaves git.
The trait now carries a second assertion exclusion alongside the existing
`wc` one: output to `/dev/null` is a presence check, not a read.

Run `python3 testdata/gha-extraheader-existence-check/check.py
<scratch-directory>`. `token-exfil-positive.sh` must report the trait;
`existence-check-negative.sh` must report no suspicious trait.

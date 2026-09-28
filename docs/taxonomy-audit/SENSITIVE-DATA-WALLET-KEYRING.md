# Wallet keyring source classification

Moved the seven-rule wallet-keyring group from generic
`objectives/exfiltration/sensitive-data` to
`objectives/exfiltration/stealer/wallet`. The matcher body, rule IDs, scopes,
criticalities, confidence and file defaults are unchanged. The group requires a
serialized wallet keyring in an HTTP request and distinguishes upload before
local encryption/sealing. The wallet is the defining stolen source; HTTP and
encryption order describe the channel and sequence.

No exact-ID consumer referenced these local rules. The shell-history classifier
accepts either the broad `stealer/` subtree or legacy `sensitive-data/`; the
moved group remains in the former subtree, so its union is unchanged. The
wallet-source leaf rises from **41 to 48** rules. Generic `sensitive-data`
falls from **141 to 134** and remains over the 85-rule cap, so this is a
source-placement improvement rather than a completed cap fix.

An exact YAML comparison confirms that all seven definitions are preserved.
The controlled corpus passes **1,842/1,842 fixtures** with no exclusions. The
refreshed full-tree inventory is in the [current audit snapshot](snapshot-2026-09-28-post-http-source/).

# Melcuratts role migration

The named package fetches Python source and executes it as a module. Its
family rule moved unchanged from `well-known/malware/supply-chain/melcuratts`
to `well-known/malware/dropper/melcuratts`, reflecting the payload-loading
role. No YAML consumer of the old namespace was found.

Both synthetic fixtures contain the same remote-source loader. The positive
adds two implementation-specific markers; the near miss has only one. A
Cleave scan matched the moved family rule only on the positive, while both
reported the independently meaningful remote-loader behavior. The fixtures
are scanned as data and are not executed.

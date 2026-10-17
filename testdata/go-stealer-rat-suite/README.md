# Go stealer suite and SOCKS tasking

Two hostile composites for Go malware built on routine-name symbols,
which survive packing that hides strings:

- `go-keylogger-screen-browser-stealer-suite` (collection): a Go
  `main.runKeylogger` routine plus `main.Steal`, `main.sendScreen`, and
  a Chromium master-key routine. The quartet is a stealer toolkit, as
  seen in the Salat family.
- `go-socks-proxied-task-loop` (tasking): a Go `main.p2pSocks` routine
  plus a SOCKS5 reference, a `main.tloop` task loop, and a C2 handler
  label. The quartet is proxied RAT tasking.

## Controls

`verify.py` builds minimal PE32 fixtures over 3MB (the symbol legs
carry a 3MB size gate) with marker strings in .text and scans them with
`cleave --traits-dir`:

- `suite-positive.exe`: the full stealer quartet. Must report only the
  suite hostile.
- `suite-negative.exe`: quartet minus the master-key leg. Must report
  neither hostile.
- `socks-positive.exe`: the full tasking quartet. Must report only the
  tasking hostile.
- `socks-negative.exe`: quartet minus the C2 label. Must report neither.

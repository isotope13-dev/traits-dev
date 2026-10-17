# IoT ARM XMRig stager

`staged-arm-xmrig-stratum-miner` (hostile) convicts an ELF that stages
the stock `xmrig-arm` release next to a `stratum+tcp://` pool endpoint
and the `--donate-level` CLI flag. That triple is how IoT botnets carry
their miner stage: the release name, pool URL, and donate flag sit in
packed string tables (e.g. `tcp-stompxmrig-armMemTotal:`) where the
word matcher for `xmrig` finds no boundary and the `.text`-scoped
`donate-level` matcher cannot see them, so the JSON-config and wallet
composites miss while the miner invocation is real.

## Controls

`verify.py` builds minimal ELF32 ARM fixtures with marker strings in
`.rodata` and scans them with `cleave --traits-dir`:

- `miner-stage-positive.elf`: all three markers. Must report
  `staged-arm-xmrig-stratum-miner`.
- `miner-name-only.elf`: the release name alone. Must not report it.
- `pool-without-miner.elf`: pool URL plus donate flag, no miner name.
  Must not report it.

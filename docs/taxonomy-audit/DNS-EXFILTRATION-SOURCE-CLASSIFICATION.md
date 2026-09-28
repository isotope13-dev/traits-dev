# DNS exfiltration source classification

The over-cap `objectives/exfiltration/dns/tunnel` leaf mixed DNS transport
techniques with classifiers that already required a particular stolen source.
The taxonomy now routes those source-specific chains to the corresponding
`stealer/<source>` child; DNS remains the transport evidence in each matcher.

Eighteen source-specific definitions moved with their effective matchers and
settings preserved:

- AWS and `.netrc` credential exports, including their Zig source fragments,
  now live in `stealer/dev-secret`.
- Alternative credential-source export through DNS case encoding lives in
  `stealer/credential`; the alternatives do not establish multi-source theft.
- A native DNS packet tunnel accepting one of several identity/credential-file
  sources lives in `stealer/file`; its `any:` sources do not prove multiple
  datasets were stolen.
- OpenBSD master-password-file exports and the OpenWrt `/etc/passwd` exporter
  live in `stealer/account-db`.
- The Go rule accepting either an SSH-key marker or Windows credential-manager
  enumeration lives in `stealer/credential`; the PE classifier requiring the
  SSH-key source lives in `stealer/ssh`.
- Two JavaScript DNS-label exporters require both `whoami` and hostname
  evidence. They now live in `stealer/system-info/identity`; the DNS method
  and resolver address are transport details.

Current counts are **100** in `dns/tunnel`, **83** in `stealer/dev-secret`,
**42** in `stealer/credential`, **70** in `stealer/file`, **44** in
`stealer/account-db`, **21** in `stealer/ssh`, and **38** in
`stealer/system-info/identity`. Every receiving leaf is within the current
100-rule cap. No exceptions were added.

The follow-up DoH audit moved provider endpoint indicators and their notable
endpoint aggregate from the exfiltration leaf to
`micro-behaviors/communications/dns/doh`; endpoint presence describes a
communication capability, not stolen data. The unchanged DoH-to-C2 composite
now lives in `command-and-control/dns/tunneling`. An explicit DNS TXT query plus
command-execution composite moved there too. A DNS heartbeat moved to
`command-and-control/beacon/network/periodic`, which rose **79 → 81**. The DNS
tunneling leaf is **85** rules. The neutral DoH capability rules remain
notable and preserve their prior scope,
conditions, exceptions, and mappings. Moved references are fully qualified at
their new homes.

The source movement does not resolve the remaining role ambiguity in this DNS
leaf: several rules describe C2 tunneling rather than stolen-data export. The
existing `command-and-control/dns/tunneling` leaf now has 85 rules, leaving
room under the current 100-rule cap for justified C2 candidates.
The current taxonomy explicitly distinguishes DNS control retrieval, source-
defined theft sent over DNS, and source-unspecified DNS exfiltration.

The effective conditions, scopes, criticality, confidence, suppressions, and
defaults were compared for all 17 moved composites. Sixteen preserve their
matcher bodies and effective settings; changed references qualify components
after they move to a new home. The heartbeat rule preserves its matcher, scope,
severity, and confidence; its ATT&CK mapping changes from T1048.003 to
T1071.004 to reflect DNS command-and-control beaconing rather than data
exfiltration. All
**1,842 controlled corpus fixtures** pass after overlaying the moved rules on
the previous passing snapshot. The latest cap-100 inventory reports 79 over-cap
directories across the catalog. A fresh strict validator run is pending because
the shared engine checkout currently fails to compile on an unrelated
`filefacts::decode_dos_com_xor_payload` API mismatch; the controlled overlay
reports no broken references for this migration.

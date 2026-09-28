# System-info exfiltration source audit

The oversized `objectives/exfiltration/stealer/system-info` leaf had 169 rules
in the initial 2026-09-28 working-tree audit. Six composites first moved to
existing source leaves, then three mixed-source profiles moved to the existing
`stealer/sweep` leaf. After that pass, `system-info` has 160 rules (75 over
cap), `sweep` has 83, and `stealer/file` has 55:

- Go global keyboard state plus upload → `stealer/surveillance`. Its host
  profile is supporting context; the sensitive captured source is input.
- A debugger-evasion wrapper around that input exporter →
  `stealer/surveillance`. The wrapper adds anti-analysis evidence but retains
  the same captured source and transfer result.
- Browser identity, network-address profile, geolocation, and local-IP facts
  plus upload → `stealer/sweep`. The matcher requires multiple source classes,
  so it is not only a browser or host-profile export.
- JVM process-profile fields plus an exfiltration endpoint →
  `stealer/process-list`.
- Swift process inventory plus its HTTP collect endpoint →
  `stealer/process-list`.
- AppleScript environment credentials plus host identity and POST →
  `stealer/env`. The secret source takes precedence over host-profile context.
- Windows domain-controller discovery and local network configuration sent by
  HTTP → `stealer/sweep`. The matcher requires both domain and host-network
  evidence plus the transfer context.
- Python system profile plus browser and wallet sources sent over HTTP →
  `stealer/sweep`. Both browser and wallet source legs are required.
- PE/DLL reconnaissance sent through a Telegram bot → `stealer/sweep`. The
  rule requires at least two independent host/network source observations and
  bounds their proximity to the send operation.

The sibling audit also removed rules that described file targeting or a single
file source from `stealer/sweep`:

- Sensitive-path filter aggregation and Node root-search targeting →
  `objectives/collection/file-targeting`; these describe source selection and
  acquisition capability, not a mandatory mixed-source sweep.
- libcurl plus sensitive-file targeting, macOS file-copy plus sensitive-file
  targeting and network context, and recursive sensitive-file traversal plus
  network context → `stealer/file`; all three point to one file-source class.

The moves preserve matcher bodies, scopes, criticalities, confidence, and
effective file/platform settings. Rule IDs were retained and repository
consumers updated. The browser/network sweep and subsequent mixed-source
migrations leave `sweep` at 83 rules. `system-info` now has 160 rules, 75 over
cap. Soft validation passes all **1,837/1,837 fixtures** after these moves.
Strict `make validate` reports no broken references or YAML errors from this
cohort; catalog-wide cap and policy errors remain.

| Previous ID | Canonical ID |
|---|---|
| `objectives/exfiltration/stealer/system-info::go-input-surveillance-http-exfil` | `objectives/exfiltration/stealer/surveillance::go-input-surveillance-http-exfil` |
| `objectives/exfiltration/stealer/system-info::go-anti-debug-input-profile-agent` | `objectives/exfiltration/stealer/surveillance::go-anti-debug-input-profile-agent` |
| `objectives/exfiltration/stealer/system-info::browser-identity-network-profile-exfiltration` | `objectives/exfiltration/stealer/sweep::browser-identity-network-profile-exfiltration` |
| `objectives/exfiltration/stealer/system-info::jvm-process-profile-exfil` | `objectives/exfiltration/stealer/process-list::jvm-process-profile-exfil` |
| `objectives/exfiltration/stealer/system-info::swift-inventory-http-exfil` | `objectives/exfiltration/stealer/process-list::swift-inventory-http-exfil` |
| `objectives/exfiltration/stealer/system-info::applescript-host-user-secret-exfil` | `objectives/exfiltration/stealer/env::applescript-host-user-secret-exfil` |
| `objectives/exfiltration/stealer/system-info::windows-domain-recon-http-exfil` | `objectives/exfiltration/stealer/sweep::windows-domain-recon-http-exfil` |
| `objectives/exfiltration/stealer/system-info::python-profiler` | `objectives/exfiltration/stealer/sweep::python-profiler` |
| `objectives/exfiltration/stealer/system-info::recon-telegram-exfil` | `objectives/exfiltration/stealer/sweep::recon-telegram-exfil` |

| Previous ID | Canonical ID |
|---|---|
| `objectives/exfiltration/stealer/sweep::sensitive-file-targeting` | `objectives/collection/file-targeting/filter::sensitive-file-targeting` |
| `objectives/exfiltration/stealer/sweep::node-sensitive-find-command` | `objectives/collection/file-targeting/command::node-sensitive-find-command` |
| `objectives/exfiltration/stealer/sweep::curl-with-file-targeting` | `objectives/exfiltration/stealer/file::curl-with-file-targeting` |
| `objectives/exfiltration/stealer/sweep::macos-file-copy-exfil` | `objectives/exfiltration/stealer/file::macos-file-copy-exfil` |
| `objectives/exfiltration/stealer/sweep::recursive-file-theft` | `objectives/exfiltration/stealer/file::recursive-file-theft` |

This is a first-pass source audit, not a complete reorganization. The
remaining system-info rules need a complete source map before any new child
leaves are defined; host/user/OS profile rules must not be split only by
language, operating system, or transport. Any path change still changes the
ML feature namespace and requires downstream evaluation.

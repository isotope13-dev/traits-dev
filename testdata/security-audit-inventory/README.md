# Single-vendor security inventory is not an AV kill list

`av-product-killer` convicted on supervision APIs (OpenProcess, terminate,
Toolhelp enumeration) plus a single vendor's product names. That trio is
what every process supervisor does, and audit tools name the products
they check: a defensive Windows auditor inventorying Defender tripped the
hostile without killing anything. The tighter sibling
`multi-vendor-security-process-killer` already demands kill-list-shaped
evidence and correctly excludes it.

Both `av-product-killer` and `security-process-name-survey` now require
the multi-vendor atom instead of any single vendor name. Likewise the
bare `TeamViewer_Service` name string moved from suspicious (persistence
self-install) to the notable `teamviewer-service-name`: naming the binary
is inventory, and the `commercial-rat-service-mode` composite keeps only
its service-registration legs (a bare-name leg would let the composite
outrank its own evidence, which validation rejects).

Run `python3 testdata/security-audit-inventory/check.py
<scratch-directory>`. Fixtures are minimal PE32 files with real KERNEL32
import tables built at runtime:

- `kill-list-positive.exe`: supervision imports plus MsMpEng.exe and
  CSFalconService.exe. Must report the hostile and the survey
  suspicious trait.
- `audit-inventory-negative.exe`: same imports, Defender-only names plus
  wireshark/procmon inventory strings and a TeamViewer_Service.exe
  reference. Must report no hostile and no survey; the sandbox
  suspicious trait and the teamviewer notable still surface.

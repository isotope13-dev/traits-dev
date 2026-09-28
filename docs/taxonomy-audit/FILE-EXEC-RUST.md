# Rust staged-file activation composites

## Decision

These rules classify complete staged-file activation under
`objectives/command-and-control/dropper/file-exec`. Their payload sinks are a
local executable launch or a file-backed script launched through a handler.
The Rust implementation and download transport do not define the taxonomy
branch.

## Moves

Four composites moved from `dropper/delivery/execute-download`, preserving their
matchers, effective scope, metadata, confidence, and criticality:

- `rust-staged-archive-platform-download-exec`: fetches and extracts an archive,
  arms a payload and launches it.
- `rust-hidden-wscript-temp-powershell-stage`: materializes a remote PowerShell
  file with a temporary VBScript launcher, then invokes it through hidden,
  detached WScript execution.
- `rust-obfuscated-endpoint-temp-executable-dropper`: ties a fragmented endpoint
  to a materialized temporary payload and concealed launch.
- `rust-hostname-unverified-temp-executable-dropper`: ties a downloaded response,
  disabled hostname verification and a temporary executable launch.

The three supply-chain trojan consumers now reference the canonical file-exec
IDs. Each rule's bounded proximity condition and evidence conjunction remain
unchanged.

## Validation

Soft validation passes all **1,837/1,837 fixtures**. The source
`delivery/execute-download` leaf drops from 310 to 306 rules; `file-exec` grows
from 11 to 15 rules. Strict validation remains at **59 issues**, including 165
over-cap directories. The move improves activation-based placement but does not
resolve the catalog-wide cap debt.

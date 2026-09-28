# PowerShell file-execution composites

## Decision

A dropper composite belongs in `objectives/command-and-control/dropper/file-exec`
when its evidence joins remotely acquired or extracted file content to launching
a staged executable or installer. The activation sink decides the leaf; the
scripting language and transport do not. A downloader without a launch, a launch
without evidence of staging, or a generic remote command remains in its own
behavioral category.

## Moves

Five PowerShell composites moved from `dropper/delivery/execute-download` with
their matchers, scopes, metadata, and criticality unchanged:

- `powershell-streamed-archive-msi-dropper`: response stream, archive extraction,
and MSI launch within 8,192 bytes.
- `powershell-cert-bypass-archive-download-execute`: HTTP byte retrieval, file
  write, archive extraction, and process launch within 120 lines.
- `powershell-unblocked-archive-hidden-launch`: remote response, archive
  extraction, unblock operation, and hidden process launch within 8,192 bytes.
- `powershell-webclient-remote-exe-launch`: WebClient download, executable URL,
and process launch within 8,192 bytes.
- `powershell-temp-msi-install`: an `Invoke-WebRequest` file download, temporary
MSI staging path, and quiet MSI installation, with corroborating hidden-launch,
no-restart, or `UseBasicParsing` evidence.

The streamed-MSI rule remains consumed by the PowerShell timing composite. The
WebClient launch rule remains consumed by the encrypted PowerShell stage
composite. The temp-MSI rule remains consumed by its unattended-RMM and
GitHub-raw wrappers and by the cleanup composite. These references now use the
canonical `dropper/file-exec` IDs. No matcher or scope was
changed, so this relocation does not broaden the detection conditions.

## Follow-up

The `powershell-unattended-rmm-msi` and `github-raw-msi-dropper` wrappers
later moved from the source leaf into `dropper/file-exec/installer/` with their
installer sink. The `batch-github-raw-quiet-rmm-dropper` wrapper moved there as
well. See [DROPPER-POWERSHELL-COMPLETED-SINKS.md](DROPPER-POWERSHELL-COMPLETED-SINKS.md).

## Validation

Soft validation passes all **1,837/1,837 fixtures** after the moves. The source leaf drops from 315 to 310 rules, while `file-exec` contains 11
rules. Strict validation still reports 165 over-cap directories and the existing
quality debt. This migration is a semantic reorganization and does not claim to
resolve the 85-rule cap on its own.

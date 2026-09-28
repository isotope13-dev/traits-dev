# PowerShell chains follow installer and spawn sinks

Five PowerShell composites moved from the legacy download leaf. The MSI rules
`powershell-unattended-rmm-msi`, `github-raw-msi-dropper`, and
`batch-github-raw-quiet-rmm-dropper` require an installer transaction and now
live under `dropper/file-exec/installer/`. The `powershell-js-to-exe-masquerade`
and `powershell-github-release-exe-launch` rules require a process launch and
now live under `dropper/file-exec/spawn/`.

Matcher bodies, criticality, confidence, proximity and effective scope are
preserved. The batch rule remains batch scoped; the others remain PowerShell
scoped. Two source atoms stay in `execute-download` and are referenced from the
new composites by canonical full IDs. No external exact-ID consumers were
found. The earlier MSI wrapper audit is superseded for the two wrappers that
now moved here; see its follow-up note.

`execute-download` falls from **195 to 190 rules**, installer grows from **10
to 13**, and spawn grows from **60 to 62**. The source leaf remains over cap.
See the [mapping ledger](dropper-powershell-completed-sinks-mapping.json).

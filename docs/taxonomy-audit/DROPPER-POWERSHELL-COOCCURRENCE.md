# PowerShell capability co-occurrence audit

The PowerShell hidden-encoded-command atom and two composites were filed under
`objectives/command-and-control/dropper/delivery/execute-download/`. Their
evidence did not consistently establish dropper execution: one rule required a
hidden, bypassed encoded command; another paired that atom with WebClient
`DownloadString`; the third paired hidden-window execution, `Invoke-WebRequest`,
and `Start-Process` by proximity without linking the response to the launched
process input.

The atom now lives at
`micro-behaviors/process/create/hidden::powershell-hidden-bypass-encoded-command`.
Its matcher, file-type scope, Windows platform, attack tags, and exclusions are
preserved. The inherited `B0030` tag was removed because it came only from the
old dropper directory default and the atom alone does not establish additional
payload installation.

The encoded `DownloadString` conjunction now lives in
`micro-behaviors/communications/http/download/webclient::powershell-encoded-downloadstring-fetch`.
Its two required observations, 4096-byte proximity, file-type scope, and attack
tags are preserved. Criticality changes from hostile to notable: it establishes
a fetch-capability conjunction, but not evaluation or activation of the fetched
text. The old inherited `B0030` tag is removed for the same evidence-boundary
reason.

The hidden request/launch conjunction now lives in
`micro-behaviors/process/create/hidden::powershell-webrequest-hidden-launch-cooccurrence`.
It retains the hidden-window, `Invoke-WebRequest`, and `Start-Process` legs,
512-byte bound, PowerShell scope, and exclusions. Its description explicitly
states co-occurrence, and criticality changes from hostile to notable because
the matcher has no response-to-process dataflow link. The Defender-exclusion
objective now references this canonical capability ID; its hostile judgment
continues to require the independent Defender-exclusion and process evidence.
The old inherited `B0030` tag is removed.

During fixture verification, a hostile Chocolatey package stopped receiving a
hostile finding because its PowerShell command used a backtick-newline between
`Invoke-WebRequest` and `-OutFile`. The existing `iwr-outfile-download` atom
matched only within one physical line. Its matcher now accepts explicit
PowerShell backtick line continuations while retaining ordinary newlines as
boundaries. This restores the precise `powershell-temp-msi-install` objective,
which binds the TEMP MSI path, its download, and the quiet installer invocation;
the broad co-occurrence rule is excluded when the file-backed download evidence
is present.

The SCCM and MSI objective consumers of the encoded-command atom were updated
to the canonical micro-behavior ID. The mapping ledger records the moves and
consumer rewrites. Full soft validation passes **1,837/1,837 fixtures** after
the line-continuation repair.

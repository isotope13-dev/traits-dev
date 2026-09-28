# Archive staging versus file execution

Six PowerShell archive composites moved from `dropper/staging/archive` to
`dropper/file-exec/spawn`. Each matcher requires evidence of a launched
payload: an embedded PowerShell archive chain launching a TEMP executable, a
download/extract chain with a process-launch leg, or a more specific Defender,
password, remote-instruction, or cloud/ProgramData variant of that chain.

The source archive helper traits remain in `staging/archive` and are referenced
by exact ID. The moved `powershell-download-archive-execute` rule also had an
external consumer in the ClickFix terminal-fix composite; that reference now
uses the canonical spawn path. `file-exec/spawn` grows from 78 to 84 rules,
within the 85-rule cap. Follow-up sibling review also moved the remote-IEX and
Dalvik-invocation rules to their eval and module-load sinks, leaving 95 rules
in archive staging. Archive extraction-only rules remain in the archive
staging leaf.

This follows the activation sink: archive format and extraction method are
evidence, while process launch decides the objective leaf. No matcher body,
effective scope, confidence, criticality, or attack mapping changed.

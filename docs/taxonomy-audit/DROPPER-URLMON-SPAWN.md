# URLMon download-and-launch rules use file-exec/spawn

Ten URLMon/WinINet composites in the generic download leaf require a process
launch sink: `WinExec`, `ShellExecute`, `ShellExecuteEx`, or a process-creation
API. They now live in `dropper/file-exec/spawn/`. The sandbox-gated and
browser-user-agent variants moved with the URLMon/direct-IP composites they
reference. No external exact-ID consumers needed updates.

The moved matcher bodies, criticalities, confidence, exclusions, size limits,
and effective scopes are preserved. The two signed-downloader rules remain PE
only; the other eight retain their PE/DLL scope. All keep their explicit
Windows scope and inherited `T1105`/`E1105` tags. `execute-download` falls from
**210 to 200 rules**; `file-exec/spawn` grows from **45 to 55**. The source
leaf remains over cap and needs continued sink-by-sink review. See the
[mapping ledger](dropper-urlmon-spawn-mapping.json).

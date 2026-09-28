# .NET launch chains use file-exec/spawn

Five C#/.NET composites require a process-launch capability alongside
download, file-write, archive, or sandbox-gating evidence. They now live in
`dropper/file-exec/spawn/`. The C#-scoped `DownloadData` rule retains its
`for: [csharp]` scope; the other four remain PE scoped. The sandbox-gated rule
still references the download-method cluster in the source leaf by its full
canonical ID. No external exact-ID consumers were found.

Matcher bodies, criticality, confidence, exclusions, proximity, and effective
scope are unchanged. `execute-download` falls from **200 to 195 rules** and
`file-exec/spawn` grows from **55 to 60**. See the
[mapping ledger](dropper-dotnet-spawn-mapping.json).

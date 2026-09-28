# .NET staged-file activation composites

Six PE-scoped .NET composites moved from
`objectives/command-and-control/dropper/delivery/execute-download` into the
language-neutral `dropper/file-exec` leaf. The filename and `for: [pe]` scope
retain implementation details; the directory classifies the activation sink.

The rules join remote file acquisition or embedded-payload writing to launch:

- `dotnet-github-httpclient-download-exec` requires a bounded HTTP download,
  file write and process start, plus two corroborating identity/staging clues.
- `dotnet-encoded-payload-write-execute` requires an embedded encoded payload,
  decode, file write and process start.
- `dotnet-temp-encoded-payload-stager` refines that chain with a temporary-file
  location.
- `dotnet-remote-wsh-script-dropper` links remote script acquisition and file
  staging to Windows Script Host execution.

Two additional PE-scoped rules also moved: `dotnet-kingspy-download-execute`
requires the exact staged-payload URL, WebClient/download evidence and process
start; `dotnet-evasive-downloadfile-temp-execute` requires DownloadFile and
process-start evidence, a temporary path, unsigned status and managed-code
obfuscation evidence.

Matchers, effective PE/Windows scope, confidence, criticality, proximity and
other matcher constraints are unchanged. The evasion file-hiding and Rockstar
masquerade consumers now reference the canonical IDs; the temp-stage wrapper
still references its base rule locally.

Soft validation passes **1,837/1,837 fixtures**. The source leaf drops from 272
to 266 rules, and `file-exec` grows from 45 to 51. Strict validation remains at
59 issues, including 165 over-cap directories.

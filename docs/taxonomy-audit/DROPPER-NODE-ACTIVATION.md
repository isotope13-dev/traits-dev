# Node dropper activation sinks

Five Node composites moved out of `dropper/delivery/execute-download`, split
by the required activation mechanism:

- `node-obfuscated-buffered-download-detached-launch`,
  `node-fetch-buffered-archive-detached-launch`,
  `portable-runtime-covert-stager`, and
  `node-passworded-archive-pe-dropper` stage a file, arm or identify it, and
  launch it as a process. These belong in `dropper/file-exec`.
- `node-remote-archive-execute` extracts an archive and activates the payload
  through Node's variable `require` loader. The module-load sink decides its
  home in `dropper/module-load`.

The download and file-write evidence remains in the rules. The first two
file-exec rules retain the 2,000-byte proximity bound and the modern Fetch rule
retains its test-harness exclusion. Effective Node file-type/platform scopes,
confidence, criticality and metadata are unchanged.

The FTP-banner download/execute composites had referenced the old directory as
a pooled alternative. They now include `file-exec`, `interpreter-stdin`, and
`module-load` alongside the remaining legacy directory, retaining access to all
relocated activation sinks without duplicating a member rule.

Soft validation passes **1,837/1,837 fixtures**. The source leaf drops from 262
to 257 rules; `file-exec` grows from 55 to 59 and `module-load` from 1 to 2.
Strict validation remains at 59 issues, including 165 over-cap directories.

# WSH Exec casing controls

`exec-method-call-text` was case-insensitive, so every JavaScript
`RegExp.prototype.exec()` call (and Node `child_process.exec`) fed the
WSH-labeled `exec-invocation-patterns`, `execution-methods`, and
`wsh-process-method` composites. It is now capital-E only, matching the
WSH JScript/VBS spelling (and the sibling `exec-member-symbol`).

`exec-positive.js` keeps a true `shell.Exec` detection; `exec-nearmiss.js`
is pure regex matching and must stay silent. Cases checked with
`cleave --traits-dir . --json` and assertions over emitted IDs.

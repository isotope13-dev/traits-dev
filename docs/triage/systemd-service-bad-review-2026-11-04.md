# systemd service filetype mislabeled-bad review — 2026-11-04

The six-file snapshot contains two bad and four inconclusive services.

`1034fd0f9ca2` downloads an executable to a hidden temporary path, marks it executable and runs it under an automatically restarting service. It is bad; both scanners already report hostile findings.

`fac4fd7d3c86` copies an executable to a different system-bin name, runs it with output suppressed and deletes it, with automatic restart. It is bad as hostile obfuscation and persistence. Both scanners match the new combined finding; changing the removal operation clears the finding. Atomscan reports the hostile trait but exits successfully. Static facts alone do not establish the behavior of the missing executable or prove the copied, run and removed paths are identical.

`d11836fae58c` names a backdoor in its description but points to a placeholder executable path. `afc438fc139e` starts an unavailable root-owned shell script; `cc0a57d94c89` starts an unavailable hidden network helper with a remote address and disabled certificate verification; `d463b0a865c0` starts an unavailable executable from a temporary directory. These are inconclusive because their executable payloads are absent; descriptions, paths and flags alone do not establish what those payloads do. Hopper records inconclusive rulings through its purgatory compatibility target.

Full validation passed after the changes; no engine features were added.

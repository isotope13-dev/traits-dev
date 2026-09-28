# URLMon launch chains follow the spawn sink

Two Windows URLMon composites require the branded downloader fingerprint, a
WinVerifyTrust reference, and either `ShellExecuteEx` or `CreateProcessW`.
The second also requires interactive-session enumeration. Their required
process-launch evidence places them in `dropper/file-exec/spawn`; the two
sibling URLMon profiles that require file staging but no launch evidence remain
in the source leaf pending a separate classification audit.

The two rule bodies, scopes, criticalities, confidence, size limit, and
suppressions are preserved. The source defaults (`for: [pe]`, Windows,
`T1105`, and `E1105`) were copied to the destination. No exact-ID consumers
needed updates. `execute-download` falls from **215 to 213 rules** and
`file-exec/spawn` grows from **43 to 45**; the former remains over cap, while
the latter stays below it. See the
[mapping ledger](dropper-urlmon-file-exec-mapping.json).

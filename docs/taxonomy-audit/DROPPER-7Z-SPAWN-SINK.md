# Passworded 7z launch follows the file-execution sink

The single rule in `dropper/staging/encrypted/7z-stdout.yaml` requires passworded
7z extraction to stdout, PE validation, a randomized temporary executable path,
and `Start-Process` on that executable. The payload's direct child-process
launch is the defining sink, so the rule now lives in
`dropper/file-exec/spawn/7z-passworded-stdout.yaml`. Archive format and
password-protected extraction remain required source evidence in the matcher.

The move is byte-for-byte: SHA-256 before and after is
`dd5ebb783bf9cca8ba1f005b7baada62878d089f2796372acbf4b904e71d7af4`. No YAML
rule referenced this composite ID, so the move required no consumer edits. Its
four evidence references remain fully qualified and unchanged.

This is not a claim that encrypted archive metadata alone proves execution.
Rules that identify encrypted archives without a linked activation sink remain
under `dropper/staging/encrypted`. The general rule is documented in
`TAXONOMY.md` beside the dropper sink contract.

# Encrypted-stage interpreter evaluation audit

Three completed source-evaluation chains move from `dropper/staging/encrypted`
to `dropper/script-eval`:

- Python base64/zlib payload passed to `exec`.
- Ruby Base64/zlib payload passed to `eval`.
- PowerShell hex-XOR-decoded source evaluated through `IEX`.

The rules are classified by their activation sink. Decoder and obfuscation
observations remain in their capability and anti-static homes; the PowerShell
rule references its decoder and stage marker by canonical exact ID. The Ruby
matcher and its composite moved together because the atomic pattern already
asserts the same compressed source-evaluation technique. There were no
external consumers of the moved IDs. No matcher body, effective scope,
confidence, criticality, or attack mapping changed.

The PowerShell ScriptBlock-construction rule remains in encrypted staging:
construction alone does not show that the block is invoked. Likewise, decoder
rules remain there until their evidence establishes an activation sink.

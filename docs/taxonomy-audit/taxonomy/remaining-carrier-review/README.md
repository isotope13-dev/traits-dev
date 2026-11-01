# Remaining encoded carrier review

The final 14 rules under `staging/encoded/carrier` have moved. All matching conditions, scopes, confidence values and references were preserved.

- Kotlin firmware API-path text, a nearby Base64/chmod sequence and payload-launch naming are now path, decode-command and naming observations. The alternative-based firmware combination is a suspicious firmware profile; one of its alternatives does not establish a decode or a launch.
- PHP payload API text near `base64_decode` and a health-module name near `proc_open` are suspicious encoding/network and execution-API observations. Their combination does not prove a fetch or a process argument.
- `Hex(AscW(...))` and file-write references are encoding and file-write observations. VBScript Base64/stream/deletion/Run and typed-value/SaveToFile/Run combinations are suspicious profiles because their conditions need not establish the previously claimed payload chain. The CopyHere/file-I/O/Run combination is an archive profile.
- The substituted Base64 plus WScript shell and hidden-style Run combination, and XOR plus file-save, hidden Run and deletion combination, remain hostile execution objectives. They describe the likely chain without requiring data-flow proof.

Non-hostile observations lost inherited attack annotations that claimed actions their individual conditions did not establish. The legacy directory has no YAML rules or YAML references.

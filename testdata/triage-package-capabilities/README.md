Matcher corrections and controls

- `node-cp-sync-call` now accepts qualified calls as well as bare imports. A string mentioning the API is a near miss. Its install-hook consumer still requires its own trigger and copying context.
- The exported-object cluster retains its matcher and scope; its ID and description now describe objects rather than requiring string-valued enums. All exact consumers were renamed without changing their evidence sets.
- Commander require evidence moved from library identity to package imports and now requires the exact package name. An unrelated package containing that name is a near miss. No exact consumers existed; parent identity selectors intentionally cease treating an import as product identity.
- Hex-shaped call arguments moved to language representation metadata, with no encoding/exfiltration mapping. Decimal-only strings are excluded. The JScript consumer references the corrected evidence; source encoding alone does not establish an attack.
- Go temporary-file API references moved to `fs/temp/file`. Source call symbols replace bare text, preventing quoted API names from matching. Scope covers Go and relevant native/WebAssembly binaries. The native runtime-string consumer was updated. The other `mktemp` selector consumers have Python or C-family scope and cannot consume these Go source symbols.
- Documentation prohibitions now target prose/documents, excluding private-API comments in executable source.

`cases.json` records positive and near-miss expectations. The Markdown fixture is scanned explicitly because directory scans skip standalone prose by default.

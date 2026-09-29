# Reusable source-command atoms follow their capability subjects

## Finding

The over-cap `anti-static/obfuscation/payload/encrypted` leaf held two
single-observation atoms that did not identify concealment: Swift's
`Data(base64Encoded:)` API reference and a Zig source argument pair selecting
`/bin/sh -c`. Their objective-level placement made capability features depend
on an encrypted-payload namespace and caused downstream composites to reference
the wrong subject.

## Reclassification

`swift-base64-decoder-call` now lives in
`micro-behaviors/data/decode/base64`; the matcher is unchanged, and its
description says API reference rather than claiming a decode executed. The
neutral capability scope covers Swift on Unix and Windows. That also repairs
the previous Windows-only inherited platform scope for Unix/macOS composites.
It carries the operation mappings `T1140` and `C0053`.

`zig-shell-c-command` now lives in
`micro-behaviors/process/create/shell/command-string`. The matcher and its Zig
and Unix scope are unchanged. The new description says the source selects
`/bin/sh -c`, which is what the matcher sees; it does not claim the command ran.
Its ATT&CK mapping is corrected from the inherited Windows shell identifier to
Unix shell `T1059.004`.

The source-command composites now reference these neutral capability IDs.
Their conditions and objective mappings remain unchanged. This follows the
matcher-identity rule: put an observation where its own evidence belongs, then
let the composite express the higher-order intent.

## Verification and remaining review

Cleave `test-rules` matched both relocated atoms against minimal Swift and Zig
source samples. The full soft validation and refreshed cap inventory are
recorded in the current audit plan and snapshot. No rule was deleted. Other
Swift path and check-in atoms in the source-command file remain under review:
their matchers are weaker and need an individually defensible destination
before relocation.

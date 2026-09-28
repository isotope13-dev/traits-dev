# PowerShell helper identity: parsed relationships

The `powershell-utils` helper is an independent library artifact, so its identity
belongs in `well-known/lib`. It is not a new PowerShell technique, and its presence
does not establish what a caller passes to it. The existing `runtime/scripted`
implementation partition remains separate migration debt; this repair does not
endorse language-based identity branches.

Three text matchers in `well-known/lib/runtime/scripted/powershell-utils/traits.yaml`
now inspect JavaScript syntax:

- `powershell-utils-encoded-command-prefix`: an actual property assignment with
  adjacent ExecutionPolicy, Bypass, and EncodedCommand array entries.
- `powershell-utils-utf16-base64-encoder`: the arrow parameter is the input to
  Buffer.from with UTF-16LE, followed by Base64 conversion. Parameter spelling
  does not define library identity.
- `powershell-utils-execfile-launch`: the result of the helper's encoder is the
  same variable passed after its argument-prefix spread to execFile in the next
  statement. Unrelated nearby names cannot substitute for this relationship.

All three retain notable criticality, scope and IDs. The module-path atom and
four-leg exception remain unchanged. The exact external consumer is
`micro-behaviors/process/create/hidden::encodedcommand-invocation`, through
`unless:`. No consumer reference changes are needed. This exception recognizes
one helper shape; it is not a general safety guarantee for files containing it.
Whole-file suppression and the broad encoded-command consumer still warrant
review independently of this identity repair.

## Evidence

Controls derive from powershell-utils 0.1.0 found inside the locally inspected
difit 5.0.1 installation. Its MIT license is included beside the controls. None
of the JavaScript was executed. Run the six exact exception traces with:

```sh
python3 docs/taxonomy-audit/controls/powershell-library/check.py
```

The original and a renamed encoder parameter match. An entirely commented copy,
a different encoder input, changed flags, and a different launch prefix do not.
These are direct rule checks because exception findings are not emitted in scans.
The controls are independent of the fixture verdict suite.

Before/after atomscan results retain the original's risk 10 and remove the
renamed parameter's false suspicious encoded-command finding (risk 46 → 10).
Commented code loses all three implementation atoms; the path observation remains.
The three mismatched variants retain their prior findings. Those findings are not
proof of malice: they expose the separate broad encoded-command consumer issue.

The checkout engine's full `validate --soft` passes **1,781/1,781 fixtures**.
It no longer reports this library's overlong regexes or descriptions.
**168 oversized directories** remain, along with separate WASM/Silver Sparrow
description issues and two suppression-count violations. The taxonomy migration
is incomplete; the soft validation pass is not a strict gate pass.

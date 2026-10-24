Oxlint 0.12.0 is BENIGN. The supplied npm archive is byte-identical to the
registry artifact (SHA-256 `ea9b5c46516cd14ff897602dba24c5203ff62f0f74fb2a0e83616aa67535b5d3`).
Forager recovered both registry releases and both upstream source tags; original
archives and their `.forage.json` records remain in the task scratch directory.

Comparison with 0.11.0 finds the same AWS-shaped example key in both binaries.
The only change to `crates/oxc_linter/src/rules/security/api_keys/mod.rs` is a
documentation link from `node-vault/tree/master` to `node-vault/tree/v0.10.2`.
The earlier release also fires under the current baseline rules, so the queue's
earlier clean result is not reproducible with these rules.

The example is documentation, introduced by an incorrect-code heading and a
JavaScript code fence. The macro emits that documentation as static strings.
Rizin inspection locates its pointer in the documentation table and traces the
separate API-key checker to token-prefix checks and diagnostic construction,
including the recommendation to use a secrets manager. Its source checks AST
string/template literals, length and entropy; it does not retrieve credentials
from the machine or send them elsewhere. The CLI reads selected source files
and applies requested lint fixes. The bundled language server runs LSP over
stdin/stdout. Native runtime capabilities remain detectable.

The assignment rule now describes a format, rather than credential acquisition.
Its suspicious criticality is retained. A matched fenced example is excluded
without suppressing another assignment elsewhere in the file. Native raw
matching is needed because text extraction splits the documentation at newlines;
a separate decoded matcher preserves the previous decoded-string coverage.
The example itself remains a notable documentation observation.

The `chmod` finding came from the JavaScript globals catalog, not a permission
operation. Its fallback now requires absence of an ELF interpreter, consistent
with its existing static-executable claim. Its sole direct consumer already
requires absent dynamic linker metadata and needed libraries, so this condition
cannot remove that consumer's static population. Structured chmod API matchers
are unchanged. WebRTC/global names, MIME strings and embedded source examples
are references, not evidence of executing those APIs or contacting services.

Run the focused controls from the repository root:

```sh
python3 testdata/taxonomy/oxlint-credential-example/check.py \
  --scratch /absolute/path/to/scratch \
  --oxlint /absolute/path/to/extracted/package/oxlint
```

The script stages controls outside test directories, preventing test-context
exclusions from deciding the results. It checks plain and encoded assignments,
documentation plus a real assignment, an existing AWS stealer fixture, raw and
encoded keys appended to the actual Oxlint image, and static/dynamic ELF name
controls. The generated ELF files are matcher fixtures, never executed or
represented as recovered attack artifacts. The static loader composite remains
detected. See `review.json` for full-archive before/after counts and classifier
results. No supported attack detection was removed; the remaining classifier
verdict agrees with BENIGN. Deployment history was not provided.

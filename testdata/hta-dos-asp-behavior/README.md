The fixtures test RC4/computed-ActiveX conjunctions, hidden HTA dispatch,
ASP raw-body evaluation and keyed XOR, executable URL references, hexadecimal
function names, and a DOS mkdir loop with shared name pointers and a backward
branch. Run `python3 testdata/hta-dos-asp-behavior/check.py` from the trait root.
The checker only invokes static analysis.

The directory contains both visible and hidden HTAs, a page without RC4,
ordinary upload and local-evaluation pages, a request XOR transform without
evaluation, and a URL whose actual suffix is `.js`. DOS near misses alter the
saved count, shared name pointer, backward branch, or OEM blank name fields.

`mkdir-oem.com` and `unclassified-stryx` are byte-identical. The latter records
a classifier limitation: the supplied headerless Stryx sample has no `.com`
extension and cleave identifies it as Unknown. YAML rejects Unknown scope;
the DOS detections apply when the same bytes are identified as DOS COM.
This gap does not change the reverse-engineered malicious verdict.

The function-name move preserves the two atomic matchers and their type and
platform scopes. Exact consumers were rewritten. The five directory-selector
consumers in VM gating, package obfuscation and Dism++ context also include the
new function-name leaf, preserving their former alternatives. Hexadecimal
argument syntax no longer claims that a decoder or string table was proved.

The PowerShell URL atom formerly under dropper staging was consolidated with
the existing executable-URL observation. That observation now covers HTML,
case variants and URLs in source text. It requires an extension delimiter, so
`update.ps1.js` does not qualify. This is an intentional matcher change,
separate from the function-name placement change.

The three DOS fragments formerly placed under directory creation were replaced
by a directory operation and linked loop/buffer observations. ASCII carry and
CX countdown fragments alone no longer imply a directory-flooding objective.
The composites remain suspicious because filesystem stress tests and unusual
OEM names admit benign uses. The HTA and ASP conjunctions likewise remain
suspicious: they do not establish decoded COM targets or request-to-Execute
variable provenance by themselves. The specimen verdicts rest on tracing the
actual code, independently of those generalized matchers.

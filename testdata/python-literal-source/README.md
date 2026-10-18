# Literal source concatenation

Run `python3 testdata/python-literal-source/check.py` from the repository root.
The checker scans copies outside `testdata` so the existing test-directory
exclusion cannot conceal a failed positive or near-miss assertion. It never
executes the fixture source.

The positive cases retain split-source detection for `exec`, `eval` and
`compile`, including longer chains, mixed quotes and escaped quotes. Negative
cases cover readable generated bodies, literal method receivers, a different
argument, a method named `compile`, a quoted example and the existing dynamic
import-statement exclusion. Ordinary compilation remains notable.

## Release investigation

Verdict: **BENIGN** for `github.com/jomcgi/homelab` at
`v0.0.0-20261018125828-58ddaed23251`, SHA-256
`288c0e01b64a3d65535a07a3d3c9af7edbb574992325b4d8b67e21eb03b04139`.
This is a personal infrastructure and application monorepo, including the
EmberVM microVM orchestrator, its Claude CLI shim, and authentik configuration.

Fetched its parent release from the Go module proxy:
`v0.0.0-20261018125828-8144017f11c0`. Both archives contain 4,511 files,
with no additions or removals. Only
`projects/embervm/chart/chart_env_identity_test.py` changes; the Python ASTs
are identical. Every current archive member also agrees with the fetched
upstream Git commit. Dependency manifests and lockfiles are unchanged.

The flagged `projects/platform/authentik/blueprint_tags_test.py` is identical
in both releases. Its test reads local blueprint YAML using a SafeLoader
subclass whose custom tag constructor produces scalar/sequence values. It
asserts invitation and enrollment restrictions, then wraps policy expressions
in a function and calls `compile(..., filename, "exec")` to check syntax.
The code object is discarded; neither `exec` nor `eval` executes it. The
underlying policies validate invitations and passwords and restrict access;
they contain no hidden payload. File facts report no parser errors or decoded
string layers in this test.

The previous matcher stopped after the opening quote of `"\n".join(...)`,
misreading a method receiver as a literal operand. The replacement checks the
complete first argument and requires literal-only concatenation. It changes
the supported claim rather than adding a filename or package exemption.

Verification: all seven control fixtures pass. The final archive-only atomscan
run analyzes 3,164 units with zero suspicious or hostile findings and retains
the notable `compile-builtin` finding in the policy test. The initial run also
followed dependencies; its sole suspicious trait was this same policy-test
false positive.

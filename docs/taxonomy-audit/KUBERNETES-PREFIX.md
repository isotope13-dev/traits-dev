# Kubernetes directory prefixes are not package integration

Two runtime observations move into general secret-store paths:

| Former runtime ID | New `fs/path/credential` ID |
|---|---|
| `secrets-path` | `kubernetes-secret-directory-text` |
| `k8s-service-account-path` | `kubernetes-secret-directory-literal` |

Both match the `/var/run/secrets/kubernetes` prefix, not a required
service-account child or particular credential. Their effective predicates,
scopes, criticality, confidence and platforms are unchanged. The text rule
covers scripts/binaries; the literal rule covers Go source. Different evidence
surfaces and scopes are not merged blindly. Filenames and scope carry those
implementation differences; the directory follows the resource.

The former runtime `kubernetes` aggregate accepted either package imports or
that Go path literal as “Kubernetes Go runtime integration”. It is replaced by
`kubernetes-package-imports`, retaining the three import alternatives and its
existing test-harness downgrade. A path alone no longer satisfies it. Its exact
namespace consumer references the renamed import aggregate. Neither an import
nor its description asserts that an API was invoked.

The apply-client and CI memory-sweep composites explicitly retain their existing
path observations at the new IDs. Kinsing retains both as workload context.
Other runtime-directory suppressions lose path-only support deliberately: a
prefix string is not trusted runtime integration. There are no retired aliases.
The ledger records seven changes; the consumer audit records 14 direct and
ancestor decisions.

## Verification

Run `python3 docs/taxonomy-audit/controls/kubernetes-prefix/check.py`.
Four inert examples verify 16 verdicts: path-only Go and Python, an actual
`k8s.io/client-go` import, and an unrelated import containing that spelling
later in its name. Only the actual import satisfies the package-import and
existing namespace aggregate branches. Examples are scanned, never built or
executed.

Before/after atomscan retains path observations under their resource IDs.
The Go path example loses the unsupported integration finding (risk remains 1);
the Python path example changes 3 → 2. The real import remains at 2 and the
unrelated import at 1. These are classification controls, not an ML accuracy
measurement.

Two new benign ZIP fixtures require general secret-store path findings and
forbid runtime findings for the bare prefix. The full soft fixture gate passes
**1,820/1,820**; no changed-rule hygiene diagnostics remain. Runtime contains
65 rules and general credential paths 37. There are **167 oversized directories
and zero mixed nodes**. Strict validation retains existing cap and unrelated
hygiene failures.

## Remaining work

`os/container/namespace::kubernetes-comp` still labels API paths or a kubeconfig
environment marker as a client library. Updating its import branch does not
solve that aggregate's other alternatives or namespace placement. Audit it and
its exact/ancestor consumers next; do not restore the removed path shortcut.

The apply-client composite still uses unbound text co-occurrence. Python
credential-access rules also retain path-only/public-file observations. Those
claims need separate evidence and consumer repairs. The general directory
prefix does not prove that any child contains a secret or that a file was read.

Follow-up: [Kubernetes namespace audit](KUBERNETES-NAMESPACE.md) retires the
unsupported namespace identity aggregate. The reusable prefix checker now keeps
its 12 import/path verdicts; the 16-verdict result above is historical.

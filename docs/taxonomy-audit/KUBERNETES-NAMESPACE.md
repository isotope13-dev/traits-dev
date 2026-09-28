# Kubernetes references are not Linux namespace operations

Three observations leave `os/container/namespace`:

| Former local ID | New home |
|---|---|
| `k8s-apps-v1-str` | `communications/http/services/kubernetes::apps-v1-path-text` |
| `k8s-pods-v1-str` | `communications/http/services/kubernetes::pods-v1-path-text` |
| `kubeconfig-env-str` | `os/env/config::kubeconfig-name` |

Their effective matchers, scope, platforms, confidence and criticality are
preserved. Descriptions now explicitly say API-path text or environment-name
reference. API route text does not prove a request or identify a client library;
KUBECONFIG names configuration, without proving an environment read or credential
contents. The new API leaf will also be the home for compatible Kubernetes
protocol observations currently scattered through runtime; those are not moved
implicitly in this change.

The `kubernetes-comp` “client library” OR had no external exact consumers and
no directory/ancestor consumers. Its alternatives were imports, API paths and
an environment name, which do not establish a library identity. It is retired,
as is its now-unused `k8s-api-paths` OR. The three atoms remain independently
available. Linux namespace flags/calls remain in their existing namespace home.
There are no aliases at the retired IDs.

## Consumer repair

The Node credential-catalog consumer keeps its existing KUBECONFIG alternative
through the relocated atom. A destination-ancestor audit found the script
catalog consumer claiming reads while accepting the whole `os/env` directory.
It now requires `os/env/read`, and its description says environment access with
cross-vendor secret names. A list of names no longer supplies its access leg.
Its four-category requirement, scope, proximity and exclusions remain unchanged.

This deliberately removes names-only catalog support from downstream consumers.
It does not prove every named value was read or transmitted: that would require
bound data flow beyond access plus co-occurrence. Other destination-ancestor
consumers retain their independent tasking, upload, exploit or named-family
conditions. The PE/DLL-only native tasking consumer cannot inherit these
source-only API atoms under their current scope. Broad HTTP/communications
references must still not be treated as proof of invocation.

The mapping ledger contains seven entries: three moves, two retirements and
two consumer changes. The reference ledger records 30 direct/ancestor decisions,
including the tightened catalog's downstream users.

## Verification

Run `python3 docs/taxonomy-audit/controls/kubernetes-namespace/check.py`.
Six inert Python examples verify **30 verdicts**: two API paths, KUBECONFIG,
a real namespace flag, a names-only catalog, and an environment-reading catalog.
The API/name examples do not become namespace operations; namespace evidence
remains. The reading catalog still satisfies the tightened consumer. Examples
are scanned, never executed.

Before/after atomscan keeps the simple reference examples' risk scores. The
names-only catalog drops **41 → 4**, losing the unsupported suspicious access
finding; the reading catalog remains at **40**. This measures these controls,
not ML accuracy or complete data-flow precision.

Four new benign ZIP fixtures enforce the new homes and names-only behavior.
The earlier prefix checker drops its retired namespace roll-up check while
retaining its import/path checks; all **12** updated verdicts pass. The full
soft fixture gate passes **1,824/1,824**; no changed-rule hygiene errors remain.
Namespace contains 45 rules, the Kubernetes API leaf 2 and environment config 30.
There are **167 oversized directories and zero mixed nodes**. Strict validation
retains existing cap and unrelated hygiene failures.

## Remaining work

The namespace directory still contains OCI/runtime library words, lifecycle-hook
words, CNI references, interface markers and chroot operations alongside Linux
namespace mechanics. These require their own subject and operation audit; a
container association does not justify keeping them under namespace.
Kubernetes runtime also retains API-route observations suitable for the new
HTTP-service leaf. The script catalog's name atoms still live in an objective
tier and some classify configuration pointers as secrets; their independent
placement and consumer meaning remain to be corrected.

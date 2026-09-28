# Kubernetes bearer-token paths

`serviceaccount-token` and `projected-serviceaccount-token` move from
`micro-behaviors/os/container/runtime` to `micro-behaviors/fs/path/token`, keeping
local IDs. The latter description now explicitly says token. Effective scopes,
predicates, confidence, criticality and platforms are preserved. There are no
retired-ID aliases and no new attacker-technique annotations inherited from
neighboring token rules.

The standard-path matcher overlaps the projected-path matcher but they are not
identical bodies: one names the standard Kubernetes mount, the other allows a
variable mount component. They remain distinct observations in this migration.
Neither proves opening/reading a file, using its token, or malicious intent.

Six surviving composites update exact references. The ledger records two
relocations and 20 exact/ancestor-reference decisions. New token ancestry can
supply credential-location context, which fits the resource. Broad filesystem
consumers already admit path evidence; their stronger operation/intent claims
remain separate review debt. No read operation is inferred by this migration.

## Verification

Run `python3 docs/taxonomy-audit/controls/kubernetes-token-path/check.py`.
Five inert JavaScript examples verify 15 exact verdicts: standard/projected token
paths, namespace and CA paths, and an unrelated token filename. Namespace and
CA examples do not satisfy either moved atom. The existing service-account
aggregate keeps its previous results. Samples are scanned, never executed.

Before/after atomscan retains all relevant token observations under their new
IDs. Both token examples remain benign (risk 1 → 2); other examples remain at 1.
Two new benign ZIP fixtures require token-path classification. The final soft
fixture gate passes **1,812/1,812**. Shared defaults remove initial authoring
warnings; no remaining hygiene diagnostics identify the moved file. Runtime has
**71 rules**, token paths **38**, and **167 oversized directories / zero mixed
nodes** remain. Strict validation is still blocked by existing cap/hygiene debt.

## Remaining aggregate defects

The runtime `serviceaccount-files` OR still combines token, namespace and CA
path references while claiming file access. Consequently, moving its token
children alone does not remove transitive runtime context or its suppressions.
That limitation is explicit: this migration fixes the atomic home, not the
aggregate's meaning. Retiring or rebuilding it requires auditing the exact
credential-theft and container-context consumers together with the remaining
resource-path migrations.

A before-change exact trace also shows `node-credential-store-targets` matching
one standard token path despite its “two or more” description. The two satisfied
conditions are token paths and secret-config paths, but the latter finding is
`container-orchestration-tooling-context`, not another secret configuration.
That context should not inhabit a resource-path category. This is a concrete
reason to audit the context and its suppressing consumers next; adding a count
exception would retain the organizational error.

Validator follow-up: a directory cardinality condition counts matching branches,
not distinct resources. Shared evidence routed through a context composite can
therefore satisfy a nominal two-resource claim. Flagging such shared ancestry
for review would complement identical-matcher checks; it is not itself proof
that two rules should merge.

Follow-up: [Service-account resource audit](SERVICEACCOUNT-RESOURCES.md) retires
the runtime aggregate. The reusable checker now follows the token-only aggregate
and rejects namespace/CA alternatives; the results above describe this earlier
migration checkpoint.

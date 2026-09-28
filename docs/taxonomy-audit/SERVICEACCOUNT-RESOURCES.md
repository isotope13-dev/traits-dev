# Service-account resources have different roles

The former runtime `serviceaccount-files` OR treated a bearer-token path,
namespace path and public CA path alike, describing them as file access.
Consumers inherited that conflation as credential evidence. This aggregate is
retired without an alias.

- `serviceaccount-namespace` moves to `fs/path/config/environment`: it names
  deployment configuration, not bearer material.
- `serviceaccount-ca` moves to `fs/path/certificate`: it names a public trust
  certificate, not a private key or the analyzed artifact's signing chain.
- `fs/path/token::serviceaccount-token-path` is the token-only OR over the
  existing standard and projected token-path atoms. Its claim is a resource
  reference, not file access or token use.

Both relocated atoms preserve their exact effective predicates, scope,
criticality and confidence. The token-only aggregate preserves the old scope
and confidence while deliberately excluding public/configuration resources.
Certificate-path placement is distinct from SSH authorization/host-trust key
paths, private-key paths, certificate operations and signing metadata; these
boundaries are documented in TAXONOMY.md. An ambiguous `.pem` suffix is not
sufficient evidence of either certificate or private-key identity.

## Consumer decisions

Credential-oriented consumers now require the token subset: Kubernetes token
abuse, secret dump, object-storage hunt, cloud-metadata pivot, HDF5 sensitive
runtime targets, packed-stage secret exfiltration and supply-chain secret
exfiltration/staging combinations. A CA or namespace file alone can no longer
supply their service-account credential leg. Other required evidence and benign
exclusions remain unchanged.

The privileged-node-pod and CI memory-sweep consumers use the bundle as workload
context alongside separate behavior evidence. They retain explicit token,
namespace and certificate alternatives. Kinsing retains token-path workload
context explicitly. The standard public/configuration paths also still imply
the existing runtime `secrets-path` prefix; relocating these atoms does not
claim to remove every runtime-context or suppression consequence of those
paths. Variable-mount tokens no longer supply the retired runtime aggregate.

The mapping ledger has **15 entries**, including 12 surviving consumer updates.
The consumer ledger records **28 decisions** covering exact and ancestor
references. The new public/configuration locations do not enter credential
path ancestry. Token-directory consumers may see the token aggregate as another
matching rule; it is not another physical resource. The preceding category-pair
repair prevents this from manufacturing another credential category.

## Verification

Run `python3 docs/taxonomy-audit/controls/serviceaccount-resources/check.py`.
Five inert Python examples verify **20 verdicts**: standard/projected tokens,
namespace, CA and unrelated paths, each accompanied by Kubernetes API paths.
Only the token examples retain the existing token-abuse finding. Examples are
scanned, never executed. The earlier Kubernetes token-path checker is updated
to follow the retired aggregate's replacement; all **15** of its verdicts pass.

Before/after atomscan shows CA and namespace examples losing their false token
abuse finding, with risk **42 → 5**. Both token examples retain their existing
finding and risk 42; the unrelated example remains 3. This tests resource
classification, not the correctness of every surviving objective or ML accuracy.

Two new benign ZIP fixtures require the certificate/configuration home and
forbid the token-files objective prefix. The full soft fixture gate passes
**1,816/1,816**. No changed-rule hygiene errors remain. Runtime contains 68 rules,
token paths 39, environment configuration paths 5, and certificate paths 1.
There are **167 oversized directories and zero mixed nodes**; strict validation
still fails on existing cap and unrelated hygiene debt.

## Remaining precision work

Python credential-access rules still conflate some public/configuration paths
with service-account secrets. Generic mounted-secret directories remain in
runtime/token categories despite not identifying a particular child resource.
Go's import/path runtime OR still allows a bundle prefix to claim integration.
These require their own effective-scope and consumer audits.

The surviving token-abuse objective itself accepts token and API *references*;
this migration does not establish token reading, an API call, authentication or
abuse. Several other consumers also use proximity rather than bound data flow.
Their operation/intent claims need stronger evidence and dedicated controls.
Those limitations are separate from the public-file credential shortcut fixed
here; fixture success is not proof that these remaining claims are exact.

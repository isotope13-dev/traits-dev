# A filename/member reference is not a Kubernetes read

The former runtime atom `serviceaccount-token-read` matches the text
`/ "token").read_text`. It requires neither a call nor a Kubernetes path.
A local parser token and a stored method reference both satisfy it. Its new home
is `metadata/file/string/file::token-read-text-reference`, described as
“Token filename beside read_text member text”. The predicate, script/binary
scope, platforms, criticality, confidence and sample reference are unchanged.
There is no retired-ID alias.

The exact `incluster-apply-client` consumer explicitly references the relocated
observation, preserving its existing condition. Four runtime-directory consumers
lose this unsupported container signal: container-tooling context, two
suppression/downgrade contexts, and the Kinsing container/cloud marker.
No destination-directory consumers exist in the audited snapshot. The mapping
ledger preserves effective before/after rules; the consumer ledger records all
five decisions. No identical effective matcher was consolidated in this change.

## Verification

Run `python3 docs/taxonomy-audit/controls/container-token-read/check.py`.
Five examples verify ten verdicts: ordinary token reads, a method reference,
another filename, a path alone, and the existing Kubernetes apply combination.
Only the Kubernetes example satisfies the apply composite. Method-reference
text intentionally still matches metadata; it must not be promoted to an
operation by directory membership. Examples are scanned, never executed.

Before/after atomscan retains the Kubernetes apply finding. The local example
loses both the runtime atom and derived container-tooling context, gaining the
neutral metadata observation instead. Its risk remains 3; the Kubernetes
example changes 41 → 42 while retaining its suspicious apply finding. These
numbers are control results, not measured ML accuracy.

Two new benign ZIP fixtures require file-text metadata and forbid container
runtime and bearer-token path claims. The full soft-validation fixture gate
passes **1,810/1,810**. No hygiene diagnostics identify the changed rules.
Runtime has **73 rules**, the destination **35**, and mixed nodes remain zero.
There are **167 oversized directories**, unchanged from this cohort's starting
snapshot; the preceding checkpoint's 166 is an earlier shared-worktree snapshot.
Strict validation remains failing on existing hygiene/cap debt.

## Remaining service-account resource audit

These findings are not completed migrations:

- `serviceaccount-token` and `projected-serviceaccount-token` identify defined
  bearer-token locations and belong in `fs/path/token`, preserving their
  differing exact/projected patterns and effective scope.
- `serviceaccount-namespace` identifies ordinary deployment configuration;
  audit `fs/path/config/environment` as its home, not credential access.
- `serviceaccount-ca` identifies public trust material. Audit certificate-path
  siblings before adding a dedicated `fs/path/certificate` leaf; do not put it
  under private keys, bearer tokens, or signing-certificate metadata. A file
  reference is distinct from the analyzed artifact's signing certificate.
- `secrets-path` and Go `k8s-service-account-path` identify a mounted bundle
  prefix, not its contents or an operation. Go's `kubernetes` import/path OR
  currently lets a path alone claim runtime integration. Reconcile the bundle
  observation and remove that shortcut when migrating the pair.
- `container-runtime-secrets-path` and `fs/path/token::container-run-secrets`
  identify generic secret mounts, not necessarily bearer tokens. Audit them
  together; text/literal matching, scopes and exclusions currently differ.
- `serviceaccount-files` is a paths-only OR over token, namespace and CA files,
  yet claims access. Audit every exact consumer before retiring that aggregate:
  container context can use explicit resource references; credential-theft
  claims need credential-bearing resources and independent operation evidence.
- Python credential-access atoms and encoded-path equivalents repeat related
  observations. Some match token, namespace and CA filenames interchangeably.
  Compare scope, encoded representation and benign-client exclusions before
  consolidation; a shared substring is not sufficient proof of equivalence.

The apply composite still combines text across a file; it does not bind the
read receiver to the service-account directory, or prove an HTTP apply call.
Preserving its predicate is not a claim that its data-flow precision is solved.
A subsequent repair needs bound-read/request controls and deliberate accounting
for embedded or compiled representations.

Validator candidate: a claim of a read/call backed only by member-name text
should receive evidence review. This is separate from duplicate detection;
API fingerprints can be useful when accurately described, so rejecting every
text matcher would be inappropriate.

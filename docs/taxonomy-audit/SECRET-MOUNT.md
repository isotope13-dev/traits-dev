# A secret directory does not identify a bearer token

Two observations move into `micro-behaviors/fs/path/credential`:

| Former ID | New local ID |
|---|---|
| `os/container/runtime::container-runtime-secrets-path` | `runtime-secret-directory-text` |
| `fs/path/token::container-run-secrets` | `runtime-secret-directory-literal` |

Both identify conventional secret-store directory references without identifying
what kind of material a child contains. Their shared home is the general
credential-path category, not bearer tokens or container runtime. A defined
child resource continues to use its specific category, including public
certificates or deployment configuration; its parent name does not turn that
child into a credential.

The effective predicates, scopes, confidence, criticality, annotations and
exclusion/downgrade clauses are preserved. The matchers are not identical:
the text form has case-insensitive leading boundaries and an optional `var/`;
the parsed-literal form has different boundaries, case behavior and scope.
They are not merged simply because both mention `/run/secrets`. No aliases
remain at their old locations.

Nine surviving consumers change. Exact references retain the same observations.
`any-credential-path` and `sensitive-secret-path-any` explicitly retain the old
literal alternative that previously arrived through token ancestry; the broader
text matcher is not added to those sets. Kinsing retains the former runtime text
observation explicitly as workload context. The private-key-directory exclusion
keeps the same condition, with its comment updated to the canonical home.

Generic mount references no longer count toward token-category pairs. Runtime
ancestry also stops admitting the relocated text atom. Thus a generic mount
alone no longer supplies runtime-based downgrades; the literal observation can
remain notable instead of being downgraded to baseline by its neighboring
mount-text rule. Actual runtime evidence and named-tooling alternatives remain.
This is an intentional consequence of removing unsupported container context,
not a change to the moved rules' criticality or suppression clauses.

## Verification

Run `python3 docs/taxonomy-audit/controls/secret-mount/check.py`.
Four inert JavaScript examples verify **16 verdicts**: a generic secret mount,
that mount plus Docker configuration, a defined service-account token plus
Docker configuration, and an unrelated path. Only the defined token plus config
satisfies the multiple-category rule. Both broad secret-path consumers retain
location evidence. Examples are scanned, never executed.

Before/after atomscan preserves risk scores 1, 3, 3 and 1 respectively. The false
token/config pair disappears for the generic mount, while the genuine category
pair remains. Two new benign ZIP fixtures require the generic credential-path
home and forbid token-path findings. The full soft fixture gate passes
**1,818/1,818**; no changed-rule hygiene diagnostics remain.

The mapping ledger has **11 entries**, including both relocations and nine
consumer updates; the consumer ledger records **21 reference decisions**.
Runtime contains 67 rules, token paths 38, and general credential paths 35.
There are **167 oversized directories and zero mixed nodes**. Strict validation
still fails on existing cap and unrelated hygiene debt.

Remaining work includes Kubernetes-specific mounted-bundle prefixes, the Go
import/path integration OR, Python path-only credential rules, and objective
composites whose operation/intent claims exceed path evidence. The current
broad private-key exclusion also remains file-wide: this migration does not
claim to solve its possible suppression of an unrelated key elsewhere in the
same file. These require consumer-specific controls rather than another
resource-category shortcut.

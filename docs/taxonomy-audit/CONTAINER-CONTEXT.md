# Context is not a credential path

The former `fs/path/secret-config::container-orchestration-tooling-context`
contained only runtime/software context alternatives. Nevertheless, its position
made every match available as a secret-configuration path. A Kubernetes service
environment variable could therefore supply credential-path evidence without
naming any file.

The rule is retired. Its only exact use was a downgrade of
`fs/path/credential::container-credentials`; the same six alternatives now live
directly in that downgrade clause. Both rules had identical effective file-type
and platform scope, so this inlining preserves the direct consumer's weighting.
No alias or replacement emitted context rule is added. This does not endorse
runtime context as proof of trusted tooling or ownership: that broad weighting
remains explicit follow-up debt.

## Cardinality repair

Removing the context rule exposed a second problem. `needs: 2` over directory
references counts matching rules, including multiple overlapping rules within
one directory. A standard service-account token path matched three token rules
and still satisfied `node-credential-store-targets` on its own. Before removal,
the misplaced context had also supplied secret-config support.

The old aggregate is replaced by `multiple-credential-path-kinds`. It accepts
six explicit pairs among token, private-key, secret-config and wallet categories;
each pair requires both category predicates with `all`. The neutral pair
observations share the existing cross-family `fs/path/credential` leaf and are
notable: each communicates an independently useful resource combination.
The two exfiltration consumers reference the new aggregate. Ordinary application
data is excluded because it need not contain credentials. Existing JavaScript /
TypeScript scope and the Node IPC exception are preserved.

This deliberately stops overlapping matches, multiple paths within only one
category, and ordinary app-data evidence from satisfying a claim about multiple
credential categories. It does not erase the underlying path observations or
separate exfiltration findings. It proves category co-occurrence, not distinct
physical files, reading, or exfiltration; consumers must supply their operation
and intent evidence independently. No filenames or fixture expectations were
weakened to preserve the old shortcut.

## Verification and remaining work

Run `python3 docs/taxonomy-audit/controls/container-context/check.py`.
Three inert examples check nine verdicts: runtime-only context, one token path,
and token plus Docker credential configuration. Runtime-only context supplies
no credential-path aggregate; one path cannot satisfy multiple categories;
two categories do. The existing container-credential downgrade still triggers
on the token-path control. Examples are scanned, never executed.

Before/after atomscan confirms that context-only secret-config findings disappear
while real token and Docker config observations remain. The three controls keep
their benign risk scores (3, 2, and 3 respectively). Two new ZIP fixtures require
the actual subject and forbid the false secret-config path finding. The final
soft fixture gate passes **1,814/1,814**; no changed-rule hygiene errors remain.
There are **167 oversized directories and zero mixed nodes**. Credential paths
contain 33 rules and secret-config paths 49. Strict validation retains existing
cap and unrelated hygiene failures.

The mapping ledger contains 11 entries, including the retirement, inlined
consumer, category-pair rules, and two objective reference updates. The consumer
ledger contains 18 direct and ancestor decisions. This change does not resolve
the runtime `serviceaccount-files` paths-as-access aggregate, generic secret
mount placement, public certificate/namespace paths, or the remaining broad
filesystem consumers' operation claims.

Validator candidate: flag directory references used for a distinct-resource or
distinct-category cardinality claim. A directory can contribute several matched
rules, and those can share the same bytes. This is different from identical-body
deduplication. Explicit pair predicates fix this case without changing global
engine counting semantics or introducing directory exceptions.

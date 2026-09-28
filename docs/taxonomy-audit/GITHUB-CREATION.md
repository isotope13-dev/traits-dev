# Repository endpoints do not establish creation

The GitHub creation OR accepted a bare `/user/repos` path. Its broader roll-up
also accepted `X-GitHub-Api-Version` near `auto_init`. Neither observation proves
creation: the path has no method, and the fields need not participate in any
request. The same field combination fed a hostile repository-exfiltration rule.

This repair makes five effective-definition changes:

- `github-create-repo-api` no longer accepts the bare collection path. Its
  explicit POST route and shell POST request alternatives remain.
- `github-create-repo` no longer accepts the field-only shortcut. Explicit
  authenticated-user and organization creation call alternatives remain.
- `github-create-repo-rest-fields` retires. Combining a version header with an
  initialization label does not add a coherent operation to either observation.
- Its now-unused `github-create-repo-auto-init-field` retires. This weak substring
  neither identifies GitHub nor supplies independently useful operation evidence.
- `objectives/exfiltration/http/upload::github-repo-contents-token-exfil-rest`
  now requires canonical repository creation rather than that field combination.

The bare endpoint atom and version-header atom remain available. Their useful
observations are not discarded or demoted. No compatibility aliases are added.
The ledger records before/after effective definitions; the consumer audit covers
37 direct and ancestor decisions, including GitHub directory exclusions.
Those exclusions must not be activated by a generic initialization label.

## Verification and coverage boundary

Run the exact creation-composite checks without executing the JavaScript:

```sh
python3 docs/taxonomy-audit/controls/github-creation/check.py
```

All seven pass: explicit POST, authenticated-user creation and organization
creation match; bare path, GET route, fields-only and unresolved helper do not.
Read-only atomscan before/after corroborates removal of the false creation
findings for the bare path, fields-only and unresolved helper. All these neutral
controls remain low risk; this repair does not manufacture malicious intent.

The unresolved helper control contains a GitHub host literal and
`api("/user/repos", "POST", ...)` without a helper definition. The old rule
called this creation solely because of the path. Removing that unsupported
inference is intentional. Recovering real helper-mediated creation requires
binding its request destination and method; mere proximity must not restore it.
Likewise obfuscated implementations retaining only `auto_init` and a header no
longer receive a creation claim from this rule. Other independently supported
findings continue to apply.

Both the initial and final full fixture gates pass **1,790/1,790**. GitHub contains **82 rules**;
**167 oversized directories and zero mixed nodes** remain. Six concurrent Android
rule additions were recorded separately from the five changes above.

## Follow-up

This is not a claim that all GitHub operation inference is repaired. In particular,
`github-create-repo-and-contents-write` still admits a contents endpoint without
binding a write; listing composites infer activity from endpoint/option text;
and broad GitHub exceptions lack destination-bound authentication. These require
their own positive and negative controls. Existing route/call matchers also need
review for comments, receiver identity and local shadowing. The service hierarchy
and generic GraphQL/GitLab overlaps remain as recorded in GITHUB-OPTIONS.md.

Validator opportunity: an OR roll-up named for mutation should not inherit
endpoint-only or field-only evidence as though it proved the operation. An
identical-body check cannot establish that logical implication; the audit must
inspect the weakest alternative and its downstream intent consumers.

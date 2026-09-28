# Generic options are not GitHub activity

The GitHub service leaf held 87 rules. Three observations had provider-specific
names and homes without provider-specific matchers: a recursive option, a
per-page count, and a bare `/graphql` literal. They now have canonical homes:

| Old GitHub local ID | New home and local ID |
|---|---|
| `github-recursive-query-enabled` | `metadata/file/string/traversal::recursive-option-enabled-text` |
| `github-repository-page-size-option` | `metadata/file/string/limit::per-page-option-text` |
| `github-graphql-path-option` | `micro-behaviors/communications/http/graphql::graphql-path-literal` |

Matcher bodies, scope, exclusions, confidence and criticality are unchanged.
The option fragments remain components; the GraphQL endpoint reference remains
notable. No identical matcher bodies were found elsewhere in the production
snapshot. No aliases or parent rules were introduced. The destination leaves
contain 1, 2 and 9 rules respectively; GitHub now contains 84.

Four local composites now reference the new exact IDs: recursive Git trees,
paginated private organization/user repository lists, and GraphQL request options.
Their other conditions and proximity constraints are unchanged. The mapping and
consumer audit record three moves and 23 exact/ancestor reference decisions.
Directory consumers intentionally lose evidence that never established their
subject. In particular, generic options cannot justify a GitHub exception.
GraphQL remains HTTP evidence, but no longer inherits GitHub-only exceptions.

## Consumer evidence and verification

Read-only atomscan controls pair each generic observation with either no operation
or `requests.post(..., data=dict(os.environ))` to an unrelated HTTPS collector.
All three ordinary settings remain benign. Before the change, each generic
observation activated a GitHub directory exclusion: only the suspicious HTTP
body-flow atom appeared for the upload (risk 42). Afterwards, the upload also
produces `python-env-harvest` at hostile (risk 156). This is intentional recovery
of detection, not a severity change to the moved atoms.

Nine ZIP fixtures use an ordinary inner `client.py` path:

- Three settings-only controls forbid the GitHub service prefix.
- Three environment-upload controls require the credential-harvest objective.
- Three actual GitHub endpoint controls preserve GraphQL, tree-query and
  paginated organization-list coverage.

The checkout engine passes **1,790/1,790 fixtures** with `validate --soft`.
Effective-definition comparison found only the three moves and four reference
updates. There are **167 oversized directories and zero mixed nodes**.
Strict validation still has separate description/suppression debt as well as
those oversized directories; a soft pass does not establish completion.

## Remaining precision audit

Meeting the cap does not complete this service family's semantic audit. Reading
the GitHub leaf, its GitLab/code-forge siblings, generic GraphQL leaf and metadata
destinations identified these follow-ups:

- GitHub `type=private`, `visibility=private`, affiliation and `auto_init`
  fragments still lack provider evidence. Classify their literal subjects
  before deciding whether stronger operation matchers are warranted.
- A query string on `/user/repos` does not establish GET or enumeration; a
  bare path does not establish POST or creation. The create-repository roll-up
  currently accepts the bare path. Provider-plus-field combinations likewise
  need more evidence before claiming creation or a transmitted write.
- `github-contents-template-api` matches only the repository URL template,
  not `/contents`; the installation-token atom similarly matches an installation
  path without the token suffix. Correct these claims and their consumers.
- GitLab public-object selectors and version directives overlap generic GraphQL
  selectors/directives. Decide canonical ownership from the schema evidence,
  then preserve exact scopes when consolidating; do not merge by name alone.
- Code-forge contribution and publication directives are textual instructions,
  not proof that a request was sent. Their labels and consumers need that boundary.
- `services/` mixes named providers with functions such as analytics, payment,
  registry and file hosting. Its eventual partition needs an explicit provider
  versus operation contract; do not add a `library` or `client` overflow branch.
- Broad GitHub exclusions still accept endpoint references anywhere in a file.
  A destination-bound authentication relationship is stronger evidence of
  legitimate token use. The three removals close demonstrated suppression holes,
  but do not prove the remaining directory exclusions sound.

Validator opportunity: audit literals used through directory-level exclusions
as well as positive intent legs. Exact-body duplicate detection cannot detect
an incorrect service claim or an unrelated token suppressing a transfer.

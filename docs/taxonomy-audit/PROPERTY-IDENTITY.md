# Property access, vocabulary and object shape

## Implemented organization

The historical `data/source/property/identity` leaf is retired. Its thirteen
observations now follow their actual subjects:

- Three customer/contact/account labels → `metadata/file/string/account`.
- Turbine-speed vocabulary → `metadata/file/string/device`.
- Client-UUID, code-snippet and flags identifiers → `metadata/file/string/identity`.
- Two member-access observations → `data/property/access`.
- Three object-key syntax observations → `data/serialize/schema-object`.
- A CommonJS exported-object shape → `os/module/export`.

The adjacent `data/source/property/read` leaf is also retired. Twelve property
access observations move to `data/property/access`; two unresolved Rust `.get()`
call observations move to `data/control-flow/dispatch`. A generic method name
cannot establish HTTP or even a particular container type. Access, rather than
read, is the common directory claim: a member AST node can also occur in a write.
Descriptions of the thirteen identity observations no longer infer collection,
schema relationships, a machine identity from `mid`, or a result read from a
member reference alone.

The first twenty-seven relocations preserve effective predicates, scopes,
criticalities, confidence, count constraints and filters, modulo qualified
references. No identical atomic `if` bodies were found across the destination
leaves. Similar method/field patterns are not interchangeable where syntax,
scopes or exclusions differ.

The engine's data-category registry now admits `property`; all eighteen directory
validation tests pass, including the updated valid-structure case. A release
build completed. TAXONOMY.md documents the new boundaries and retired namespace.

## Consumers and a reproduced false positive

Both directory-wide identity consumers retain their original thirteen named
alternatives. The HTTP consumer also requires an independent Git path. A new
canonical `fs/path/secret-config::git-configuration-path` composite preserves
its two original Git alternatives, allowing identity alternatives in the outer
`any` group without mixing the two Boolean requirements. No broad destination
reference substitutes unrelated sibling evidence.

The DNS helper's 2,048-byte proximity requirement is preserved as one required
dot join plus any original identity observation. Direct controls confirm that
nearby evidence matches and evidence separated by more than 2,048 bytes fails,
even though both component conditions match in the latter control.

That positive control exposed a false claim: the helper detected a field name
near a dot join, not DNS assembly or data flow. It is the twenty-eighth
relocation, now `data/string/concat::named-fields-near-dot-join`, described as
co-occurrence. Its inherited DNS-exfiltration ATT&CK tag is removed. Its exact
DNS objective consumer keeps the dependency and still requires its own resolver
and host/user-query context.

This intentionally narrows broad `objectives/exfiltration` consumers: a neutral
join must not satisfy their exfiltration requirement. Four such references were
audited: a package-manifest rule (incompatible with this helper's JavaScript
scope), two MCP configuration-injection rules, and a multi-browser stealer rule.
They no longer inherit this neutral helper. They were not given a replacement
neutral fallback that would perpetuate the classification error.

A benign control merely writes local JSON settings, contains host/user labels,
and joins two constant values with a dot. Before correction it triggered
`windsurf-mcp-injection` as suspicious, scoring **42/41** for archive/member.
After correction it has **no suspicious or hostile findings**, scoring **5/4**.
`dot-join-config-without-exfiltration.zip` permanently checks this regression.

## Verification

The [53-entry ledger](property-identity-mapping.json) records twenty-eight
relocations, twenty-four consumer updates and the new Git-path composite. Every
after-definition verifies against current YAML. The twenty-seven straightforward
relocations were separately checked for unchanged matching conditions.

Initial three-control scans gave eight archive/member comparisons with identical
finding sets and criticalities modulo the migration map. This is not wholly
score-neutral: the multi-language archive rises 7→8 and its JavaScript member
4→6; the other six scores are unchanged. The near/far fixtures were subsequently
strengthened to use a named receiver for `.join`, so the join atom actually
matches. Direct rule traces verify the positive and negative proximity cases;
the initial scan comparison is not a claim about those subsequently edited bytes.

Four new benign fixtures are permanent. All **1,697/1,697 fixtures pass** after
the final helper correction and fixture changes. Strict `make validate` exits 2
only on **173 oversized directories**. There are **zero mixed rule directories**.
The principal destination counts are property/access 14, schema-object 83,
string/concat 39, dispatch 43, module/export 1, account vocabulary 22, device
vocabulary 4, identifier vocabulary 59, and secret-config 50.

Logs: `/tmp/taxonomy-property-identity-{before,after}.json`,
`/tmp/taxonomy-property-identity-config-{before,after}.json`,
`/tmp/taxonomy-property-identity-{near,far}-final-trace.log`,
`/tmp/taxonomy-property-identity-{soft,strict}-final.log`,
`/tmp/taxonomy-property-identity-engine-tests.log`.

## Remaining audit and validator opportunities

The other property siblings still need semantic separation: assignments include
a generic `.put()` call; attributes includes an ordinary attributes-member
access; computed mixes access, invocation and argument vocabulary; transition
mixes buffers, loops, definitions and ordering/proximity claims. Move each by
its supported operation rather than relocating these mixed leaves wholesale.

Some existing access descriptions assert reads from text/member syntax that can
also occur in writes or quoted examples. The actual positive/negative evidence
needs review before tightening those matchers. Generic identifier vocabulary and
object serialization leaves likewise need a wider subject audit; being below
the cap does not finish their organization.

The preserved hostile HTTP/DNS consumers still rely on co-occurrence, not bound
source-to-destination data flow. This cohort preserves their explicit dependencies
while correcting the independently demonstrated neutral-helper leak; it does
not claim to solve every relationship weakness in those consumers.

Validator improvements worth pursuing: flag objective helpers without the
claimed operation, and show which descendant of a broad objective reference
actually supplied its evidence. A proximity constraint establishes nearby
observations; it must not be presented as proof that one value feeds another.

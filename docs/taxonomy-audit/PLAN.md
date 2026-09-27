# 85-rule taxonomy audit and migration plan

Snapshot: 2026-09-26, traits revision `a8b72b286f0d2ac29e005e151472eaaf701b596e`.
Validator checkout: `../cleave`, based on `a1819d4a488714542871132564b36753722aa3a2`.

The cap measurements below retain that initial snapshot. The follow-up
[implementation-layer audit](IMPLEMENTATION-LAYERS.md) records its own later
snapshot; do not combine the two sets of counts.

## Decision and measured impact

### Latest checkpoint: unbound API argument-byte claims repaired

[Call-argument byte audit](CALL-ARGUMENT-BYTES.md) reproduces six false OpenSSL
operation claims on inert ELF controls whose calls target a local return stub.
Six observations move to metadata; a beacon consumer retains its predicate
under a corrected name. Seven ledger entries and ten ancestor decisions record
the changes, including two intentional profile criticality corrections.
**1,755/1,755 fixtures pass**; strict validation reports **169 oversized
directories**, with zero mixed nodes. Actual call-target binding remains a
requirement before these byte shapes can support an API-operation claim.

### Latest checkpoint: warning suppression consolidated

[Warning suppression audit](WARNING-SUPPRESSION.md) moves general urllib3
warning control to diagnostics, merges a narrower matcher into the existing
canonical rule, and retires a redundant OR roll-up. Twelve ancestor decisions
remove warning suppression as HTTP/communications evidence. Three fixtures
separate warning controls from disabled verification. **1,753/1,753 fixtures
pass**; **169 oversized directories** remain. The literal option/guard observation
and other legacy TLS operations still need audit.

### Latest checkpoint: canonical TLS verification-disable operation

[TLS verification consolidation](TLS-VERIFICATION.md) moves nineteen rules from
HTTP/socket branches to `communications/tls/verify/disable`, retiring `http/ssl`.
All moved effective predicates are unchanged. Fifty ledger entries and seventeen
ancestor decisions cover the moves and consumers; five controls retain identical
findings modulo IDs. **1,750/1,750 fixtures pass** on the rebuilt engine; strict
validation reports only **169 oversized directories**, with zero mixed nodes.
Remaining TLS observations still need operation-based placement and precision
repairs described in the preceding boundary audit.

### Latest checkpoint: TLS evidence boundaries

[TLS boundary audit](TLS-BOUNDARIES.md) moves generic NSPR I/O and domain-intel
vocabulary out of socket TLS, preserves the corroborating I/O composite, and
removes an unsupported word-only exclusion from disabled-verification detection.
Three controls and eight ancestor decisions cover the changed boundaries.
**1,745/1,745 fixtures pass**; socket SSL is **85 rules**, leaving **169 oversized
directories** and zero mixed nodes. The report records the operation-based
reorganization needed across socket/ssl, http/ssl and http/tls.

### Latest checkpoint: accounting literal claims corrected

[Accounting literal audit](ACCOUNTING-LITERALS.md) moves eleven rules whose
matchers detect quoted text, not the source declarations their old names claimed.
Before/after traces preserve all eleven literal matches and reject actual syntax.
The ledger and 89 ancestor decisions document intentional removal of vocabulary
from compiled-language suppression. **1,742/1,742 fixtures pass**; **170 oversized
directories** remain. The account/accounting sibling-name advisory is reviewed
as distinct subjects, without a validator exemption. The engine now makes
shared-stem reviews non-blocking; strict validation reports only cap debt.
Remaining compiled-source
and runtime observations still require audit.

### Latest checkpoint: WebAssembly declarations separated from attribution

[WASM observations](WASM-OBSERVATIONS.md) moves seven parsed export/producer
facts to existing metadata subjects and preserves three attribution profiles.
The ten-entry ledger and 105 ancestor decisions document effective predicates
and intentional removal of weak suppression evidence. Three inert controls test
exports, name-only text, and isolated-helper attribution. **1,740/1,740 fixtures
pass**; **170 oversized directories** remain, with zero mixed nodes. Strict
validation reports only cap debt. `lang/compiled` is now 79 rules but still
contains misplaced source/runtime observations requiring further audit.

### Latest checkpoint: graphics vocabulary and provider identity

[Graphics audit](GRAPHICS-VOCABULARY.md) moves nine observations, retires three
weak library-reference aggregates, and replaces word-only Mesa identity with
provider-name/interface evidence. Four controls distinguish vocabulary, identity,
and each missing requirement. The 30-entry ledger and 74 ancestor decisions
record the migration and associated duplicate/hygiene repairs. **1,737/1,737
fixtures pass**, with **171 oversized directories** and **zero mixed nodes**.
Strict validation still fails on that cap debt; the overall plan remains open.

### Latest checkpoint: ABI recognition repaired with consumer cleanup

[ABI repair audit](ABI-REPAIR.md) fixes two normalization-sensitive regexes,
removes unsupported library identity and exception-obfuscation inferences,
and consolidates sparse-string predicates and redundant wrappers. The 21-entry
ledger excludes unrelated concurrent archive edits; 95 ancestor occurrences
are reviewed. A directory-reference cycle is avoided by retaining system-fn's
five original primitive alternatives. **1,733/1,733 fixtures pass**; **172
oversized directories** remain, with zero mixed nodes. The previously recorded
ABI matching gap is closed; broader library and binary-metric audits continue.


### Latest checkpoint: binary declarations and string counts separated from intent

[Binary observation audit](BINARY-OBSERVATIONS.md) relocates eleven observations
and records twenty-seven consumer updates in a verified 38-entry ledger.
Thirteen ancestor occurrences are audited. Binary-metrics/shape falls **88→85**,
reducing cap violations to **172** with zero mixed nodes. **1,730/1,730 fixtures
pass**. A pre-existing ABI-symbol normalization gap is reproduced before and
after migration and remains open; its library-family exclusions must be audited
when repairing those regexes. Remaining Mesa references and other binary metrics
still need precise placement.


### Latest checkpoint: runtime-indirection directory retired

[Runtime profile audit](RUNTIME-PROFILES.md) moves three observations, retires
two unsupported aggregates and preserves three specific exclusions in an
eight-entry ledger. Thirteen ancestor consumers are audited. Neutral conversion
no longer receives an obfuscation verdict, and package tests no longer supply
exfiltration evidence. Four controls bring the gate to **1,728/1,728 passing
fixtures**; strict validation still reports **173 oversized directories**, with
zero mixed nodes. Binary string-count/graphics dependencies, remaining
code-metrics, source/syntax and retry branches still require work.


### Latest checkpoint: runtime-indirection atoms separated from decoding claims

[Runtime observation audit](RUNTIME-OBSERVATIONS.md) moves two neutral atoms to
identifier metadata and character conversion, updates their composite and
preserves a conservative helper exclusion. The four-entry ledger and five
ancestor decisions document preserved matching and intentional concealment
boundary corrections. **1,724/1,724 fixtures pass**, with **173 oversized
directories** and zero mixed nodes. The three remaining runtime-indirection
composites still require a semantic audit; this checkpoint does not endorse
their existing category or intent claims.


### Latest checkpoint: source/array leaf retired into semantic subjects

[Array operation audit](ARRAY-OPERATIONS.md) relocates all eighteen rules and
updates fourteen exact consumers in a verified [32-entry ledger](array-operations-mapping.json).
The obsolete source/array directory is removed with no remaining YAML references.
Four new controls include standalone Rust zero initialization.
**1,722/1,722 fixtures pass**; strict validation reports only **173 oversized
directories**, with zero mixed nodes. Remaining source/syntax, runtime-indirection,
retry and composite-relationship audits remain in scope.


### Latest checkpoint: hexadecimal notation separated from operations and concealment

[Hexadecimal observation audit](HEX-OBSERVATIONS.md) relocates nine observations
and updates eighteen consumers in a verified [27-entry ledger](hex-observations-mapping.json).
Twenty-one ancestor consumers were audited. Matchers, scopes and criticalities
are preserved; names no longer invent mixed radices, arrays, string operations
or decoding. The hex obfuscation leaf falls from **30 to 23 rules**.
**1,718/1,718 fixtures pass** with four new controls; strict validation reports
only **173 oversized directories**, with zero mixed nodes. Remaining composite
relationships and source-array, runtime-indirection and retry siblings are
recorded for continued migration.


### Latest checkpoint: function shape and computed access placed in neutral subjects

[Neutral function-shape audit](NEUTRAL-FUNCTION-SHAPE.md) moves six observations
to function metadata, property access and dispatch; six exact consumers and five
ancestor consumers are recorded in a [12-entry ledger](neutral-function-shape-mapping.json)
and accompanying inventory. Threshold-distinct metadata siblings remain separate.
**1,714/1,714 fixtures pass**, including three new controls. Strict validation
reports only **173 oversized directories**, with zero mixed nodes. The report
records a standalone debugger stall and the remaining runtime-indirection,
retry and hexadecimal sibling audits.


### Latest checkpoint: archive regression repaired; full fixture gate restored

[Archive validation audit](ARCHIVE-VALIDATION.md) repairs cross-member
retroactive suppression and a separately reproduced container-evaluation
starvation bug. **29 unit tests** pass, and the encrypted-stage fixture again
retains three hostile findings and its required staged-payload observation.
The rebuilt checkout engine passes **1,711/1,711 fixtures** with unchanged
expectations. Strict validation fails only on **173 oversized directories**.
Resume the remaining neutral-obfuscation and oversized-leaf migration work.


### Latest checkpoint: capture-free AST queries repaired and misclassified observations moved

[AST capture audit](AST-CAPTURES.md) repairs five canonical observations from six
inert queries, consolidates the nested-array duplicate, and moves unsupported
encoding/timing/family claims to neutral homes. A [12-entry ledger](ast-capture-mapping.json)
and seventeen ancestor consumers were verified. Five direct positive and five
negative query checks pass, as do six new fixture controls. Strict validation
reports only **173 oversized directories**, with zero mixed nodes.

**Historical verification failure, resolved above:** the then-newly rebuilt checkout engine
loses an existing encrypted-stage archive finding with both the before and
after rules. The installed engine retains it with both. The report records
this isolated engine regression; fixture requirements remain unchanged.


### Latest checkpoint: computed dispatch and member access classified by evidence

[Computed-dispatch audit](COMPUTED-DISPATCH.md) relocates thirteen neutral
observations, retires one redundant aggregate and records ninety-three consumer
updates in a [107-entry ledger](computed-dispatch-mapping.json). Seventy-five
ancestor consumers were audited. An inert AST query now captures indexed
addition with a verified negative boundary. Five new fixtures bring the corpus
to **1,705/1,705 passing**; strict validation reports only **173 oversized
directories**, with zero mixed nodes. Syntax remains oversized at 101 rules.
Remaining neutral obfuscation measurements, six capture-free AST queries and
relationship-sensitive composites are documented for the next audit.


### Latest checkpoint: property operations migrated and reference validation corrected

[Property operation audit](PROPERTY-OPERATIONS.md) completes retirement of
`data/source/property`, with **53 relocations** and a verified
[113-entry ledger](property-operations-mapping.json). An overlooked ancestor
consumer now retains all **74** former alternatives. The attributes matcher is
repaired, and the validator no longer requires widening partial `any` lists or
replacing `all` conjunctions. **75 validator tests** and **1,700/1,700 fixtures
pass**; strict validation reports only **173 oversized directories**, with zero
mixed nodes. The report records the local dependency used for engine validation
and remaining computed-call, loop-duplicate and relationship audit work.


### Latest checkpoint: property identity split and false exfiltration helper corrected

[Property audit](PROPERTY-IDENTITY.md) retires the historical identity/read leaves,
classifies twenty-eight observations by their supported subjects, and preserves
consumer alternatives in a [53-entry ledger](property-identity-mapping.json).
A field/dot-join helper is now neutral; this removes a reproduced suspicious
MCP-injection false positive (archive/member scores **42/41→5/4**). Direct traces
verify its 2,048-byte proximity behavior. Eighteen engine directory tests and
**1,697/1,697 fixtures pass**. **173 oversized directories** and zero mixed nodes
remain; the report identifies the remaining property-sibling and relationship
work. The wider migration remains incomplete.


### Latest checkpoint: account vocabulary receives a canonical home

[Account vocabulary audit](ACCOUNT-VOCABULARY.md) moves nineteen observations
from relational schema, serialization and telemetry to neutral account naming.
The [26-entry ledger](account-vocabulary-mapping.json) verifies preserved matching
conditions and consumer references. Four archive/member controls preserve
findings and criticalities; their aggregate scores fall by one point, documented
as a classification effect. **1,693/1,693 fixtures pass**, with **173 oversized
directories** and zero mixed nodes. The report identifies the remaining
source-property, telemetry and relationship-consumer audit work.


### Latest checkpoint: SQL mutation operations separated

[SQL operation audit](SQL-OPERATIONS.md) moves fifteen syntax observations into
row-write, row-delete and schema-delete leaves while preserving predicates and
consumer alternatives. The [31-entry ledger](sql-operations-mapping.json)
verifies against current definitions. Three new controls preserve findings and
scores across six archive/member comparisons; **1,691/1,691 fixtures pass**.
SQL falls from **78 to 65 rules**; **173 oversized directories** and zero mixed
nodes remain. Editor/API fragments, account fields and catalog siblings are the
next documented precision work; the wider migration is incomplete.


### Latest checkpoint: SQL-based suppression dependency removed

[SQL suppressor audit](SQL-SUPPRESSORS.md) moves eleven language/vocabulary
observations to neutral homes, removes unrelated SQL exclusions and retires a
string-pattern-only dropper verdict. The [22-entry ledger](sql-suppressors-mapping.json)
verifies. The metadata section-filter recommendation is now advisory as its
validator contract intended; five related tests pass. Six archive/member checks
exercise SQL-present and SQL-absent controls, and **1,688/1,688 fixtures pass**.
IRC bot falls from **90 to 81 rules**, oversized directories from **174 to 173**,
with zero mixed nodes. SQL operation regrouping and wider migration remain open.


### Latest checkpoint: database mutation claims corrected

[Mutation-claim audit](DB-MUTATION-CLAIMS.md) replaces an unsupported
telemetry-deletion conclusion with accurate method/symbol observations, adds
a receiver-specific row-truncation observation, and corrects the plaintext-
password claim. The [five-entry ledger](db-mutations-mapping.json) verifies.
Three new controls reproduce the old errors and check actual truncation syntax;
all six archive/member checks and **1,686/1,686 fixtures pass**. SQL contains 78
rules; strict validation reports **174 oversized directories**, with zero mixed
nodes. SQL mutation regrouping and the wider migration remain open.


### Latest checkpoint: SQL schema observations relocated

[SQL/schema audit](SQL-SCHEMA.md) moves ten observations to existing relational,
introspection and stored-code leaves. The [20-entry ledger](sql-schema-mapping.json)
records those relocations and consumer updates. An ADO consumer now explicitly
requires the catalog its comment promised; the report documents this intentional
tightening and the directory-counting ambiguity behind it. **1,683/1,683 fixtures
pass**. SQL falls from **89 to 79 rules**, oversized directories from **175 to
174**, and mixed nodes remain zero. The report lays out remaining SQL/editor/API
and schema-sibling corrections; the wider migration is incomplete.


### Latest checkpoint: generic DOM operations separated from browser UI

[DOM operation audit](DOM-OPERATIONS.md) moves 24 observations into the generic
DOM leaf, preserves the sole parent-subtree consumer's original alternatives,
and fixes a local consumer reference. The [26-entry ledger](dom-mapping.json)
verifies unchanged relocation conditions and current definitions. A new control
retains identical findings modulo renamed IDs and identical scores.
**1,682/1,682 fixtures pass**, with **175 oversized directories** and zero mixed
nodes. Generic DOM contains 25 rules. Parser/HTML/browser sibling boundaries and
the wider cap migration remain open, as detailed in the report.


### Latest checkpoint: Base64 backend partition retired

[Base64 symbol consolidation](BASE64-SYMBOLS.md) migrates 19 observations into
15 canonical rules and removes `decode/symbol-base64`. Five Go API variants
share their exact predicate union; compiled decoder identity now requires the
Base64 package. The [156-entry ledger](base64-symbols-mapping.json) accounts for
those observations and 137 updated consumers, including three deliberately
broadened Go consumers. Ten archive/member checks distinguish hexadecimal from
Base64 decoding. **1,681/1,681 fixtures pass**, with **175 oversized directories**
and zero mixed nodes. The unified Base64 leaf contains exactly **85 rules**.
Generic DOM siblings, remaining predicate precision issues, and the broader
cap migration remain open.


### Latest checkpoint: XML observations separated from codec direction

[XML codec audit](XML-CODECS.md) relocates ten observations by DOM operation,
XML parsing or XML typing; corrects the Base64 aggregate; and adds bound
JavaScript encode/decode sequences. Two consumers retain their requirements
under names that do not assert unproven conversion flow. The
[15-entry ledger](xml-codec-mapping.json) verifies. Four new archives test both
directions and unrelated receivers/types; all 17 archive/member exact-ID checks
pass. **1,679/1,679 fixtures pass**, with **175 oversized directories** and zero
mixed nodes. Base64 decoding is at 70 rules. Generic DOM siblings, symbol-backend
consolidation, and the wider cap migration remain open. The report documents
the intentionally bounded directional coverage and remaining consumer risks.


### Latest checkpoint: arithmetic separated from codec claims

[Arithmetic audit](ARITHMETIC.md) relocates 25 observations, retires one
unsupported decoder aggregate, and narrows the Base64 umbrella. The
[27-entry ledger](arithmetic-mapping.json) verifies that all relocated matching
conditions are preserved. Ordinary shifts and binary formatting retain their
specific findings without claiming Base64 decoding. **1,675/1,675 fixtures
pass**; strict validation reports only **175 oversized directories**. There are
zero mixed rule directories, and Base64 now contains 78 rules. The validator's
18 directory tests pass with the documented arithmetic category admitted.
XML conversion direction, the symbol-backend partition, and the wider cap
migration remain open; this checkpoint does not complete the plan.


### Latest checkpoint: mixed encoded-data branch retired

[Format-branch migration](DECODE-FORMATS.md) moves six observations into existing
format/assembly leaves and retires `data/decode/encoded`. Its mixed transformation
umbrella is expanded into the same named alternatives in three consumers. The
[ten-entry ledger](decode-formats-mapping.json) verifies; a control exercises all
six moved observations. **1,674/1,674 fixtures pass**, with **175 oversized
directories** and zero mixed rule directories remaining. Base64 is at 82 rules.
Symbol-backend consolidation, XML directionality, and the wider cap audit remain
open; the report records the proximity/span-grouping limit of this migration.


### Latest checkpoint: Buffer calls and JSON conversion

[Computed-call and JSON audit](BASE64-CALLS.md) relocates generic Buffer dispatch
and JSON conversion observations, replaces a nearby-token test with a structured
Base64-to-JSON relationship, and corrects the parenthesized-eval classification.
The [ten-entry ledger](base64-calls-mapping.json) verifies. **1,673/1,673 fixtures
pass**; the Base64 leaf is now **80 rules**, with **175 oversized directories**
and zero mixed rule directories overall. XML directionality, the symbol-backend
partition, and the remaining format cohort are still open work, documented in
the report. This checkpoint does not complete the migration.


### Latest checkpoint: Base64 supporting observations

[Base64 cohort audit](BASE64-SUPPORT.md) moves eleven import, alphabet and file-
write observations to their actual subjects, updates consumers, and corrects
an umbrella that treated supporting observations as decoding. The
[13-entry ledger](base64-support-mapping.json) verifies. The decoding leaf drops
from 90 to **84**, and oversized directories drop from 176 to **175**. Three new
controls distinguish imports/constants, decoding and encoding; **1,670/1,670**
fixtures pass, with zero mixed rule directories. The report records remaining
symbol-backend, XML, computed-call and format sibling work; fitting this one
leaf under the cap does not complete that cohort or the broader migration.


### Latest checkpoint: encoded reverse-shell leaf retired

[Final encoded-leaf audit](ENCODED-FINAL.md) retires the Python import/shell and
PHP label verdicts, places six neutral observations in their semantic homes,
and removes `reverse-shell/encoded`. The [eight-entry ledger](encoded-final-mapping.json)
verifies. New stored-text controls score 12 as an archive, and an encoded Python
relay retains stream-bridge coverage. **1,667/1,667 fixtures pass**; strict
validation still reports **176 oversized directories**, with zero mixed nodes.
The audit also records a reproduced PHP decoded-snippet parsing gap, which labels
cannot repair. This checkpoint does not finish the cap migration or sibling audit.


### Latest checkpoint: encoded Unix/JVM carriers

[Encoded carrier audit](ENCODED-UNIX.md) retires four unsupported Perl, Elixir
and Kotlin reverse-shell verdicts, relocates three neutral shell observations,
and removes the related decode/exec proximity verdicts and dependent wrappers.
The [17-entry ledger](encoded-unix-mapping.json) verifies; two new benign
archives score 4 and 5, while all three real encoded payloads retain hostile
`dev-tcp` detections. The full soft suite passes **1,665/1,665** fixtures.
Strict validation still fails only on **176 oversized directories**; no mixed
rule directories remain. Three Python/PHP rules remain in `reverse-shell/encoded`.
This is an intermediate checkpoint, not completion of the cap migration.


### Execution revision: simplify placement before expanding the tree

The directory policy remains **strictly leaf-only**. Mixed parent/child YAML
was tried previously and gave similar rules multiple homes. Broad evidence
must be resolved by its actual shared operation, metadata claim, or independently
meaningful alternatives; an opaque broad capability needs a defensible leaf
partition before migration. An unresolved placement is recorded rather than
hidden in a generic bucket or an invented narrower claim. Follow the
[placement procedure](../../TAXONOMY.md#directory-budgets-and-placement-contracts).

Leaf-only recheck (2026-09-27): scanning 19,940 YAML files found one mixed
directory, `metadata/package/documentation`, with parent rules in
`npm-readme-anomalies.yaml`. Audit those rules against its documentation
children and package-description metadata before moving them; their README
claims, manifest-description observation, and filename observation do not all
have the same subject. Parent composites and aliases are not exceptions to
the leaf-only requirement. This live finding supersedes earlier zero-mixed
snapshots; the migration remains incomplete.

That mixed node is now resolved: see [Documentation leaf repair](DOCUMENTATION-LEAVES.md)
and its [10-entry mapping](documentation-parent-mapping.json). A fresh four-tier
scan finds **zero mixed rule directories**. All destination leaves fit the cap
(36, 27, 10, and 13 rules), and every ledger destination matches its recorded
effective definition. No stale moved IDs remain in rules, fixtures, or engine
sources. The final soft run passes **1,631/1,631** fixture checks, including
four new controls capped at 5; local atomscan scores those controls at 1–4.
Strict validation still reports **176 oversized directories**, plus **six
four-platform scope findings** inherited from the migrated definitions. The
report explains why retaining Android/iOS coverage requires resolving that
separate validator heuristic. No scope exception or coverage reduction was
used to make the migration appear complete.

Work in this order:

1. Resolve broad-evidence destinations and nearest-sibling boundaries in each
   proposed split. Keep the author-facing decision procedure short; put
   historical rationale in this audit rather than repeating it in contracts.
2. Fix duplicate normalization and the reproduced scope/confidence blind spot.
   Compare effective scopes and constraints before recommending a merge;
   retain genuinely different quantitative observations.
3. Finish retiring `reverse-shell/socket-exec`, including its references and
   positive/negative fixtures. Use the completed migration as the pilot.
4. Coordinate boundaries across dropper, obfuscation, injection, exfiltration,
   and supply-chain, then migrate bounded batches with all dependent references
   updated together. Do not make the entire cross-domain audit one edit batch.

Review outcomes separately: fewer competing destinations, preserved or
explicitly corrected detections, and measured model effects. A move from
`obfuscation/string/encoding` to `obfuscation/string-encoding` does not by itself
change the current direct prefix `objectives/anti-static/obfuscation`.
Use independent placement reviews on representative unfamiliar matchers to
check whether contracts actually give authors the same destination.

The implemented policy is **85 atomic traits plus composite rules combined per
directory**, inclusive, with **no exemptions**. There is no separate atomic cap.
There is **no hard physical-depth limit**. Depth above five directories below
any tier receives a soft, non-blocking validation warning; the tier and YAML
filename do not count. Prefer breadth when sibling techniques remain equally precise;
retain depth when it gives a matcher one unambiguous semantic home. The current
path-presence/max-criticality model feature uses the tier plus two descendants,
so deeper distinctions are not guaranteed direct features; the taxonomy must
record that model limitation without forcing lossy flattening. The validator
now reports sparse sibling cohorts as an advisory. A first path-resource
migration tranche is recorded in the [implementation-layer audit](IMPLEMENTATION-LAYERS.md);
cap and semantic taxonomy audits remain active work.

| Measurement | Result |
|---|---:|
| YAML files containing rules | 19,764 |
| Atomic traits / composites | 79,169 / 39,509 |
| Total rules / directories containing rules | 118,678 / 8,637 |
| Directories exceeding the old 75-atomic cap | 0 |
| Directories exceeding the intermediate 80-combined cap | 219 |
| Directories exceeding the chosen 85-combined cap | **180** |
| Violators by tier | 143 objectives, 24 capabilities, 7 metadata, 6 identities |
| Rules in violating directories | **20,215** |
| Sum of excess above 85 | **4,915** |
| Violators plus sibling subtrees inventoried | 2,826 rule directories / 61,219 rules |
| Identical atomic `if` bodies touching violators | 128 groups / 284 rules |

4,915 is the minimum number of rules that must leave their *current* oversized
directories or be removed; it is not a proposed deletion count. Reclassifying
all contents of a retired directory will move more. Destination capacity must
also be measured; moving 20 rules into an 80-rule sibling simply moves the error.

The released/default binary initially enforced the old atomic-only policy.
The sibling engine checkout already contained uncommitted combined-counting
work at 80. That work was preserved, its threshold changed to 85, and the
reverse-shell exemption removed. The old exemption concerned `reverse-shell/dup`,
which currently has only 52 rules. The actual reverse-shell violator is
`reverse-shell/socket-exec`, with 151. Removing the exemption therefore creates
no additional failure at this snapshot, but prevents future bypasses.

Validation evidence:

- Before: `make validate` passed all 1,583 fixtures.
- After rebuilding the engine: `make validate` fails with exactly **180**
  `policy/oversized-dir` directory violations, and no other hard policy failure.
- `cargo test --lib taxonomy_tests`: **26 passed**. Tests include all-atomic,
  all-composite and mixed 85/86 boundaries, 76 atoms without an atomic cap,
  separate-directory budgets, the former exempt path, and depth counting.
- `cleave --traits-dir . validate --soft`: all **1,583 fixtures pass** on the
  rebuilt engine. This diagnostic run allows policy errors through; it is not
  a claim that strict validation is green.

## Current migration progress

**Latest batch (2026-09-27):** the
[Windows encoded-launcher audit](ENCODED-WINDOWS.md) moves command flags, hidden
Run arguments and encoded TCP type references to their actual subjects, reuses
canonical Run observations, and retires four unsupported reverse-shell verdicts.
An explicit creation-name observation moves from TCP to socket/create, keeping
every destination within 85. All **1,661/1,661** fixture checks pass, including a
genuine decoded command channel. The 11-entry ledger verifies; no mixed rule
directories remain. Strict validation still fails only on **176 oversized
directories**. Seven encoded rules and the broader cap/implementation cohorts
remain open; carrier-decoding limits are documented in the report.

**Preceding batch:** the
[C# stream audit](CSHARP-STDIO.md) consolidates four source verdicts around
bound bidirectional transfers, retires an unsupported CLR-name aggregate, and
moves named dispatch/TCP observations to their neutral subjects. The nine-entry
ledger verifies. `reverse-shell/stdio` is now empty and removed; socket/tcp is
exactly **85** rules. All **1,657/1,657** fixture checks pass, with zero mixed
directories. Strict validation again fails only on **176 oversized directories**.
The earlier independent exception/suppression findings no longer appear. Source
coverage limits, other relay siblings, and the broader cap migrations remain open.

**Preceding batch:** the
[Telnet relay audit](TELNET-RELAYS.md) consolidates overlapping FIFO verdicts,
requires a shell in two-channel pipelines, and retires a persistent-shell
aggregate reproduced by printing four strings. Genuine FIFO and two-channel
forms belong in stream-bridge, not PTY. All **1,653/1,653** fixture checks pass;
the six-entry ledger verifies and no mixed directories remain. Strict validation
reports **176 oversized directories** plus one exception-member error in a
separate live PyPI credential-reference edit, recorded in the report. Two C#
rules remain in stdio; the broader sibling and cap migrations remain open.

**Preceding batch:** the
[Python stdio migration](PYTHON-STDIO.md) replaces three overlapping verdicts
with one stream-bridge composite requiring explicit input/output transfers and
shell creation. It retires unsupported receive/send and PTY aggregates, renames
keyword-argument observations honestly, preserves the blockchain consumer, and
repairs a TCP-profile placement found during the connection audit. All
**1,644/1,644** fixture checks pass. The 11-entry effective-definition ledger
verifies, every destination fits 85, and no mixed rule directories remain.
Strict validation still fails only on **176 oversized directories**. Three
C#/FIFO rules remain in stdio. Callback identity/data-flow limitations and the
remaining sibling/cap migrations are documented as unfinished work.

**Preceding batch:** the
[unsupported stdio audit](UNSUPPORTED-STDIO.md) retires five verdicts that lacked
their claimed relay or gating evidence and moves the self-deletion composite
to its existing subject leaf, now exactly **85** rules. The local computed-code
false positive is verified by restoring the old rule in an isolated snapshot:
the archived control scores 126 with the old hostile finding, versus 8 under
the current rules. This avoids a fixture-path exclusion that masked the plain
source regression. All **1,641/1,641** fixture checks pass; there are zero mixed
directories, and strict validation still fails only on **176 oversized leaves**.
Seven Python/C#/FIFO rules remain in `stdio`; encoded and the other planned
cohorts remain open.

**Preceding batch:** the
[JavaScript pipe-endpoint follow-up](JAVASCRIPT-PIPE-ENDPOINTS.md) replaces
independent pipe co-occurrence in seven relay composites with a neutral atom
requiring matching peer and child identifiers. The reproduced local-file-pipe
false positive disappears; mismatched children also fail, while output-first
and comma-separated genuine relays remain detected. All **1,640/1,640** fixture
checks pass, including 24 reverse-shell controls. All seven effective mappings
verify; `fd/stdio` holds 71 rules and there are zero mixed rule directories.
Strict validation still fails only on **176 oversized directories**. This
syntactic matcher does not resolve aliases or prove the peer's network type;
those coverage limits and the opaque-obfuscation verdict remain explicit audit
work alongside the remaining reverse-shell siblings.

**Preceding batch:** the
[JavaScript stdio audit](JAVASCRIPT-STDIO.md) fixes a reproduced four-verdict
false positive on independent networking and local shell execution. Three
overlapping relay composites merge with explicit input/output pipe requirements;
the variable-shell and extension wrappers gain the missing evidence. Neutral
environment/pipe observations have canonical homes, and reviewed relay rules
move into `stream-bridge`. All 21 recorded dispositions verify. The three new
controls preserve genuine JS/TS and extension relays while rejecting independent
local operations. All **1,636/1,636** fixture checks pass; zero mixed directories
remain. Strict validation still fails only on **176 oversized directories**.
Next: cross-call peer/child binding checks, the opaque-obfuscation verdict, and
the remaining Windows/.NET, Python, FIFO and encoded siblings.

**Preceding batch:** the
[Go/JVM stream and scope follow-up](STDIO-STREAM-OBSERVATIONS.md) moves three
neutral observations out of reverse shells and merges four overlapping Go
stdio definitions into one canonical atom. Nine effective mappings verify;
destination leaves hold 70 and 31 rules. The platform-count heuristic is now
a non-blocking review across all tiers, without directory exemptions or reduced
coverage. Its boundary regression passes and the release build succeeds.
All **1,633/1,633** fixture checks pass, including two new neutral-stream
controls. Strict validation again fails **only on 176 oversized directories**.
The remaining `stdio` and `encoded` rules still need semantic reconciliation.

**Preceding batch:** the
[documentation leaf repair](DOCUMENTATION-LEAVES.md) removes the remaining
mixed node and consolidates a duplicate advisory statement. All 1,631 fixture
checks pass. Strict validation retains 176 oversized directories and flags six
preserved platform scopes; the platform-policy conflict remains unresolved.

**Preceding completed batch:** the
[parser/DOS consolidation](PARSER-DOS-CONSOLIDATION.md) resolves the final two
original duplicate pairs. The validator reports no shared-matcher reviews;
all 1,627 fixture checks pass in soft mode. Parser guards now describe real
member structure, and DOS query evidence is neutral. The new value-field
constraint check passes 17 pattern-validation tests. Strict validation still
fails on 176 oversized directories; `stdio`/`encoded` reconciliation is next.

**Preceding member-name batch:** the
[member-name consolidation](MEMBER-NAME-CONSOLIDATION.md) resolves three more
duplicate pairs and moves eight adjacent filename observations out of the
retired `files/credentials` leaf. Twelve of the 14 original pairs are resolved;
the parser-error and DOS-call pairs remain. Platform-equivalence diagnostics
now distinguish Unix coverage from Linux/macOS; all 144 duplicate-related
tests pass. The name leaf has 19 rules and remains leaf-only.
All 1,623 fixtures pass in soft mode. Strict validation still reports two
shared-matcher pairs and 176 oversized directories.

**Preceding canonical-observation batch:** the
[canonical-observation consolidation](DUPLICATE-CONSOLIDATION.md) merges nine
of the 14 shared-matcher pairs. Dependency, runtime-variable, path and metric
observations now have one canonical home; contextual composites retain their
additional requirements. All **1,623 fixtures pass** in soft mode. Five pairs
remain under review, and 176 directories remain over the cap. All destination
leaves remain at or below 85, with no mixed nodes or exemptions.

**Preceding descriptor batch:** the
[descriptor mechanism migration](DESCRIPTOR-MECHANISMS.md) removes `dup` and
`syscall`: 27 more rules moved, two retired. Neutral descriptor observations
have operation-specific homes; outbound and accepted socket shells have
separate objective evidence. All **1,619 fixtures pass** in soft mode, including
five new controls/positives; copied controls also pass outside the benign
fixture path. All destination leaves stay within 85. Strict validation still
reports 176 oversized directories and 14 shared-matcher review pairs.
`stdio` and `encoded` remain to be reconciled before the reverse-shell audit
is complete. The policy remains strictly leaf-only.

**Previous completed batch:** see the
[socket-shell pilot report](SOCKET-SHELL-PILOT.md). The remaining 43 rules in
`socket-exec` were resolved and that directory was removed. Including necessary
destination cleanup and Perl descriptor observations, 60 rules moved and 11
unsupported verdicts were retired. The duplicate-validator changes pass 142
tests and surface 14 previously missed shared-matcher pairs. Soft validation
passes **1,614/1,614 fixtures**; strict validation still reports **176** oversized
directories, the shared-matcher findings, and unrelated authoring issues.
This batch completes `socket-exec` retirement, not the entire reverse-shell
family audit; subsequent descriptor work is recorded above. All directories remain
strictly leaf-only.

The following progress notes preserve earlier checkpoints; their counts are
historical and must not override the completed-batch report above.

The current worktree is based on traits revision `31568d2bbf`; the table above
is the preserved initial cap snapshot and has not been silently rebased. The
latest `cleave version` reports **79,242 atomic traits and 39,502 composites**;
strict validation reports **177** cap violators. A fresh behavior-tier path
inventory has 253 YAML files at depth 2, 8,452 at depth 3 and 5,560 at depth 4
(levels below the tier, excluding filenames). Depth is not a policy violation.
The validator currently reports **88** sparse sibling cohorts under its
35-rule advisory threshold; this is a review signal, not a directive to
flatten. `validate --soft` preserves all **1,610/1,610** fixtures.
These current measurements are distinct from the preserved initial cap audit
table above.

### Depth and breadth are semantic choices, not physical limits

Collimator's `_finding_paths` currently emits the tier and first two directory
prefixes for direct path-presence/max-criticality features; Scan uses the same
vocabulary. A third taxonomy level below the tier is therefore not guaranteed
its own direct feature. Full paths may appear in higher-order features when
trained vocabulary supports them. The previous physical limit of three
subdirectories was not aligned with this implementation and did not measure
misorganization. A future feature-limit change can make more levels directly
visible without changing semantic taxonomy.

Audit each path by what its hidden fourth segment means:

- **Prefer a broader sibling placement** when it stays equally exact and
  disambiguates the behavior in a visible level. For example,
  `objectives/anti-static/obfuscation/string/encoding/` and its sibling
  `.../string/fragmentation/` both currently feature as
  `objectives/anti-static/obfuscation` as direct path prefixes. Candidate
  sibling subjects such as `anti-static/obfuscation/string-encoding` and
  `.../string-fragmentation` should be used only if each has a clear, unique
  placement contract and doesn't merge neighboring behavior.
- **Promote a useful protocol distinction** only when it changes the behavior
  being learned. For example,
  `micro-behaviors/communications/email/access/imap/` shares direct path
  features with MAPI and ManageSieve. Decide whether protocol-specific behavior
  merits a separate visible subject, or whether the operation is the desired
  shared signal; do not infer bad organization from depth alone.
- **Collapse redundant or implementation-only levels** when the segment adds
  no behavior meaning. Move the rule to its semantic parent and keep language,
  platform, or sample-specific distinctions in filenames and scopes.

Do not add an artificial intermediate node just to satisfy a fixed path shape.
The goal is to expose distinctions the model should learn while retaining a
single, semantically defensible placement for each behavior. Prefer breadth
over depth only when that does not reduce taxonomy precision.

Behavior-preserving migration tranches now cover path resources, bind shells,
string APIs and technique-specific library fingerprints:

- **Path-resource placement:** 12 rules formerly under
  `micro-behaviors/fs/path/library` now live in cache, system recovery, font,
  application-data, system-log and metadata-store subjects. Eight composite
  reference occurrences follow those IDs. The six remaining rules in
  `fs/path/library` point to shared-library files. Their effective matchers,
  scopes, criticalities and confidence are preserved.
- **Bind-shell placement:** all eight rules in
  `objectives/command-and-control/backdoor/dispatch/bind-shell` moved under the
  canonical `backdoor/bind-shell` subject. Two Ruby bind-shell composites also
  moved out of `reverse-shell/socket-exec`; three supporting observations moved
  to neutral socket-listener and process-stdio capabilities. Their matchers
  and the two composites' effective predicates are unchanged after reference
  remapping. `socket-exec` was still oversized at 146 rules before the current
  reverse-shell audit tranche.
  This is a pilot rather than completion of the nine-leaf reverse-shell cohort.
- **String and path-operation placement:** the 21 string API rules formerly
  under `micro-behaviors/data/string/library` now live under operation leaves.
  Three reference-only Java code-generation framework fingerprints moved to
  `micro-behaviors/metaprogramming/generation`, and all reflection exclusions
  and the cglib fixture expectation follow the new IDs. The .NET `Combine`
  and `GetDirectoryName` API-name tokens moved to pathname join and parse
  leaves. Matcher bodies and effective scopes remain unchanged; the codegen
  names state only that a library is referenced, not that code generation ran.

The `micro-behaviors/metaprogramming/{ast,generation,reflection}` contract is
now language- and filetype-neutral. AST operations and reflection are code
techniques, not a `data/source` or language subcategory. Existing
`data/source/` contents still need a rule-by-rule semantic migration; the path
is closed to new rules until that audit is complete.

The Go parser/source-generator example is now a concrete migration: parser
calls and their composite live in `metaprogramming/ast`; formatting generated
source and the composite that additionally requires a file write live in
`metaprogramming/generation`. Its matcher bodies and effective composite
predicate are unchanged. The boundary guide distinguishes a program's AST
behavior from an analyzer's internal AST and from ordinary data parsing.

The existing `micro-behaviors/process/interpreter/reflection/` collection also
needs a rule-by-rule placement audit: actual reflective discovery or invocation
maps to `metaprogramming/reflection`, while indirect dispatch, evaluation, and
loading must go to their own technique leaves. Keep language names in rule
scopes and filenames, not as taxonomy branches. Do not bulk-move this
collection based on its current `reflection` path name.

The current audit tranche moves Go AST parsing into `metaprogramming/ast`,
separates source generation into `metaprogramming/generation`, moves Node
socket/child-stream shell bridges into `reverse-shell/stream-bridge`, and moves
the native ELF socket/`dup2`/shell composites into `reverse-shell/fd-redirect`.
Ruby's receive → command execution → socket response loop now lives under
`remote-command/dispatch`, and its VM-aware consumer follows the relocated ID.
The Node library/extension consumers now require one of the stronger bridged
shell composites instead of socket-plus-exec co-occurrence. Zig's host/port
literal and shell-launch facts now live in neutral socket-endpoint and process
capability paths, and its reverse-shell composite requires the `dup2` link.
The Lua fixture is classified as remote-command dispatch and now requires
connect, receive, shell execution and response send. The weak WSH object
co-occurrence verdict was removed; its TCPClient and stream-object observations
now live as neutral capabilities. After these changes, the retired
`reverse-shell/socket-exec` directory contains 51 rules
and is below the cap, but is not empty. At that checkpoint, strict validation
reported 177 unrelated oversized directories and soft validation preserved all
1,610 fixtures (243 hostile, 338 benign, 175 does-nothing, 45 drop-exec, 572
supply-chain, 66 impact-wipe, 82 obfuscation, 24 reverse-shell, 65 simple-stealer).

- **Direct-socket HTTP correction:** the Bash `/dev/tcp` + HTTP-token rule was
  hostile despite proving no shell I/O over the socket. Its shell-specific
  observations and neutral notable composite now live in
  `micro-behaviors/communications/http/direct-socket`; the existing raw HTTP
  capability was moved there and its three consumers remapped. The taxonomy
  distinguishes protocol-first raw HTTP, HTTP client APIs, and socket-only
  behavior. A benign health-check fixture guards against restoring the false
  reverse-shell claim.

- **Reverse-shell precision and method placement:** HTTP polling agents now
  live under `remote-command/http-poll`, and netcat remains the specific
  `reverse-shell/netcat` technique (14 rules; invocation children are not
  justified at this size). Java, Kotlin and Scala stream-bridge composites
  moved to `reverse-shell/stream-bridge`; generic Java transfer and Kotlin
  shell-process observations live under neutral process capabilities. Socket
  plus shell co-occurrence without stream evidence no longer qualifies as a
  reverse shell in Java, Kotlin, Scala or Swift. Swift's separate stdio-wiring
  composite remains. Reverse-shell fixtures now require one confirmed hostile
  finding each instead of a second, weaker co-occurrence result. The former
  140-rule `socket-exec` violator is now below the cap at 51 rules, as reported by strict
  validation; all 24 reverse-shell fixtures pass. The remaining JavaScript
  HTTP GET-command/POST-result composite moved from `socket-exec` into
  `remote-command/http-poll`; its legs prove polling and task dispatch, not a
  persistent socket-coupled shell. A Node hosted-reverse-shell curl-pipe
  composite was removed after confirming it was a strict branch duplicate of
  the existing `dropper/delivery/pipe` composite. The canonical dropper rule
  already requires the same three facts, so detection remains and now retains
  both JavaScript and shell ATT&CK facets. The retired `socket-exec` catch-all
  now has 51 rules and is no longer a cap violator, but its remaining rules still
  need routing to the documented mechanisms before the directory can be removed.
  The native ELF socket+`dup2`+shell rules now live in
  `reverse-shell/fd-redirect`, where their required evidence identifies the
  inherited-descriptor mechanism.
The full reverse-shell fixture group still passes.

- **PHP socket-shell and staged-eval placement:** PHP socket setup, shell
  creation and descriptor-spec stdin mapping now live as neutral socket,
  process and fd capabilities. One nearby composite under reverse-shell
  `fd-redirect` requires all three; the weaker socket-plus-shell co-occurrence
  rule was removed, and the existing webshell composite now references the
  stronger reverse-shell result. Network-order length unpacking, buffer
  reassembly and `eval($b)` moved to framing, buffer-transfer and direct-eval
  capabilities. Their socket-delivered stage composite moved to
  `remote-command/dispatch`; a new hostile fixture confirms the whole chain.
  Both PHP fixtures pass against their relocated composites. JSP's socket
  read-to-exec loop moved to `remote-command/dispatch`. Swift's former
  endpoint-plus-shell/stdio co-occurrence composite was tightened to require
  Network.framework connection, start, send and receive facts plus shell-pipe
  wiring, then moved to `reverse-shell/stream-bridge`. Its endpoint literals,
  connect state, send and receive observations now live in neutral socket
  capability subjects. Python's shell invocation facts and AppleScript's
  interactive Bash fact also moved to neutral process capabilities; AppleScript
  reverse-shell composites still match under `dev-tcp`. Objective-C shell
  launch and interactive-argument observations moved to neutral process
  capabilities. Its socket/dup2 reverse-shell composite now requires an actual
  connect; socketless shell/dup2 co-occurrence no longer receives a hostile
  reverse-shell verdict. The systemd unit's dev-tcp shell composite moved to
  the `dev-tcp` technique and reuses canonical persistence/restart facts; a
  hostile fixture confirms it.

- **Certificate metadata ownership:** script signature-block observations
  moved into the existing `signed/certificate/signature` subject, and direct
  signer-subject observations moved into the new `signed/certificate/subject`
  subject. Authenticode integrity and verification facts moved out of the mixed
  identity file into `signature/pe-chain`; 91 YAML reference owners were
  remapped without changing predicates. Moving the three script markers brought
  `certificate/identity` from 88 to the inclusive 85 cap and removed one
  violator; subsequent subject moves made the residual identity set smaller.
  The mixed PE certificate matcher was then separated by the field or property
  it reads: `subject`, `issuer/name`, `issuer/chain`, verified issuer sets
  (`issuer/microsoft`, `issuer/attestation`), certificate security properties,
  and signature validity/integrity. A Microsoft CA name string remains only an
  issuer-name observation; platform trust requires a verified-chain thumbprint.
  The forged-name and genuine-chain fixtures both pass after this split.

Current strict validation remains **red only on the known 177 oversized
directories**. Soft validation reports all **1,610 current fixtures passing**
(245 hostile, 338 benign, 175 does-nothing, 45 drop-exec, 572 supply-chain, 66
impact-wipe, 82 obfuscation, 22 reverse-shell, 65 simple-stealer); it also checks
parsing and rule quality while allowing that cap policy failure.
The destination leaves created or extended by these migrations remain below
85. The minimum cap excess is now **4,848**, down from 4,920 in the earlier
pre-migration inventory; there are no new violating directories. The broader
cohort ledger below remains open.

## Evidence and audit coverage

- [oversized.csv](oversized.csv): every violator, with atomic/composite counts,
  excess, source-file count, and physical depth.
- [disposition.csv](disposition.csv): every violator assigned to a migration
  cohort, with the proposed organizing question, action, and source examples.
- [siblings.csv](siblings.csv): all rule-bearing leaves under each violating
  directory's parent, including siblings' descendants. Overlapping audit scopes
  are counted once. Both YAML rule kinds were parsed, not counted by regex.
- [matcher-overlaps.csv](matcher-overlaps.csv): identical `if` bodies and their
  effective surrounding settings. These are **candidates**, not equivalent
  detections: file types, platform, size, confidence, criticality and exclusions
  can differ. For example, the same `exec` symbol means different things in
  Python and PHP. Do not merge it across those scopes merely because text agrees.
- [reference-impact.csv](reference-impact.csv): distinct YAML reference owners
  per violating directory, including references to its ancestor directories.
  Counts overlap between rows and are not additive. Tests, external consumers,
  and engine-emitted IDs need the additional migration checks below.
- [structure.csv](structure.csv): whole-tree depth, single-child, mixed-leaf,
  and broad-parent inventory. Structural review flags are not proof of semantic
  errors or a new validator policy.
- [summary.json](summary.json): machine-readable totals and scope roots.
- [IMPLEMENTATION-LAYERS.md](IMPLEMENTATION-LAYERS.md): technique-first placement
  of embedded library evidence, all 15 literal `library` nodes, related
  implementation terminology, and the artifact-identity boundary.

The inventory covers every rule. The semantic audit inspected a spread of rule
IDs/descriptions and source files in **each of the 180 violators**, the sibling
structures, and actual matcher/composite bodies for the conflicts documented
below. It does **not** claim line-by-line adjudication of all 61,219 rules in
those subtrees, or all 8,637 directories. The migration must produce a complete
old-ID → new-ID disposition before moving each cohort. Proposed child sizes are
not yet measured and must not be represented as guaranteed to fit.

Reproduce the structural reports with PyYAML available:

```sh
python3 scripts/audit-taxonomy.py --out /tmp/taxonomy-audit
make validate
```

`disposition.csv` and this plan are reviewed recommendations; the inventory
script does not manufacture semantic classifications.

## Duplicate-validator findings and proposed improvements

**Implemented checkpoint:** exact and scope-only atomic passes now share
matcher/default normalization, normalize set ordering, and retain architecture
and downgrade constraints. The logic pass reports file-scope differences and
confidence differences below 0.1, checks architecture overlap, and retains
different quantitative observations. The reproduced DOS pair now appears in
the 14-pair review output. Diagnostics request a scope/verdict review rather
than asserting that every shared matcher can safely be merged. Seven new
regressions cover these boundaries; all 142 duplicate-related tests pass.
Further candidates below remain proposals unless explicitly covered here.

Identical matcher bodies should enter a common duplicate review, but a merge
must preserve the **effective predicate**: inherited defaults, file type,
platform, architecture, bounds, exclusions and conditional verdict changes.
The 128 groups in `matcher-overlaps.csv` are body matches, not 128 confirmed
validator defects. Confidence alone is not a different observation.

### Confirmed missed merge: overlapping scope plus a small confidence difference

Two existing rules in `objectives/impact/infect/binary/dos` have exactly
`if: {type: hex, pattern: "B4 52 E8"}`:

| Rule | Effective file types | Confidence |
|---|---|---:|
| [`dos-list-of-lists-call`](../../objectives/impact/infect/binary/dos/com-bytes.yaml) | `dos_com`, `static-lib` | 0.88 |
| [`dos-get-list-of-lists-near`](../../objectives/impact/infect/binary/dos/direntry.yaml) | `dos_com`, `static-lib`, `data` | 0.80 |

Both have `crit: notable`, `platforms: [windows, unix]`, and `size_max: 65536`,
with no differing exclusions or other matching constraints. Their scopes
overlap, and they assert the same DOS observation. Merge into one canonical
observation after reviewing the broader `data` scope and choosing one supported
confidence; rewrite both sets of consumers.

The current engine's `src/capabilities/validation/duplicates.rs` lets this pair
fall between three checks:

- `find_duplicate_atomic_traits` includes `for` in its fingerprint, so the
  different lists separate the pair.
- `find_for_only_duplicates` includes confidence to two decimal places, so the
  different confidences separate the pair again.
- `find_atomic_logic_duplicates` checks that the file types overlap, but does
  not count a differing `for` list as a metadata difference. It only treats a
  confidence difference of at least 0.1 as different. This pair is skipped on
  the assumption that the exact checks handled it.

**Reproduced against the rebuilt binary:** isolating these two rules with their
effective defaults produces no duplicate diagnostic with all validators enabled
(`validate --exclude ''`). Changing only 0.80 to 0.88 produces the existing
“trait groups differ only in scope (should be merged)” error. The tiny isolated
bundles also report unrelated whole-tree allowlist/default-style errors; this
experiment compares the duplicate diagnostics, not overall exit success.

**Priority 1:** group by normalized matcher independently of confidence, then
compare effective predicates and report the actual differences. Do not make
one check assume another handled a pair without checking its equivalence
criteria. Add this exact pair as a regression, plus overlapping and disjoint
file/platform scopes with equal and slightly different confidence.

### Additional patterns to cover, without erasing precision

- **Share normalization across duplicate passes.** Currently only the logic
  pass normalizes `count_min: 1` and an explicit `exists: true` spelling. Its
  “exact check handled this” shortcut deserves regressions for those variants
  with otherwise identical settings. Canonicalize set-valued scopes after
  defaults/group expansion; do not sort ordered ranges or other ordered data.
  These are source-review candidates, not additional reproduced failures.
- **Account for architecture and conditional verdicts.** The exact and
  scope-only fingerprints omit `arch` and `downgrade`; the logic pass compares
  downgrades but does not test architecture overlap. Add disjoint-architecture
  and differing-downgrade regressions before recommending automatic merges.
  The diagnostic must distinguish shared matching work from equivalent output.
- **Explain why identical bodies were retained.** In
  [`fetch-exec/shell.yaml`](../../objectives/command-and-control/dropper/delivery/fetch-exec/shell.yaml),
  `spl-payload-names--rx-7` and `arch-args-arm--rx-18` both match the word
  `splarm`, but require six and two occurrences respectively. Several adjacent
  payload-name pairs repeat this pattern. These are different quantitative
  observations, and the logic pass deliberately skips unequal bounds. Report
  such groups as shared-matcher review candidates with the threshold difference,
  not mandatory merges. Factor matching work only if the reference mechanism
  preserves each count constraint. The stale comments in that function which
  recommend merging overlapping bands should also be reconciled with its code.
- **Give scope-only and logic-duplicate findings dedicated diagnostic IDs.**
  The reproduced scope-only merge appears under generic `qual/validation`.
  Stable IDs and explicit skip reasons would make audit reports and regression
  assertions distinguish a missed check from an intentional exception.
- **Report composite overlap with effective-predicate differences.** The Node
  reverse-shell collection had two rules sharing socket-connect, shell-bridge
  and `/bin/sh` requirements; one required `exec` without proximity, while the
  other allowed `exec` or `spawn` within 4096 bytes. They overlapped but neither
  predicate implied the other. The broad non-proximity branch was retired after
  review because it had no consumer and could join unrelated functions; this
  was an accuracy judgment, not a proven duplicate. A validator could surface
  common required legs and the exact differences after expanding directory
  references and normalizing `all`/`any`/`needs`, proximity, file/platform/
  architecture scope and verdict modifiers. Keep it a review warning:
  overlapping rules can be intentional, and shared legs are not permission to
  merge or remove either rule.

Implement these as a separate validator change with focused regressions. The
current implementation changes only the directory cap/depth policy; it does
not silently alter duplicate semantics during the taxonomy inventory.

## Taxonomic contract

The normative [behavioral directory contracts](../../TAXONOMY.md#behavioral-directory-contracts)
now document domain ownership, admission predicates and ordered disambiguation.
They apply before the legacy illustrative tree or existing directory placement.
The [implementation contract](../../TAXONOMY.md#implementations-and-library-fingerprints)
also applies to every software-identity recommendation below: embedded library
evidence goes to its supported technique or capability group; `well-known` is
for the independently identified artifact, not every application containing it.

Linnaean containment is a useful discipline: every child must be a narrower
kind of its parent. Security observations also have independent facets, so
containment alone cannot ensure unique placement. **Ordered evidence tests**
must resolve intersections. The directory owns one claim; cross-references
express other claims without duplicating their matchers.

For each parent, document: its admission predicate, the single question its
children answer, positive and negative examples for each child, and the first
matching placement test. The full path must read as a narrowing statement.
Classification follows required evidence, not the rule's name, author intent,
language, sample label, optional corroboration, or whichever directory has room.

Apply these tests in order:

1. **What does this matcher actually establish?** A neutral API/path/field goes
   to its capability or metadata subject. Embedded implementation evidence goes
   to its supported capability; independently identified artifacts go to their
   identities. Neither acquires attack intent from a consuming composite.
2. **What result must a composite prove?** Sensitive source plus transmission
   belongs in exfiltration; source access without transmission belongs with
   collection/credential access. An install hook or archive is context, not a
   second copy of that result. Persistence requires a durable activation change.
3. **Which required mechanism distinguishes the result?** Use the ordered
   contracts below; place a mechanism-neutral rule at a genuinely defined
   broader claim only when it cannot truthfully assert any child.
4. **Does it require several independent outcomes?** Factor canonical outcome
   composites. Keep a higher composite only when the conjunction establishes a
   distinct documented claim. Do not create `combined/`, `behavioral/`, or
   `multi/` overflow directories whose only definition is “several things.”
5. **Is it a suppressor?** `crit: exception` remains the composite-only
   suppression role from RULES.md. Its placement is the documented exception
   to evidence-tier placement; it still counts toward the 85-rule budget.

Do not lower criticality to disguise misplacement. Conversely, moving a falsely
hostile neutral observation does require correcting the overstated finding:
preserving a wrong verdict is not a migration invariant. Record such semantic
changes separately from moves and test them explicitly.

### Breadth, depth, and the ML distinction

The current Collimator and Scan implementation extracts direct path features
from the tier plus the first two path segments below it. No downstream
feature-limit change is part of this taxonomy audit.

The current behavior-tier inventory has 253 rule files at depth 2, 8,452 at
depth 3, and 5,560 at depth 4. Only the first two levels below the tier are
currently guaranteed direct path-presence/max-criticality features. Prefer
breadth over depth when the sibling names remain equally precise, but don't
flatten distinctions that need separate canonical homes. Any feature-depth
change should be a separate extractor/model-schema migration with retraining
and evaluation.

Whole-tree structural findings:

- **Single-child parents.** Keep their count as an inventory statistic, not a
  validation warning. The leaf-only rule permits an internal parent with one
  child and no YAML of its own; it forbids mixing YAML and subdirectories.
  A meaningful refinement does not become redundant because it is the only
  subtype currently represented. Child count, depth, and identical current
  descendant sets cannot establish that the parent and child mean the same thing.
  Use existing name-restatement and duplicate-matcher checks where applicable.
  Broader semantic redundancy needs evidence that the documented admission
  predicates are equivalent, not merely that one name looks generic. The
  sparse-sibling advisory reports a parent only when at least two child
  branches together contain fewer than 35 rules; it does not warn on a
  single-child parent by itself.
  Candidates for that semantic review include `trigger/activation`, `self-modify/runtime`,
  `fs/quota/control`, `mem/advise/hints`, and `hardware/block/device`.
  After confirming redundancy, remove the unnecessary level while preserving
  the leaf-only rule, references, and capacity limit. If moving YAML to
  the parent, remove the obsolete child directory; do not leave a mixed node.
  Do not flatten `trigger/activation`'s 97 rules into another oversized leaf;
  identify actual mechanisms instead.
- **Retain real refinements** such as `crypto/symmetric/gost/cbc`,
  `os/compat/wow64`, and `persistence/system/wmi/subscription`: CBC, WOW64, and
  permanent subscriptions answer a specific question about their parents.
  Do not add a taxonomy level merely to satisfy a minimum path-depth rule.
- **Promote/merge duplicate subjects:** `process/fork/clone` with
  `process/create/fork`; `process/script/wsh` by actual execution mechanism;
  `discovery/host/browser/identity` with browser discovery subjects;
  `collection/app-data/notes/app` loses the final `app` word. Account for the
  existing siblings rather than blindly renaming a path.
- **Remove wasted identity layers:** `tool/development/cli/dev-cli/<tool>`
  repeats CLI; use `tool/development/cli/<tool>`. Under
  `tool/development/agent/ai-cli/<tool>`, keep either a defined agent function
  or CLI role, not both grouping words by habit. `.../elex/dropper/elex` repeats
  the family; classify identity facets under the one canonical Elex family.
- **Breadth pressure exists before 150:** `well-known/lib/development` has
  149 immediate children, `well-known/app/system` 139, `well-known/lib/web`
  134, `well-known/tool/development/vscode-extension` 131,
  `well-known/lib/format` 129, and `well-known/lib/network` 127. Subdivide the
  broad catalogs by primary function, e.g. development → compiler, testing,
  linting, build; consolidate into existing function homes first. For identities
  spanning functions, use their documented primary purpose, never alphabetical
  chunks. A product directory still has one canonical home.
- `metadata/package/documentation` is the one inventory entry with both rules
  and descendants. Investigate its direct rules and migrate to their document
  subjects. This inventory observation was not an additional hard error in
  the engine run.

## Cohort 1: neutral subjects and software identities

This work goes first because objective migrations depend on canonical atoms.

| Current violator(s) | Organizing question and disposition |
|---|---|
| `metadata/binary/{framework,vendor}` | Is this a format part, vendor claim, signer, or product fingerprint? Keep format anatomy under `binary`; move signer evidence to `signed`, OS vendor claims to `vendor`, and product/framework identity to existing `well-known` homes. Audit `binary/{bundle,license,signing,toolchain}` too. |
| `metadata/lang/compiled` | What language/toolchain does the artifact prove? Move source-language syntax to `lang/source`, compiler provenance to `lang/compiler`, and independent runtime/library artifact identity to `well-known/lib`. Embedded implementation markers go with their supported capabilities: `rust-zstd-library-marker` is not a language. Split residual language evidence by compilation model only if necessary. |
| `metadata/package/files/system-package` | Which package property is read: container format, member layout, declared fields, or signature? Route into format/member/field/signature subjects, with APK/RPM/container implementation in filenames. Compare all ecosystem siblings, including BSD, MSI and wheel/sdist. |
| `metadata/package/testing/presence/fixture` | Does the matcher prove a fixture's role/location, a testing framework identity, or a generic token? Keep fixture location/content-shape facts; merge path overlap with `presence/path`, move framework identities and certificate facts to their subjects, and keep suppressors explicit. |
| `metadata/permission/host` | What host authority is declared? Split by grant breadth (`all-origins`, `domain-pattern`, `explicit-origin`), then resource category where needed. Distinguish content-script scope in the rule/file. Move extension name/description claims out; provider identity does not establish a grant. |
| `metadata/signed/certificate/identity` | Which certificate role/property is asserted: subject, issuer, timestamp authority, or revocation endpoint? Split those roles and compare with existing `signed/leaf`, `signed/unknown`, and `certificate/signature`; a timestamp issuer must not establish the leaf signer. |
| `micro-behaviors/dylib/library/family` | Loaded-library reference, named-software identity, or API operation? Route each accordingly; a `XCreateWindow` reference belongs with window creation and GDB identity with tools. Retire `family` as a mixed library bucket. |
| Six oversized `well-known` leaves | Keep family/product-specific evidence only. Remove generic `memcpy`, archive-size and API flags, preserving scope through references. For residual overflow, use genuine family components or identity facets, not languages. |

Concrete checks: `metadata/binary/vendor::glarysoft-ltd` reads a certificate
subject; `...::hwmonitor-product-marker-rsrc` reads `HWMonitor`.
`well-known/malware/stealer/amos::memcpy-symbol-macho` matches exactly `memcpy`
and already has a neutral matcher counterpart. It is not AMOS identity.

`well-known/tool/detection/security-scanner` mixes product identities with
generic defensive pattern catalogs. Merge identifiable tools into their named
sibling homes; generic catalogs belong with the documented content/build
subject or a suppressor, not in a purported specific-software identity.
`security-scanner-identity` is a competing sibling to audit together.
`powershell-empire` should retain Empire-specific module/protocol names;
`daemontools-cc` should separate the actual implant components from generic
Toolhelp/API atoms; `elex/worm` needs reconciliation with the other Elex leaves;
`tenorshare` must distinguish product identity from evidence of a trojanized
copy. Product identity alone must not be treated as malware identity.

## Cohort 2: process creation and reverse shells

### Process creation

Apply the existing TAXONOMY process-creation decision table to the *whole*
`process/create` family. The overfull leaves are `agent`, `direct`, `spawn`,
`shell/bridge`, and `shell/spawn`. Siblings `exec`, `execv`, `spawnv`, `system`,
`api-system`, `popen`, `subprocess`, `launch`, `local-exec`, and `shell/lang`
show the same competing axes.

Required shell parsing → `create/shell`; interpreter source argument →
`create/eval`; a child-process object → `create/subprocess`; desktop handler →
`create/shellexec`; native argument-vector launch → `create/exec`. API spelling
and language go in filenames. A bare shell pathname belongs with interpreter
identity, a pipe with IPC/process I/O, and imported `child_process` does not
prove a shell. Agent permission/configuration text does not prove creation of a
process; move it to its configuration/authority subject.

Retire `direct` and `spawn` as competing synonyms, and retire `shell/bridge`
as a JavaScript bucket. Under `shell`, use required command form: interactive
session, command text, script file, or pipeline; encoded text is represented by
canonical decoding atoms plus the executing composite, not another generic
shell directory. More specific forms win over unspecified forms. If only a
shell-capable API is observed, the description and directory must say that;
do not pretend its optional shell argument was present.

### Reverse-shell contract

Strict validation reports 128 rules in the over-cap `socket-exec` subtree.
Netcat currently has 14 rules, so direct-exec and FIFO/pipeline forms remain
together. Netcat has its own technique directory because its utility invocation
is a sufficiently specific shell-relay method; split it by invocation only if
a meaningful subtechnique distinction or directory size requires it. Three
HTTP-only `/dev/tcp` rules moved to neutral HTTP mechanics.

First establish direction and behavior. A listening server is a **bind shell**;
an HTTP request parameter passed to a command is a **webshell/remote-command**
surface. Receiving independent commands is **remote-command dispatch** unless
the rule requires a persistent shell session. Reverse-shell admission requires
an outbound connection and evidence connecting it to the shell's I/O. Socket
plus shell existence alone is not that relationship.

For admitted reverse shells, use the first required mechanism in this order:

| Evidence required | Canonical destination | Exclusion / counterexample |
|---|---|---|
| Shell pseudo-device creates the connection and redirects shell I/O | `reverse-shell/dev-tcp` | `/dev/tcp` used to send HTTP alone is neutral networking. |
| Netcat directly owns the shell relay | `reverse-shell/netcat` | A netcat banner/import alone is not a shell. |
| Pseudoterminal explicitly carries the session | `reverse-shell/pty` | Merely opening a PTY does not meet admission. |
| Socket is installed as inherited standard descriptors | `reverse-shell/fd-redirect` (merge `dup` and applicable `stdio`) | An arbitrary file `dup2` is neutral descriptor manipulation. |
| Explicit read/write/copy loop joins socket and persistent child streams | `reverse-shell/stream-bridge` | A per-command request/result loop goes to remote-command dispatch. |

`encoded` and `syscall` are evidence representations, not competing shell
mechanisms: route their rules using the same table. The three HTTP polling
command agents moved from `reverse-shell/http-poll` to
`remote-command/http-poll`; this directory requires repeated fetch/dispatch
and does not represent a persistent shell session. Retire `socket-exec` after
redistributing, not by adding another
generic child. If a rule proves a reverse shell but its bridge mechanism cannot
be inferred, strengthen it or document that missing mechanism before deciding
a new child; do not manufacture a catch-all to clear the cap.

Verified examples in `socket-exec`:

- The Ruby listener plus shell composites now live at canonical
  `objectives/command-and-control/backdoor/bind-shell`; their server-loop,
  client-accept and descriptor-redirection atoms live with socket/process
  capabilities. The old `backdoor/dispatch/bind-shell` sibling was merged into
  this canonical bind-shell directory.
- `ruby-http-query-command-shell` is not a reverse shell. Determine from the
  surrounding server/client evidence whether it is a webshell endpoint or a
  remote-command client before moving it.
- `objc-connect-call`, `csharp-tcpclient-host-port`, and
  `swift-process-launchpath-bin-sh` are neutral socket/process capabilities;
  `open3-popen` still needs a matcher-level audit before final placement because
  one variant is a string-literal API token rather than a proven call.
- The Objective-C connect call, C# `TcpClient(host, port)`, Swift shell launch
  path, and Node RFC1918 address observations have been moved to their neutral
  socket, process-creation, and IP-literal capabilities with consumer
  references remapped. Their matcher predicates, scopes, confidence, and
  criticality are preserved. The reverse-shell leaf is smaller by six rules;
  remaining objective composites still need admission review.
- `objc-systemd-wantedby-default` only matches `WantedBy=default.target`;
  it is a service configuration fact. `any-shell-exec` is a neutral aggregate.
- `dev-tcp::shell-dev-tcp-http` required only TCP redirection plus an HTTP
  GET/Host token. It now lives as a neutral notable direct-socket HTTP capability;
  the benign `/dev/tcp` health-check fixture forbids any reverse-shell finding.
- The shell and PowerShell HTTP poll agents moved to
  `objectives/command-and-control/remote-command/http-poll`. Their matched
  fetch/evaluate/post-or-loop predicates and verdicts are unchanged; their
  descriptions now identify task polling rather than a reverse shell.

## Cohort 3: payload delivery, hiding, and loading

Audit **all** `command-and-control/dropper` siblings with
`anti-static/obfuscation/payload`, `evasion/fileless`, and
`evasion/process/injection`. The largest leaf has 324 rules, so moving whole
files or renaming one node is inadequate.

`delivery/execute-download` (324), `delivery/fetch-exec` (133),
`execution/exec-download` (115), `execution/execute-download` (15),
`delivery/fetch-eval` (129), `execution/eval` (78), and `execution/fileless`
(112) demonstrate duplicate concepts across delivery and execution. The
current four-phase dropper tree puts full-chain composites under whichever
phase the author happened to emphasize.

**Proposed change to TAXONOMY:** put complete payload-activation chains directly
under `dropper/<activation-mechanism>`. The child question is “how does staged
payload become running code?” Apply required sink precedence:

1. execution in a different process → `process-inject`;
2. same-process native image mapping → `image-map`;
3. runtime module/assembly loading → `module-load`;
4. source evaluated in the current interpreter → `script-eval`;
5. source fed through stdin to a new interpreter → `interpreter-stdin`;
6. a staged file launched through a process/file handler → `file-exec`.

These are proposed paths, to be reconciled with the canonical evasion and
execution atoms/composites, not six new copies of them. Dropper admission
requires a demonstrated payload-staging/activation relationship. Evasion
composites which merely establish an injection technique stay in evasion;
the delivery-chain composite references that one technique. A carrier file
shape alone is metadata. Document a narrower child only when its necessary
evidence refines the activation mechanism; fifth-level room is available for
such a refinement.

`staging/{encrypted,embedded,memory,archive}` overlaps source, transform, and
storage axes. Retire full-chain rules from those branches into activation
homes. Put standalone decryption/decoding/archive mechanics into capabilities;
concealment *objectives* into anti-static; neutral section/entropy/layout facts
into metadata. A remote encrypted assembly therefore has one complete-chain
home (`module-load`), with cipher and download evidence referenced.

Likewise retire language/container buckets `execution/{batch,script,wsh}` and
`node-bootstrap`; classify their actual chains. `execution/installer` contains
SFX, MSI custom actions, signed overlays and scripts—installer identity is not
an execution mechanism. `builder` contains neutral compiler/build settings
alongside malware-generator templates; separate build facts from actual
payload construction.

Evidence: `staging/memory` includes a temporary AppleScript file path and
file-writing launchers; `payload/encrypted` includes plain large-data-section
measurements; `execution/script::msi-scheduled-task-action` only searches for
`New-ScheduledTaskAction`. Neither an MSI nor that API proves a dropper.

Capacity planning is deliberately deferred to the rule-by-rule map. These
large families may need real submethods and composite consolidation even
after neutral atoms leave. Do not promise that these six leaves alone fit 85.

## Cohort 4: HTTP, protocols, and system capabilities

| Family | Required boundary and sibling reconciliation |
|---|---|
| HTTP `post`, `upload`, `request/client` | Method evidence stays in `post`; attachment/multipart/file-source mechanics in upload; method-unspecified client request in client. A GET belongs in existing GET handling, a header token in its header subject. Split upload by attachment mechanism, not SDK; raw body writes are not automatically uploads. |
| HTTP `oauth` | Separate authorization request, code exchange, token refresh, and token use; move fields/scopes to their field/authority subjects. Reconcile `auth`, `token-auth`, `device-code`, `authorization-header`, `idp`, `jwt`, and `login`. Token refresh must not also be classified merely as token exchange. |
| HTTP `services/{github,microsoft}` | Endpoint presence and an actual operation are different claims. File named-service endpoints under service/resource purpose and neutral operations under their behavior. Compare existing `sharepoint`, `dataverse`, `entra-directory`, `devops-azure`, GitHub URL and CLI siblings before creating anything. A CLI call is not HTTP evidence merely because its vendor has an API. |
| HTTP `url/query`, `user-agent` | Separate constructing/parsing query parameters from particular field meanings; separate setting/reading a User-Agent from comparing it and spoofing/rotation intent. Reconcile `http/query`, `request/params`, `url/telemetry`, `fingerprint`, and header siblings. Campaign labels are not generic query operations. |
| MCP | Protocol negotiation, tool registration/listing/call/result, and resource access are legitimate children. Config-file presence and product identity leave the protocol bucket; filesystem/shell APIs exposed as tools remain canonical capabilities referenced by the MCP composite. |
| TLS / proxy | Reconcile `socket/ssl`, `http/{ssl,tls}`, proxy `tunnel`, `relay`, `socks`, `reverse`, and C2 tunnels. Separate handshake, certificate validation, and encrypted I/O. TLS verification disabling needs its own factual validation-setting observation and an intent composite where appropriate. Move cloudflared/ngrok identities to their existing software homes. |
| Blockchain / SQL | `crypto/library/blockchain/client` mixes transaction semantics, payment services, identities and address decoding. Keep a neutral `communications/blockchain/client` composite for actual chain queries and transaction behavior, while relocating atoms to RPC, transaction, crypto and wallet/provider operation homes; imports, endpoint strings and offline key operations alone do not establish client use. SQL divides query/execute/schema/connection; Entra credential-table targeting leaves generic SQL, tool fingerprints leave capabilities. |
| Base64 decoding | Consolidate equivalent variants before a split. Compare `symbol-base64`, `native-base64`, `reflection-base64`, `request-base64`, `environment-base64`, `repeated-base64`, and `quartet-base64`. Input origin and matcher implementation are not alternate meanings of Base64 decoding. A required repeated decode is a refinement; a decoder reached by a symbol matcher is not. |
| Registry | One operation axis: open, read/query, write, create key, delete, enumerate, watch; key/hive references have distinct factual homes. Retire mixed `access`/`manipulate` buckets by routing to existing siblings first. A write API alone is not persistence. |
| Scheduled tasks | Task definition, registration, launch, query, deletion, and trigger properties are different facts. Reconcile `scheduled`, `task-trigger`, and `task-xml-scheduled`; a scheduled-task API is neutral. Durable malicious task installation is a persistence composite. |
| Container / network interface | Split container lifecycle, inventory, image, exec, namespace and authority facts with existing siblings. Split interface enumeration, address queries and configuration; saved WLAN credentials leave interface handling. `android-play-store-package-literal` matches `com.android.vending`, not an interface. |

## Cohort 5: observations and objective boundaries

All oversized directories in these groups are enumerated in disposition.csv.

| Group | Canonical axis and required corrections |
|---|---|
| Debugger / sandbox / VM detection | Classify the probe mechanism: debugger API, process status, tracing interference, debug registers; sandbox resource/user/artifact/timing gates; VM instruction/firmware/device probes. Remove bare APIs/vendor strings to neutral observations. `check`, `script` and `vendor` mix these axes. Compare `combined-checks`, `artifact`, `dmi`, `process`, `registry`, `instruction`, `timing` before splitting. |
| Self-modification | `runtime` restates the parent. Separate required code rewrite, import-table rewrite, and decoder self-update; relocate ordinary memory protection and GOT hook observations. Reassess anti-analysis placement when static-analysis obstruction or production interposition is the actual effect. |
| Obfuscation / packing | Separate required concealment mechanism: API hash resolution, escaped import names, dynamic dispatch, string selection/permutation/concatenation, runtime decryption, bytecode/VM dispatch, runtime unpacking. Reconcile string `reconstruct`, `fragmentation`, `concat`, `array`, `reverse`, and `recovery`; do not leave synonymous subsets. `binary-metrics`, `code-metrics/structure`, `section-anomaly`, and `detect` are rule-form/judgment buckets. Their neutral metrics go to the part measured. Named packer identity goes to well-known; actual unpacking/concealment stays objective. |
| Keylogging / screenshot / monitoring | Classify capture source/mechanism: keyboard hook, device input, DOM input, terminal; screen/display capture; camera; microphone. Generic capture APIs are capabilities; objective composites must establish surveillance context. Collection plus transmission goes to stealer. `monitor/capture` must not duplicate screenshot/keylog. `go-empty-recover` only matches empty panic recovery, not a screenshot. |
| Browser activity / messaging / email | Distinguish browsing/history collection, message/mailbox content, contacts, and credential/session stores. Route cookie/session theft to credentials, source-plus-send to exfiltration. `email-harvest::mailitems-accessed-operation` is an audit event fact; `monitor/tracking::sentry-self-hosted-dsn` is a telemetry endpoint shape, not proof of covert tracking. |
| C2 dispatch / RAT / webshell | One request-to-action axis for remote-command dispatch; polling/socket/HTTP are channel facts. Retire duplicate `control`, `tasking`, `rat/multi`, and parallel `backdoor/tasking` placements after mapping actual required operations. Keep server request-to-command webshells separate from an outbound reverse shell. Memshell intercept splits by required installed hook: request filter, listener, handler/route; plain framework registration is a capability. |
| Botnet / IRC / tunnels | `iot` is a deployment platform, `irc/client` contains protocol mechanics and malicious actions. Move neutral protocol evidence, family names, DDoS and propagation to their subjects; retain fleet-control evidence. C2 tunnels must show control/relay intent beyond proxy capability. DNS command retrieval and DNS data exfiltration are different required directions. |
| C2 trigger / infrastructure | Replace `trigger/activation` with packet knock, message/content gate, or local artifact gate when attacker activation is required. `ci-abuse` mixes ordinary Jenkins/Groovy references with credential theft, pipeline tampering, persistence and C2: retire it by effect. Brand impersonation is deception/phishing unless C2 role is independently established. `groovy-package-json-rewrite` matches only `package.json`. |
| Browser credentials / system dump / SSH / wallets | Filepaths and neutral store APIs leave objective buckets. Classify actual extraction by store and bypass/decryption mechanism. Browser source/store contracts should reconcile Chromium, Firefox, multi-target, DPAPI and session hijack. SAM/NTDS/shadow/LSASS are distinct system stores. SSH key harvesting is not host-key validation bypass. Wallet mnemonic entry phishing is not a local-wallet-store read. |
| Phishing | Deceptive prompting, form harvesting, origin/proxy relay and session interception have distinct admission predicates. `credential`, `lure`, and `mfa-relay` must not each own the same full harvest chain. Complete phishing source-plus-send chains go to `exfiltration/stealer/phish`; the deception/relay composite is referenced. |
| Discovery | `network/scan/port` requires active probing/enumeration, not a literal port or generic socket. Distinguish connect, SYN and protocol-response probing; compare `banner`, `utility`, `http`, `ics`, and distributed scanning. Host profile requires multi-property reconnaissance, with plain hostname/interface APIs in capabilities. |
| Defender / EDR | Stealth bypass/exclusion belongs in evasion; process termination, service disabling, update teardown and driver-assisted killing in impact/degrade. Reconcile `platform/defender`, `amsi`, `teardown`, `terminate`, `driver`, `targeting`, and `autostart` by required action. |
| Injection / fileless / rootkits | Require target and execution transfer for injection; hollowing, APC, thread hijack, module stomping, and remote-thread creation are distinct mechanisms. Same-process shellcode execution is not cross-process injection. A userspace LD_PRELOAD rootkit is not a kind of kernel hiding: move to an evasion concealment parent with distinct userspace-interposition and kernel-manipulation children, and reconcile existing preload/hook leaves. |
| Masquerading / logs | Classify deception by the identity surface actually falsified: process title, filename, version metadata, signer claim, or format. Retire `identity/fabricated` and reconcile `binary`, `file/lure`, `process/name`, `process/title`, `identity/process-title`. Log removal, truncation, selective record removal and disabling audit production must reconcile `logs`, `log-removal`, `audit`, `application-logs`, and `accounting`. |
| LLM prompt abuse / automation | Classify the violated boundary: instruction authority, tool arguments, policy/config mutation, sensitive export, or output disclosure. Prompt wording/carrier alone is evidence, not a unique attack. Reconcile `prompt`, `override`, `persona`, `output-steering`, and `sandbox`; neutral agent configuration must not imply code execution. |
| Destruction / ransom / infection | Destructive deletion vs overwrite vs encryption vs host infection are different effects. DOS API calls go to OS capabilities; DOS/source are not infection techniques. Split infection by append, prepend, entrypoint replacement, cavity/section insertion, or script insertion. Ransom notes/config are evidence for ransom, not necessarily encryption. Reconcile filesystem encryption with `bulk-encryption`, `hybrid` and runtime wrappers. |
| DDoS / rival removal / ICS | Protocol flood mechanism, target-disabling action and industrial control mutation define children. Botnet tasking alone is C2; neutral protocol/config methods leave impact. Merge rival `competitor` with applicable `killer`/`scan-terminate` rules. An industrial read is not sabotage. |
| Brute force / exploits | Separate credential guessing strategy (spray vs per-account dictionary vs fixed defaults) from service transport, with ordered precedence. Neutral SSH authentication leaves brute-force. Split exploit claims by exploit primitive or affected boundary, retain specific CVE context in rule metadata/files. `vulnerabilities` restates `exploit`; `network-device` mixes provisioning, discovery and exploitation. |
| Persistence | Put durable activation mechanism before platform. Merge Run-key rules in `login/startup/registry` into `login/registry/run-key`, but route Active Setup/Winlogon separately. Reconcile shell `config`, `rc`, `profile`; service `install`, `systemd`, and sibling `system/systemd`. User services/timers are not necessarily OS-boot persistence. Backdoor account creation grants continued access; it is not code executing at login. Revise the boot/login-only parent rubric accordingly. |

## Cohort 6: exfiltration and supply chain

For exfiltration, the existing `stealer/<source>` contract is already the best
canonical home for complete chains. Route the full chains in HTTP `upload`
(201), `collect` (120), `agent` (95), and `sensitive-data` (142) there; neutral
HTTP atoms leave objectives. DNS transport does not override the source of a
complete theft chain. Keep transport-specific objective leaves for transport
abuse whose required evidence does not identify a narrower source, rather than
duplicating every source under every transport.

Split the oversized stealer sources semantically: browser → cookie/session
versus saved-login versus browser history/content; system-info → host identity,
hardware/platform profile, account profile, or a required joint host profile.
Define precedence when a single chain steals several: a mandatory multi-store
sweep uses the existing sweep contract; optional extra sources do not move a
browser stealer. Network configuration already has its own source sibling.
Whether these distinctions should replace the third-level source or sit one
level below it is an explicit ML-schema choice, not an accidental overflow fix.

The supply-chain tree has the same dimensional duplication at larger scale:

- `recon-exfil/install-hook` (209) and `npm-install-targeting` (88) duplicate
  source-plus-send chains; use canonical stealer source directories and reference
  the install/build/import trigger. `install-hook/build/behavioral` (134) and
  `install-hook/dropper/hook-setup` (94) duplicate payload activation chains.
- `hidden-payload/{runtime,package,exec,staging,trojan}` mixes carrier, lifecycle,
  concealment and result. Move neutral facts to metadata/capabilities; full
  theft/delivery chains to their existing objective; keep supply-chain-specific
  concealment only when the package trust boundary is required.
- `trojanized/{package,app/package}` overlaps itself. Require unauthorized
  modification/substitution of a legitimate component. Separate dependency
  substitution, build-input/output replacement, update substitution, and
  configuration/extension poisoning. A package that is simply a loader is not
  evidence that a previously legitimate application was modified.
- `trojanized/app/config-injection` needs distinctions between instruction-file
  poisoning, tool-server configuration, authority changes and endpoint swaps.
  Reference the resulting behavior; avoid reproducing the entire attack tree
  below “agent”. `build-pipeline` should retain boundary crossings such as
  untrusted PR code under privileged credentials, not generic curl/build facts.
- `impersonation/{package/wheel-sdist,registry/manifest,registry/snapshot,
  registry/wheel-sdist}` is organized by evidence container. Move manifest and
  registry observations to metadata; retain deception comparisons by the thing
  misrepresented (name, provenance, functionality, declared contents). Registry
  versus artifact remains a source/scope distinction in the matcher. A tiny
  package, version churn, or self-disclosed security purpose is not itself
  impersonation. `cargo-dep-litcrypt` is a manifest dependency identity.

This resolves a contradiction already inside TAXONOMY.md: the “trigger is not
an objective” passage criticizes install-hook duplication while the main tree
still prescribes install-hook/recon-exfil branches. The migration must replace
that tree and its examples with these canonical ownership rules in the same
change that moves each cohort.

## Migration sequence and acceptance criteria

0. **Establish placement contracts first — documented.** Use TAXONOMY's
   level-1–3 contracts and technique-first implementation test. Before each
   migration, complete any missing leaf admission predicates and disambiguate
   overlapping siblings. Planned paths in the guide are not already migrated.
1. **Canonical atoms and metadata/identity cleanup.** Start with registry,
   process creation, HTTP, binary metadata, then source/store observations.
   Retire implementation-only layers alongside these canonical subjects,
   following the implementation-layer audit. Refine the documented contracts
   when a concrete matcher reveals an unresolved boundary.
2. **Reverse shells as the first complete pilot.** Map all 342 rules across the
   nine sibling leaves, including neutral atoms and bind/HTTP counterexamples.
   Use its reference and fixture migration as the pattern for later cohorts.
3. **Coordinate dropper/obfuscation/injection boundaries; migrate bounded batches.** Produce all
   old-ID → new-ID mappings and destination counts before moving. Fold redundant
   complete-chain composites only after comparing scope, required evidence,
   proximity and exclusions. Do not preserve a stale parent to host aliases.
4. **Exfiltration and supply-chain chains together.** Otherwise each migration
   repopulates the other's old buckets. Move trigger/context facts first, then
   route result composites and update package/archive scope deliberately.
5. **Remaining objective cohorts and broad identity catalogs.** Follow the
   disposition ledger; use the structure report to prune redundant depth and
   introduce primary-function breadth where required.

For **every** cohort:

- Materialize a mapping for every old rule: keep, move, merge into named
  canonical rule, or retire with evidence. Record inherited defaults before
  splitting YAML files. Language-specific matchers may remain separate within
  one directory; collapsing them must preserve supported scopes.
- Compute destination counts including incoming rules and existing residents.
  All must be ≤85, with no exemptions, and every internal directory must be
  free of YAML leaves. Do not choose an arbitrary “misc” remainder.
- Rewrite local references, fully-qualified references, positive directory
  references, `unless`, `downgrade`, fixture expectations, source/docs examples,
  and engine consumers. Compare the **resolved member sets** of directory refs
  before/after; a syntactically valid reference can still change meaning.
- Snapshot match results before moves. For pure relocations, compare detections
  modulo the ID map, including criticality, scope, exclusions, confidence and
  evidence. For semantic repairs, document expected verdict changes and add
  targeted positive/negative cases: HTTP-over-dev-tcp vs reverse shell,
  bind vs connect-back, legitimate registry writes vs persistence, ordinary
  installers vs payload activation, and authorized telemetry vs theft.
- Require all focused tests and `make validate` before declaring the migration
  complete. Until all cohorts fit, track the exact remaining oversized set;
  `--soft` is diagnostic, never the final acceptance check.
- Update the feature schema/mapping supplied to downstream consumers. A path
  migration changes ML features even when runtime findings are equivalent;
  retraining/evaluation is needed before claiming improved ML accuracy.

The outcome should be fewer overlapping concepts and stronger canonical
observations. Passing a numeric cap alone is not evidence of a defensible
taxonomy or better model performance.

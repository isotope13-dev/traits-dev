# Runtime-indirection atoms: symbols and conversion

Two atoms leave the obfuscation namespace. The [four-entry effective-definition
ledger](runtime-observations-mapping.json) records both moves, their direct
consumer update and the conservative exclusion update. Predicates, size/count
thresholds, scopes, platforms, confidences and criticalities are unchanged.
Unsupported atomic ATT&CK/MBC labels are removed.

| Previous observation | Canonical home | Evidence limit |
|---|---|---|
| js-indexof-decoder-heavy | metadata/file/naming::indexof-symbol-cluster | Counts symbols named indexOf; neither receiver type, invocation nor decoding is established. |
| js-charcode-decoder-heavy | micro-behaviors/data/string/conversion::character-code-conversion-cluster | Repeated charCodeAt near fromCharCode arguments; the regex does not establish a decoder or bind a data-flow relationship. |

The direct consumer becomes `js-runtime-string-conversion-profile`, described
as long-line code with searches and character conversion. Its conjunction,
thresholds and criticality remain unchanged. It requires the relocated atoms,
long-line metadata and high-entropy identifiers; its old name overstated this
as a runtime string decoder. No alias is retained.

## Siblings and consumers

String/search contains actual search-call shapes and inline alphabet searches;
those establish more than the untyped symbol count. String/conversion already
owns fromCharCode aliases and keyboard-code conversion. Character access alone,
XOR conversion, and explicit hexadecimal parsing are different observations.
Neither relocated atom has an identical `if` body elsewhere in the pre-migration
inventory; similar names do not justify a merge.

The [ancestor audit](runtime-observations-ancestor-audit.json) identifies five
obfuscation-directory consumers. Four retain their category reference without
backfilling neutral evidence: the long-tail config requirement, hidden listener,
concealed exfiltration and PHP backdoor alternatives should require actual
obfuscation evidence. This intentionally removes these two atoms as sufficient
concealment evidence; all other alternatives and requirements remain intact.

The fifth, `js-has-tests-without-obfuscation`, receives explicit exclusions for
both moved atoms. This preserves its historical conservative admission and
prevents relocation from expanding a benign-context helper. The exclusions do
not classify the atoms as obfuscation. There are no destination ancestor
consumers to broaden.

## Verification

Two benign archives exercise 25 indexOf symbols and four ordinary character-code
roundtrips, with comment padding to satisfy existing size floors. Atomscan
before/after comparisons preserve all four archive/member finding sets and
criticalities modulo relocated IDs. Scores remain 3/2 for the symbol archive
and member, and 6/4 for the conversion archive and member. Neither archive fires
the remaining runtime-indirection composites. Fixture prefix requirements
check the new subjects and forbid that objective leaf.

A direct checkout-engine trace confirms 25 matching indexOf symbol records
and no character-conversion match on the symbol control. It completed normally
(after about a minute); no debugger timeout is counted as a pass. Atomscan uses
the installed engine, whereas the fixture gate and trace use the sibling release.

`validate --soft`: **1,724/1,724 fixtures pass**, including 434 benign cases.
Strict `make validate` still fails solely on **173 oversized directories**.
The inventory has **zero mixed nodes**. Naming grows 70→71, conversion 33→34,
and runtime-indirection shrinks 5→3. No cap exception was introduced.

Logs: `/tmp/taxonomy-runtime-observations-{before,after}.json`,
`/tmp/taxonomy-runtime-observations-indexof-trace.log`,
`/tmp/taxonomy-runtime-observations-soft-final.log`, and
`/tmp/taxonomy-runtime-observations-strict.log`.

## Remaining work

This does not endorse runtime-indirection as a precise category for the three
remaining composites. The obfuscator-output and npm-malware names also exceed
what their structural conjunctions establish. Their claims and final homes need
the broader code-metrics composite audit; the conversion profile likewise
establishes co-occurrence, not a bound decoder. Retiring that category requires
accounting for all three composites and their ancestor consumers. The broader
173-directory cap debt, source/syntax and retry audits remain open.

Follow-up: [Runtime profile retirement](RUNTIME-PROFILES.md) removes the remaining
runtime-indirection leaf and the misplaced benign summary. The ledger above
remains the historical snapshot of the atomic migration.

# Neutral observations previously suppressed by SQL context

Moving schema operations exposed two broad SQL-based exclusions. They were
compensating for overstated claims rather than establishing benign context:
SQL does not change whether a program contains a comma expression or command
vocabulary. This cohort removes that accidental dependency from the taxonomy.

## Classification corrections

Eleven observations move to neutral homes:

- A parenthesized expression containing three strings moves to
  `data/control-flow/sequence::three-string-comma-expression`.
- Repeated delimiter removal via split/join moves to
  `data/string/replace::repeated-split-join-removal`.
- Eight command/status string observations and their three-of-eight aggregate
  move to `metadata/file/string/command`.

Matching predicates, count/size limits, scope, confidence, local `not` filters,
and existing downgrade conditions are unchanged. SQL-related exclusions are
removed from the comma expression and vocabulary aggregate. Other exclusions
on the two language operations remain unchanged. Intent-only ATT&CK/MBC
annotations are removed from these neutral observations. Split/join removal and
a standalone KILLPROCESS label become notable instead of suspicious because
neither proves malicious intent; placement and descriptions are corrected too.

The former `split-join-wsh-dropper` verdict required only split/join and comma or
concatenation patterns. It required no Windows script host, payload, download,
file write or execution. It is retired; specific WSH combinations remain and
reference the canonical language operations. Existing intent consumers are not
all proven precise by this change and remain eligible for relationship audits.

A control performing ordinary name formatting reproduced a hostile dropper
finding (archive score 146). Adding unrelated SQL to one member suppressed the
comma observation while leaving string cleanup suspicious. Both operations now
remain visible in both members without implying a dropper. A compiled program
that only printed command labels scored 47 and received a suspicious KILLPROCESS
finding; it now receives neutral vocabulary observations instead.

The [22-entry ledger](sql-suppressors-mapping.json) records the 11 relocations,
10 consumer changes and retired verdict. Effective definitions verify against
current YAML, and all relocated core predicates/scopes/counts are preserved.
Removing SQL suppressions intentionally permits downstream combinations to
match even when unrelated SQL is present; this is not an identical-output claim.

## Validator correction

The metadata section-filter function already documents its result as a
recommendation for potentially file-wide properties. The loader nevertheless
turned it into a fatal validation issue. Its diagnostic is now advisory for all
metadata, with no directory-specific allowlist. Whole-file command vocabulary
must not be assigned an arbitrary section merely to permit correct placement.
The separate requirements for well-known binary fingerprints and binary hex
conditions remain strict. RULES.md and TAXONOMY.md document the distinction.

Five section-filter tests pass, including a new test that ensures binary-only
metadata still receives the recommendation. The release validator was rebuilt;
full validation verifies that these recommendations no longer become blockers.

## Verification and remaining work

Two new benign archives contain JavaScript string operations and compiled
command-printing programs, each with and without SQL content. They are scanned,
not executed. The controls require their new neutral homes and forbid the
inappropriate dropper/IRC objectives. All six archive/member exact-ID checks
pass; the compiled SQL variant also exposes its password-column observation,
proving the control exercises a former exclusion. The string archive now scores
5, and the command-vocabulary archive 12. Full validation passes **1,688/1,688
fixtures**. Strict validation reports only **173 oversized directories**, with
zero mixed nodes. Logs: `/tmp/taxonomy-sql-suppressors-controls.json`,
`/tmp/taxonomy-sql-suppressors-soft-final.log`, and
`/tmp/taxonomy-sql-suppressors-strict-final.log`.

IRC bot drops from 90 to 81 rules. The command vocabulary leaf contains 11 rules,
string replacement 14, and sequence evaluation 1. No parent aliases or mixed
rule directories were introduced. Only the explicit Classic ASP database
consumer still references the entire SQL leaf; its ADOX requirement was made
explicit in the preceding schema cohort.

Remaining work includes the SQL row/schema operation regrouping, parser/editor
misplacements and wider cap migration. IRC protocol co-occurrence and tiny-PE
verdicts in the old sibling file still warrant precision review: protocol tokens,
file size and ordinary file APIs alone do not prove bot control or propagation.
The strengthened taxonomy does not excuse those remaining intent claims.

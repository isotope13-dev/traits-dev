# SQL leaf and database schema siblings

The 89-rule `data/db/sql` leaf mixed row operations, connection APIs, schema
operations, editor integrations, HTTP route fragments and embedded implementation
references. All seven files were read, together with the existing schema leaves
and PostgreSQL, MySQL and configuration siblings. No identical raw atomic `if`
bodies were found across the database subtree; that does not establish that
predicates are disjoint or semantically distinct.

## Implemented schema cohort

Ten observations now use existing operation-specific homes:

- Four table/column observations move to `schema/relational`.
- Five catalog/introspection observations move to `schema/introspection`.
- The SQL trigger with JavaScript source marker moves to `schema/stored-code`.

Predicates, scopes, confidence, criticality, counts and exclusions are unchanged.
The table-plus-BLOB and catalog-reference composite descriptions now state what
the evidence establishes, without claiming a shared table or executed query.
The trigger description no longer assumes the generic marker alone identifies
an H2 implementation. TAXONOMY.md documents admission and tie-breaking rules.

The [20-entry ledger](sql-schema-mapping.json) records ten relocations and ten
consumer changes. Effective after-definitions and all relocation conditions
were verified against current YAML, modulo canonical reference names.

## Directory-reference consumers

Two existing suppressors retain SQL observations that moved out of their old
subtree. Python-only catalog references cannot match their JavaScript or PE
file scopes and were omitted. The table/BLOB composite is redundant with its
already included atomic conditions. The text/script-only trigger is likewise
irrelevant to the PE consumer. Pruning these dead or subsumed alternatives
preserves the relevant exclusion evidence without exceeding suppression limits
or broadening the exception to unrelated schema siblings.

The Classic ASP ADO rule's comment describes SQL evidence **and** an ADOX catalog.
Its former `any: [SQL directory, ADOX]` with `needs: 2` is ambiguous: the evaluator's
`condition_count_weight` counts distinct matched IDs beneath a directory, not
just one matched branch. Two SQL matches can therefore satisfy the numerical
condition. Mandatory-reference prefiltering also interacts with this shape.
The rule now explicitly requires ADOX in `all` and one SQL observation in `any`,
including the moved observations. This is an intentional tightening to its
stated requirements, **not a general equivalence claim**. The full fixture suite
passes, but is not proof of identical behavior for every untested input.

Validator improvement: flag `needs` expressions where a broad directory can
supply the whole threshold despite apparently independent neighboring legs.
The diagnostic should explain cardinality and distinguish leaf-counting from
branch-counting; authors should not have to infer this from implementation.

## Verification and impact

The new benign schema archive includes table/column definitions, catalog
references and a stored trigger. Its finding sets are unchanged modulo the
migration map for archive and both members. Nine moved findings are visible;
the baseline BLOB composite can be omitted from rendered output. Scores remain
3 for the archive, 3 for schema source, and 1 for the trigger text.

**1,683/1,683 fixtures pass.** SQL drops from **89 to 79 rules**. Existing schema
leaves now contain 9 relational, 12 introspection and 7 stored-code rules.
Oversized directories drop from **175 to 174**, with zero mixed rule directories.
Strict validation reports only that remaining cap debt.

Logs: `/tmp/taxonomy-sql-schema-{before,after}.json`,
`/tmp/taxonomy-sql-schema-soft-final.log`, `/tmp/taxonomy-sql-schema-strict.log`.

## Remaining SQL and sibling plan

Fitting SQL under the cap does not finish its organization. The remaining audit
must resolve these subjects by their actual required evidence:

1. Separate row selection/modification, connection setup, prepared execution,
   schema destruction and extension management. Preserve broad API references
   honestly; an import is not an executed query.
2. Move editor operations and inter-editor event channels to their UI/IPC
   techniques. Ace access and an arbitrary `/explain` route do not establish
   SQL or AI. Strengthen service identification before assigning generic route
   fragments to a named database service.
3. Review schema siblings: quoted `user_id`/timestamp fields do not establish a
   relational database; JSON aggregation alone does not establish schema
   introspection; query-tool start/poll routes are not catalog queries.
4. Correct `sql-plaintext-password-storage`: a password column and an assignment
   do not establish that the assigned value is plaintext. Keep credential-table
   access observations separate from unsupported storage or theft conclusions.
5. Keep crypto operations with crypto, parser implementation evidence with its
   supported parsing capability, and database connectivity with its supported
   operation. Existing PostgreSQL/MySQL driver and URL observations require
   their own scope and identity audit before regrouping.
6. Audit overlapping SQL syntax predicates before merging: SELECT/INSERT/UPDATE/
   DELETE/DROP variants differ in literal versus raw evidence, scope, exclusions
   and required clauses. Similar descriptions alone do not justify consolidation.

The broader 85-rule migration remains active. This report records a completed
schema cohort and the concrete unresolved boundaries, not a completed database
reorganization.

# SQL row mutations and schema destruction

## Placement and migration

Fifteen existing observations now follow the operation they describe:

- Five INSERT, UPDATE and REPLACE observations → `data/db/write/row`.
- Six DELETE and TRUNCATE observations, including the DELETE composite →
  `data/db/delete/row`.
- Four DROP observations → `data/db/schema/delete`.

Thirteen came from the SQL leaf and two from the MySQL leaf. These are syntax
observations, not proof that a database operation executes. The directory contract
in TAXONOMY.md distinguishes removing records from destroying schema objects.
Dialect and source-language details stay in filenames and matcher scopes.

The [31-entry ledger](sql-operations-mapping.json) records the fifteen moves and
sixteen consumer updates. Effective predicates, scopes, criticalities, confidence,
counts, exclusions and downgrades are unchanged, modulo qualified references.
Two descriptions are corrected: the DELETE aggregate includes terminated as well
as clause-qualified statements; REPLACE syntax establishes a row write, not
specifically an update. No aliases remain at the former locations.

The Classic ASP ADO consumer retains the thirteen former SQL alternatives by
name alongside the residual SQL directory. It does not inherit the unrelated
MySQL alternatives or other rules in the destination leaves. The two broad MySQL
exclusions in Python socket rules need no expansion: the moved MySQL rules have
PHP-only scopes. Other consumers use updated exact references.

## Duplicate and sibling audit

No identical atomic `if` bodies occur in the current database subtree. Similar
SQL statements still differ materially in literal versus raw-text evidence,
clauses, supported file types, exclusions and size limits. This cohort does not
merge those distinct predicates or claim that the absence of exact duplicates
proves the absence of redundancy.

Remaining precision work, confirmed against current matchers:

- `sql-set-password-assignment` does not require UPDATE context; placing it under
  row writes would assume an operation it does not establish. Keep it unresolved
  until account-password and row-assignment syntax are distinguished.
- `sql-truncate-object` still accepts TABLE, DATABASE and SCHEMA tokens. Its
  preserved description claims syntax only. Dialect validity and the meaning of
  each accepted form need a separate audit before changing coverage.
- Editor object access, editor event-channel names and generic route fragments
  in `sql/browser-extension.yaml` do not establish SQL execution. `/explain`,
  `/generate-query` and `/add-comments` do not establish an AI service. Move each
  observation to its actual subject; composites must not invent a relationship
  from co-occurrence alone.
- `schema/introspection` includes JSON aggregation without a catalog target,
  plus query-tool start/poll route fragments. Neither alone establishes schema
  introspection. Its actual catalog references belong here, with descriptions
  limited to reference evidence where no call is matched.
- `schema/relational` still includes quoted user and timestamp field names and
  nearby dataset/user identifiers. These do not require a relational schema or
  establish key relationships. Audit serialization/record-field siblings before
  relocating them, to avoid creating a second home for the same observation.
- Connection, parser, extension and vendor-driver observations remain mixed in
  SQL and vendor leaves. Continue the operation-based audit across their siblings.

Potential validator improvement: present overlapping SQL matcher candidates with
all scope/filter differences rather than treating similar descriptions or regex
fragments as mergeable duplicates. Exact duplicate detection remains necessary;
semantic overlap needs evidence and review before consolidation.

## Verification

Three permanent benign archives display SQL strings without executing them:
`sql-row-writes.zip`, `sql-row-deletions.zip`, `sql-schema-deletions.zip`.
All six archive/member comparisons retain identical finding sets and criticalities
modulo the migration map, and identical scores of 2. Each control requires its
own operation home and excludes the other two; none emits suspicious or hostile
findings. Permanent fixture expectations enforce the operation boundaries.

All **1,691/1,691 fixtures pass** with soft validation. Strict `make validate`
exits 2 because **173 directories still exceed 85 rules**. The inventory has
**zero mixed rule directories**. SQL falls from 78 to **65** rules; row writes
contain **6**, row deletion **7**, schema deletion **4**, and MySQL **31**.
All 31 ledger after-definitions match the current YAML.

Logs: `/tmp/taxonomy-sql-operations-{before,after}.json`,
`/tmp/taxonomy-sql-operations-soft.log`,
`/tmp/taxonomy-sql-operations-strict.log`.

This completes the operation cohort, not the database audit or wider migration.

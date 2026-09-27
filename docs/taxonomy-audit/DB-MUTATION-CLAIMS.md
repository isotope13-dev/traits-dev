# Database mutation claims versus names and value evidence

The existing `db/delete/table` leaf did not establish table deletion. Its
`model-truncate-call` predicate matched any PHP static `truncate()` call;
`clear-all-logs-function` matched a symbol name. Their conjunction claimed
telemetry deletion without a database receiver or a relationship between the
observations. A control with unrelated, harmless functions reproduced all three
findings. There were no external consumers of these three IDs.

## Corrections

- Preserve the exact static-call predicate under
  `data/control-flow/dispatch::static-truncate-call`, accurately described as a
  static method call. Its arguments, scope and confidence are unchanged.
- Preserve the `clearAllLogs` symbol observation under
  `metadata/file/string/telemetry::clear-all-logs-symbol`. A name alone does not
  prove an invoked operation or deleted logs.
- Retire the unsupported telemetry-deletion composite and remove the obsolete
  `db/delete/table` leaf.
- Add `db/delete/row::query-builder-truncate-call`, requiring the direct
  `DB::table(...)->truncate()` receiver chain. The [Laravel query-builder
  documentation](https://laravel.com/docs/9.x/queries#delete-statements) describes
  this as removal of table records, distinct from dropping the table object.
  The trait claims call syntax, not proof that execution occurred.
- Move the former plaintext-password-storage composite to
  `db/write/row::password-column-and-assignment`, preserving its conditions.
  A password column, SET assignment and table/update/insert syntax establish
  neither the value assigned nor whether it is plaintext. The hashed-password
  control reproduced the erroneous plaintext claim.

The [five-entry ledger](db-mutations-mapping.json) records three relocations,
one retirement and one new observation. Its effective definitions verify against
current YAML. No criticality demotion was used to conceal a classification error.

The relocated password composite had no exact consumer. Its removal does not
remove a Boolean match from the broader SQL directory: the composite already
requires `sql-set-password-assignment`, which remains there. The known SQL
subtree consumers no longer use that directory as a multi-match threshold;
the prior schema batch made the ADO requirement explicit.

## Validation

Three benign archives exercise unrelated function names, actual query-builder
truncation syntax, and an update that binds a computed hash. All six
archive/member exact-ID checks pass. The unrelated functions retain their
observations without any database-deletion finding. The real truncation syntax
gets its new row-deletion finding. The password update gets the accurately named
assignment observation and no plaintext-storage finding.

Archive scores change from 2 to 3 for the unrelated functions and from 2 to 3 for
query-builder truncation; the password update stays at 4. All are below caps of
10. Score reductions are not the objective of these classification corrections.

**1,686/1,686 fixtures pass.** Strict validation reports only **174 oversized
directories**, with zero mixed rule directories. SQL now contains 78 rules.
Logs: `/tmp/taxonomy-db-mutations-{before,after}.json`,
`/tmp/taxonomy-db-mutations-soft-final.log`,
`/tmp/taxonomy-db-mutations-strict.log`.

## Remaining scope

The new truncation predicate covers the direct query-builder chain. It does not
establish row deletion for arbitrary `SomeModel::truncate()`, aliases or saved
query-builder variables. Those retain their generic method observation until
model/receiver evidence can support the stronger classification. A local class
can also shadow the conventional DB facade name; resolving such identity would
require stronger semantic facts than this call-syntax matcher uses.

SQL DELETE/TRUNCATE/DROP and INSERT/UPDATE observations still require coordinated
operation-specific migration. Deleting row contents and destroying schema
objects must not share a vague table-deletion category. Directory-level consumers
and their broad SQL-based suppressions need particular care before those moves.
This cohort fixes the false boundary exposed during that audit; it does not
complete the SQL or wider taxonomy migration.

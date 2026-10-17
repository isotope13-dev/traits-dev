Source: [Frozen Privilege, Varonis](https://www.varonis.com/blog/remote-code-execution-in-snowflake-managed-postgresql).

The article's screenshots supply a pg_cron job rewrite that creates a
SECURITY DEFINER dynamic-SQL function, an internal pg_read_file binding, and
an archive_command payload. The text specifies rebinding lo_export and
exporting a large object over postgresql.auto.conf. These support static
reconstructions; no exploit was executed against a database.

The feed-3820 scratch testdata/hostile directory contains raw SQL, Python,
and PowerShell client variants. All three fire two hostile traits. Variants
rename functions and roles and quote identifiers/language names. The
PowerShell client targets a remote Linux server: pg_cron is not assumed to
run on Windows. Matchers accept scripts, source, SQL text, ELF, Mach-O and PE
and carry Unix/Windows scope for PostgreSQL SQL semantics; no Snowflake name,
client package, collector filename, or attacker-chosen name gates a verdict.

Neutral SQL observations stay in micro-behaviors/data/db/postgresql.
The cron rule belongs under privilege escalation because it requires a
scheduler identity change plus an arbitrary-SQL definer function and an
execution grant. Its dynamic-SQL matcher cannot cross a statement terminator
after SECURITY DEFINER. The archiver rule belongs under service command
injection because it combines internal file-export binding, large-object
staging, an archiver shell setting, and an auto-config output argument.
Its evidence is bounded co-occurrence; it does not claim a parsed SQL value-flow
proof. It requires the server-mandated postgresql.auto.conf name.

Eight controls live in cleave/tests/fixtures/postgresql-privilege-chain:
ordinary backup/scheduling, internal arithmetic binding, file export without
config overwrite, invoker dynamic SQL, separate restricted-definer and invoker
functions, prose, ordinary database connection configuration, and unrelated
environment access. None fire the hostile rules. Internal file binding and a
standalone cron postgres-identity rewrite remain suspicious observations.

The preexisting Python DATABASE_URL matcher moved from supply-chain harvesting
to os/env/config::python-database-url. The regex and testing exclusion are
preserved; database-client presence no longer downgrades a useful configuration
observation. Its exact consumer and ancestor-selector exclusion were updated.

Saved cleave facts were reviewed for raw SQL text, driver literals, and decoded
content. These samples have no encoded payload layer. No hashes, malicious
package coordinates, or hostile network endpoints were published. The feed's
postgresql.auto.conf indicator is a filename. Empty SHA256, PURLS and ENDPOINTS
files record the absence of indicators in those categories.

To check saved evidence:

```sh
python3 testdata/postgresql-privilege-chain/check_reports.py atomscan-final.jsonl controls-final.jsonl
```

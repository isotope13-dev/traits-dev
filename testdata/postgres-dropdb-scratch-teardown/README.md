# PostgreSQL CLI capability review

Sample: FerrLabs/.github at `62a681d7ed2fb422b2f326e837b8bf0e4cc71947`,
SHA-256 `a0a7ef74a41972ee33e7adeea35961d6ba2a9f116740ee4f0440a4069dc14c7e`.
Verdict: **BENIGN**.

The reusable Rust workflow's integration job is opt-in (`default: false`). It
selects the CI Postgres host, creates
`ci_${GITHUB_RUN_ID}_${GITHUB_RUN_ATTEMPT}_${RANDOM}`, writes that database's name
and URL to `GITHUB_ENV`, runs `cargo test`, and drops the same database on exit
when the name is nonempty. Creation and deletion are separate embedded shell
steps; the cleanup step alone cannot see the creation step's evidence. No
database commands were executed during this review.

The archive immediately preceding this sample,
`022afb4b12b4ac3347b58f559a0b7d9e4cb6ca03`, was fetched with forager from
GitHub codeload, retaining its `.forage.json` in scratch. Comparing member bytes
shows only `.github/FUNDING.yml` changed: `open_collective: ferrlabs` was added.
The Rust workflow is byte-identical.

History traces the first `dropdb` to `01011fe13483f120dd1a98fa6f5d3d17d2ba7f30`
("feat(ci-rust): add DB-backed integration test job"). That commit changes only
the Rust workflow, adding 98 lines for the opt-in job, including both per-run
creation and guarded cleanup. Its predecessor,
`e2a424c455a4fa96d2fc9fddfa8982caa485a415`, was also fetched as a codeload archive;
its scan has no suspicious or hostile findings. This is ordinary test
infrastructure, not an inserted destructive payload. Other inspected execution,
download and credential paths configure build caching, package registries,
release tools, security scanners and authenticated Sonar/GitHub reporting.
The Sonar Python block uses Base64 for HTTP Basic authentication, not payload
obfuscation. Actual callers, runner state and externally fetched action code
are outside the artifact's static evidence.

## Rule correction and consumers

`objectives/impact/destroy/database::postgres-dropdb-command` only required a
generic `dropdb` command with an argument. This proves neither an attacker
objective nor unauthorized destruction; the fixture above demonstrates ordinary
cleanup. Move its unchanged positive matcher and shell/PowerShell/platform scope
to `micro-behaviors/data/db/schema/delete::postgres-dropdb-command`, describe
the command text, assign notable severity, and remove the unsupported T1485
mapping. Keep the operation visible on both test harnesses and standalone drops.
The old testing, command-corpus, Markdown and created-database exclusions are
unnecessary for this neutral claim; creation of any database never proves that
a different dropped database is scratch data.

Add the distinct creation observation
`micro-behaviors/data/db/schema/relational::postgres-createdb-command` at notable
severity. Neither command claims that its arguments resolve or execution succeeds.

Consumer audit: no behavioral composite explicitly references the old ID or its
database/destroy ancestors. The only `objectives/impact/` ancestor consumer is
the `crystalx-rat` exclusion, restricted to Windows PE files of 5–15 MB; it cannot
consume this shell/PowerShell-only matcher. Its effective scope is unchanged, so
no reference rewrite or broadened exclusion is needed. Remaining database
destruction rules and their positive matchers are unchanged.

## Verification

`python3 testdata/postgres-dropdb-scratch-teardown/verify.py <scratch-dir>` tests
the existing benchmark teardown and standalone drop controls, plus unrelated
creation followed by deletion, creation alone, isolated workflow cleanup,
PowerShell, quoted/comment mentions and similarly prefixed command names.
All eight pass. Database creation and deletion remain notable in positive
controls; near misses match neither CLI trait.

Outside this batch, `testdata/hostile/mcp-cluster-delete.{py,js}` retain both
`listener-kill-postgresql-cluster-delete` and
`mcp-session-postgresql-cluster-delete` at suspicious severity.
`testdata/benign/database-command-comments.py` and
`testdata/benign/database-backup-cleanup.py` match neither destruction rule.

Original archive rescans with atomscan, including embedded shell steps:

| Observation | Before | After |
|---|---:|---:|
| Unique hostile traits | 0 | 0 |
| Unique suspicious traits | 1 | 0 |
| Suspicious occurrences (workflow + shell step + archive roll-up) | 3 | 0 |
| Notable occurrences including roll-ups | 1256 | 1262 |
| Classifier verdict | BENIGN | BENIGN |
| Raw ML probability | 0.7163523 | 0.6859945 |
| Rust workflow risk | 48 | 10 |
| Cleanup shell-step risk | 40 | 2 |

Only the old objective ID disappears; all its matched locations retain the
notable deletion trait, and creation gains three occurrences. Every other
existing finding and severity is preserved. No material operation coverage is
lost and no rule/classifier disagreement remains. Atomscan reports that its
feature-spec version 18 predates engine version 21; the verdict is supporting
context, not evidence of intent.

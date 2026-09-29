# Legacy `dropper/execution` taxonomy audit

`dropper/execution` was a historical phase bucket. It mixed activation sinks,
carriers, languages, file formats, concealment, persistence, and family
identity, so the same kind of evidence could appear under several unrelated
children. TAXONOMY.md now treats it as a migration source only.

The final inventory is empty:

| Measure | Result |
|---|---:|
| YAML files remaining | 0 |
| rules remaining | 0 |
| rule-bearing directories remaining | 0 |
| directories over the inclusive 100-rule cap | 0 |

The migration preserved rule bodies and rewrote all consumers. The former
cohorts now use these technique boundaries:

| Former cohort | Canonical destination | Reason |
|---|---|---|
| batch command chains | `dropper/file-exec/command/{batch,shell}` | A shell command is the activation sink; the script carrier is a refinement. |
| ClickFix and browser lures | `dropper/delivery/clickfix/{browser-cache,clipboard,remote-command,shell}` | Human-mediated command delivery is the shared technique; cache, clipboard, and command route remain distinct. |
| WSH/JScript execution | `dropper/file-exec/command/script-host/{download,embedded}` | A script host evaluates or launches command text; source language stays in scope and filenames. |
| remote/fileless response pipelines | `dropper/script-eval/response-pipeline` | The required relationship is a fetched response reaching an interpreter/evaluator. |
| resource and native wrapper stages | `dropper/staging/{native,script}` | These rules establish a carrier or wrapper, with no separate language branch. |
| process-injection profiles | `dropper/process-inject/{hollow,remote-thread}` | Cross-process transfer and hollowing are activation mechanisms. |
| native loader profiles | `dropper/staging/native-loader` | Memory-resident native loader evidence is a carrier mechanism, not a generic execution phase. |
| build-script observations | `metadata/build/toolchain` or the relevant masquerade leaf | Build provenance and output identity are not payload activation. |

The split follows the matcher’s required relationship. A URL, interpreter name,
resource API, encoded blob, or loader-shaped filename remains a neutral
capability unless the rule links it to a sink. No new rule should be added to
`dropper/execution`; use the activation and staging contracts in
[TAXONOMY.md](../../TAXONOMY.md).

The reproducible checker is
[`scripts/audit-dropper-execution.py`](../../scripts/audit-dropper-execution.py).
It handles an empty source tree and writes an empty CSV plus a zero-count
summary, so a future reintroduction is visible in review.

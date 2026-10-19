# otto-sh release review

`otto_sh-0.17.0-py3-none-any.whl` is **BENIGN**. It is Our Trusty Testing
Orchestrator, an asyncio framework and CLI for operating user-configured lab
hosts, running tests, transferring builds and collecting monitoring/coverage
data. SHA-256:
`611b2915fe67176d11910f29a5bebf42806ec7bb1d5fad73a4be647a031ab5ff`.

Fetched the preceding release through the PyPI JSON API at
<https://pypi.org/pypi/otto-sh/0.16.1/json> and downloaded the wheel URL in that
record. Its SHA-256 is
`7b36fa23960908502e88c3a85f3d55523dc133f13ffdcbfae1e05f41787bea73`.
Compared all wheel members and Python source, inspected executable statements
and extracted call/literal facts, and traced the behavior described below.
No sample code was executed.

## Decisive diff and execution paths

Every method in `BashFrame`, including `quiet_history`, `handshake`, `frame`,
`recover`, and `restore_interactive`, has an identical Python AST in 0.16.1
and 0.17.0. The module-level `history_prefix` function is also identical.
The command-frame delta changes registry registration/resolution, validation,
exports and a Zephyr parsing helper; it introduces no new history-erasure
payload. Both releases fire the old suspicious rule when scanned with the
starting ruleset. The queue's detection-free baseline claim therefore cannot
be reproduced for the immediately preceding release. 0.16.0 and 0.15.0 also
already contain `HISTFILE=/dev/null`.

`UnixHost.shell_history` defaults to false to keep machine-generated commands
out of a shared lab account's history. `SessionManager` passes this option to
`ShellSession`, whose first handshake calls `history_prefix`. False selects
`BashFrame.quiet_history`: guarded shell builtins export `HISTFILE=/dev/null`
and disable history recording; a zsh-only clause evaluates the same static
export statement. This is ordinary static shell syntax, not a decoded or
network-supplied program. True returns an empty history prefix. The interactive
login bridge explicitly supplies true and restores terminal echo before the
human handoff. No existing history file is deleted or truncated. Existing
history survives; the code explicitly avoids `HISTSIZE=0` for that reason.
The command session records command output and exit status through sentinel
framing and logging.

The larger release diff adds project/session composition, registries, CLI
configuration and diagnostics, test-completion caching, protocol probes,
monitoring and coverage work. The newly introduced `subprocess.Popen` sites
launch the current virtual environment's `otto` executable with a fixed argv
to refresh test completion after answering TAB; they have locks, time bounds
and cooldowns. They do not fetch or activate an external payload. Remote
execution, privilege wrappers, transfers and tool installation follow explicit
host/project settings and the tool's documented purpose. An AST inventory
found no new hardcoded HTTP destination in Python string constants.

The monitor asset contains bundled React/UI/localization code, module preload
fetches and application requests to same-origin `/api/mode`,
`/api/monitor_sessions` and the configured event stream. The coverage asset is
the report UI and syntax-highlighting code. Inspected the fetch/EventSource
sites and decoded strings: Unicode escapes represent UI/localization and
regex data; the apparent Base64 candidates decode to short non-code strings.
In `command_frame.py`, the decoded strings are a short accidental Base64
candidate and the ANSI escape-strip regex. None supplies a hidden execution
stage. The scanner's flow-limit notices were not treated as proof of safety.

## Trait corrections

The history exception requires executable Python literal evidence for echo-off
readiness framing, command/exit-status sentinels, echo restoration and the
existing notable HISTFILE setting. It is file-scoped and independent of package
name, release, filename or comments. It suppresses only `histfile-devnull`;
the notable setting remains. Two irrelevant suppressors (TypeScript declaration
and YAML rule-catalog contexts outside this rule's script scope) were removed
instead of growing the suppression budget.

The other firing observations were reviewed against their actual source:

| Previous ID | Correction |
| --- | --- |
| `objectives/anti-analysis/sandbox-detect/script::python-sandbox-tool-process-set` | `micro-behaviors/process/debug/tool-markers::python-analysis-tool-name-set`; the sample declares installable `gdbserver`/`strace` tools, rather than testing whether analysts are running them. Moved its owned tool-name atoms/groups with it. |
| `objectives/command-and-control/backdoor/rat/control::python-transfer-helper-import` | `metadata/import/package::python-transfer-helper-import`; use the import view and complete helper names. The former substring matched `self._dry_run_transfer(...)`, an ordinary transfer preview method. |
| `objectives/command-and-control/infrastructure/tracking::sessions-table-sql` | `micro-behaviors/data/db/schema/relational::sessions-table-sql`; this creates the local monitoring sessions table, without C2 evidence. |
| `objectives/persistence/login/shell/profile::python-login-profile-targets` | `micro-behaviors/fs/path/config/shell::python-login-profile-targets`; referenced startup paths establish locations, not durable activation. |
| `objectives/credential-access/financial/credit-card/card-number::mastercard-bin--rx-3` | Replaced with `micro-behaviors/data/string/search::numeric-prefix-22-27-or-51-55`, requiring a complete JS `startsWith` call and exact two-digit argument. The old pattern mislabeled Python's FTP `data.startswith(b"220")`. Removed the redundant prefix wrapper and updated its card-context consumer. |
| `objectives/collection/file-targeting/filter::credential-wildcard-name-filter` | Neutral password-path wildcard observations; source constants exclude Python docstrings, and PE strings retain binary coverage. The sample's `*login*` is docstring emphasis on a parameter. |
| `objectives/discovery/network/scan/port/probe::scan-port` | Word boundaries stop partial matches inside the documented `scan_ports` option. |
| `micro-behaviors/os/env/write::histsize-zero-setting` | `micro-behaviors/os/env/runtime::histsize-zero-setting`; the sample mentions this configuration to explain why it is avoided. It establishes no write. |
| `metadata/import/package::python-importlib-base64-import` | `micro-behaviors/os/module/load::python-importlib-base64-import`; this matcher observes a dynamic module-load call, not a declaration. This also keeps the import directory within its existing budget. |

Exact consumers were rewritten. Ancestor selectors of the former objective
homes intentionally no longer select the newly neutral observations; no broad
neutral directory was substituted into an objective. Neutral tool-name groups
remain notable instead of being mislabeled as incomplete anti-analysis signals.
The wildcard PE matcher retains its original population; source matching and
numeric-prefix matching are intentional precision corrections. No global
directory budget was raised and no new taxonomy leaf was created.

## Verification

`check.py` writes focused controls outside `testdata`, where test-directory
exclusions cannot mask errors, and checks positive and negative trait IDs in
actual atomscan JSON. Controls cover complete framing, missing echo restoration,
comment-only framing, standalone history suppression, real imports versus a
transfer method, neutral schema/path/tool references, exact numeric arguments,
FTP banners, docstring emphasis and actual wildcard literals.

Run with:

```
python3 testdata/otto-version-drift/check.py /absolute/scratch/otto-controls
```

Full-wheel atomscan runs on both 0.16.1 and 0.17.0 report zero hostile and zero
suspicious traits after the corrections. Full source diff, downloaded baseline,
scan output and extracted/decoded facts are retained in the supplied scratch
directory under `otto-*` names. The judgement marker is next to the supplied
0.17.0 wheel. The final required check is `make validate`.

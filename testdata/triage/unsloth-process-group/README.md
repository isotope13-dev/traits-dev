# Unsloth 2026.10.8 process-group review

Verdict: **BENIGN**. This is the Unsloth training/inference library, CLI and
Studio distribution. The flagged shell code manages the lifetime of Studio's
own WSL inference engines. The balance of the traced behavior and release
comparison supports ordinary application maintenance.

## Artifact and release evidence

Both exact releases were fetched with `forager fetch --all-wheels` using
`pkg:pypi/unsloth@2026.10.8` and `pkg:pypi/unsloth@2026.10.7`.

| Release | Wheel SHA-256 |
| --- | --- |
| 2026.10.8 | `12c5d8fb7ba7a9092d880f309d350a3491773e9a86bd8ecedf9056b7676e2ac1` |
| 2026.10.7 | `3ffd1dc001d799eb4ec5a955852f41a3505febb9075504bb2f64a1621c9c7c4e` |

The recovered 2026.10.8 wheel matches the submitted bytes. Downloads,
`.forage.json` provenance, PyPI metadata, full source diff, `cleave facts`
outputs and full atomscan reports are retained under
`/usr/local/var/cyclotron/tmp.noindex/cyclotron-d11fe31e/scratch/version-drift-review`.

The `RUNNER` constant in `studio/backend/core/inference/wsl_host.py` is
identical in both wheels. The file's changes update uv 0.12.19 to 0.13.5,
replace its URL/hash/size, enforce the pinned installed version, and change
an ownership-error message. They add no process killing. The earlier release
also fires the old process-group rule with this checkout, so the supplied
clean-baseline observation does not reproduce under the current rules.

The wider diff adds model/GPU support and rebuilds frontend assets. Relevant
new execution paths include loading the bundled ebook data-preparation helper
on the MLX path, and downloading a SHA-256-pinned Level Zero SDK for Intel
Triton compilation. Added MCP resource Base64 decoding returns text to the
model after checking the requested URI against the server's resource list.
These paths support the application's documented work. The wheel contains
no `.pth`, native executable or Python bytecode members.

## Execution trace

The authenticated engine-install routes require owner authority. Windows
engine installation calls `engine_install._install_wsl`, then
`wsl_host.prepare` and `ensure_distro`. This imports Studio's named WSL
distribution, installs the shell runner with mode 755, and obtains pinned
Ubuntu/uv artifacts through `download`, which verifies SHA-256 before
replacing the destination. WSL enablement invokes the fixed
`wsl.exe --install --no-distribution` command through Windows' `runas` UAC
mechanism. This requests elevation through the normal user consent path.

The runner executes `setsid "$@"` and saves its child PID. A watcher waits
for stdin EOF, sends TERM to that child's process group, waits ten seconds,
and escalates to KILL. After the group leader exits, a second cleanup path
checks for surviving workers and sends TERM followed by KILL. The negative
PID denotes the group started by the runner. No service/security-product
target or reactivation mechanism is required by this code.

`managed_engine._teardown` closes the stdin pipe and waits for shutdown;
fallback cleanup is restricted to the selected engine environment's Python
path. `guest_command` constructs argv for Studio's distro and transfers
selected engine credentials through WSLENV. The parsed Python literal and
extracted shell were inspected directly; the runner is ordinary plaintext,
with no hidden decoding or payload reconstruction.

Machine deployment and operator activity were not supplied. The judgment
concerns these wheel bytes and traced paths. Static inspection does not
establish how an installed instance was configured or used.

## Trait correction and retained coverage

Move `objectives/persistence/system/init/script::process-group-kill` to
`micro-behaviors/process/terminate/command::process-group-kill`, describe the
SIGKILL command, and set it to notable. The matcher establishes a process
termination capability. Persistence and ATT&CK T1489 service disruption are
unsupported by that matcher; the mapping is removed. The pattern, platform,
file scope, confidence and existing exclusions are unchanged.

The three exact init-composite consumers now reference the new ID. Searches
also reviewed ancestor directory selectors: the SQL consumer is C# scoped;
the timing consumers select process termination with independent date/launch
requirements. The wheel comparison confirms that none gains a finding here.
The destination is the existing command-termination leaf. The migration map
and existing untracked-kill/jest-fixture cases use the relocated ID.

`check.py` copies controls into a neutral scratch directory before scanning,
so test-directory exclusions cannot conceal the positive. Six cases pass:
the actual supervisor runner, a contextual init-hunting control, the existing
untracked-group-kill fixture, the existing tracked jest-worker cleanup archive,
a single-PID kill, and a signal-0 group probe. Both hostile init-hunting
composites and the suspicious init-group composite retain their findings.
The synthetic init control verifies consumer preservation, not the sample's
intent. No attack technique is erased.

## Full rescan

Commands used the same local rules, atomscan model v18.18, slow mode and
`--follow=none` before and after. `cleave facts` was run on the original wheel,
the flagged member and the extracted runner. The model reports a schema-v18
compatibility warning against extractor v19; these probabilities are model
outputs rather than verdict evidence.

All 1,971 analyzed files remain present. Only the wheel's aggregate finding
and `wsl_host.py` replace the old suspicious ID with the new notable ID.
Every other trait ID and criticality is unchanged. There are no remaining
suspicious/hostile findings or material detection losses. Classifier levels
remain unchanged across every member; the wheel stays benign (`lvl: -1`),
with probability 0.6051445 before and 0.59632623 after. The flagged member
stays benign, changing from 0.0023596883 to 0.0001843969. There is no remaining
rule/classifier disagreement with the judgment. Compact results are saved in
`comparison.json`.

Reproduce the focused checks:

```sh
python3 testdata/triage/unsloth-process-group/check.py --scratch /path/to/scratch
```

# zlibxjson 8.2 member review

The supplied wheel's conviction is retained. Its stranded `zlibxjson/main.py`
member is independently **MALICIOUS**: the package's sole implemented command
downloads an external Windows executable into APPDATA and launches it without
a console. There is no zlib or JSON implementation, documented installation
interface, or coherent provenance beyond placeholder author/repository fields.
Those facts together tip the judgment; Discord hosting alone does not.

The original wheel SHA-256 is
`a46e553386f6ecd2e1429a77dadbf8074aa31ad7f5ab502342af6c06162b37d4`.
The member SHA-256 is
`962b6e6e1e4de055943db28e786b56e16df1ed066716e6d921d7338f34552bcb`.
Both hashes were verified, including byte equality between the supplied member
and the original wheel entry. No specimen was executed.

## Execution trace

1. The console entry point `zlibxjson_command` invokes `zlibxjson.main:init`.
   Importing the package exports `init` but does not invoke it.
2. `init` reads APPDATA and passes that directory and a fixed Discord attachment
   EXE URL to `download_file`. Without APPDATA it only prints a diagnostic.
3. The helper creates the directory if missing, joins it with the URL basename,
   and strips the query before choosing the saved filename.
4. `requests.get(stream=True)` supplies the response. After `raise_for_status`,
   `iter_content` chunks are written to that same path in binary write mode.
5. The returned path flows to `run_silently`, then to `subprocess.Popen` with
   `shell=True` and `creationflags=subprocess.CREATE_NO_WINDOW`. Launch
   exceptions are printed. There is no download verification beyond HTTP status.

Source and `cleave facts` reveal no obfuscation or decoded additional stage,
persistence, credential access, exfiltration, privilege escalation, or cleanup.
The downstream EXE and original deployment circumstances remain unknown.
Forager returned HTTP 404 for the exact attachment URL. The required
`forager fetch --all-wheels pkg:pypi/zlibxjson@8.2` also failed: registry 404,
then an unavailable Chromium ICU-data fallback. The original supplied wheel
was available throughout; no reconstruction was substituted.

## Trait correction and preservation

Moved `pkginfo-single-word-summary` from `metadata/package/ecosystem` to
`metadata/package/description/length`. It measures a declared summary's
1–30-character ASCII token, not ecosystem identity. The entire atomic
definition, effective type/platform scope, severity, and confidence are equal.
The other eleven definitions in the source file are unchanged.

Updated all four exact consumers and preserved the moved observation in both
Steam rules' former ecosystem-directory exclusions. Audited source and target
ancestor selectors; no destination-description directory consumers gained a
new alternative. No matchers or attack severities were weakened.

Existing ten `testdata/stranded-review/run_cases.py` cases passed, including
renamed helpers and wrong output/return/execution or visible-launch controls.
Before/after scans of the existing first-release metadata positive, two
multiword-summary near misses, and the external UNKNOWN-summary archive
`pypi-testingbrooasqa-blankobf-placeholder-stealer.tar.gz` retained all findings
after normalizing the moved ID (fourteen analyzed units).

## Scan comparison and limitations

Controlled Atomscan scans used local analysis, no refresh, no following, slow
mode, and a pristine HEAD rule snapshot versus the edited tree. An initial
standalone diagnostic returned extra derived findings; fresh baseline and
after scans agree, so that difference is not a rule-induced coverage loss.

| Unit | Hostile before/after | Suspicious before/after | Notable before/after |
|---|---|---|---|
| Extracted main.py | 0 / 0 | 2 / 2 | 25 / 25 |
| Wheel | 0 / 0 | 2 / 2 | 31 / 31 |
| Embedded main.py | 0 / 0 | 2 / 2 | 25 / 25 |
| METADATA | 0 / 0 | 0 / 0 | 3 / 3 |
| entry_points.txt | 0 / 0 | 0 / 0 | 3 / 3 |

There are no material detection losses. The metadata observation changes ID
only. Both member and wheel retain probability 0.99525124, calibrated FP level
5000, confidence 54: a weak alert despite the manual malicious judgment.
The scanner reports feature-spec v18 versus expected v21 and
`flow-query-incomplete` on the Python member; source tracing resolves this
member's execution path independently.

The 3–5 hostile-trait goal is unmet. Reviewed the linked stream/file/return/
execution query, APPDATA staging query, executable-hosting context, console
entry point, and package declarations. The implemented behavior is one
download/launch chain; ordinary installers can share its general mechanics.
Existing suspicious chain detections and notable staging/execution primitives
are retained. No additional independent hostile outcome is implemented, and
the unrecovered downstream bytes prevent supported detection of later
behavior. A malicious identity alone would not close that gap.

# AppleScript file-operation coverage and member review

The four notable rules cover AppleScript file I/O found in the decoded Installer:
opening with write permission, truncating to zero, assigning an unbounded read,
and writing at EOF. They accept ordinary AppleScript and statements embedded in
an osascript command, including decoded Mach-O text. Identifiers, destinations,
seed values, server names and specimen filenames do not select the detections.
Existing attack matchers and severities are unchanged.

The read belongs under `fs/read/file/handle`: an unbounded read from an already
open handle may begin at its current file mark. It does not prove a whole-file
read from byte zero. Explicit bounded reads and offset arithmetic are negative
controls. Opening for writing does not establish an actual write or truncation;
the other rules independently detect those operations.

`python3 testdata/applescript-file-operations/check.py` scans four controls,
never executes them, and checks 20 presence, absence and severity assertions.
The ordinary local-report and embedded-report controls match all four notable
observations without any suspicious or hostile finding. Reference-only comments,
a bounded read, nonzero truncation expression and EOF offset miss them.
The eight existing three-member controls pass 25 assertions; the native password
lure suite retains its positive, its three benign near misses and the Installer.

## Independent member judgments

**Installer: MALICIOUS.** Both universal Mach-O slices were disassembled. Their
entry paths build a decoded string, obtain its buffer and call `system()`.
The state-XOR loop uses seed 0x11667, multiplier 0x3785, 32-bit multiplication,
and modulus 35999 (derived from the embedded `09:59:59` value). Independently
recovering both 37,077-byte buffers produces identical NUL-terminated commands
and agrees with Cleave's recovered text. Their buffer SHA-256 is
`d5f34825a22b62491186eaa28065b6f539046d333a56199b996526173be22428`.

The command launches AppleScript. Its reachable handlers validate a cached or
phished login password with `dscl . authonly`, copy browser login/cookie and
wallet stores, copy the login Keychain database, collect Notes and selected
Desktop/Documents files, write staged reports, zip the tree with `ditto`, and
POST the archive with curl. They remove the staging tree and ZIP, replace an
installed Ledger Live app with downloaded content, and use the captured password
to install/bootstrap a LaunchDaemon whose command is downloaded. The daemon's
UserName selects the current user; root payload execution is not inferred from
the privileged installation. A nohup fallback is present. File access, upload,
persistence and replacement success were not observed. The recursive upload
retry omits an argument, so successful repeated uploads cannot be assumed.
These linked theft, phishing and persistence paths establish the verdict
independently of the parent archive's conviction or installer branding.

**perl_cmd.pl: MALICIOUS.** DK's small CGI backdoor reads QUERY_STRING, decodes
percent-encoded spaces and semicolons, feeds that same scalar to backticks,
captures stdout and prints its lines into the HTTP response. There is no
in-file authentication or command allowlist. The `/etc/passwd` text is a usage
example, not a fixed file-read action. DAVTest's real `-sendbd` execution path
uploads files from this directory after testing server-side language execution;
its README explicitly documents deploying this member as a backdoor. This is an
operational remote-command payload, despite a legitimate assessment distribution.
Authorization and server-side deployment/access controls are unknown. No
unauthorized deployment is invented. Both hostile findings and the suspicious
request-to-command finding are retained. This short file has no separate loader,
persistence, evasion, cleanup or fixed secret-theft behavior to support a third
distinct hostile detection. Its URL decoding, command execution and returned
output already have accurate detections; adding duplicates would not improve
coverage. No matcher limitation prevents detecting its actual command channel.

**process.py: BENIGN.** The complete Python CLI requires an explicit app package,
checks Frida connectivity, enumerates app components, disables root checks and
TLS pinning through Objection, uses ADB to inspect debug configuration, searches
memory for secret-like strings and lists Keystore entries. It counts memory
matches and records up to 2,000 characters of Keystore output in a local JSON
report. Its inline Frida-script helper is defined but not called by main.
Subprocesses use argv lists; ADB intentionally invokes the device shell.
The target selection, visible assessment sequence and local output tip the
verdict. No deployment authorization is supplied or assumed. The root-check
bypass remains suspicious; pinning bypass, memory search, process creation,
Keystore enumeration and other supported dual-use observations are preserved.
Forager fetched every original wheel for `pkg:pypi/ai-forge-cli@2.1.6` and
recovered the exact supplied wheel SHA-256, corroborating package identity.
The archive's existing conviction is not revisited.

## Scan comparison

| Artifact | Hostile before → after | Suspicious before → after | Alert level |
| --- | ---: | ---: | ---: |
| installer | 7 → 7 | 7 → 9 | 0 |
| perl | 2 → 2 | 1 → 1 | 0 |
| android | 0 → 0 | 1 → 1 | -1 |
| pkg | 7 → 7 | 8 → 10 | 0 |
| deb | 19 → 19 | 7 → 7 | 0 |
| whl | 3 → 3 | 35 → 35 | 25 |


All three members and all three original archives were scanned before and after
with atomscan (`--no-update --follow=none --analyze local --mode slow`). Cleave
facts were collected for all six inputs. The new read observation also activates
two existing suspicious wallet-extension storage/read profiles on the Installer;
inspection of its extension-targeted copy handlers supports that finding.

The initial cached universal-binary scans selected different slices and showed
neutral finding drift. The recorded controlled native comparisons use the same
original HEAD rules versus final rules with `CLEAVE_SKIP_CACHE=1`. Both native
comparisons lose no detections, and all seven original hostile findings remain.
The other archives retain every member finding. Counts and per-unit deltas are
in `review.json`. Classifier alert levels agree with all member judgments and
remain unchanged: 0 for Installer and Perl, -1 for the Android utility. The
model warns that its feature specification is v18 while the engine expects v21;
that independent model limitation does not establish a verdict disagreement.

Raw scans, facts, independently recovered commands, disassembly and Forager
provenance are under the task scratch directory `scratch/stranded-review`.
Only the three member verdict markers are written; parent verdicts are retained.

The marker notes (one line each, preserved verbatim for the commit body) are:

```text
Installer stealer: phishes and exfiltrates; add file operations
DAVTest Perl CGI: query-to-shell backdoor with returned output
Android analyzer: explicit target and local report; retain bypasses
```

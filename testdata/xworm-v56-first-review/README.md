# DLL destruction, slopfix source, and XWorm V5.6

This review follows the bytes, independently of the queue's HOSTILE labels.
No specimen, command from a specimen, or recovered CIL was executed. Baseline
and final `atomscan --no-update --analyze local --mode slow -f json` reports,
`cleave facts` output, extracted source, resolved CIL, and static control reports
are in the task's `scratch/fallout-review`. `review.json` records full paths,
hashes, model results, per-unit changes, and marker lines.

## DLL action: MALICIOUS

`dll-wipe.js` imports `child_process.execSync` and exports a zero-argument
function. Calling it executes `del /F /S /Q C:\Windows\System32\*.dll` with
`shell:true` and discarded streams. An empty catch suppresses failure. This
is indiscriminate system-library destruction with no servicing parameters,
confirmation, repair path, or other functionality. Requiring the module only
exports the function; invocation and sufficient Windows permissions are not
established. Those limitations affect runtime success, not the action's purpose.

All existing detections are accurate and retained. The entire 169-byte program
implements one hostile objective. Its silent execution, recursive deletion,
and error swallowing already have separate supporting observations. Adding
three hostile traits would duplicate that objective; no distinct uncovered
hostile behavior is supported by this source. The existing DLL-action fixture
and its visible-output, logged-error, unrelated-executor, and specific-file
controls retain their exact findings.

## slopfix master source snapshot: BENIGN

The archive contains the Go `github.com/wow-look-at-my/slopfix` project: a
text/repository linter, formatter, LSP, CI action, and Claude Code policy hooks.
The entry point calls `cmd.Execute`; the hook command parses JSON and dispatches
the event to selected guards. `autoallow.Run` parses embedded XML rules and
returns allow/deny responses. PreToolUse only denies; PermissionRequest may
approve permitted commands. The XML's shell/Python examples are parser and
policy tests, not an execution loop. The highest-scoring local member is
`autoallow/rules.xml` (model probability 1.0).

The concrete side effects fit the declared purpose. Repair mode writes selected
repository text and can remove tracked executable files; its writing/writable
checks gate those operations. Git subprocesses inspect source state and fork
scope. `forkscope.fetchRepo` uses the configured GitHub API and supplied token
for repository metadata. The CI action downloads the published linter and runs
`check .`. These are explicit development operations, with no recovered covert
collection, foreign payload, backdoor, or deception. Hook installation context,
operator authorization, and the trustworthiness of future mutable action refs
are unknown; none supplies evidence of compromise in this snapshot.

The local-only scan covers 760 units. The ordinary scan also follows four
successfully fetched GitHub artifacts (one is this identical source archive),
for 2,791 total units. Some references in test data return 404, one Go pseudo
version is unavailable, and the engine reports flow/embedded-source analysis
gaps. Thus this is not a claim that every future or unavailable dependency is
safe. Every analyzed unit has zero hostile/suspicious findings, before and
after; every unit's existing findings and criticalities are unchanged. No
inaccurate dependency trait was identified, so no dependent-package exception
or dependency rule suppression was added. The installed classifier still
flags the archive: a model false positive, not grounds to erase accurate
network, process, permission, or syntax observations.

## XWorm V5.6 client: MALICIOUS

`payloadA.bin` is an unsigned managed Windows executable with a GUI subsystem,
CLR entry token `0x06000026`, and version-resource name `WinServices.exe`.
Resolved CIL establishes these paths despite the randomized type/member names
and numerous junk constant-return methods:

* Entry method M38 decrypts configuration through M291. M291 derives a 32-byte
  key from MD5, including the overlapping copy at offset 15, and decrypts
  Base64 data with Rijndael/AES ECB. The decoded configuration selects a remote
  address alongside loopback, a port, task delimiter, self-copy name, self-copy
  directory, three payment replacement addresses, and Telegram configuration.
  Endpoints and addresses were not contacted or used as detection keys.
* M38 invokes Defender-exclusion setup, self-copy and minute-task/Run-key or
  Startup-shortcut setup, keyboard-hook installation and worker creation.
  Privilege checks affect which persistence path is attempted.
* M64 connects a socket and installs the M73 receive callback. M73 assembles
  length-prefixed messages, then dispatches through M81/M74 to M125. M125
  decrypts and splits task data. M75 encrypts and frames responses and calls
  `BeginSend`. Plugin bytes are loaded and reflectively invoked in M126/M136.
* M125 handles command launch, downloaded file launch, shutdown/restart/logoff,
  threaded incomplete-body HTTP POST flooding, hosts-file read/write, plugin
  storage/removal, keylog-file responses and screen capture. Screen bytes are
  JPEG encoded and returned over the socket. Plugin task names alone do not
  establish additional credential-theft or UAC-bypass implementations.
* The keyboard callback M193 translates keys, records special-key state and
  window titles, and appends to the configured log through StreamWriter.
  `OfflineGet` reads that same log field into a response.
* `NotificationForm.WndProc` M273 handles clipboard updates, tests Bitcoin,
  Ethereum and TRON regexes, skips the configured destination, replaces the
  detected address, and calls M258. Its STA-thread delegate M266 calls
  `Clipboard.SetText`. This implements covert payment redirection.
* M39 constructs a username, OS, CPU/GPU/RAM and group report, appends that
  report to a Telegram `sendMessage` URL, and passes it to WebClient's
  `DownloadString`. This host-reporting operation is newly recorded as notable;
  the generic behavior can also occur in legitimate notification software.

The combination of covert keylogging, remote task execution, Defender
exclusions, and configured wallet substitution establishes malicious purpose.
No authorized deployment, active operator session, successful persistence,
remote plugin content, or successful network exchange is inferred.

The missed clipboard detection resulted from valid CLR #Strings suffix sharing:
the `Clipboard` TypeRef name points into `currentClipboard`, so a byte-level
`fullword` check fails. The rule now accepts a NUL-terminated suffix as well as
its original word form. All regex, clipboard read/write/listener and CIL field
and local-equality requirements remain. The original matching population is
retained, while the existing hostile backdoor-plus-clipper composite now fires.

The new Telegram observation requires both metadata/report vocabulary and CIL
that transfers the same constructed report local into a URL-parts array,
concatenates that array, and invokes the client method. Removing the report
local relation, client call, getter metadata or Telegram text carrier prevents
it from firing. It asserts request construction, not runtime delivery.

## Results and controls

Counts are unique IDs across all analyzed units, including fetched artifacts.

| Sample | Judgment | Hostile before/after | Suspicious before/after | Local model probability before/after; level |
|---|---|---:|---:|---|
| DLL action | MALICIOUS | 1 / 1 | 3 / 3 | 0.98603785 / 0.98603785; -1 |
| slopfix source | BENIGN | 0 / 0 | 0 / 0 | 1.0 / 1.0; 0 |
| XWorm V5.6 | MALICIOUS | 17 / 18 | 3 / 4 | 0.99 / 0.99; 25 |

No finding was removed or weakened in any sample or external positive control.
XWorm gains the suspicious wallet-replacement implementation, its existing
hostile backdoor combination, and the notable Telegram report operation.
All 2,791 archive/dependency units preserve their exact findings and severities.
The local DLL result remains outside the model's calibrated alert grid
(`lvl=-1`, confidence 0) despite its hostile rule and concrete destruction:
a retained classifier miss. The slopfix model false positive also remains.
The scan warns that its v18 feature specification is older than the engine's
v21 expectation. Scores did not determine either judgment or trait severity.

`check.py` performs 39 assertions across 13 static controls: the original PE,
valid standalone and shared-suffix type names, removed write/listener/wallet
patterns, mismatched replacement destination, removed report source/carrier/
client call, unrelated report local, and two independent clipboard controls.
A separate baseline/final comparison of 19 controls retains every previous
finding and criticality, including real XWorm v3 and v7.1 fixtures. The existing
DLL/source suite passes 20 assertions across 15 fixtures.

Judgment marker lines (each copied verbatim):

```
Node DLL destroyer: silent recursive System32 DLL deletion
slopfix source: linter and policy hooks; classifier false positive
XWorm V5.6: RAT and wallet substitution; repair missed clipper
```

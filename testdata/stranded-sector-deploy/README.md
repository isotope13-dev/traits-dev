# Stranded member review: sector writes and deployment placement

All six listed members are **MALICIOUS**, judged individually from source.
The three archive convictions are retained without rejudgment. Supplied
archive and member SHA-256 values were all verified. No specimen was executed.
`cleave facts` and Atomscan were run on all nine supplied paths; scans used
this checkout, slow mode, no rule refresh and no dependency/reference following.

## Execution paths and verdict evidence

* `writer.js` snapshots the entire environment, package submodule version,
  platform, hostname, username and MACs of external IPv4 interfaces. Its
  hex decoder resolves `axios`, `post`, an HTTPS endpoint, `headers`,
  `x-secret-header`, `secret`, and `then`. The exported arrow ignores its
  arguments, POSTs that record, evaluates the reply's `data` field and discards
  rejections. Concealed whole-environment export and remote-source execution
  have no logging/session justification. The supplied extraction lacks the
  `src/package.json` this member requires. Its package entrypoint references
  a missing `.pnpm/httpreslog` writer, and its declared postinstall script is
  missing too. Successful package activation is therefore unproven.
* `v.js` exports a zero-argument action executing forced, recursive, quiet
  deletion of Windows System32 DLLs. It ignores child streams and exceptions.
  This is system destruction with no servicing interface. Windows permissions
  may prevent success; no elevation mechanism is implemented.
* `f.js` opens physical drive zero in writable mode, allocates 512 zero bytes
  and writes them to the same disk handle at position zero. This clears boot
  code and partition-table bytes. It subsequently attempts `bootrec /fixmbr`,
  which does not reconstruct the erased partition table. The fixed disk,
  silent destructive export and swallowed errors tip the malicious verdict.
* `t.js` silently executes both boot-failure-policy suppression and boot
  recovery disablement through BCDEdit. The exported action has no arguments,
  restoration path or configuration interface. That combination supports
  deliberate recovery sabotage rather than an ordinary repair command.
* `p.js` enumerates C:, D:, E: and F: roots, joins each entry to its drive,
  checks the same path for a regular file and overwrites it with an empty
  string in default truncating mode. This destroys arbitrary root-file
  contents. It does not recurse or delete directory entries. Errors are
  swallowed at every level.
* The osinthell entrypoint's `sorgu(userId)` ignores its argument and calls
  a-z actions in order. Earlier `j.js` enters an endless synchronous allocation
  loop, so reaching p/t/v through this entrypoint is not established. Each
  member independently implements its described effect; f occurs before j.
* `zlibxjson/main.py` exposes `init` through the wheel's console script.
  Importing the module does not call it. `init` passes a hardcoded Discord
  EXE URL and APPDATA to its download helper. The helper removes the URL query
  from the basename, streams the HTTP response to a binary file and returns
  that saved path. The next helper passes the returned path to `Popen` with
  `shell=True` and `CREATE_NO_WINDOW`; launch failures are printed. With no
  APPDATA, it only prints a diagnostic. The sole implemented command is an
  external executable loader, despite the zlib/JSON-like package name and
  placeholder provenance. No compression/JSON work or documented installer
  purpose is supplied. This tips the individual malicious judgment. The EXE,
  deployment authorization and successful execution remain unknown. Forager
  returned 404 for the exact payload URL. The required all-wheels attempt
  found PyPI metadata unavailable and failed its browser fallback because
  Chromium ICU data was missing. The supplied original wheel remains intact.

## Trait changes and preservation

* Added notable
  `micro-behaviors/fs/disk/raw::node-physicaldrive-first-sector-zero-write`.
  It binds a writable physical-disk handle, freshly zero-filled sector,
  buffer length and same-handle write at disk position zero in adjacent
  statements. The existing hostile silent destructive action stays intact.
  Ordinary visible disk initialization retains the neutral capability without
  receiving that hostile action. Read-only opens, other handles/buffers,
  nonzero fills, later-sector writes, image files and an intervening handle
  assignment fail the new matcher. The shared fs/ ancestor consumers have
  PE, PowerShell or autorun scopes incompatible with this JS/TS rule.
* Moved `python-cdn-executable-hidden-shell` from
  `objectives/execution/payload/file-exec` to
  `micro-behaviors/process/deploy/file-exec`. Matcher, effective scope,
  mappings, confidence and suspicious severity are unchanged. The composite
  requires an HTTP-file-to-hidden-shell chain alongside a Discord executable
  URL; it does not bind that URL to the downloaded bytes or establish an
  unauthorized/deceptive result. Legitimate updaters can share this pattern.
  No exact YAML consumer or relevant ancestor-directory consumer selects
  either moved membership. Existing regression expectations now name the
  canonical capability ID. No alias or duplicate was left behind.
* Corrected the descriptions of `raise-for-status` and
  `response-stream-python`. The former is a method-name matcher without a
  required Requests receiver; the latter observes streaming syntax rather
  than proving consumed response bytes. Their matchers and scopes are intact.

All analysis units, including every archive member, were compared. There are
**no material attack detection losses or severity reductions**. The only
removed ID is the preserved Python observation under its former placement.
The disk primitive adds one notable finding to f.js and its archive parent.

## Counts and classifier gaps

H/S counts are distinct hostile/suspicious IDs on the root analysis unit;
archive parents inherit member findings. Exact member-by-member differences
and model probabilities are in `comparison.json`.

| Artifact | H before → after | S before → after | Default classifier |
| --- | ---: | ---: | --- |
| writer.js | 6 → 6 | 6 → 6 | suspicious → suspicious |
| v.js | 1 → 1 | 3 → 3 | suspicious → suspicious |
| f.js | 1 → 1 | 1 → 1 | suspicious → suspicious |
| t.js | 1 → 1 | 3 → 3 | suspicious → suspicious |
| p.js | 2 → 2 | 1 → 1 | benign → benign |
| main.py | 0 → 0 | 2 → 2 | benign → benign |
| parser-session archive | 6 → 6 | 6 → 6 | hostile → hostile |
| osinthell archive | 6 → 6 | 10 → 10 | hostile → hostile |
| zlibxjson wheel | 0 → 0 | 2 → 2 | hostile → benign |

The corrected placement exposes a zlibxjson wheel classifier miss: probability
0.9958744 / calibrated FP level 1 becomes 0.99408424 / level 5000. Both
suspicious behaviors remain. main.py remains at level 5000; p.js remains
outside the calibrated alert grid despite two hostile findings. Writer, v,
f and t remain suspicious at level 1750 despite the individual malicious
judgments. The model warns that its v18 feature specification predates v21;
flow facts also report limitations. Manual source tracing resolves the
supplied code, without claiming runtime success. Model repair is outside
the YAML task; inaccurate objective placement was not restored to raise scores.

The 3–5-hostile goal is unmet for p/t/v/f: each implements one distinct
destructive result, already covered by hostile detections and supported
primitives. Inspecting their complete bodies and package call chain revealed
no additional persistence, exfiltration, escalation, cleanup or staged-code
effect. Extra hostile findings would duplicate those results. Writer's six
accurate hostile findings are retained. For zlibxjson, the complete linked
download, APPDATA staging, shell launch and window suppression are covered,
but generalizable static evidence also fits legitimate updaters. No supported
hostile detector can infer the unrecovered executable's downstream actions.
The package-level verdict therefore remains stronger than the shared rules.

## Reproduction and markers

`python3 testdata/stranded-sector-deploy/check.py` passes 13 assertions across
12 cases. Existing boot-sector positive and near-miss specimens are reused;
the two new controls distinguish visible initialization from a changed handle.
`python3 testdata/stranded-review/run_cases.py` passes all 10 existing cases,
including renamed helper/URL positives and unrelated output/return/launch
and visible-process negatives. New fixture expectations also participate in
`make validate`.

Raw before/after Atomscan JSON, facts, Forager failure logs and exact marker
paths are retained under the task scratch directory recorded in `review.json`.
Exactly one MALICIOUS marker is beside each member and original archive.
Its one-line contents, each at most 72 characters, are recorded verbatim:

```text
parser-session writer: covert env export and remote reply execution
osinthell v.js: silently deletes Windows System32 DLLs
osinthell f.js: zeroes boot sector; add raw-write coverage
osinthell t.js: silently disables Windows boot recovery
osinthell p.js: truncates files across Windows drive roots
zlibxjson loader: hidden Discord EXE launch; relocate trait
parser-session archive: confirmed malware; member theft verified
osinthell archive: confirmed malware; destructive members verified
zlibxjson wheel: confirmed malware; hidden EXE loader verified
```

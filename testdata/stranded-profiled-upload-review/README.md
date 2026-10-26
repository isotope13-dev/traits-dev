# Six stranded members

Each listed member is **MALICIOUS**, independently of its archive. Original
SHA-256 hashes were verified. Every member and original archive received
`atomscan --no-update --analyze local --mode slow -f json` and `cleave facts`.
No sample code, destructive command, remote endpoint, or downloaded stage was
executed. Full local evidence is in the task's `scratch/stranded-review`;
`review.json` retains counts, complete finding differences, classifier levels,
hashes, and the six marker notes verbatim.

## Evidence and execution paths

* **Installer, 8202c3887b75:** Universal Mach-O containing the same encrypted
  AppleScript in both architecture slices. Rizin tracing shows ARM64 main
  constructing a string and passing its C string to `system()` at
  `0x1000006b8`. The decoder XORs each input byte with the low state byte,
  updating state with `((state * 0x3785) mod 2^32) mod 35999`, initially
  `0x11667`. Independent decoding from both original constant regions exactly
  agrees with the 37,076-character command exposed by facts. That command
  launches `osascript`, assembles return-joined source and runs it. The script
  validates a cached or newly phished login password using `dscl . authonly`.
  Its fake Installation dialog masks the answer. It copies Chromium/Gecko
  login and cookie stores, Safari cookies, desktop/extension wallets, Keychain
  databases, Notes databases/media, and extension-filtered Desktop/Documents
  files into temporary staging. Notes scripting is an alternate collection
  path. It profiles the host, archives staging with `ditto`, uploads the ZIP
  using curl, and deletes both staging and archive. It also replaces Ledger
  Live from a downloaded ZIP after killing/removing the existing app. Another
  handler fetches command text, inserts it in bash `-c` ProgramArguments,
  installs and bootstraps a system LaunchDaemon using the captured password,
  and falls back to detached `nohup` execution. Password deception, secret
  theft, upload and durable execution establish malicious purpose.
* **writer.js, 419285d369ff:** All source was traced, including every hex
  constant. The export ignores its arguments, POSTs a snapshot of the entire
  process environment, OS platform, hostname, username and external IPv4
  interface MACs using Axios, and evaluates the response's `data`. Promise
  failures are silently discarded. Concealed export and response execution
  contradict a session/logging library's purpose. Its relative manifest
  import resolves to a missing `src/package.json`; the package entrypoint
  also names an absent `.pnpm/httpreslog` writer. These activation defects do
  not make the implemented malicious behavior benign.
* **v.js, 2e5535f938bc:** An exported action calls the real
  `child_process.execSync` with forced, quiet, recursive `del` against
  System32 DLLs, suppressing output and errors. This deliberately deletes OS
  components; it does not prove secure erasure.
* **f.js, 190bbe0e147e:** The exported action opens PhysicalDrive0 read/write,
  allocates 512 zero bytes, writes that same buffer through the disk handle
  at position zero, and closes it. A separate try invokes `bootrec /fixmbr`.
  That command does not undo the zeroed partition-table bytes. Deliberate
  first-sector destruction establishes its purpose.
* **p.js, d6f337222fab:** The export enumerates C/D/E/F roots, joins each entry
  to its root, checks for a regular file and writes an empty string using
  default truncating mode. Nested catches continue after failures. This
  destroys arbitrary drive-root file contents; it does not recurse or encrypt.
* **t.js, 28db8a38c16d:** The export synchronously requests both
  `bootstatuspolicy ignoreallfailures` and `recoveryenabled No` with ignored
  streams and an empty catch. First-command failure skips the second. Paired
  hardcoded recovery sabotage without a maintenance interface establishes
  malicious purpose.

The osinthell entrypoint imports these functions and calls them from `sorgu`.
Import alone does not run them. Its earlier j.js action contains a synchronous
infinite allocation loop, so reaching the later p/t/v actions through that
entrypoint is not established. Invocation, Windows privileges, runtime success,
server responses and replacement-app contents are unknown. The Installer's
upload retry omits one handler argument; successful retries are not assumed.
Outer-package actions are not attributed to the Installer executable.

## Rule correction and controls

The existing `applescript-fingerprint-c2-beacon` rule was limited by its own
`for: [applescript]`, despite detecting behavior recovered from native code.
Rename it to `password-phishing-upload-with-system-profiling` and include
Mach-O and shell carriers. Preserve its required password-phishing file-upload
leg, profiler alternatives, confidence and hostile criticality. Describe the
required evidence as co-occurrence: the matcher does not bind profiler output
to the uploaded bytes or prove a recurring C2 beacon. Correct its mappings
from file collection to system discovery and exfiltration. No endpoint,
campaign label or attacker-chosen filename is added to the matcher.

There are no exact consumers of the old ID. Ancestor consumers were inspected:
the JS/TS, Python and package-manifest rules cannot consume the added Mach-O
scope; the native browser-stealer consumer still requires browser-targeting
evidence and uses the source selector as a single alternative. No threshold
can be newly satisfied by counting this observation twice in the added scope.

`python3 testdata/stranded-profiled-upload-review/check.py` checks four source
controls without executing their contents. The positive matches; ordinary
upload/profiling, profiling alone, and a phishing upload without profiling do
not. Both independently decoded real stages match. An existing out-of-batch
upload control (`reasoned-fallout-20261024/amos-exfil.applescript`) remains
negative for this rule. Native `test-rules` confirms both required roles.

Every implemented destructive outcome in v/f/p/t already has hostile coverage,
plus its supporting execution, delete/write/truncate, raw-disk, boot-policy,
and error/output-handling observations. These exports contain only one main
attack outcome each. No distinct uncovered behavior or matcher limitation
prevents coverage; adding three hostile outcomes per member would invent
behavior or duplicate existing detections. All accurate traits are retained.

## Rescan comparison

H/S count distinct hostile/suspicious trait IDs. Archive rows include inherited
findings; their confirmed convictions are unchanged.

| Artifact | H before → after | S before → after | Calibrated model before → after |
| --- | ---: | ---: | --- |
| Installer member | 17 → 18 | 11 → 11 | malicious → malicious |
| writer.js | 6 → 6 | 6 → 6 | malicious → malicious |
| v.js | 1 → 1 | 3 → 3 | benign → benign |
| f.js | 1 → 1 | 1 → 1 | benign → benign |
| p.js | 2 → 2 | 1 → 1 | benign → benign |
| t.js | 1 → 1 | 3 → 3 | benign → benign |
| macOS archive | 17 → 18 | 12 → 12 | malicious → malicious |
| parser-session archive | 6 → 6 | 6 → 6 | malicious → malicious |
| osinthell archive | 5 → 5 | 10 → 10 | malicious → malicious |

Every archived member was compared. Only the Installer and its ancestor
containers gain the profiling/upload combination. There are no hostile or
suspicious losses. The standalone Installer's initial scan also differs in
lower-severity roll-ups and architecture-specific decoder findings. A
cache-disabled scan with an isolated, unchanged HEAD rules snapshot reproduces
the final report exactly except for the one added hostile ID: no loss or
severity change is attributable to this edit. Both decoder implementations
exist and recover the same executed script.

The four destructive modules retain calibrated model level -1, despite high
raw probabilities and explicit hostile findings. Those benign classifier
verdicts are false negatives. The scanner reports model feature schema v18
versus expected v21; raw probability alone is not the calibrated verdict.
No inaccurate rule or duplicate was added to raise their classifier scores.
The final repository check is `make validate`.

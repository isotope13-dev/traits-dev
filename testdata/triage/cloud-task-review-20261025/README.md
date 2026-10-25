Cloud task agent review, 2026-10-25
=================================

All three supplied sources are judged MALICIOUS from their implemented RAT
behavior: cloud-file tasks activate downloaded .NET code, return execution
results and upload arbitrary local files whose paths arrive over HTTP. They
also write HTTP bytes to task-selected local paths. A cloud token is read from
the environment for authentication; that is not credential theft.

The Python source explicitly identifies itself as a behavioral reconstruction.
It is byte-identical to the repository's named-suffix-tasks.py fixture; the
renamed C# source is identical to renamed.cs. These are source-level specimens,
not recovered BlackX binaries or evidence of a particular intrusion. Research
and authorized remote administration are plausible deployment contexts. The
judgment concerns the functioning remote code/file-control agent an engineer
would investigate on a machine; authorization and actual deployment are not
established. The arbitrary remote file selection and executable task dispatch,
without a local approval or target restriction, tip the behavior judgment.

Source identification and execution paths
----------------------------------------

* 46993b826bef: Python with pythonnet/CLR. Main authenticates a WebClient,
  lists Graph drive root children and dispatches each item every 30 seconds.
  `.module` downloads bytes into Assembly.Load, resolves a type/method,
  invokes it with argv and PUTs its return value. `.collect` downloads a
  local filename, reads its bytes and PUTs them to the drive. `.receive`
  parses JSON and downloads a referenced item to the supplied path.
* 116bbaf9142c: C# CloudTasks with 0X01/03/05 selectors. The first two paths
  execute an HTTP-fetched assembly and upload remotely selected local bytes.
  The third splits a downloaded descriptor to obtain a destination, then
  re-fetches the descriptor URL as bytes and writes those bytes. It does not
  fetch a distinct payload item. An OK status is uploaded after the write.
* 9a4261cc7a2a: the same C# task architecture with renamed selectors and
  entry point. Its write handler correctly uses descriptor element zero as
  the cloud item selector and element one as the local destination.

The sources are cleartext and have no encoded execution stages. Full cleave
facts were inspected, including literals, text/decoded-string views, call
records, flow limitations and empty archive-member lists. Python's flow
producer omits the third elif handler, so a structural call matcher is needed
for the write. C# local-alias flow is limited; adjacent AST statements bind
the downloaded task array to the actual write destination. Analysis is static;
no cloud access or payload execution was needed. Token/account ownership,
downloaded assemblies, initial installation and consent are unknown. No shell
execution, persistence, bootkit, encryption, credential theft or anti-analysis
behavior is inferred from method names or the external report.

The repository's cited [Securelist report](https://securelist.com/uefi-bootkit-blackx/121539/)
was checked. Its user-mode RAT task protocol corroborates the technique, not
the identity or deployment of these reconstructions.

Detection changes and safeguards
-------------------------------

* File exfiltration keeps cloud context, HTTP-delivered assembly invocation
  and a bound remote-path-to-local-bytes-to-upload chain. Hex suffixes no
  longer gate this separate behavior. The original hex task channel remains.
* File-write tasking now requires the established result-returning assembly
  channel and a write capability. The former hex-suffix/download combination
  falsely convicted the ordinary hex-download-only.py handler (one hostile
  before, zero after). The notable write remains. This correction does not
  assert that generic cloud downloads are attacker-controlled.
* C# download coverage adds the line-delimited task-array form while retaining
  the original async JSON form. Fixed destinations, unrelated task arrays and
  intervening array reassignment do not satisfy the new relationship.
* The Python write observation now requires a real syntax-tree call. The old
  text regex matched the inert example in write-docstring.py; the structural
  rule excludes it while retaining the actual code paths and multiline forms.
* The existing Assembly.Load variable-argument regex does not distinguish a
  name string from bytes. Its misleading buffer ID was renamed, with all
  seven YAML consumer files updated. Its matcher, scope and severity are
  unchanged. string-assembly-name.cs is the concrete benign overload control.
  Generic Assembly.Load, GetType and the assembly/reflection co-occurrence
  descriptions also no longer claim a particular overload or proven flow.

The added upload grouping preserves the two existing alternative matchers.
All ancestor directory consumers were inspected (ancestor-consumers.json).
None counts two upload descendants toward a threshold; mutually exclusive
Python/C# arms retain the underlying evidence spans, including proximity.
The write objective has no exact consumers. Existing cloud-task positives and
all nine benign controls were compared before and after. No attack finding
was lost after mapping the renamed neutral ID. All original sample findings
are retained with that same mapping.

Verification
------------

`python3 testdata/triage/cloud-task-review-20261025/check.py` checks 24 cases:
existing attacks, partial attacks, existing benign controls, ordinary cloud
download, bound JSON/line tasks, descriptor re-download, mismatched or
overwritten destinations, inert documentation and the name-string overload.
Fixtures with a removed write path still contain malicious execution/upload
handlers; their assertions exclude only the unsupported write observation.

Atomscan and full cleave facts were run for each original. Local atomscan
was rerun after edits. review.json records identities, hashes, exact additions,
hostile/suspicious counts and classifier probabilities. All verdicts remain
HOSTILE; no rule/classifier disagreement remains for these three. Atomscan
warns that its v18 feature specification predates expected v21, so this result
does not establish model coverage for every current feature. No archive
members or fetched package dependencies are involved. The final command is
`make validate`; its exit status is recorded in the task's tool output.

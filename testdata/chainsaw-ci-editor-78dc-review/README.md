# Chainsaw, CI exploitation, and editor-task first review

Verdicts: **BENIGN** for Chainsaw core and the standalone editor task;
**MALICIOUS** for the CI exploitation workflow. Verdict markers are beside the
three original samples. All fixture commands are analyzed as data, never run.

## Evidence and execution paths

**Chainsaw core**, archive SHA-256
`78dcf094b661574d470f46c567180509314093452c458ce11493e365c8c6aaee`,
is the Go supply-chain enforcement/scanning project, with the action default
updated to v0.22.124. `cmd/chainsaw/main.go` calls `cli.Execute`; the production
scanner matches source and manifest contents rather than executing the submitted
install hooks. `installscripts/detect_test.go` reads the flagged fixture files
with `os.ReadFile`, passes their bytes to `NPM`/`Pip`, and asserts classifications.
`pysource/scan_test.go` and `scriptsource/scan_test.go` similarly pass embedded
Python/PHP/shell programs to analysis functions. Those programs are not startup
hooks of the Go project.

The fixture `eval_encoded_npm/package.json` evaluates `Buffer.from(...,
'base64').toString()`. Decoding its repeated alphabet blocks yields 162 bytes
starting `00 00 00 04 10 41 08 20 82 0c 30 c3`; this is not a hidden executable
JavaScript program. The named manifest even describes its simulation purpose.
`remote_fetch_pip/setup.py` really contains an `os.system(curl ... | bash)`
pipeline and a separate wget subprocess, aimed at `evil.example.com`. Those
capabilities remain visible. Their fixture role is established by the callers,
not inferred from a test filename or a package name. The Go telemetry path is
explicitly consent-gated in `cli/telemetry_runtime.go`; its operational client
supports a disabled mode. No stealing, backdoor, destructive behavior, or
compromised initialization was found in the reviewed paths.

The pinned dependency was obtained independently with forager:
`pkg:github/chain305/chainsaw-core@1c4b6342b7bc94a7a200243d461970e32061d1e4`.
Its recovered tarball has SHA-256
`bc85dd5398edbbbfe910dcd3c3c5fd32f3f9a64b1147b181cbe9d5bcaaa64e3e`;
its `.forage.json` is retained in scratch. This is the pinned earlier source
archive, not a reconstruction of the original archive. The scanner engines,
entry point and flagged install fixtures match the local archive exactly.
A full comparison found 21 changed files and three additions in the newer
archive. The operational changes update release/checksum pins, handle NuGet
sentinel dates, and add a dormant-lookalike warning; the other changes are tests
and documentation. Both source versions have the same benign explanation for
the flagged fixture behavior. Dependency findings were corrected directly;
there is no exception for the dependent package.

**ci-23076207.yml**, SHA-256
`8f73b1e13874e3781731c4926850a25862dc0d837cd6ad88441ebb200c928a37`,
is a manually triggered GitHub Actions exploitation/credential-result collector.
Step 0 maps `uname -m` to a download architecture, tries curl then wget against
an external IP, saves `/tmp/.svc`, and sets executable permissions. This step
prepares an executable; it does not by itself prove C2 or execution.
Step 1 actually invokes it with `ipscan --source random`, a CVE exploit selector,
1,000 workers, multiple ports and an enormous target count. A background loop
sends the last log line every 30 seconds and incrementally reads selected result
files, including credential/token results, into form POST bodies. The offset
advances in 2,000-line chunks; it advances even on a failed POST, so reliable
remote receipt is not established. Step 2 always attempts final 5,000-line
uploads. The process is used for random Internet exploitation and credential
collection, which tips the verdict over a legitimate bounded security test.
The downloaded executable and actual exploit success are not claimed to have
been observed; the workflow bytes establish the attempted hostile operation.
The CVE number is a command argument, not independent proof the vulnerability
exists. There is no persistence or self-deletion in these bytes: killing the
heartbeat child merely stops that background reporting loop.

**tasks.json**, SHA-256
`8a8b65d70e82b88cf5541567d09bab96ff8a371cb941331aedfda408428392bb`,
is a VS Code 2.0 task declaration. Its folder-open task asks a shell to run
`node .github/init.js || bun .github/init.js`; a Windows command override uses
nested try/catch. On a POSIX shell the second interpreter is attempted on a
failure. PowerShell try/catch catches terminating errors and does not guarantee
fallback for every external command's nonzero exit. The referenced script is
absent. These bytes establish a local bootstrap declaration and automatic task
activation, not stealing, a remote loader, or concealment. Actual placement,
workspace trust/automatic-task approval, and the contents of `init.js` are
unknown. On the supplied evidence the likely verdict is BENIGN. No claim is
made that an unknown companion script is safe.

## Trait corrections and retained coverage

`moves.json` lists 32 relocated observations. An independent comparison with
committed definitions verified that every moved matcher, effective file/platform
scope, proximity constraint and existing exception was preserved. Names,
criticalities, ATT&CK/MBC mappings and placement were corrected separately:

- Curl text beside Python setup/process calls does not bind downloaded bytes to
  execution and cannot establish a packaging trojan. The retained neutral
  composite now describes that co-occurrence. The two setup pipeline rules
  retain their process/pipeline evidence at notable criticality.
- Missing repository metadata does not make a named package anonymous, and
  inline Node plus `Buffer.from` is not proof of a hostile encoded program.
  Source conversion names/call text, inline execution, the missing repository
  field, and postinstall eval/conversion text remain observable. The benign
  repeated-byte fixture and an encoded `console.log(1)` control demonstrate
  the unsupported hostile inference. The build-system-trojan umbrella no
  longer promotes the generic npm eval/pipeline branch; its other attack
  branches remain intact.
- The Go environment “probe” matched the literal regex text `\bTRAVIS\b` in
  the scanner's pattern table. VM/CI regex target names are now notable source
  observations, including the sibling pattern and its OR group. Actual
  environment-access consumers keep explicit references to those observations.
- PHP eval/file-get-contents text is a neutral read-to-eval capability. The
  former “PHP URL” alternative also admits `php:` stream wrappers and did not
  prove a remote PHP payload. Both exact patterns remain under script deployment
  with descriptions stating URI/HTTP read text. Their existing attack composites
  and the plugin ancestor consumer use explicit new references.
- `.github` task-script references, interpreter fallback, setup.mjs names and
  agent-directory references are command declarations. Folder-open relationships
  are activation metadata, with co-occurrence wording rather than unsupported
  same-task data flow. A Windows command-override observation was added.
- Public-IP fetching plus hidden-path chmod, even with architecture selection
  and downloader fallback, does not prove a hostile C2 dropper. Both matching
  populations remain suspicious download/permission observations.

The remaining eight archive suspicious rules describe actual test-payload
patterns: TLS-verification disabling, Defender disabling command text, two
Base64-to-shell patterns, chr-list string construction, font-named interpreter
execution (atom and aggregate), and Node execution from asset directories.
They were not suppressed on the strength of the archive's benign verdict.

The old CI exploitation rule did not require random targeting or an exploit
invocation; the old result-upload rule did not require credentials or bind the
uploaded value to a read. They were replaced by distinct hostile detections in
remote exploitation, credential export and beaconing. The exploitation atom
requires actual shell-command argument pairs, excluding comments and echo/printf
text. The upload primitive joins the tail/head chunk variable to the curl form
argument in the same loop body; neither the variable name, payload basename,
endpoint, CVE number nor result-file campaign prefix is fixed to this sample.

Seven nonempty ancestor-selector consumers were inspected. Go-only regex observations
cannot directly satisfy the JavaScript obfuscation consumers. Source conversion
text is deliberately no longer attacker-obfuscation evidence. Neutral download
arming does not supply a C2 identity and no longer acts as such in the broad
family-classification exclusion. The plugin fetch/eval consumer explicitly
retains its two moved PHP alternatives. Exact references in the other consumers
were updated without widening directory selectors.

## Before/after results

Counts below are unique H/S findings on each input aggregate, including inherited
archive/fetched-dependency findings once. `fetch/dependency-verdict` is engine
output: the archive's final nine S findings comprise eight source patterns and
one inherited suspicious dependency result. Detailed changed-member counts are
in `comparison.json`.

| Input | Human verdict | Before H/S | After H/S | Atomscan probability before → after |
|---|---|---:|---:|---:|
| Chainsaw archive | BENIGN | 4/17 | 0/9 | 0.99993265 → 0.95 |
| Pinned dependency in isolation | BENIGN | 4/17 | 0/9 | 0.99993265 → 0.95 |
| CI workflow | MALICIOUS | 4/0 | 3/3 | 0.999941 → 0.9963677 |
| Editor task | BENIGN | 0/3 | 0/0 | 0.9992976 → 0.000060985487 |

The scanner moves from hostile to suspicious for the archive and dependency;
the remaining disagreement with BENIGN is explained by retained fixture
techniques. The workflow remains hostile, with three distinct supported hostile
behaviors, and the editor task becomes benign. The first flagged FP levels
move 0→279 for the archive/dependency, 0→1 for the workflow and 1→-1 for the task.
The older v18 model reports that newer features are absent; no inaccurate rule
was restored to manipulate those scores.

The encoded npm fixture changes **1H/5S → 0H/0S**, the curl/npm fixture
**0H/1S → 0H/0S**, and the pip fixture **1H/1S → 0H/0S**; their concrete source,
encoding, process and command declarations remain notable. The embedded Python
setup test changes **1H/0S → 0H/0S**. CI step 0 changes **2H/0S → 0H/2S**,
step 1 **2H/0S → 3H/1S**, and step 2 **1H/0S → 1H/0S**.

## Checks and limits

Run `python3 testdata/chainsaw-ci-editor-78dc-review/check.py --work-dir <scratch>`.
There are 47 assertions over 15 static controls: positive and renamed attacks,
ordinary CI results, a comment-only exploit selector, fixed targeting, absent
exploitation, a mismatched uploaded variable, no file read, no log field,
harmless encoded execution, a native-build download, local PHP stream input,
Go regex literals and the original editor task.

Existing controls outside this batch retained every concrete hostile finding:
JWT secret export, three shortened/per-OS script-delivery findings, disguised
folder-open execution, two setup download/execute findings, and the Python remote
code loader. The deliberately removed missing-repository conviction on the JWT
fixture is replaced by a neutral declaration; its actual JWT export remains
hostile. No concrete hostile detection was lost in these controls.

The final validation suite exposed one additional affected fixture,
`testdata/hostile/dropper.sh.xz`. Its entire decoded script downloads one file
from a literal IP to a hidden home path, chmods it, and invokes it. The former
second hostile finding came only from IP download plus chmod; it established
neither a C2 channel nor a distinct hostile result. Its hostile count changes
2→1, with the same suspicious arming and notable download/chmod/launch evidence.
The fixture's hostile minimum changes to one and now explicitly requires those
four supported behaviors. The score floor remains 120. No duplicate hostile
rule was added to satisfy the old count, and the script's execution capability
was not removed. This is a correction of an unsupported conviction, not a lost
concrete attack technique.

Original samples and the pinned PURL were scanned before and after; facts were
collected from all originals, the recovered npm fixture and extracted CI shell
steps. Reports, decoding evidence, full logs and forager provenance remain under
`scratch/fallout-review`. The engine reports limited Go value flow, and PURL
following warns about rereading some URL archive members. The recovered local
source was inspected directly, so neither limitation is treated as proof of
benignness. Analysis was static; no fixture hook, scanner executable or downloaded
payload was run. The final repository gate is `make validate`.

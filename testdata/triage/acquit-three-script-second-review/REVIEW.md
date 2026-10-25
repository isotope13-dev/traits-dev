All three supplied scripts are judged MALICIOUS from their source behavior.
These are descriptive identifications, not independently verified package or
malware-family attribution. No registry archive, exact published version,
installation authorization, or deployment context was provided. Comments and
collector-selected filenames were not used as behavioral evidence.

| Artifact | Hostile before/after | Suspicious before/after | Default classifier before/after |
|---|---:|---:|---|
| `947a98165211`, Memos-style Python implant stub | 1 / 1 | 1 / 4 | benign / malicious |
| `fc266418e962`, Telegram PowerShell loader | 4 / 5 | 1 / 1 | malicious / malicious |
| `0377259b2d46`, Telegram Python command/attachment backdoor | 3 / 3 | 1 / 1 | malicious / malicious |

Source review and limits:

* The Memos-style stub calls `_launch_implant` at module scope. That helper
  selects an adjacent platform-specific executable, checks that it exists,
  and launches it with `--daemon`, inherited environment, and discarded output.
  These flags do not prove actual detachment. The executable is not supplied,
  so its language, functionality, and successful execution remain unknown.
  `_harvest_files` reads up to 64 KiB from each listed developer credential,
  token, and SSH-key file into a mapping. `_harvest_env` retains secret-named
  environment values. `_run_signed_tasks` fetches HTTP JSON, Base64-decodes
  each task's field, verifies that exact payload with an Ed25519 key, and
  passes the decoded/split argv to `subprocess.run`. This is direct process
  creation; the code does not request a shell. `_exfiltrate` would JSON-encode
  its argument and send an urllib request body. None of those four routines
  is called in this source. In particular, there is no credential-to-send
  chain or import-time exfiltration. The combined credential collectors,
  signed arbitrary task execution, and import-triggered sidecar launch,
  without an implemented memory-library API, tip the verdict to malicious.
  A signed task runner by itself can be legitimate and is not sufficient for
  the revised hostile composite.
* PowerShell creates the visually spoofed `C:\Windows \SysWOW64` directory,
  copies an adjacent executable there, attempts a Defender path exclusion,
  and writes the executable path to an HKCU Run value. These actions occur
  before its mutex guard. It then polls Telegram updates every 20 seconds,
  resolves document IDs through getFile, saves the response to a local path,
  and starts that same path hidden. The shortened `[Threading.Mutex]` type
  is a valid constructor form; the created flag gates duplicate polling.
  Neither the writable spoofed path nor the exclusion attempt demonstrates
  UAC bypass or successful elevation. Persistence plus defensive exclusions,
  masquerading, and hidden remote payload execution establish the verdict.
* The Python bot registers `analyze_command` as a text handler and `downloader`
  as an attachment handler, then runs PTB polling at module scope. Messages
  prefixed `@@` go through `os.popen`, and their output is replied in chat;
  the `##runexe` branch passes message-derived text directly to Popen.
  The registered downloader resolves Telegram file metadata, fetches bytes,
  saves them under TEMP using the remote document name, and launches that
  same path. No sender/chat allowlist is implemented. The separate requests
  polling function has another document-download/launch path but is never
  called; PTB handlers already establish active dispatch. Arbitrary chat
  execution and attachment activation without an authorization gate tip the
  verdict. Personal remote administration is possible in principle, but no
  opt-in configuration or authorized deployment is present in this artifact.

All supplied artifacts are plain source files: there are no archive members or
embedded executable stages. `cleave facts` yielded no embedded decoded string
payload. Base64/hex here are runtime operations on future task data, not a
recoverable static second stage. The flow adapter reports limitations for the
Python files; the decisive relationships are verified in source and matched
with bounded structural queries rather than invented from missing flow facts.

Corrections and preservation:

* Replaced the import-launch/secret-catalog/HTTP-body hostile supply-chain
  inference with an accurately described suspicious co-occurrence under
  credential access. Its original required evidence did not bind a module
  call to harvesting or harvested data to HTTP, and did not establish
  package trust abuse. Added credential-list-to-open/read/map coverage and
  signed task-field-to-verification/argv coverage. The hostile signed-task
  composite also requires the independent credential collectors; generic
  signed automation is retained at suspicious/notable levels.
* A token literal, an encoded Telegram endpoint, and a token initializer
  calling an arbitrary helper do not establish exfiltration, C2, or decoding.
  Moved them to authentication, service endpoints, and source assignment
  shape respectively, preserving matchers and exclusions. The token and
  endpoint observations remain notable. All exact consumers follow the
  moves, including existing theft and desktop-lockdown composites.
* Moved hardcoded Telegram polling configuration to a notable service
  observation. Replaced the unbound PTB/Popen and requests/Popen hostile
  co-occurrences with registered-handler input-to-execution checks. The
  old requests-plus-shell derived rule added no operation beyond its two
  retained canonical legs and falsely suggested data flow; it is consolidated
  into those legs. No shell or polling capability was removed. New document
  task coverage requires actual HTTP-response-to-writer data, matching file
  handle and matching launched path, plus the demonstrated remote shell.
* Extended the existing assigned Run-key matcher to allow a contiguous series
  of directory/copy/Defender setup commands without allowing intervening
  variable assignments. The original adjacent-statement alternative remains
  unchanged. This activates the existing hostile persistence composite; no
  duplicate persistence rule is added. Recognizes the shortened mutex type.
* The environment-prefix exception previously treated a dynamic secret-hint
  tuple as an application namespace and could suppress real harvesting.
  It now requires a positive literal prefix and includes that prefix in its
  evidence so secret-prefix exclusions actually work. Literal application
  namespaces are retained; secret tuples no longer become benign context.
* Moved the existing public-key verify operation into `crypto/verify` and
  added receiver-proven Ed25519 verification. RSA consumers and their positive
  fixture remain covered. Provider secret-name references moved out of
  credential-access objectives. Three native credential-like identifier
  matchers and their grouping composite moved from environment names to
  authentication secret references: none of those three matchers requires
  environment access. Their scopes, matchers, exclusions and criticalities
  are unchanged, and their credential-harvest consumer follows the move.

Shared consumer review includes exact IDs and ancestor selectors. The two
ancestor C2-channel consumers are JavaScript-only and do not inherit or lose
these Python-only members. Existing positive RSA and desktop-lockdown fixtures
outside this batch remain detected. Existing concealed PowerShell document
execution remains detected, while visible-launch, different-path and
fetch-only controls retain their near-miss behavior. Authentication identifier
exclusions retain the SDK/error-constant near misses.

No material supported attack coverage is lost. Removed hostile claims are
unproven source-to-sink relationships, and the accurate primitives remain.
The Memos sample has one hostile finding rather than the target 3–5: credential
collection, HTTP body construction, and signed task execution are covered, but
the source provides no collection-to-send invocation, bundled agent bytes,
persistence, or evasion chain to justify additional hostile findings. The
local may-flow adapter cannot manufacture the absent calls. We did not
reinstate false exfiltration/supply-chain claims or add duplicate traits.

The overall classifier now flags all three. Its broad `az` route still emits
class 0 for the first two while the applicable script/type routes emit class
2; this route disagreement remains in the saved comparison. The scanner also
warns that its v18 feature specification predates v21. Raw probability changes
are recorded in `review.json`; neither probabilities nor labels determine the
behavioral verdicts.

Run `python3 testdata/triage/acquit-three-script-second-review/check.py --samples
/path/to/samples` with the original artifacts available. The 31 controls parse
specimens and generated variants only; they never import or execute them.

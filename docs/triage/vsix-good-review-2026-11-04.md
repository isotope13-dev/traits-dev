# VSIX mislabeled-good review, 2026-11-04

`03b3ff18820f` is SAP Mobile Development Kit Editor. Its active commands
cover application builds, deployment, and service synchronization, including
prompted service credentials. The local no-follow scan examined 25,392
members and reports OData, workspace, and process-launch observations without
suspicious or hostile traits. Endpoint ruling: good; validation passed and Hopper confirmed the label (no-op).

`86a8f033af84` is an AI novel-writing assistant with bundled model-runtime
libraries. It connects to configured model providers and batches telemetry to
its service when both VS Code telemetry and the extension setting are enabled.
The fresh local no-follow scan reports the model-provider, telemetry-route, and
VS Code machine-ID observations and no suspicious or hostile traits. Endpoint
ruling: good; validation passed and Hopper confirmed the label (no-op).

`7fdf8ef71c3c` is a Sourcegraph Cody testing extension. It exposes coding
assistant commands, accesses workspace content, integrates model providers,
and can launch local processes. The fresh local no-follow scan reports those
capabilities and no suspicious or hostile traits. Endpoint ruling: good;
validation passed and Hopper confirmed the label (no-op).

`cb989c6d6813` is SiFli SDK CodeKit for building and debugging embedded
projects. It starts debug adapters and terminals and can download development
tools; the scan records those behaviors. The fresh local no-follow scan
examined 2,115 members and reports no suspicious or hostile traits. Endpoint
ruling: good; validation passed and Hopper confirmed the label (no-op).

`7aedda19868b` is Codaro, an editor code-review assistant. It reads workspace
content and constructs edit deltas. A legacy heartbeat sender contains network
code for those deltas but returns unconditionally before reaching it; the
separate compliance reporting path defaults to disabled and reports event
metadata when enabled. The fresh local no-follow scan reports workspace
access and no suspicious or hostile traits. Endpoint ruling: good; validation
passed and Hopper confirmed the label (no-op).

`2af2763767dc` is Spring Boot Tools, an editor extension with a bundled Java
language server and its libraries. The extension launches a language server;
its declared role is Java and Spring configuration assistance. The fresh
local no-follow scan examined 1,783 members and found no suspicious or hostile
traits. The earlier dependency-following scan also inspected a separately
fetched Java extension; that dependency was not part of this artifact. Endpoint
ruling: good; validation passed and Hopper confirmed the label (no-op).

`8cfbfbbbeea5` is Multi, an AI coding assistant. Its extension registers
user-facing task, explain, fix, and approval commands; its bundled providers
include Anthropic and OpenAI integrations and local process-launch support.
The fresh no-follow scan reports those provider and execution observations
and no suspicious or hostile traits. Endpoint ruling: good; validation passed
and Hopper confirmed the good label (no-op).

`4a35030a8b49` is n8n Atom, an editor client for user-configured n8n
servers. Its code sends the configured n8n API key in the n8n header and
uses a localhost proxy for workflow operations; it also verifies its own
license. The fresh no-follow scan reports the n8n extension and API-key
observations and no suspicious or hostile traits. Endpoint ruling: good;
validation passed and Hopper confirmed the good label (no-op).

`27760e37b6af` is the Azure Cosmos DB extension. Its active code uses Azure
identity and Cosmos DB clients and provides database and query-editor operations.
It offers a visible `dotnet tool install` of Cosmos DB Shell, outside the bundled
archive. The fresh local no-follow scan reports Azure identity and process-launch
observations and no suspicious or hostile traits. Endpoint ruling: good;
validation passed and Hopper confirmed the good label (no-op).

`b7ae0e17eaf1` is the Kubernetes extension. Its code manages cluster resources,
uses kubeconfig credentials, invokes Kubernetes tools, and supports configured
authentication commands. The fresh local no-follow scan reports Kubernetes
configuration and process-launch observations and no suspicious or hostile
traits. Endpoint ruling: good; validation passed and Hopper confirmed the good
label (no-op).

`ff28d3093bf1` (Exegol Studio) is an offensive-security agent framework. Its
bundled executable code registers a shell-command tool, passes agent commands
to an executor, and spawns an interactive shell in an Exegol container. It
also registers a kill-chain graph tool and makes a bundled attack-reference
corpus available to the agent. The corpus is documentation; the ruling rests
on the implemented attack-agent framework, not those documents alone or the
operator's authorization. Two new hostile observations in separate directories
report the command-runner and framework identity. The original archive matches
both hostile traits; removing the command
handoff or offensive-context clue prevents them from matching. Validation
passed, Hopper confirmed the bad label (no-op), and the hash-verified snapshot
was moved to `/tmp/triage/misplaced-bad`.

`88d0de9d0b74` (The Stratus) synchronizes files to user-configured cloud and
SSH destinations. The archive also contains four standalone Expect scripts
for inspecting a remote server; each embeds an SSH password. No references to
those script filenames were found elsewhere in the archive. A new suspicious
observation requires the Expect shebang and the literal-password, SSH, and
password-send sequence; it does not assert the credential is valid. The
controls without any one of the shebang, literal, SSH invocation, or send
sequence do not match. The commands perform remote server diagnostics; the
full no-follow archive scan reports this one suspicious observation and no
hostile traits. Endpoint ruling: good, with the packaged credential noted;
validation passed and Hopper confirmed the good label (no-op).

`4f0403aa9eb0` is Saropa Log Capture. It records debug-session output and
provides viewing, import, and sharing features; its network-capable code
includes user-facing Gist and webhook integrations. The no-follow archive scan
examined 1,831 entries and reported no suspicious or hostile findings. The
endpoint ruling is good; validation passed and Hopper confirmed the existing
label (no-op).

`86582c7c28c7` (Infracost) bundles a Go Mach-O language server and editor
extension for Terraform cost estimation. Its bundled source map and executable
were reviewed: the service references and authentication support that role.
A new notable observation requires both an Infracost LSP Go module reference
and its pricing API hostname in the executable's relevant sections. The actual
binary matches; copies missing either marker do not. A slow, local, no-follow
VSIX scan reports the observation and no suspicious or hostile findings. The
endpoint ruling is good; `make validate` passed and Hopper confirmed the
existing good label (no-op).

`3bcadf119ed2` (AntiKnife) manages Google account tokens and redirects the
editor's Cloud Code endpoint through a local daemon. The bundled entry point
spawns that daemon and configures the local proxy; its README describes account
rotation and an optional remote team mode. The VSIX contains two distinct Go
executables, including a newer core, and the latter references Google OAuth,
Cloud Code and a vendor API. The extension uses the newer core; both binaries
were included in the archive scan.
On startup the extension reads the IDE's OAuth token information and passes
access and refresh token fields to the loopback daemon's `importIdeAccount`
request. A new notable observation records the OAuth and account-import clues;
it appears in the no-follow VSIX scan. Controls removing both OAuth markers or
the import call do not match. Static inspection of the Go import handler shows
a local-mode check, calls to encrypted database storage, and Google account
operations; its direct calls do not include the remote token-upload client.
The remote upload client is called by admin handlers, and the bundled admin UI
invokes the local-token upload handler on an upload-button click. This supports
a good endpoint ruling; validation passed and Hopper confirmed the good label
(no-op).

`ca4dd0641078` is a LaTeX graphics helper. Its JavaScript handles selected
PDF, image, and Draw.io files, and invokes configured local conversion tools
with `execFile` argument arrays. A slow no-follow archive scan examined 2,170
members and found no suspicious or hostile traits. The endpoint ruling is good;
validation passed and Hopper confirmed the good label (no-op).

`0a683b54ec13` is a developer HUD for a local MCP server. On activation, if
`uv --version` fails, its JavaScript runs the uv installer's HTTPS response
through a shell after showing an informational message. It later starts a
configured or workspace MCP server, or falls back to `uv tool run visor-mcp`.
These network and process behaviors are material operational risks, and the
scan reports the curl-to-shell execution as a notable trait. The extension's
own code and bundled UI were reviewed, and a no-follow scan of 1,732 members
has no suspicious or hostile findings. Endpoint ruling: good; validation passed
and Hopper confirmed the good label (no-op).

`82f054674f86` is a GitHub-based chat extension. On sign-in it requests
GitHub OAuth scopes including `repo`, stores the token in VS Code secret
storage, and posts that GitHub token to the extension's configured service.
Its uninstall hook also sends an identifier derived by hashing hostname and
username; the raw values are not sent by that hook. The archive rescan reports
one suspicious finding for the GitHub-token POST and a separate notable
uninstall fingerprint observation. Controls removing the relevant token field,
POST, hash update, or request write do not match their respective rules.
The reviewed code implements the described chat and account-linking features;
the endpoint ruling is good with the credential-transfer finding. Validation
passed and Hopper confirmed the good label (no-op).

`57427878c7a3` is a coding assistant that reads workspace context and offers
agent actions. It stores its API key in VS Code secret storage, but its account
profile check puts that key in a URL query before calling `fetch`; URL logging
can expose it. A new suspicious observation describes the adjacent URL and
fetch clues. The actual source and compiled code match, while controls without
the key query or fetch call do not. The no-follow scan of 2,579 members reports
that one suspicious finding. A synthetic notable branding fixture contained the
same unrelated key query; its query was redacted to preserve its intended
branding test without suppressing the real finding. Endpoint ruling: good
with this unusual security finding; validation passed and Hopper confirmed the
good label (no-op).

The initial pool contained 40 archives. A slow local Atomscan directory scan
finished with 40 JSON records at `/var/tmp/vsix-good-scan.jsonl` (exit 2,
indicating severe findings). It began before the rule changes below, so the
records are preliminary. Thirty-four archives have since been confirmed good and three confirmed bad;
the other three still require endpoint-based review.

* `72b2b5ac83ca`: Python autopep8 extension with five ZIP members. Its active
  handler concatenates the editor filename into a shell command without quoting.
  This is an ordinary formatter extension with a command-injection weakness.
  A linked-source-and-sink finding now reports that risk. The rescan reports
  this one suspicious finding; Hopper confirmed the good label (no-op).
* `20c6cba50f6e`: Lua Debug contains a macOS x64 executable whose bytes have
  a LuaJIT version banner, bytecode preload format, and LuaJIT command-line
  help. The generic AMOS cipher-variant heuristic falsely matched this member.
  A Mach-O LuaJIT CLI identity now guards that heuristic; the individual member
  rescan no longer reports it. The extension also attaches to selected Lua
  processes through GDB, LLDB, or a platform helper and loads its debugger
  library. A new notable observation reports the debugger-attach, spawn, and
  `dlopen` clues together; controls without the attach or load clue do not
  match. This is consistent with the debugger's purpose. A full no-follow scan
  reports the new observation and no suspicious or hostile traits. Validation
  passed, and Hopper confirmed the good label (no-op).
* `37970fc037c9`: Batchitt is a chat extension whose webview authenticates with
  a service-issued key and communicates with its own chat service. The key is
  inserted into the login URL path, an unusual security-relevant choice that can
  expose it in URL logs. The former finding inferred capture from unrelated
  co-occurring signals; it was replaced by neutral co-occurrence observations
  and a separate linked-input-to-URL finding. The full archive rescan reported
  that single suspicious finding. Endpoint ruling: good; Hopper confirmed the
  existing good label (no-op).
* `4331210f8b4d` and `6a289d3d93fc`: RTL Cursor versions 1.0.11 and 1.0.13
  patch the editor to enable right-to-left rendering. When enabled, they install
  a per-user Run-key watcher to reapply the local patch and remove it on disable.
  Their shipped code was inspected for network and command execution; the
  watcher is local. Both now report the Run-key write and one suspicious hidden
  PowerShell policy-bypass launch. The latter was previously missed in 1.0.11
  because whitespace exceeded the proximity limit. Ruling: good, with one
  unusual finding each; Hopper confirmed the existing labels (two no-ops).
* `5809dcfcdfcb`: terminal-failure sound extension. Its Windows playback path
  starts a hidden PowerShell process with execution-policy bypass and sends a
  Base64-encoded bundled WAV to a sound player; the encoding is audio data.
  Its shipped code has no observed remote transfer. The hidden-process rule
  now handles the bundler's `(0, x.spawn)` wrapper and `windowsHide: !0`; the
  archive rescan reports this one suspicious finding. Ruling: good; Hopper
  confirmed the existing label (no-op).

Five Vibrancy Continued versions (`c524af5a2ffb`, `37d206f0a8f8`,
`3628df0fcdcb`, `8476c183b87c`, and `89304290d276`) install visual changes
by modifying editor resources. Their uninstall hook launches a hidden
PowerShell cleanup script, explaining the existing suspicious finding. Their
HTML transform adds a named Trusted Types policy to the workbench CSP; a new
notable observation reports the CSP reference alongside the text replacement.
The extension code and native source were inspected, and both architectures
of the native binaries import only `KERNEL32.dll` directly. The 1.1.86 release
also creates a writable NixOS editor mirror and desktop entry. These are
good rulings. Slow local Atomscan rescans with
reference following disabled report the CSP observation and one suspicious
hidden-PowerShell finding for each, with no hostile traits. The CSP observation
also matches all five actual transform files and rejects controls missing the
CSP reference or the trusted-types replacement. A current `make validate`
run first found a duplicate reward-claim matcher; its sole consumer now uses
the canonical natural-language matcher. After rebuilding the scanner against
the current source, `make validate` passed and Hopper confirmed the five good
labels (five no-ops).
* `b2efc28a78a4`: Commit Defender installs a repository pre-commit hook, reads
  staged diffs and sends review content to a configured AI provider. Its hook
  installer asks before replacing an existing hook and stores its configuration
  with owner-only file mode. The new staged-diff helper finding complements
  existing hook and HTTP findings. The archive rescan has no suspicious or
  hostile findings. Endpoint ruling: good; Hopper confirmed the existing label
  (no-op).

A fresh no-follow scan of `af55e4111d3d` (CodeGPT) found implemented
Cloudflare challenge clicking in its browser-automation code. Its other
reported prompt-extraction and repository-directive findings originate in
protective instructions forbidding disclosure of the system prompt and
describing tool-name presentation. The time-related finding came from an
unrelated timing measurement followed by a `Function` call for Readability.
The timing and prompt detectors were narrowed at their matching clauses.
Positive, mixed-file, and real-source controls pass. A fresh full no-follow
scan reports only the challenge-clicking observation as suspicious; endpoint
ruling: good, with that behavior noted. Validation passed and Hopper confirmed
the label (no-op).

The initial scan also flagged `d504a4d979ac` (Kombai) and `af55e4111d3d`
(CodeGPT) for several behaviors, including fingerprinting or browser/automation
clues. Kombai's entry point attaches the output of `getFootprintV2` to client
context sent to its own authenticated WebSocket and uses the same helper in an
HTTP header. Static decoding of this archive's own obfuscated runtime shows
machine and editor/session identifiers, process context, and a persisted random
ID. The reviewed fingerprint does not collect passwords or workspace files.
A hostile exfiltration claim based only on fingerprint, lazy loading,
VS Code and socket/header references was relocated to capability observations
that state co-occurrence. The runtime retains one suspicious obfuscation
finding. An unrelated iOS version parser and script loader were 250 KB apart
on the same minified line, so their proximity rule now also bounds byte
distance; nearby and separated controls respectively match and reject.
The fresh archive scan reports no hostile traits and one suspicious trait.
Endpoint ruling: good, with the fingerprint and obfuscation noted; validation
passed and Hopper confirmed the good label (no-op). The scan
also fetched npm `optimize` and Google Chrome packages from referenced URLs
(`rel: fetched`); they are not necessarily bytes bundled in the VSIX and must
not be attributed to it without following the reference chain.

`c55411fa467b` (Angular Schematics) was flagged as a bundled artifact with an
appended obfuscated line. Its vendor bundle has seven lines, two of them over
1,000 bytes, even though the finding requires at least 30 lines and exactly
one long line. The scanner had copied line metrics from plain embedded code
onto the host, allowing them to combine with unrelated host traits. A focused
scanner regression now passes with those unlocated snippet metrics kept out
of the host. A no-follow scan of the whole VSIX using the rebuilt scanner
clears the appended-payload finding and reports no suspicious or hostile
traits. Its separate entry-point bundle is nevertheless heavily obfuscated;
the scan reports string-table rotation and obfuscation as notable observations.
Static decoding of its rotated string table exposed Angular code-generation and
workspace operations. Its literal service endpoints are license enablement and
verification, a purchase page, and a walkthrough; license enablement submits
the editor machine ID. The reviewed code does not establish credential theft
or a staged executable payload. Endpoint ruling: good; validation passed and
Hopper confirmed the good label (no-op). The scanner does not itself recover
all of the obfuscated license-service behavior.

`3cec32595b0f` (Fitten Code) ships a single 8.4 MB JavaScript bundle beginning
with a rotated string table and heavily mangled identifiers. The initial scan
flags obfuscation, and the manifest lists a separate `FittenTech.fitten-code-local`
extension pack member. Static substitution of the string table exposes code
that enumerates workspace files, stages selected files in a ZIP, and posts
them to a hard-coded HTTP endpoint. The enumeration skips dot-prefixed paths,
ignored paths, and files classified as binary. Its automatic upload entry point calls a
configuration function that unconditionally returns the same value it treats
as off; a separate invocation path has not been established. Other data flows
are still under review. After connecting to its local WebSocket service, the
extension also starts a legacy conversation-state migration that submits the
old state to that service and clears it after a reported successful transfer;
whether that service forwards the content elsewhere has not been established.
Further static substitution and literal folding found no other literal
invocation of the upload command, but remaining computed references prevent
establishing whether the upload class has another entry point. Endpoint ruling:
inconclusive because that invocation path and the separately installed local
service's handling of migrated content remain unresolved. The fresh scan shows
one obfuscation warning; validation passed, Hopper moved the sample to
inconclusive, and the hash-verified snapshot was placed in
`/tmp/triage/misplaced-inconclusive`.

`0b0893983983` (Auto Retry Agent) uses a local Chrome DevTools connection to
inject code that clicks agent approval controls. Its setup can add a remote
debugging port to editor launchers. When the user clicks its session-summary
button, the code collects visible conversation text and logs, redacts a few
specific patterns, and posts the result to its remote summary service. The
button describes a recap but does not itself identify that remote transfer.
The initial scan records the CDP capabilities. A new notable observation reports
co-occurring visible-conversation reader and JSON POST calls, without claiming
that the reader's output reaches the request. It matches the actual source and
rejects controls with either the reader or POST removed. The bundled code and
external destinations were inspected; the recap is requested through a button,
and the implementation is consistent with this automation utility. A slow
local rescan with reference following disabled reports no suspicious or hostile
traits and includes the new observation. After validation passed, Hopper
confirmed the good label (no-op).

`df47457a0b8d` (Oxc) integrates the installed Oxlint and Oxfmt tools with the
editor. Its bundled JavaScript locates and launches local tools and can collect
shell environment settings; no remote transfer was found in that code. The
manifest's preinstall command conditionally downloads an image-named URL to
`icon.png`. A new notable trait identifies curl writing to an image-named file
without claiming the bytes are an image. The full no-follow rescan reports the
new observation and no suspicious or hostile traits. After validation passed,
Hopper confirmed the good label (no-op).

`8752f68614c2` (Protobuf VSC) bundles a language client and server and offers
installation of `protoc`, `buf`, and `grpcurl` from their release sites. The
first two have embedded expected hashes for the listed platforms, while the
`grpcurl` installer logs that hash verification is not implemented. The
extension also references third-party webview scripts. A new notable trait
reports the warning as text rather than inferring that all downloads lack
verification. The real bundle and positive/negative controls matched as
expected; a no-follow Atomscan rescan reports the warning and no suspicious
or hostile traits. After validation passed, Hopper confirmed the good label
(no-op).

Both `bbb21a99269f` (Memory Vault) and `745bc96b9baf` (Quokka) contain the
same `tar-fs/test/fixtures/invalid.tar`: it has symlink `foo -> ../` and a
`foo/bar` file containing `hello`. The adjacent test code extracts it and
asserts an outside `bar` is not written. The JavaScript harness actively sends
the crafted archive to the extractor and checks the outside path, so it is an
executable path-traversal test under the requested PoC policy. Quokka is bad:
its updated scan reports both hostile findings in different directories. After
validation passed, Hopper moved it to bad and its snapshot was moved to
`/tmp/triage/misplaced-bad`. Memory Vault's completed rescan reported the same
two hostile findings; after validation passed, Hopper moved it to bad and its
snapshot was relocated to the same pool.
Quokka additionally has findings in a fetched Twisted package. The scan's
parent chain runs from the bundled `pythonTestWorker.py` to a fetched pytest
wheel, then from its `_pytest/unittest.py` to the fetched Twisted wheel. The
Twisted test bytes are therefore not evidence of a file bundled in the VSIX.

The traversal fixture now has a structural hostile trait for a root symlink
pointing above extraction followed by a file below that link. A second hostile
trait requires the matching `invalid.tar` fixture and JavaScript extraction and
outside-path check within the same archive. A small ZIP containing the actual
bundled fixture and harness produces both findings; safe-link, missing-harness,
wrong-name, unrelated-child, and non-root-link controls do not. The harness
test also includes an earlier unrelated extraction call.

Normal archive scanning initially missed the inline YARA trait even though
`cleave test-rules` matched it. The archive analyzer now evaluates inline YARA
against the original archive bytes; a scanner unit test covers standalone and
nested containers and a YARA-disabled control. The focused traits test and
`make validate` pass. A full Memory Vault rescan ran out of memory during concurrent
builds. A retry grew beyond 75 GiB and was stopped to protect the shared
machine; its `RAYON_NUM_THREADS` setting did not limit this scanner, which uses
`CLEAVE_RAYON_THREADS`. A retry with the correct four-thread setting grew past
35 GiB during member analysis and was stopped; limiting concurrency alone did
not resolve the problem.
An updated atomscan has now been built from a temporary compatibility-adjusted
copy against the scanner fix. Its no-reference-following Quokka scan reports
the hostile payload and test-harness traits in different directories on the
actual VSIX; no other hostile traits were reported in bundled files. The
neighboring scanner checkout's rebase was left untouched.

The cached Memory Vault retry also exceeded the 30 GiB watchdog and was stopped.
An isolated scan of its 3.4 MB bundled `libcrypto-1_1.dll` peaked around
10 GiB. A YARA-disabled scan also peaked around 10 GiB, so YARA alone does not
explain the resource cost. The standalone `cleave facts text` command likewise
peaked around 10 GiB; that view initializes the full filefacts extraction
pipeline, which narrows the investigation to extraction rather than verdict
aggregation. A standalone binform probe recovered 11,237 functions in that
library; their overlapping extents total about 2.2 GB of code walks. Building
call-site facts peaked around 9 GiB while returning 34,773 distinct sites.
A dependency fix deduplicates overlapping sites during the walk while retaining
the richest result at each address. On this library the old and new probes
produced byte-identical records for all 34,773 sites; peak RSS fell from about
8.7 GiB to 27 MiB. The call-site unit tests, including an overlapping-functions
regression, pass. A temporary classifier incorporating the fix completed the
full Memory Vault scan at about 5.4 GiB peak and reports both required hostile
findings on the original VSIX. The dependency fix remains in the separate
binform checkout and was used in the temporary classifier for this scan.

Memory Vault also contains three byte-identical copies of the PyInstaller
executable `memory-vault-fixing.exe` (SHA-256 `e0476df0ef1d111bc7c99d16ce483ead493cde11abe937623213caa7d8922978`).
Its bundled Python 3.11 entry point was extracted and disassembled without
execution. It creates the local `.memoryVault` directory and SQLite note/code
tables, then displays a Windows message box; the entry point contains no network
or process-launch behavior. This does not by itself clear every bundled member.

`test-macho-luajit-identity.py` builds minimal Mach-O objects to verify that all
three runtime identity signals are required. The individual real member was
extracted to `/var/tmp/vsix-luajit-darwin.bin` for inspection and rescan.
The test and `make validate` passed after the guard was added.
`test-vsix-login-evidence.py` checks the independent observations and the
specific input-to-login-URL pattern, including missing-source and missing-sink
negatives. `make validate` passed after those changes.
`test-vscode-filename-shell.py` checks the formatter's filename-to-shell flow
and negative cases using a different source, a different argument, `execFile`,
or an escaped argument. `make validate` passed after that rule was added.
`test-vscode-fingerprint-context.py` checks fingerprint/header/socket evidence
and negatives, and verifies an independently supported concealed-enrollment
exfiltration fixture remains hostile. `make validate` passed after the migration.
`test-node-run-key-command.py` verifies Node `reg add` writes to Run keys and
rejects queries and unrelated keys. `test-node-hidden-powershell.py` binds the
two PowerShell switches to one call, including reversed order and negatives
where switches are split across calls. Both tests and `make validate` passed.
The PowerShell test also covers bundled calls and both `windowsHide: true` and
`windowsHide: !0`, with `!1` as a negative; the focused test and validation pass.
`test-node-staged-diff.py` checks the Git-helper staged-diff call and negative
cases; the focused test and `make validate` passed.

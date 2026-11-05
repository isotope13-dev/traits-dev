# Wheel mislabeled-good review, 2026-11-04

The initial 40-entry queue was scanned locally in slow mode with reference
following disabled; the JSON records are at `/var/tmp/whl-good-initial.jsonl`.
These are preliminary scanner results, not endpoint rulings. Several packages
contain scanner evidence of exploit or reverse-shell functionality and require
particular attention under the endpoint classification policy.
Thirty-nine entries have been reviewed: thirty-one good, six bad, and two dual-use.

`f64028fac5b1` is AIA MCP, a collection of user-started MCP servers. Its
development shell tool accepts a command and working directory and runs the
command through a shell; the other modules expose configured service tools.
The fresh local no-follow scan reports no suspicious or hostile traits.
Endpoint ruling: good; validation passed and Hopper confirmed the label (no-op).

`f7379439c8d5` is ANSH, a desktop assistant with an optional Telegram remote
control. When no chat is paired, it accepts the first `/start` or `/pair`
sender and accepts incoming files before the chat authorization check can
reject them. A new suspicious observation reports those conditions and the
file write. The real source matches; controls without pairing or file write
do not. The fresh no-follow scan reports this single warning. Endpoint ruling:
good with the pairing risk noted; validation passed and Hopper confirmed the
label (no-op).

`31981f706a5a` is NX, a coding-agent CLI. A prior unrestricted-persona
finding matched a conditional instruction not to refuse a project solely
because it is outside the tool's configuration directory; the prompt still
restricts system and secret paths. The detector now considers that sentence
at the match level. The original clears; standalone and mixed-file
unconditional refusal-bypass controls still match. The fresh no-follow scan
reports no suspicious or hostile traits. Endpoint ruling: good; validation
passed and Hopper confirmed the label (no-op).

`80dc0b183ad6` is FlowJet, a general-purpose coding-agent CLI. It uses
configured model providers and a workspace for its file and shell tools.
The fresh local no-follow scan reports no suspicious or hostile traits.
Endpoint ruling: good; validation passed and Hopper confirmed the label (no-op).

`d96ca9567d36` is an Obsidian vault processing pipeline. It uses local process
helpers and configured model services to process and generate vault content.
The fresh local no-follow scan reports no suspicious or hostile traits.
Endpoint ruling: good; validation passed and Hopper confirmed the label (no-op).

`148220e02aa0` is AI Artifact Risk Validator. Its dynamic MCP scanner
constructs traversal payloads aimed at `/etc/passwd`, sends them as parameters
to live MCP tools, and checks their responses for file-content indicators.
That executable exploit test makes the wheel bad under the endpoint policy.
Two new hostile observations in separate directories report the payload
delivery and response confirmation; controls without the payload or tool
call do not match. An unrelated quoted credential-read example and a
confidentiality guardrail no longer trigger the corresponding execution or
prompt-extraction traits; direct and dynamically executed credential reads
still match. The fresh local no-follow scan reports both hostile findings.
Validation passed, Hopper moved the sample from inconclusive to bad, and its
hash-verified snapshot was relocated to `/tmp/triage/misplaced-bad`.

`a06425dd4d76` is the Sibyl Memory CLI, which pairs a user with its
configured service and can invoke pip during an explicit update. The fresh
local no-follow scan reports no suspicious or hostile traits. Endpoint ruling:
good; validation passed and Hopper confirmed the label (no-op).

`194c29f972e1` is the CoAkka logger Python connector with bundled native
logging libraries. Its loader selects a local library and binds its exported
logging API. The fresh local no-follow scan reports no suspicious or hostile
traits. Endpoint ruling: good; validation passed and Hopper confirmed the
label (no-op).

`6f4935b14082` is Cordless, a Discord interactions framework with AWS
Lambda deployment and local development helpers. Its fresh local no-follow
scan reports no suspicious or hostile traits. Endpoint ruling: good;
validation passed and Hopper confirmed the label (no-op).

`96a2c1d38c43` is EnLang, a programming-language interpreter and transpiler.
It translates user-supplied programs to Python and runs or debugs the resulting
code; shell commands and environment access are language capabilities. Its
fresh local no-follow scan reports no suspicious or hostile traits. Endpoint
ruling: good; validation passed and Hopper confirmed the label (no-op).

`8fc2fc1de8c9` is Argus Security, a security-scanning orchestrator. It
combines source, dependency, and container scanning and runs ZAP against
configured web targets. The reviewed code delegates to scanners; no executable
exploit payload was identified in the wheel. Its fresh local no-follow
scan reports scanner and process capabilities with no suspicious or hostile
traits. Endpoint ruling: dual-use as a security scanner; validation passed,
Hopper moved it to dual-use, and its hash-verified snapshot was relocated.

`65a40b857529` is Prism, an LLM usage-observability SDK. Its opted-in
instrumentation can send usage events and a truncated system-prompt hash;
full request/response payload capture is configurable and defaults off. The
fresh local no-follow scan reports its HTTP and model-client observations
without suspicious or hostile traits. Endpoint ruling: good; validation passed and Hopper confirmed the label (no-op).

`d92df0adbcc6` is Collab Runtime, a collaborative file-locking service and
CLI. It starts a localhost dashboard, invokes local Git and process helpers,
and supports a configured shared lock backend. The fresh local no-follow
scan reports process-launch and service observations without suspicious or
hostile traits. Endpoint ruling: good; validation passed and Hopper confirmed the label (no-op).

`a8f4baf7734e` is Mithwire MCP, an interactive browser automation server.
It starts an isolated browser by default and registers a tool that returns
cookies visible to the current browser context. A new suspicious observation
reports that tool; controls without the registration or cookie read do not
match. The fresh no-follow scan reports this one warning and no hostile traits.
Endpoint ruling: good with cookie access noted; validation passed and Hopper
confirmed the label (no-op).

`8b9c82c4d990` is the Aquin training-run client. Its explicit `push` command
uploads a previously packaged run to its configured service; the fresh
no-follow scan reports archive and HTTP upload capabilities with no suspicious
or hostile traits. Endpoint ruling: good; validation passed and Hopper confirmed the label (no-op).

`5b2867c552e2` is Browse Code, an agent bridge between browser chat and a
local command server. The server exposes its key in an unauthenticated ping
response and accepts any nonempty session token; its command endpoint checks
the exposed key. A new suspicious observation reports those combined clues.
The actual source matches; controls without the key response or permissive
session acceptance do not. Browser visibility spoofing was relocated to a
neutral capability because those DOM overrides alone do not prove anti-bot
intent. The fresh no-follow scan reports the bridge warning and no hostile
traits. Endpoint ruling: good with the authentication weakness noted;
validation passed and Hopper confirmed the label (no-op).

`53a7fcc5ec5f` is Flexygent, a general agent framework with local Python and
shell tools. Its shell tool compares only the first word against a blocklist
before running the full command with `shell=True`, so the blocklist is not
a security boundary. A new suspicious observation reports that pattern;
the actual source matches and controls without the blocklist or shell mode
do not. A prior system-prompt-extraction match was a protective instruction
not to reveal it; the corrected rule no longer fires. The fresh wheel scan
reports the one shell warning. Endpoint ruling: good with that weakness noted;
validation passed and Hopper confirmed the label (no-op).

`1337bcc4afd9` is the AKF agent-knowledge library. Its user-invoked install
command writes a Python `.pth` startup hook that instruments LLM SDKs, and
by default installs a background file watcher. A new suspicious observation
reports the startup SDK hook; the original matches, while controls without
the write or import hook do not. The fresh no-follow scan reports this one
suspicious observation. Endpoint ruling: good with the startup hook noted;
validation passed and Hopper confirmed the label (no-op).

`e32f5c1ce90b` is the ProSocks forwarding agent. It registers with a
user-configured panel and starts a SOCKS5 proxy on localhost. Although it
generates and displays a password, the server selects the protocol's
no-authentication method. A new suspicious observation reports that
selection and relay code; the original matches and controls without either
the selection or relay sink do not. Endpoint ruling: dual-use as a networking
forwarder; validation passed, Hopper moved it to dual-use, and the hash-verified
snapshot was moved to `/tmp/triage/misplaced-dual-use`.

`5fdd61924295` is an inert dummy package with a version string and an info
function. The fresh local no-follow scan reports no suspicious or hostile
traits. Endpoint ruling: good; validation passed and Hopper confirmed the label (no-op).

`15b5f4c0f6f0` is a Zebflow CLI bootstrapper. On first invocation it
downloads a platform-specific GitHub release archive, extracts it, marks the
expected binary executable, and launches it. The wheel does not include that
remote binary or perform checksum validation. The fresh local no-follow scan
records the download, archive extraction, executable permission, and process
launch observations with no suspicious or hostile traits. Endpoint ruling:
good for this wrapper; validation passed and Hopper confirmed the label (no-op).

`6307631e2d65` is Evil-Ollama, a scanner and offensive framework. Its
implemented exploit path serves a rogue OCI registry manifest with a
path-traversal digest and sends an Ollama pull request naming that registry.
The RCE branch refers to an uninitialized payload-size variable, and the
claimed file-read outcome is not established by the inspected code; neither
outcome is assumed successful. The endpoint ruling is bad for the implemented
exploit workflow. Two new hostile observations in separate directories
report that workflow and its Evil-Ollama context; the fresh no-follow wheel
scan reports both. Controls without the traversal digest or pull request do not match either
hostile observation. Full validation passed, Hopper moved the sample to bad,
and the hash-verified snapshot was relocated to `/tmp/triage/misplaced-bad`.

`65008e17bddb` is a small requests wrapper that forwards attributes and
provides a JSON GET helper. Its fresh no-follow scan reports no suspicious or
hostile traits. Endpoint ruling: good; validation passed and Hopper confirmed the label (no-op).

`c458fa5e01aa` is a one-file test archive, not an installable wheel. Its
snippet writes an HTTP response to a Python file but leaves the URL undefined
and has no execution call. A suspicious response-to-script observation
accurately describes the available code; no hostile trait matches. Endpoint
ruling: good as an inert fixture; validation passed and Hopper confirmed the
label (no-op).

`1175f6759f57` and `174f9db715f0` are pytapo camera-control library
versions. Both contain the same video-saving method: it formats a caller's
output path into a shell command and passes it to `os.system`. Double quotes
do not make a path containing shell metacharacters safe. A new suspicious
tree-sitter observation ties the function parameter and formatted path to the
same command variable executed by `os.system`. The original code matches;
controls without the input path or execution call do not. Fresh local
no-follow scans report that single suspicious observation for each wheel.
Endpoint ruling: good with the injection risk noted; validation passed and
Hopper confirmed both labels (no-op).

`e08cca244d68` is the generated nominal-api Python client. Its package
contains generated API models and request code with authentication headers;
the fresh local no-follow scan reports those capabilities and no suspicious
or hostile traits. Endpoint ruling: good; validation passed and Hopper confirmed the label (no-op).

`bbf593eb5c6e` and `a4d4de95e770` are Keris Toolkit versions 0.9.0 and
0.10.0. Their identical shell module generates Bash, Python, and PowerShell
reverse shells and performs command-injection confirmation. Their identical
XXE module sends file-disclosure and callback payloads. These are executable
attack implementations; the authorization guard and non-destructive intent
do not change the bad ruling. Fresh no-follow scans of both wheels report
hostile reverse-shell and XXE traits in different directories. `make validate`
passed, Hopper moved both good-to-bad, and their hash-verified snapshots were
relocated to `/tmp/triage/misplaced-bad`.

`0750e2161740` (pipeline-check) has hostile reverse-shell findings in rule
metadata and scanner patterns. The examined `exploit_example` strings are
documentation supplied to a CI scanner, while `_malicious.py` uses regular
expressions to identify hostile build steps. The findings require further
context-sensitive review: a documentation exception must not suppress any
executable exploit or payload elsewhere in the same archive. No ruling yet.

`ddd74950964c` (PyVaultRCE) is a remote code-hosting client. Its `run` method
fetches code, invokes a decryption helper, and calls `exec(compile(...))`
locally on the result. The package includes a shared literal Fernet key, and
the helper falls back to plaintext if decryption is unavailable or fails.
The calls are user-invoked as part of the code-hosting client; the endpoint
ruling is good with a suspicious compiled-execution observation. A separate
notable trait reports the literal-key constructor. Both match the actual code
and reject controls without the relevant inputs or calls; the fresh wheel scan
reports the intended findings and no hostile traits. Validation passed and
Hopper confirmed the good label (no-op).

`d9357e2e1ca3` is an inert security-verification package containing
credential-shaped literals. Its sole function prints a message and returns a
fixed status; the literals are not used or sent. The scan reports the key-shaped
data as notable and has no suspicious or hostile findings. Endpoint ruling:
good; validation passed and Hopper confirmed the label (no-op).

`85e530b18a3c` (gallery-dl) imports browser cookies when the user selects a
browser through an option or configuration, to authenticate downloads. Its
fresh scan reports one suspicious browser-credential-access observation and
no hostile traits. Endpoint ruling: good; validation passed and Hopper
confirmed the label (no-op).

`744060c7c805` is an eMoney MCP client. When an authenticated session is
needed and no saved session works, it attempts to read and decrypt Chrome
cookies whose host contains `emaplan`, saves the selected cookies locally, and
uses them for the eMoney session. The local session file is written with
owner-only permissions where supported. The prior scan raised two overlapping
suspicious observations for that cookie query and decryption. A guarded
downgrade now retains the specific decryption warning while reporting the broad
query at notable when no login-table clues exist. A control adding Login Data
and login-table references preserves the broad suspicious warning. The fresh
wheel scan has one suspicious cookie-decryption finding and no hostile traits.
Endpoint ruling: good; validation passed and Hopper confirmed the label (no-op).

`69dc74f12c76` is a Tovuk deployment CLI wrapper. Unless an override, bundled
binary, or cached binary is available, normal invocation downloads a native
release from GitHub, writes and marks it executable, and replaces the process
with it. The wrapper does not verify a checksum. New notable observations
report the response write and the co-occurring `execv` call; controls without
the response read or process replacement do not match. The no-follow wheel scan
has no suspicious or hostile traits. The remote binary is not in this wheel.
Endpoint ruling for the wrapper: good; validation passed and Hopper confirmed
the label (no-op).

`a6dfb93ccf1c` is a Python debugger, logger, and profiler. It executes a
selected local script, inspects traceback frames, and can send signed reports
to a configurable Socket.IO endpoint, normally localhost. The prior trait
placed a mere `secure_payload`/`emit` text proximity under exfiltration and
asserted signing and Socket.IO; it has been relocated to a neutral syntax
observation. Separate traits report the actual Socket.IO and execution APIs.
The fresh wheel scan has no suspicious or hostile findings. Endpoint ruling:
good; validation passed and Hopper confirmed the label (no-op).

`2c3f29116d20` and `a0288be63d47` are aioconsole versions 0.6.0 and 0.5.1.
Their identical server module exposes an interactive Python console over a
configurable TCP or Unix socket, defaulting TCP to localhost. It is a general
Python development library with an optional user-started remote console; the
ability to misuse that facility does not by itself make the package dual-use
under the endpoint policy. A new suspicious observation identifies the async
server, connection handler, and interactive console clues. Both wheels match;
controls without any one of those clues do not. Validation passed. An initial
dual-use ruling was corrected to good in Hopper, and both hash-verified
snapshots were restored to the review tree.

`2727f68d03e2` (riciplay-cli) contains a callable payload factory with MySQL
file-read injection strings and Jinja command-execution gadgets, plus a harness
that passes generated probes to a target callback. Its authorization gate does
not remove that exploit functionality. New hostile SQL-injection and template-
injection observations both match the original wheel; controls removing each
payload or the parsed generator call reject the respective findings. Endpoint
ruling: bad. Validation passed, Hopper moved it to bad, and its hash-verified
snapshot was relocated to `/tmp/triage/misplaced-bad`.

`46f6e333513c` (lents_adutils) implements an attack-and-defence CTF exploit
orchestrator: an abstract user-provided attack is dispatched across teams and
collected flags are submitted to a configured server. Although its base class
does not include a target-specific exploit, the implemented repeated dispatch
and flag collection make it a dedicated attack framework rather than an inert
helper. New hostile observations report target dispatch and flag submission in
separate directories on the actual wheel. Controls without dispatch, flag
buffering, or submission test those prerequisites. Endpoint ruling: bad;
validation passed, Hopper moved it to bad, and its hash-verified snapshot was
relocated to `/tmp/triage/misplaced-bad`.

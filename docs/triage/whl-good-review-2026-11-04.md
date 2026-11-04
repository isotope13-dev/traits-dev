# Wheel mislabeled-good review, 2026-11-04

The initial 40-entry queue was scanned locally in slow mode with reference
following disabled; the JSON records are at `/var/tmp/whl-good-initial.jsonl`.
These are preliminary scanner results, not endpoint rulings. Several packages
contain scanner evidence of exploit or reverse-shell functionality and require
particular attention under the endpoint classification policy.
Twelve entries have been reviewed: eight good and four bad.

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

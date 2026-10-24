# First reasoned review: DarkCore and Ethereum stage loaders

All three samples are **MALICIOUS**. Judgments follow executable paths and
recovered source templates, independently of the queue labels, filenames,
atomscan scores, and sandbox labels. No sample or fetched payload was executed.
Full hashes, exact per-member changes, classifier probabilities, and marker
lines are in `review.json`. Raw facts, scans, IL, extracted PEs, full resource
sources, and Forager provenance remain in the task's `scratch/fallout-review`.

## Windows sample: 4be93d28a571

This is the DarkCore controller/client builder, not a preconfigured victim
agent. Its CLR entry token is `0x0600002b`; `MyApplication.Main` enters the
Windows Forms application and `OnCreateMainForm` constructs FormClientsList.
`SenderBuilder.Build` (`0x06000d4c`) reads client source resources, applies build
options and renaming, parses the resulting source, and calls the compiler's
`Emit`. In particular it obtains `Sender_CryptoClipperHook` for a client source
unit. The version information, namespaces and PDB path corroborate this identity;
they are not the verdict evidence.

The .NET resource parser initially truncated some multi-byte serialized string
lengths. Recovering all resource strings with .NET 7-bit lengths exposed the full
client paths:

* `CryptoClipperHook.StartClipper` registers a clipboard consumer. The callback
  rejects its own addresses and obeys an optional cooldown, matches a currency
  regex, selects `addresses[pattern.Item1]` through TryGetValue, assigns the
  result to `replacement`, and calls `ClipRelayHub.TrySetText`. Addresses come
  from operator configuration/build placeholders. CommandReceiver implements
  address updates and enable/disable operations. This is payment-address
  replacement, beyond an ordinary clipboard manager.
* Browser collection extracts and decrypts browser stores. The native helper at
  `0x5a2c58` is duplicated at `0xd079f8`. Rizin identifies DuplicateHandle calls
  at VAs `0x140003c50` and `0x140003fc5`, and the browser-handle copy paths.
  In `fcn.1400190e0`, VirtualAllocEx allocates the destination, WriteProcessMemory
  at `0x140019573` copies a DLL path, and QueueUserAPC at `0x14001959a` queues
  LoadLibraryW with that path. Debugger detach resumes the target; a pipe returns
  the helper's output. The Firefox extraction routine calls this machinery and
  reports recovered key material. These are real secret-acquisition/injection
  paths, not conclusions from imports or log messages alone.
* `GhostPersistence.InstallGhost` reads the client executable, stores gzip/Base64
  chunks in HKCU, writes a hidden script launcher, and registers XML containing
  a hidden Windows-script-host action and a logon trigger (also a timer trigger).
  The launch script reconstructs the executable from registry chunks and starts
  the reconstructed path. The template also writes policy Run/Winlogon entries;
  its watchdog restores removed entries. `RemoveGhost` removes the task,
  registry payload/autorun values and staged files. Task-removal and registry/
  filesystem primitives already describe this cleanup; it is not proof that
  cleanup happened on the sandbox machine.
* Keylogging, browser/Discord/wallet harvesting, hidden desktop surveillance,
  Phone Link SMS acquisition, remote shell control and Telegram host reporting
  are implemented in the client templates. Existing supported observations
  remain, including the native helpers and the embedded dual-use components.

The builder's offensive purpose is established by covert collection and
operator-controlled wallet substitution. A legitimate controller UI does not
explain those effects. No victim deployment, operator authorization, active
controller endpoint or successful extraction is established by this artifact.
Those missing facts do not negate the implemented malicious client generation.

## JavaScript: 4323f55072cf and c73752b6cb9e

These are two representations of the same Ethereum dead-drop Node loader. A
QuickJS context with no system/network bindings evaluated only the extracted
string-table function, index decoder and rotation prelude. No module imports,
networking, child launches or payload code ran. Replacing decoder calls exposed
these paths, also readable directly in the decoded copy:

1. `run` queries the Ethereum head and searches transactions from a configured
   sender. It races providers, checks blocks around 1000-block boundaries, uses
   account nonce queries to locate the latest sender transaction, and falls back
   to a Blockscout transaction-list query.
2. `decodeAddress(tx.to)` converts recipient hex to bytes, interpreting the first
   two four-byte ranges as dotted IPv4 addresses. They configure stage/control
   URLs. The ledger therefore supplies controller addresses, not payment logic.
3. The stage fetcher issues HTTP GET and falls back to HEAD. It collects the body
   or reads the Base64 `X-Payload-B64` response header, XORs bytes with a repeating
   key, and converts the recovered bytes to UTF-8 source.
4. The first acquired stage is evaluated and also passed to `node -e`; the second
   is passed to `node -e`. Child options detach the process, ignore its streams,
   hide its Windows console and unref the child. Global/module aliases and the
   resolved controller URLs are prepended to the stage source. The obfuscated
   true-option expressions were evaluated independently and resolve to true.

The decoded copy has a syntax error in `toBlockHex`: `toString] 16` lacks call
parentheses. Whole-file syntax checking confirms it cannot execute unchanged;
the obfuscated copy parses. This is a broken representation of malicious code,
not evidence of a benign program. The verdict does not claim runtime success.
No final remote stage was supplied or fetched, so no credential theft,
persistence, or other downstream payload behavior is attributed to the scripts.
No package manifest or original injection/deployment context was supplied.

## Rule corrections and coverage

* Expanded existing clipboard wrapper atoms to recognize both Clipboard and
  ClipRelay wrappers. The matcher retains the actual consumer registration and
  replacement-text write. Existing map selection and currency validation remain
  required by the hostile clipboard-replacement composite.
* Added a hostile hidden-logon-task template composite requiring that clipper
  context, task-creation options, logon trigger, hidden setting and script-host
  action. XML configuration by itself remains notable.
* Generalized the HTTP/XOR/eval/inline-child loader rule: it requires HTTP-request
  evidence instead of a chosen stage path and no longer gates on particular RPC
  providers. Updated every explicit consumer and suppressor. The blockchain
  rendezvous still separately requires recipient and dotted-byte construction.
* Added concealed detached-child coverage in the loader context. The generic
  detached option remains notable. Moved generic bracket `unref` from encrypted
  staging to neutral handle detachment, preserving its matcher/type/scope and
  updating its consumer. An ordinary background helper is a negative control.
* Removed the hostile Telegram-to-PowerShell dispatch composite: the actual
  Telegram paths only send notifications/host information; the separate shell
  feature does not accept Telegram messages. Its three constituent observations
  remain. There were no consumers of that composite. This does not weaken the
  separately supported TCP remote-control and Telegram host-export findings.
* Moved the two managed GitHub/HTTP hidden-shell composites to neutral execution
  API profiles with the same match conditions. The actual GitHub release path
  belongs to CloudflaredManager's Cloudflared installer. No required evidence
  connected that URL to the hidden PowerShell operation. Inspected and migrated
  all three NuGet consumers too: package role plus that API profile does not
  establish a supply-chain compromise. These observations are retained, rather
  than replaced with a DarkCore or dependency-specific exception.
* Moved the tick-count/CBC/PE/protection profile to neutral memory capabilities
  with the same conditions. A clock import plus crypto/protection APIs and an
  overlay establishes no timing gate or evasion. No consumers selected the old
  rule. Other timing-gate/evasion rules are retained.
* Removed the unsupported anti-debug technique mapping from the debugger loader
  composite, retaining its injection finding and all matching conditions.
  Corrected global-alias obfuscation's mapping from single-instance execution
  (B0024) to obfuscation (B0032).

The removed/relocated claims were inspected against actual code, consumers,
and an independently fetched earlier DarkCore build, SHA-256
`6a1080c515871475ba7a73ba3752ebbbe0296ff938550bf0a3de975351274892`.
Its original bytes were recovered by Forager from Triage and hash-verified;
the artifact and `.forage.json` stay in scratch. The previous reasoned-review
fixture/report was also inspected. Both real builds retain browser key/handle
acquisition and payment-address replacement coverage. No verified attack
technique is removed. No dependent-package exception was used.

## Scan comparison

Counts below deduplicate IDs across all analyzed members/layers. `review.json`
also records outer-file counts and every changed member.

| Sample | Verdict | Hostile before/after | Suspicious before/after | ML before/after |
|---|---|---:|---:|---|
| DarkCore, 17 units | MALICIOUS | 29 / 28 | 38 / 37 | HOSTILE / HOSTILE |
| injected.decoded.js | MALICIOUS | 2 / 3 | 2 / 2 | HOSTILE / HOSTILE |
| injected.pretty.js | MALICIOUS | 2 / 3 | 2 / 2 | HOSTILE / HOSTILE |

DarkCore's outer file changes from 28 hostile/36 suspicious to 27/36. Its two
copies of the native injector each change from 3 hostile/12 suspicious to 3/11,
replacing the unsupported timing-evasion finding with the notable API profile.
Other embedded members lose no findings. The JavaScript stage rule is renamed
and generalized; its old ID disappearing is not an execution-coverage loss.
There is no remaining classifier/verdict disagreement. The installed classifier
warns that it uses v18 features while the engine supports newer features; its
unchanged verdict is reported, not used to validate rule correctness.

`check.py` provides 16 static controls: both real DarkCore builds, current and
legacy clipboard wrappers, removed replacement source/write effects, removed
logon/hidden task settings across ASCII and UTF-16, both original scripts,
changed stage routes, removed eval/hidden-child options, and a benign detached
helper. The complete first 14-control run and the additional persistence checks
are recorded in scratch. None of these controls executes sample code.

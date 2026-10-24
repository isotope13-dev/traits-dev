# Task loaders and Baileys fragments: second review

All three submitted artifacts are **MALICIOUS** on balance. This judgement
comes from the execution paths below, not scanner scores or a public-registry
label. No external feed, advisory, or scanner corroboration was used.
The original bytes were hashed and left unchanged.

## Identification and execution paths

### 954d6373a855: cmdlet_task_loader.ps1

A Windows PowerShell archive bootstrapper with CROSSROAD-associated indicators.
It constructs a global named mutex and exits if WaitOne(0) cannot acquire it.
It downloads component.zip from an HTTPS endpoint into TEMP, expands that same
archive under LOCALAPPDATA/Runtime, and constructs a scheduled-task action
for FamItrfc.exe in that same extraction directory with --runtimechk.
The one-time trigger has a three-hour repetition interval; task registration
is forced. Finally, Remove-Item targets PSCommandPath, its own source file.

The source establishes staging, persistent task activation and self-removal.
It does not prove an immediate payload launch, C2, privilege escalation,
successful installation, an in-memory payload, or alternate-stream deletion.
The URL is not evidence that the host is malicious by itself. The shared
global mutex and runtime argument reinforce the otherwise concealed,
self-erasing executable deployment. The script supplies no integrity check,
installer identity, user-facing installation flow or configuration documenting
the deployment. That combined evidence tips the judgement toward malicious.
An authorized Radmin deployment could change the contextual judgement;
deployment authorization and the downloaded ZIP's contents are unavailable.
The family association is tentative rather than independently corroborated.

### bf270c4dcad6: argv_task_loader.py

A Python implementation of the same Windows bootstrap chain. It calls
CreateMutexW through ctypes, exits on GetLastError()==183, downloads a ZIP
to tempfile.gettempdir(), and extracts it under LOCALAPPDATA/Radmin.
The task action is the extracted directory joined to FamItrfc.exe, followed
by --runtimechk. subprocess.run receives an argument vector for schtasks:
create, hourly, interval three, action path, and force replacement.
This is a subprocess launch, not shell command-text execution.
The script deletes __file__ after task registration succeeds.

The verdict and missing context are the same as for the PowerShell variant.
No obfuscated stage is embedded in either script. The final executable is
not supplied, and its capabilities are not inferred.

### e5c1a1dbfe08: Baileys-derived fragment archive

The supplied tgz contains exactly two source members, not a complete npm
package. Its collected name suggests @elfhkry666/baileys 0.3.25; no manifest
inside these bytes independently validates that package name or version.
Imports, exported socket factories and WAProto usage identify Baileys-derived
WhatsApp library code. All source, including the message utilities' trailing
helpers, was inspected. Missing dependencies were not invented or executed.

In lib/Socket/newsletter.js, makeNewsletterSocket installs a connection.update
handler. On its first open event it sets isStreamSynced, decodes the Base64
constant to 120363413381964356@newsletter, and passes that value directly as
newsletter_id to executeWMexQuery with QueryIds.FOLLOW and the newsletter join
path. The wrapper forwards those arguments to the imported WMex query helper
using the active socket's query function. The catch is empty. This is a
session-triggered follow of a library-selected target, distinct from the
public newsletterFollow(jid) API that uses a caller-supplied target.
The guard is set before awaiting the query, so a failed attempt is not
retried during that socket instance. Success was not observed.

In lib/Utils/messages.js, mediaAnnotation is a module-level array. Hex
decoding supplies 120363404006644139@newsletter and server message id 103.
Environment variables can override the fields, but the built-in channel is
the default. prepareWAMessageMedia copies caller input into uploadData,
then overwrites annotations for image/video input. Both normal and raw
newsletter-media branches spread that modified object into the outgoing
protobuf; cached media also receives it through Object.assign. Thus the
built-in channel attribution reaches outgoing content rather than remaining
unused configuration. This unconditional replacement is distinct from the
opt-in externalAdReply, offer and order helpers, whose constant defaults are
accurately described by existing notable traits and were not promoted.

The rest of the utilities prepare messages and sticker packs, fetch a
caller-derived profile image, hash media, invoke encryptedStream, call the
provided upload callback, and unlink temporary media. Sticker packs are
assembled with fflate.zip. These are ordinary library capabilities, not
credential theft, ransomware, host execution or attacker exfiltration.
The archive cannot run as a standalone complete library, but its source
still establishes the unwanted session and content changes. Silent automatic
subscription and replacement of user content justify MALICIOUS independently
of missing external corroboration. No account-holder consent or deployment
policy was provided.

## Trait corrections and coverage

* Retained all hostile and suspicious detections, including the six aggregate
  archive detections and each member's existing detections.
* Personal-folder paths now use parser literals rather than raw source text.
  The previous matcher mistook the comment “WhatsApp Web/Desktop and iOS”
  for a filesystem reference. The same regex still recognizes actual path
  constants and quoted destructive commands. Its live consumer is the
  source-user-document-recursive-delete-command composite; the quoted
  Documents-delete control retains that objective.
* Moved Python gettempdir reference, symbol and grouping rules from
  fs/temp/directory to os/sysinfo/directories: they discover an existing
  directory, not create one. The two atoms are now notable. Matchers,
  Python/pyc scope and platform scope were preserved. Updated all four exact
  consumers: bytecode staging, screenshot staging, messaging staging and
  CryptoAITools. Ancestor fs selectors were inspected; their PE, PowerShell
  or autorun scopes cannot consume these Python/pyc facts.
* Renamed global-mutex-single-instance-script to
  global-guid-mutex-management. Creation, a GUID and release/wait/exit
  context do not prove an exit guard. The matcher and severity are unchanged;
  both loader/injection consumers now reference the new name.
* Renamed setup-active-urlretrieve-entry to
  download-call-or-setuptools-entry-context. Its alternatives also match a
  non-setup module or a setuptools run override without a proven download.
  The transparent description reflects that OR. Its three setup-payload
  consumers retain the same matching evidence.
* Added notable fflate ZIP creation, encryptedStream helper invocation and
  upload-method/callback invocation. A named zip call alone is a source-call
  observation because collection zipping exists; the ZIP creation composite
  additionally requires an fflate import. Upload detection specifies neither
  HTTP nor exfiltration. No sample-specific endpoint, channel, task, executable
  or mutex constant was added.

The loader pair remains below the 3–5 hostile-trait goal: each has one hostile
family-associated finding. ZIP staging, recurring executable activation and
self-removal are covered by existing suspicious composites and notable
primitives, but independent hostile coverage remains incomplete. The stronger
AppData/action/force combinations were reviewed and tested; they also match
explicit administrator-invoked, digest-pinned maintenance installers in the
new controls. Promoting or duplicating them would falsely infer hostile intent.
Manual tracing binds the extraction directory to the task action, but the
generic file-local composite matchers do not prove that relationship, and
Python flow analysis reports incomplete coverage. Even a stronger relationship
matcher would still need attack admission beyond an ordinary maintenance
install. No final payload, unauthorized policy change, security-control bypass
or remote command channel is present to justify additional distinct hostile
claims.

## Verification and scanner disagreement

Scans used the checkout through CLEAVE_TRAITS_DIR, local analysis, slow mode,
no updates and --follow=none. A git-HEAD snapshot supplied the unchanged
baseline. No referenced payload was run. Full facts were collected for all
three artifacts and both source members, with encoded constants separately
decoded and traced into their consumers.

| Artifact | Hostile before → after | Suspicious before → after |
|---|---:|---:|
| PowerShell loader | 1 → 1 | 5 → 5 |
| Python loader | 1 → 1 | 5 → 5 |
| tgz aggregate | 6 → 6 | 1 → 1 |
| newsletter.js | 5 → 5 | 1 → 1 |
| messages.js | 1 → 1 | 0 → 0 |

No material attack detection was lost. The only removed sample finding is the
false personal-folder reference, in messages.js and its archive aggregate.
The mutex observation was renamed without changing coverage. Low-value OR
groupings can be internally matched but omitted from scan output; this is
presentation filtering, not a reason to add redundant required legs.

Atomscan 2.13.0 with v18.18 models classifies the PowerShell sample as benign
(cls=0, lvl=-1), despite its hostile family-associated rule and this review's
malicious judgement. Python and the archive retain hostile classifications
(cls=2, lvl=0). Individual JavaScript members remain below the ML decision
threshold although their rule findings establish hostile behavior. The
classifier also warns that its v18 feature specification predates v21.
These are reported gaps, not reasons to restore inaccurate detections.

Eleven focused fixture cases cover new capabilities, source comments,
collection zipping, unused imports, directory discovery versus creation,
mutex management, real path literals, quoted destructive commands, and the
two digest-pinned maintenance installs. Nine existing controls outside this
batch retain every hostile/suspicious finding: malicious setup download/exec,
history profiling, three benign setup controls, hardcoded and parameterized
channel follows, an encoded-channel follow, and a metadata-only query.
Copies outside testdata were scanned to avoid path-based test exclusions.
The maintenance controls are standalone review controls: the benign fixture
validator forbids suspicious objective findings regardless of a permissive
max_suspicious value. Run their explicit retained-finding/zero-hostile checks
with python3 testdata/triage/task-loader-baileys-review/check.py <scratch-dir>.
Compact results and decoded values are in results.json.

Raw before/after scans, full facts, baseline rules and scan logs are under
the named scratch directory, scratch/acquit-review. The final repository
check is make validate; its outcome is reported with the completed work.

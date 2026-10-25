# Registry console and browser-agent second review

All three supplied artifacts are **MALICIOUS** on their implemented capabilities
and attack-oriented packaging. This is a static judgment of the supplied bytes,
not attribution to a known campaign or evidence that any deployment succeeded.
The PHP explicitly calls itself synthetic; the C# and extension are similarly
small attack specimens. No package URL, registry history, authorized assessment
context, server configuration, or successful exploitation was supplied. A
confirmed security-training or regression-fixture deployment could change the
operational judgment; none is assumed here.

## Identification and execution paths

- `35d83ff564a02efe0923113d94291ca51c29c2a98568130bb33b00114364f7f3`:
  synthetic PHP command/upload console. `$_POST['cmd'] ?? null` enters a null
  guard, reaches `shell_exec($command . ' 2>&1')`, and is echoed into the page.
  There is no authentication or command restriction in the file. `php_uname()`
  and `SERVER_SOFTWARE` are displayed locally. Verified uploads are moved to
  the current directory using the client basename, without a type restriction;
  the page constructs and publishes a host/script-relative link. `basename`
  prevents client pathname traversal but does not restrict executable extensions.
  Actual webroot placement and PHP execution policy are deployment-dependent.
  There is no outbound host-profile upload: the browser uploads to the server.
  The unauthenticated command surface plus arbitrary upload capability tips the
  verdict, despite the explicit synthetic-specimen comment.
- `fd61696d31c9a4b12a4a8d1bd377884f2f8596da66b2fff5e6edceced68d5a22`:
  `ExchangeHeaderAgent`, a C# header-command backdoor specimen, not a proven
  Exchange module. `Handle` Base64-decodes `X-Task-Frame`, copies the first 16
  bytes into an IV, decrypts the remaining bytes with AES and a zero-filled
  32-byte key, decompresses with GZipStream, then dispatches tag 2 by decoding
  the remaining bytes as UTF-8 and starting `cmd.exe /c`. No authentication or
  integrity validation is implemented. The command's output is not captured.
  `BlindTelemetry`, separately callable and never invoked by `Handle` here,
  passes AMSI/ETW export names and return-zero byte arrays to `Patch`. That
  helper resolves each export, requests RWX protection, and writes the patch
  with Marshal.Copy; it does not restore the saved protection. Rizin confirms
  both `31 C0 C3` and `33 C0 C3` decode as `xor eax,eax; ret`. Success depends on
  architecture and API state; the intent to blind scanning/telemetry is explicit.
  The devtunnels URL and RDP port are only concatenated into returned text:
  there is no socket connection, RDP forwarding, or implemented tunnel. No
  HttpModule registration, ASP.NET integration, or caller is supplied. Encrypted
  request-command dispatch and defender patching jointly tip the verdict.
- `2a1a595554bdbabe7e7efd61909aca28ce3dad6d0747c967613861d929e98347`:
  Manifest V3 extension **Browser Workflow Helper**. ZIP member bytes were
  compared with all three extracted files and are identical. The manifest
  enables a static DNR ruleset, grants HTTPS wildcard host access and debugger
  authority, and declares scripts on assistant/marketing origins. The debugger
  permission is declared; no debugger API is invoked. DNR rules substitute an
  external script, remove CSP, set CORP to cross-origin, set credentialless
  Document-Isolation-Policy, and remove Location on a targeted origin. The
  script-replacement and policy-modification URL filters differ: no common
  response or actual fetched script is proved, and `.invalid` endpoints are
  placeholders. Credentialless isolation is not itself a disabled security
  control; descriptions now distinguish the header/value evidence.

  `agent_bridge.js` requests GLIC tab creation, context permission and focused
  tab text/screenshot/PDF access through wildcard-origin postMessage, opening
  `file:///etc/hosts`. It trusts the first message's `event.source`, without an
  origin check. Its initial synchronous call dereferences `privilegedFrame`
  before the asynchronous message handler can initialize it, stopping the
  initial path. The independently defined Comet routine sends START_AGENT to
  a fixed extension; the Edge routine awaits a disable/query/enable sequence;
  the Opera routine sends a sidebar SEND_MESSAGE_REQUEST but references an
  undefined `neon`; the Claude routine forges an onboarding target on the body,
  installs an instruction attribute and programmatically clicks it. These are
  static attempted capabilities, not observed successful actions. APIs and
  receivers also depend on browser privileges and supported versions. No
  responses are collected or exported. The combination of script substitution,
  navigation/security interference and forged privileged-agent control tips the
  verdict over its innocuous helper name; missing runtime wiring is recorded.

The sources are readable. Runtime Base64/AES/gzip handling is not a hidden
embedded payload. `cleave facts` was saved for each original and each archive
member, including text/decoded views, calls, literals, values and flow limits.
No specimen was executed. The byte stubs were only disassembled.

## Trait corrections and additions

`id-map.json` in the scratch review records the exact relocation map. Every
changed observation retains its original matcher and effective scope except the
explicit decryptor repair and new detections below. Exact consumers were updated;
ancestor directory consumers were inspected before moving observations.

- The PHP profile/upload combination is an incoming HTTP request handler, not
  a suspicious attack objective or outgoing transfer. It now lives under
  `micro-behaviors/communications/http/server/request` at notable severity.
  `diagnostic-upload.php` demonstrates its supported benign interpretation.
- PHP upload data plus request-URL construction does not prove URL publication
  or hostile intent. The retained notable co-occurrence lives under URL building.
  The sample's actual publication was traced manually; the old matcher did not
  bind an upload destination to the emitted anchor. All constituent upload and
  URL behavior remains detected. The hostile command/upload finding survives.
- Three PHP upload-move observations move to `fs/file/move`; the structured
  temporary-file matcher and its exclusions are unchanged. A received file move
  does not establish an outgoing HTTP upload, a copy, or ATT&CK T1105.
- `Buffer.BlockCopy` moves from embedded-resource extraction to `mem/copy`;
  resource-loader consumers retain it as their memory-copy leg. The sample
  extracts an IV from a network frame, not an embedded resource.
- `CompressionMode.Decompress` moves from zlib to algorithm-neutral stream
  decompression. Existing DeflateStream consumers retain their algorithm leg.
  A new constructor matcher detects this specimen's gzip-specific operation.
- A devtunnels endpoint beside 3389 is retained as notable proxy configuration
  context, not suspicious C2 forwarding. `endpoint-config.cs` demonstrates the
  false forwarding inference; there is no transport operation to match here.
- Literal return-zero bytes move from ETW blinding to source-literal metadata;
  all ETW patch composites retain the same evidence. A byte catalog is not
  itself telemetry patching. The original status-stub and ordinary-interop
  corpus controls remain free of the affected patching claims.
- The CreateDecryptor symbol matcher accepts receiver-qualified call names,
  which facts actually emits (`aes.CreateDecryptor`). The encrypted-header
  composite now explicitly requires that retained direction-specific evidence.
- GLIC command literals are described as names, not sends; cross-file DNR/GLIC
  composites say co-occurrence rather than a proven remote-code data flow.
  Edge sequence IDs say tool-mode toggles rather than an unproved concurrent race.
- New browser findings cover wildcard postMessage target origins, the Opera
  message-type reference, and the previously missed Claude body/onboarding
  prompt forgery. The hostile Claude composite additionally requires extension
  content-script deployment; a standalone code fragment remains suspicious.
  No arbitrary extension filename or vendor hostname gates the new composite.

## Findings and classifier comparison

Counts include inherited findings at the archive root; member rows are separate
and must not be summed again into the root.

| Artifact | Hostile before → after | Suspicious before → after |
|---|---:|---:|
| PHP console | 1 → 1 | 2 → 0 |
| C# header agent | 3 → 3 | 3 → 2 |
| Browser extension ZIP | 4 → 5 | 6 → 7 |
| `agent_bridge.js` | 0 → 0 | 3 → 4 |
| `manifest.json` | 0 → 0 | 0 → 0 |
| `rules.json` | 1 → 1 | 2 → 2 |

After normalizing moved/renamed IDs, **no existing detection is lost** on any
original or archive member. All eight pre-existing hostile findings across the
three roots remain (the ZIP's four are included in that total); the additional
archive finding covers Claude prompt forgery. Two PHP and one C# suspicious
weights were corrected to notable for the specific unsupported intent claims
above; their accurately named observations remain visible.

The v18.18 local classifier gives PHP probability 0.98642623 → 0.872385,
calibrated level 5000 → -1 and confidence 54 → 0. Thus the corrected traits expose
an ML miss at every calibrated flagging level, despite the retained hostile
rule. C# remains at probability 0.99998885 → 0.99998087, level 0, confidence 100.
The ZIP remains 0.99994844, level 1, confidence 99 (its rules member drives the
aggregate). The JS member rises from 0.95714188 to 0.98495173 but still has no
calibrated flagging level; the manifest remains 0.20696722. No inaccurate
trait was restored or duplicated to raise these scores.

The PHP hostile-count goal remains unmet: this short file supplies one attack
objective, a command/upload webshell. Request-to-shell output, upload validation
and destination/link construction, host reporting, encodings, persistence,
staging, cleanup and network effects were investigated. Every observed behavior
is covered, but host diagnostics and upload/URL operations alone do not justify
additional hostile objectives. There is no supported exfiltration, persistence,
encoded payload or separate execution stage to add. A second command-shell rule
would duplicate the already detected objective rather than close a behavioral
gap. This is an evidence limit, not a reason to inflate severity.

## Verification

`check.py` passed **14 focused positive/near-miss controls and 25 existing corpus
regressions**, using both HEAD's original traits and the edited traits. This
includes existing PHP upload/webshell fixtures, .NET decompression fixtures,
status-stub and native-interop controls. The focused telemetry-patch control
retains AMSI and ETW hostile coverage. All existing findings on the 25 available
corpus controls remain after ID normalization. One path referenced by the old
WordPress case manifest (`testdata/benign/tebink-php-console.php`) is absent from
this checkout and was not counted or reconstructed.

Original scans, member facts, ID mapping, final scans and per-file added/lost
comparison are retained under the named scratch directory `scratch/acquit-review`.
The last repository check is `make validate`; no inline YARA source was changed.

# Atom's Connections 1.7.1 beta

Verdict: **BENIGN**. Reviewed SHA-256:
`f11834e37011385acbe45cbd9c00cf0a60577ed9a8fc0f751941aec6821d5e81`.
This is a Windows .NET Framework wrapper around a peer-to-peer social and
messaging application. The verdict follows the recovered code, not its version
resource, external verdicts, or the scanner's scores. Nothing was executed.

## Execution and data flow

All 17 managed methods were disassembled with dnfile/dncil; rizin confirmed
the PE layout and sole native import, `_CorExeMain`.

- `Main` calls `Run`. The command-line options configure the port, storage
  directories, idle shutdown, browser launch, and shortcut creation. An `atoms:`
  argument supplies an invitation, not a shell command.
- `Run` starts an HTTP listener on `127.0.0.1:47800` and `localhost:47800` by
  default. It opens that local URL through `Process.Start` with
  `UseShellExecute = true`. It does not receive arbitrary process commands.
- `LoadFiles` reads the managed `app.pak` resource, checks its SHA-256, opens
  a GZipStream in decompression mode, and parses length-prefixed assets into
  an in-memory dictionary. The three entries are `index.html` (616829 bytes),
  `player.html` (5019 bytes), and `vendor/peerjs.min.js` (92865 bytes). There is
  no embedded assembly loading, native injection, or executable staging.
- The resource SHA-256 is
  `db2fd6b4dc620bdddf8cad94e451514066e9cd8181f40ba9a4905159800ccc3c`.
  Its gzip bytes explain the near-maximum entropy in the executable section.
- The local `/device-key` route exposes the application's own random 32-byte
  key, saved with current-user DPAPI as `device.key`. It does not decrypt
  browser password databases or another application's secrets. Sensitive
  routes require POST, an `X-Atoms` header, and non-cross-site Fetch Metadata.
  The server also checks the Host header against its loopback hosts and port.
- `/save` writes user-selected content beneath the app's Pictures or Documents
  subdirectory. `SafeTarget` rejects traversal, reserved device names, invalid
  components, and paths outside the selected root. Static GETs use an explicit
  asset route table. `/quit` and `/bye` control only this application.
- `EndOtherCopies` is reached after listener startup fails. It queries
  `ProcessId, CommandLine FROM Win32_Process WHERE Name=...`, selecting its own
  executable basename, excludes its PID, and checks the configured port before
  using `GetProcessById`, `Kill`, and `WaitForExit`. This recovers from a stale
  application instance; it is not defender termination.
- `RegisterProtocol` writes HKCU `Software\Classes\atoms` with a quoted own-path
  handler and `%1`. `MakeDesktopShortcut` uses WScript.Shell automation to save
  a desktop shortcut to the same executable. Neither installs a login trigger,
  service, scheduled task, nor privileged component.

## Obfuscation, network services, and dependencies

The two HTML scripts use rotated Base64 string arrays and arithmetic decoder
wrappers. The application script was decoded by evaluating only its inspected
string decoder, array, rotation, and pure wrappers in a time-limited QuickJS
context. 10979 constant decoder calls were replaced; the application itself
was not evaluated. The player uses the same scheme with a small string array;
its URLs resolve to YouTube's privacy player and Vimeo, and it restricts
messages to the player and local parent origins and a fixed playback-command
list.

The main script generates local identities, authenticates invitation-based
peers, and uses ephemeral plus identity ECDH P-256, HKDF, and AES-GCM for
messages and media. Sequence checks reject replayed frames. IndexedDB holds
the application's encrypted records. PBKDF2 protects user-created backups.
Network dispatch handles posts, chats, groups, file chunks, plugins, and calls,
with contact/session checks. Microphone and camera requests belong to call and
device-selection flows. No credential harvesting, covert host survey, operator
shell, or unauthorized export was found.

External content was fetched over HTTPS on 2026-10-19:

- `https://unpkg.com/peerjs@1.5.4/dist/peerjs.min.js` is byte-for-byte identical
  to the embedded dependency, SHA-256
  `ad5d8870d1e389914f9cba8d35be313c4327c69ee0a221e482e9bf7621136fe5`.
  Its default broker is `0.peerjs.com`; this is WebRTC signaling, not tasking.
- `https://atomsconnections.com/` describes the same application and links its
  installer and portable distribution. The fetched portable ZIP contains the
  newer application, README, and license. The README's browser, invitation,
  file-sharing, and local-key behavior agrees with the recovered 1.7.1 code.
- `https://atomsconnections.com/version.json` advertises 1.7.3 and a same-origin
  installer. The recovered updater only presents a download action; it does not
  silently execute the installer.
- `https://atomsconnections.com/plugins/catalog.json` lists Compass Player and
  Atom Math Lab. Both downloaded archives match their advertised SHA-256 values:
  `5655b2cfc5017261e83e19f2547b233196401ad977204b6619b667b377482642`
  and `26bf4ce88d8d4834bdcf7e21867557109f8c9b5c95e93fd132a612366f941289`.
  Their scripts implement music storage/playback and math exercises. Plugins
  are opt-in ZIP assets loaded in an `allow-scripts` iframe without same-origin
  authority, with CSP denying connections and frames. App-mediated permissions
  gate storage, widgets, notifications, and peer messages.

The external malware label is plausibly a heuristic false positive: the
unsigned, newly built PE has a large compressed resource, high overall entropy,
obfuscated JavaScript, DPAPI references, COM shortcut creation, a local server,
and process-termination references. None establishes hostile intent. Most
provided engine names were generic or machine-learning detections.

## Trait changes and controls

Resource size belongs in `metadata/binary/resource/size`, and resource entropy
in `metadata/binary/resource/entropy`. The composite states that the independent
maxima include large and high-entropy entries; it cannot prove both properties
belong to one entry, or establish obfuscation (B0032). Exact active consumers
were updated. No selectors of the three affected leaves were present, and
their common ancestor retains its member observations. Historical review
snapshots are unchanged.

| Previous ID | Current ID |
| --- | --- |
| `metadata/binary/resource/identity::clr-resource-large` | `metadata/binary/resource/size::clr-resource-large` |
| `metadata/binary/resource/size::clr-resource-high-entropy` | `metadata/binary/resource/entropy::clr-resource-high-entropy` |
| `metadata/binary/resource/size::dotnet-large-high-entropy-managed-resource` | `metadata/binary/resource/entropy::clr-resource-size-and-entropy` |

The existing WQL process-query trait now covers PE/DLL decoded strings, and a
CLR-gated GetProcessById reference records PID lookup. Both are notable neutral
capabilities. The GZipStream composite description now states its reference
evidence without implying compression direction.

`check.py` checks the reviewed assembly, large/low-entropy and small/high-entropy
resource controls, a small zero-filled resource, projected and select-all WQL
queries, another WMI class, a bare class name, and a native method-name near
miss. It checks the relocated IDs and notable severities, rejects retired IDs,
and requires the reviewed sample to have no suspicious or hostile traits.

Validation outcome: all nine focused controls passed. Lowercase WQL needed an
explicit inline case-insensitive regex modifier to pass the analysis pipeline
as well as the direct matcher. The final atomscan report contains zero hostile
and zero suspicious findings, and retains every previous observation under
the resource-ID mapping above.

## Follow-up: API placement and independent recheck

The same sample was independently disassembled and its resource unpacked again.
The three asset lengths, resource digest, 10979 recovered decoder calls,
loopback-only routes, bounded save paths, stale-instance termination, and
byte-identical upstream PeerJS 1.5.4 were confirmed. No hostile behavior was
found. A fresh HTTPS fetch of version.json advertised 1.8.5; the current catalog
contained only Atom Math Lab 1.4.0. Its archive matched the advertised SHA-256
`26bf4ce88d8d4834bdcf7e21867557109f8c9b5c95e93fd132a612366f941289`.
Its arithmetic question generation, independent answer verification, progress
storage, and interface handlers agree with the declared learning-game purpose.
The downloaded portable executable is a newer build, not a hash match for this
sample. Live-site version and catalog changes do not alter the recovered code.

Two additional placement corrections preserve their matchers and scopes:

- `micro-behaviors/process/interpreter/reflection/runtime::invoke-member-token`
  becomes `micro-behaviors/metaprogramming/reflection::invoke-member-token`.
  The API name covers reflected invocation and C# dynamic member binding; it
  establishes neither script execution nor a staged-code handoff. All exact
  YAML consumers were updated. The only old-ancestor directory consumer is
  an Empire Python rule, incompatible with this atom's PE/C# scope. No new-home
  directory consumers were present. The destination now has 100 rules.
- `micro-behaviors/process/enumerate/managed::dotnet-get-process-by-id-member`
  becomes `micro-behaviors/process/info/query::dotnet-get-process-by-id-member`.
  Looking up one known PID is not process enumeration. The termination consumer
  follows the moved trait. Four broad enumeration selectors remain unchanged:
  their analysis-tool co-occurrence claims should no longer accept a singleton
  PID lookup as enumeration. No new-home directory selectors were present.
  The inherited enumeration mappings T1057/E1057 were removed from this atom.

The HttpListener type and GetManifestResourceStream method references also lose
unsupported C2 and concealed-payload ATT&CK mappings (T1071.001 and T1027.009).
Their descriptions explicitly state the API-reference evidence. Severities
remain notable. No product-name exception or score-based suppression was added.

Full before/after reports have exactly the same finding IDs after applying the
two relocation mappings, with zero suspicious/hostile findings. Static mutated
controls independently remove InvokeMember and GetProcessById and each loses
only its respective atom. The expanded check.py also removes the WQL process
class while retaining the PID lookup; this must produce no process-enumeration
finding. Original resource and WQL controls remain in the check.

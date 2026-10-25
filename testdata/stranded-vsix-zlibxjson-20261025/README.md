# VSIX and zlibxjson member review, 2026-10-25

The two supplied archives retain the user's confirmed-malware verdicts. Each
listed member was independently examined. No specimen code was executed.

| Member | Judgment | Deciding evidence |
|---|---|---|
| `extension/client.js` | MALICIOUS | An outbound Socket.IO connection accepts shell commands, returns their stdout, transmits desktop frames, and applies received mouse coordinates. These functions are unrelated to the extension's advertised TypeScript restructuring. |
| `extension/hello-world.js` | MALICIOUS | Two rotated string tables conceal a five-second environment/host-report check-in and evaluation of a server-supplied reply field. |
| `libvips-42.dll` | BENIGN | Byte-identical to the official `@img/sharp-win32-x64@0.34.5` DLL. Export and native-code review confirms image operations and ordinary GLib services. |
| `jimp/browser/lib/jimp.js` | BENIGN | Byte-identical to official Jimp 0.22.10. The bundle implements image loading, bitmap transformations and codecs, with ordinary fetch and module-loader helpers. |
| `zlibxjson/main.py` | MALICIOUS | The sole implemented command downloads an external EXE into APPDATA and starts that returned path using a hidden shell. No zlib/JSON implementation or coherent installer interface explains it. |
| wheel `METADATA` | BENIGN | Declarative identity, placeholder author/repository fields and a requests dependency; no executable payload. |
| wheel `entry_points.txt` | BENIGN | Ordinary declarative console-command mapping. Its referenced implementation is malicious; the mapping bytes alone do not implement hostile behavior. |

The extension package declares startup activation. Its activation function loads
`hello-world.js`, `test.js` and `client.js` before reaching its broken notification
statement. Thus the notification error does not prevent the preceding modules'
load-time setup. The screen client captures JPEG frames every 500 ms after the
operator starts sharing, resizes them to 1920x1080, encodes at quality 50, and
emits Base64. A received click saves the cursor position, applies the requested
coordinates, clicks, and restores the cursor. The shell handler returns either
stdout or an error object. There is no implemented local consent/authentication
step. Operator activity, runtime success, original installation circumstances,
and subsequent commands are unknown; none are assumed in these judgments.

The obfuscated script's first table rotates 22 times and its second table 15
times. The lower-first Base64 decoder resolves `hostname`, `platform`,
`networkInterfaces`, `JSON.stringify`, `Buffer.from`, `base64`, `toString`,
`utf8`, `json`, and `error`. The endpoint resolves to
`http://45.43.11.211:1224/api/checkStatus`. A query carries the hostname, OS
version/platform, the first non-internal IPv4 MAC, the complete `process.env`,
a tracking value and a server-assigned `sysId`. An initial request and a 5000-ms
interval invoke the same helper. The helper parses the fetch response, extracts
`status`, `message`, and `sysId`, and evaluates `message` when status is `error`.
Caught evaluation errors are discarded. No later returned code was recovered.

The Python wheel's console script calls `main:init`; importing `__init__.py`
exports `init` without calling it. `init` reads APPDATA and passes the directory
and Discord attachment URL into `download_file`. The helper makes the directory,
strips the URL query to choose its basename, streams successful HTTP response
chunks to the binary file, and returns that exact path. `run_silently` hands it
to `subprocess.Popen(shell=True, CREATE_NO_WINDOW)`. Missing APPDATA prevents
the download; launch exceptions are printed. There is no payload verification
beyond HTTP status, persistence installation, cleanup, credential collection,
privilege escalation or exfiltration in this member. The remote EXE is unknown:
forager returned 404. The required exact-version all-wheels fetch also failed:
PyPI metadata was removed and its browser fallback lacked Chromium ICU data.
The original supplied wheel and its member remained available and hash-checked.

## Detection changes

The new Socket.IO rules bind handler input to shell execution and returned
stdout, image capture through sharp to emission on the connected peer, and
received coordinates to pointer movement on the connected peer. Event labels,
endpoints, command-property names and local data-variable names are not IOCs.
The polling rule binds the same named helper to initial and interval calls,
fetch-response access, destructured reply field and evaluation. The environment
rule binds `process.env` through query construction into the fetch URL. Hostile
composites add the actual control/concealment context. Their precision scores
exceed the 3.5 authoring bar; behavioral controls remain the decisive checks.

| Previous observation | Correction | Supported evidence retained |
|---|---|---|
| Desktop capture / capture plus synthesized input classified as backdoor behavior | Move to display/input capabilities; suspicious becomes notable | Both compound observations and their import/call primitives remain. Local RPA can perform them. The network-bound objectives supply the attack claims. |
| Arbitrary `click()` called a DOM action | Move unchanged matcher to source call syntax | Desktop and DOM calls both remain visible; all six explicit consumers are updated. |
| GLib `GSocket` treated as the gsocket command | Require the command's lowercase spelling | Actual gsocket and gs-netcat tooling and retained hostile composites still match. The official gsocket script was fetched as an external positive. |
| A zero-width space in a `ReadableStream` documentation comment called evasion | Keep comment evidence as metadata; scope source evasion to actual string constants | Runtime string splicing and document splicing remain suspicious. A separate identifier rule preserves valid JavaScript zero-width-joiner identifiers. An isolated comment control alone is not an attack claim. |
| PNG/7-Zip magic immediates called embedded images/payloads | Move unchanged byte matchers to magic-constant metadata | Native codec signature construction remains notable; related consumers retain the exact observations. |
| An English pangram called payload filler | Move unchanged matcher to natural-language phrasing | The Pango sample sentence is still detected; the padding composite retains its explicit reference. |
| Bare `clazz`/`codes` vocabulary filed as SUPERNOVA identity | Move unchanged component to vocabulary metadata | The SUPERNOVA composite still references it with its other discriminating markers. |
| Webpack wrapper filed as obfuscation | Move unchanged matcher to bundler metadata | Its explicit exclusion is already covered by the existing metadata/build exclusion. Neutral bundling no longer supplies intent through broad objective selectors. |
| A DLL containing Rust components called a Rust library | Rename/reword the unchanged composite as a large image with Rust markers and exports | Its injection-rule exclusion is preserved. |
| Socket.IO module-name literal filed as library identity | Move unchanged matcher to source-literal metadata | Its three explicit consumers retain the reference; it does not identify the file as the library. |
| `application/x-msdownload` filed as email behavior | Move unchanged substring/exact forms to MIME data format | Email and upload consumers keep the exact scope-specific references. |

Exact references and ancestor directory selectors were audited before changing
shared rules. No directory was split and no new taxonomy leaf was introduced.
Moves preserve type/platform/size/section scope unless explicitly described
above. Unsupported ATT&CK/MBC attribution was removed from neutral observations.
The media library network, execution, encoding and crypto capabilities remain
visible. Neither benign judgment is used as an exclusion for those behaviors.

## Coverage and limits

`check.py` exercises the new linked paths and their broken-input/output/peer,
local-only, wrong-response and wrong-interval near misses. It copies sources
outside test-named directories during analysis so exclusions do not decide the
result. It never runs the fixture programs. External comparisons cover the
existing gsocket persistence and Unicode-splicing positives, the existing
remote-desktop npm artifact, and the fetched official gsocket script. Full
repository validation also covers the established malicious and benign corpus.

The wheel and its Python member retain zero hostile and two suspicious traits.
Their implemented outcome is one download/hidden-launch chain; ordinary
updaters share its general mechanics. The linked stream/file/return/launch
matcher, APPDATA staging, console entry point, URL context and package purpose
were reviewed. Existing ten download-helper boundary controls were retained.
No additional independent hostile outcome exists in the supplied Python bytes,
and the unrecovered EXE prevents downstream detections. The malicious member
judgment does not close that detection limitation.

`hello-world.js` has two independently supported hostile results: environment
export and remote reply execution. The host report is also traced manually;
computed OS method names prevent an independently bound general host-profile
export rule without depending on this sample's field/table names. Its source
field observations, query transfer, concealment and interval execution are
covered. A third hostile rule would currently duplicate a result or overclaim
those computed calls.

Controlled before/after counts, classifier levels, archive-member deltas,
material losses and remaining classifier disagreements are in `review.json`.
Absolute artifacts, full facts, decoder substitution, native disassembly,
forager provenance and scan envelopes are retained in the task scratch directory
`stranded-vsix-zlibxjson`. The archives' existing malware conviction is retained.

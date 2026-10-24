Second review of three public-registry artifacts
===============================================

All three are MALICIOUS on behavioral evidence. No feed, advisory, scanner
conviction, package name, or classifier score supplies the judgment. Original
archives and their declared extraction trees were inspected. atomscan was run
locally with this checkout, slow mode, no updates, and --follow=none; cleave
facts was collected for all originals and the important JavaScript/Lua members.
Additional source recovery and traces are in the session scratch directory
`acquit-review-v2`. No real network request or native payload was executed.

Web3 Connect 1.1.2 (d4033fe563a2)
-------------------------------

The XPI declares the popup index.html, whose module loads the React/Vite bundle.
It declares no required data collection. Its application code presents Trust
Wallet imagery, password setup, and recovery/private-key import screens.
The created password only gates the UI; it does not create an encrypted wallet.
The mnemonic form validates 12/18/24 words, joins them, and passes the phrase
to Hi. Hi passes the text to nu and selects the error screen. The private-key
form validates the selected network's key shape, then ru formats `[network]:
key` and passes that text to the same nu sender before selecting error.

nu Base64-encodes its parameter into an encoded event property, serializes the
event, and POSTs it to https://api.segment.io/v1/track using a built-in analytics
write key. This exports the secrets rather than importing them. The unrelated
blockchain dashboard and bundled Ethers/BIP39 implementations do not explain
this export. The false no-collection declaration and error-after-export UI
reinforce the judgment. Successful delivery, browser CORS behavior, operator
identity and the number of affected installations are unknown.

The privateKey match at byte 271991 is in the ordinary Ethers signing-key
implementation: length validation, a getter, public-key derivation, and signing.
A bare token establishes neither wallet harvesting nor suspicious activity.
Its matcher and JS/TS scope move unchanged to crypto/key/representation at
notable severity. SQL-storage consumers reference the moved atom, retaining
their original source evidence. The private-key export composite moves with
unchanged matcher, scope, severity and ATT&CK/MBC mappings from HTTP transport
to stealer/credential: its required source is a private-key entry, without a
wallet-specific requirement. No exact external consumer selected its old ID.

There are two supported hostile export findings, for mnemonic and private-key
paths. This remains below the three-to-five goal. Review of the full application
found no additional installation, browser-store theft, injection, persistence,
or destructive behavior to justify a third distinct hostile result. Encoding,
networking, cryptography and UI capabilities remain detected. Adding another
name for the same theft would not close a behavioral gap.

TikTok LIVE API repository archive (b628c0545f27)
----------------------------------------------

The Go-registry ZIP contains a TypeScript project whose package.json claims
tiktok-live-api 1.2.2 and a different upstream repository. Its replacement README
directs nontechnical Windows users to the exact bundled 1.6-alpha.2 ZIP and
instructs them to run its application and approve permission prompts.
Application.cmd runs `loader.exe module.cso`. Rizin imports and interpreter help
identify loader.exe as a LuaJIT CLI, with lua51.dll providing its runtime.
This is manual delivery; no npm lifecycle execution of the Lua file was found.

module.cso is Lua source, despite its suffix. Its nested closures, large
arithmetic state machine, decimal escapes, indexed concatenation and encrypted
string lookups hide the application. Facts recovery exposes folded source and
decrypted API/command strings. A restricted Lua 5.1 interpreter then traced the
original VM with mocked ffi, libraries, OS, I/O and networking. Native module and
export resolver routines were replaced with mocks after their roles were
traced; their numeric entry points are harness details, never rule evidence.

The original VM reaches GetConsoleWindow/ShowWindow hiding, resolves Windows
APIs, assembles host identity and geolocation records, captures the display via
GetDC/CreateDIBSection/BitBlt, packs the bitmap buffers, and supplies the result
to a multipart WinInet request. The mocked bitmap bytes were empty; this trace
establishes the source connection without claiming a real screenshot or send.
Static code constructs comment-padded PowerShell Start-Process RunAs commands
that broadly exclude the system drive and EXE/DLL files from Defender. It also
constructs daily highest-runlevel schtasks actions and one-time PowerShell
scheduled tasks. Task/action configuration selects file and native-thread
launch paths. A hard-coded HTTP endpoint has Polygon eth_call fallback
infrastructure; response text is converted into Lua table source with load.

Concealed AV disabling, unwanted activation and surveillance in a purported
TikTok desktop release tip the judgment. An installation, successful elevation,
working remote server, final downloaded payload or malware-family attribution
is not assumed. Some executable-memory allocation serves PEB/API resolution;
it is not automatically process injection or a downloaded shellcode payload.

The added raster-copy atom binds a BitBlt lookup to the same called alias and
the SRCCOPY raster operation. Intervening assignments may not replace the alias.
The capture objective requires that call, the existing display/DIB API profile,
and the independently supported obfuscated broad Defender exclusions. It claims
capture beside AV bypass, not statically proven screen exfiltration. Existing
AV and scheduled-task findings remain intact. Full payload activation and
screen-to-send findings remain limited by data transfers through separate VM
states and captured cells; no unbound network/API co-occurrence is promoted
to a source-to-sink rule.

Python sitecustomize loader (805ef90eb811)
----------------------------------------

The exact source activates main when imported under Python's startup-hook name.
It obtains a nonblocking exclusive lock, forks, creates a detached session,
changes to /, and redirects descriptors 0, 1 and 2 to /dev/null. The child reads
a GitHub raw-content routing document, selects its first hostname/optional-port
line, retrieves http://<selected-host>/codepy, and passes the response to exec
through the bound async helper. It suppresses BaseException and retries hourly.

An offline trace mocked imports, filesystem, lock, fork, descriptor and HTTP
effects and verified startup dispatch, the selected request authority, execution
of a controlled local response, and the 3600-second interval. The supplied file
does not prove installation into an import path or disclose the remote payload.
Its silent detached recurring arbitrary execution and explicit startup hook
support a malicious judgment without those missing facts.

The new neutral URL-building observation binds the actual HTTP helper, returned
routing text, selected stripped line and formatted request host. Its hostile
consumer additionally requires the existing bound response-execution daemon.
Neither the GitHub URL, chosen path, helper names nor polling interval gates
the new finding. Existing tasking and startup persistence detections remain.

Regression and classifier results
---------------------------------

Run `python3 testdata/taxonomy/acquit-registry-review/check.py`: 13 fixtures and
26 assertions cover renamed helpers, local/overwritten hosts, unexecuted bodies,
ordinary private-key references, SQL storage, Lua semicolons, wrong raster ops,
different callees and overwritten aliases. Two pre-existing hostile wallet XPI
fixtures retain their hostile clipboard and wallet-export findings. The only
direct moved-token consumer is SQL storage; the wallet-keyword directory's Rust
consumer cannot select the JS/TS-only atom. Existing Python startup and Lua task
fixtures remain available to the full validator. Moves add no directory or
budget exception and duplicate no matcher.

Hostile/suspicious counts (archive parents deduplicate member findings):

| Unit | Before | After |
|---|---:|---:|
| Web3 XPI and main JavaScript member | 2/1 | 2/0 |
| TikTok outer and nested ZIP, module.cso | 2/6 | 3/6 |
| module.cso decoded script | 2/5 | 3/5 |
| sitecustomize.py | 2/2 | 3/2 |

No attack behavior was lost. The two old Web3 IDs are replaced by the same
private-key export in its source-specific home and the same token at notable.
Other archive members retain their findings. Aggregate ML remains BENIGN for
the malicious XPI (0.7551865 -> 0.6767319), and MALICIOUS for the TikTok archive
(0.9999494 unchanged) and Python loader (0.99661434 -> 0.99688363). The XPI is a
classifier miss; restoring a false suspicious token or duplicating hostile
traits would obscure it. The model also reports using v18 features while the
engine expects v21; no model or threshold was changed.

Judgment marker lines
---------------------

Web3 Connect 1.1.2: seed/key telemetry theft; fix key traits

TikTok API lure: Lua AV bypass and persistence; add capture

Python startup loader: hourly remote exec; detect host indirection

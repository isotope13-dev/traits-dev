# First reasoned review of the three queued PEs

Verdicts below come from PE parsing, native disassembly and resolved CIL
instructions. No sample was executed. The supplied sandbox pages could not
be retrieved; their scores and vendor labels were not used as behavioral proof.
`check.py` identifies the exact inputs by SHA-256 and provides static controls.

## bd0e540860b7: MALICIOUS, StormAttack loader

The native x86 executable contains the StormAttack server/welcome markers,
resource-extraction implementation and DLL-injection implementation. This
supports the existing family attribution, rather than the collector's Remcos
or WannaCry filename labels. There is no evidence here of ransomware.

The entry path reaches 0x401cb0. The configuration at file offset 0x4120 is
3, selecting 0x401f75 -> 0x401900 -> 0x401390. At 0x401900 the program generates
a GUID, constructs a destination executable path and creates an HKLM Active
Setup Installed Components key. RegSetValueExA at 0x401a4b writes StubPath.
It then reads its own image, patches the future launch mode to 4, writes the
copy and calls CreateProcessA at 0x401b7e. The self-delete routine obtains its
module path, converts it to a short path, reads COMSPEC, constructs `/c del`
and launches/resumes the cleanup process (0x401390 through 0x4014d9).

Mode 4 calls 0x401b90, which extracts resource DLL/101 to a DLL path and calls
0x401150. Obfuscated detours in the RWX .htext section contain long runs of
self-exchanges/self-moves and rejoin the injector at 0x401163. Its code creates
a target process, allocates and writes the DLL path remotely, resolves
LoadLibraryA and supplies that address and remote path to CreateRemoteThread
(0x4011b1 through 0x40123d). The alternate mode 1 branch extracts the resource
and calls 0x401260 to replace LanmanServer's ServiceDLL registry value.
The existing traits accurately describe these code paths and API profiles;
they do not assert that all installation alternatives execute together.

Important limit: the 39,936-byte embedded PE is about 94.5% zero bytes. Its
entry RVA is 0x741a, it has no parsed imports or executable section, and the
entry bytes are zero. Do not infer a functioning DDoS implementation or successful
DLL loading from its banners. The engine's percent-decoding observation at
0x43b4 is generated from a GUID printf format, not an encoded URL or payload.
It is a decoder observation rather than a YAML behavior claim; no shadow rule
or malicious encoding attribution was added. Existing native traits unchanged.

## 7e767a5cb2c0: MALICIOUS, custom .NET stealer/ransomware

The assembly calls itself NanoCoreUltimate. It contains many malware names
and mutex labels; these do not establish NanoCore, Remcos or any other family.
Its unobfuscated CIL makes the hostile behavior independently verifiable.

Main (MethodDef 0x0600001d) calls BlockInput(true), the Defender-disable and
security-service-stop helpers, hosts blocking, UAC bypass and recovery deletion,
then self-replication, InstallPersistence and StartKeylogger. InstallPersistence
(0x0600002e) writes its assembly location to HKCU/HKLM Run keys, copies the image
to Startup, and launches schtasks with onlogon and recurring triggers. BypassUAC
sets the ms-settings shell command and empty DelegateExecute value, then starts
fodhelper.exe. The IFEO helper points taskmgr/regedit/msconfig Debugger values
at its own executable. These are attack operations, not API-name speculation.

StartKeylogger registers a low-level keyboard callback and starts a separate
GetAsyncKeyState loop over keys 1..255. The callback records timestamps,
window context and key values in a StringBuilder. FlushKeylog (0x06000032)
encodes its buffer and calls SendToC2 with a KEYLOG record. ContinuousScreenshot
(0x06000034) calls CopyFromScreen, saves JPEG bytes, Base64-encodes them and
calls the same helper with a SCREEN record. The HighLevelFileStealer state
machine recursively selects document/image/archive extensions, stages the first
1,024 bytes of each file and sends FILE records. Browser targeting separately
copies Chrome Login Data/Cookies and Edge Cookies; no credential decryption
was established by these copies.

SendToC2 (0x0600005a) appends the argument to local logs, constructs a WebClient,
sets a User-Agent and calls UploadString("http://synchrolife.io", argument).
The actual call instruction is at file offset 0x429c. Thus the helper's local
logging does not mean network transmission is disabled in this build. The new
multi-source rule requires three independent recording sources, WebClient and
UploadString references and the literal/argument-forwarding call layout. The
wildcarded layout alone is neutral metadata and cannot resolve the callee;
the composite describes file-scoped code clues, not a proven generic data-flow
analysis. Removing the send instruction while retaining all metadata disables
this profile on the reviewed sample.

## 286d0bf63df5: MALICIOUS, related .NET keylogger/ransomware

The namespace is ExtremeRansomwareBotnet; a campaign field says blackcat.
Neither establishes a recognized malware family. Main (0x0600001a) calls the
same classes of security disruption, persistence, surveillance and extortion
helpers. InstallPersistence writes the executable path to HKCU Run, copies it
to Startup and starts an onlogon task. The keyboard hook writes key values to
KEYLOG_FILE; its independent polling thread also appends keystrokes. Screenshot
capture saves JPEGs locally. The browser helper copies Chrome stores, and the
file collector stages selected file prefixes locally.

ContinuousDataExfiltration's MoveNext (0x060000a2) reads KEYLOG_FILE and CLIP_FILE,
caps the sent tails to 1,000/500 characters and passes keylog/clipboard records
to SendToC2 every 30 seconds. SendToC2's state machine (0x060000a4) JSON-serializes
the argument and posts URL-encoded form fields through HttpClient.PostAsync to
C2_URL, initialized to http://synchrolife.io. Existing input-exfiltration coverage
applies. Unlike the other variant, the inspected screenshot and document staging
paths do not feed this sender, so the new three-source WebClient rule must not
fire. These differences are covered by the static controls.

## Shared limits and rule cleanup

Both managed samples attempt to encrypt files inside Desktop/TestFolder,
writing a suffixed result and deleting the original only after EncryptAES
returns. Their UTF-8 key has 17 bytes and their IV has 15; set_Key throws before
the IV assignment, encryption or deletion, and the loop catches the exception. Keep
the existing *attempt* wording; do not claim successful disk encryption.
Input lockout, ransom notes, wallpaper changes and hostile surveillance remain
concrete independently of that defect. USB copies plus autorun.inf writes are
real spreading attempts; the fake PDF content does not establish a working
PDF exploit. Remote injection helpers use a trivial RET payload, so their API
profile does not establish a functioning injected backdoor.

Removed the duplicate `start-process::dotnet-hidden-process-launch` finding
and redirected its two exact YAML consumers to the existing, stronger hidden
startup setup trait. The old matcher only required ProcessStartInfo and the
CreateNoWindow setter, which did not prove a process launch. The canonical
trait also requires process-start/diagnostics/shell-execution configuration
context. No direct start-process directory selectors needed expansion; broader
process/create selectors still see the retained canonical setup finding.
The UploadString atomic description now explicitly says method-name reference.
No filename, domain, family token, exact size or hash gates the new detection.

Ten static controls passed: all three originals, an identically renamed PE,
four missing-source/API-name cases, removal of the actual send instruction,
and an ordinary WebClient source program. The new composite's test-rules
precision is 12.1; that authoring diagnostic is not proof of runtime behavior.
Final atomscan reruns retain at least two hostile findings on every original,
add the new profile only to the Chrome-named variant, and omit the retired
duplicate from all three.

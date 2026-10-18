# Reasoned review of three managed executables

All three verdicts are **MALICIOUS**, based on ILSpy C# and CIL recovery of
the supplied bytes. Samples were not executed. Atomscan classifications and
Triage scores were leads, not evidence. These are standalone PE assemblies;
no fetched dependency is involved. References below are method RVAs.

The assemblies contain many borrowed family names and deliberately created
mutexes/artifacts. Those names do not establish NanoCore, HiddenTears, or any
other recognized family. The code is unobfuscated apart from transport data
transforms; there is no concealed second-stage payload established here.

## 671396d0cd03 — Windows Update impersonator

SHA256: `671396d0cd03cc1e5ed393bc9e6548f07e70c7acb6d22d736dddee68de243ca2`

`NanoCoreFinal.Program.Main` (0x2910) obtains its own assembly location,
copies itself, writes startup and Run-key entries, creates a logon task,
installs an ms-settings/DelegateExecute fodhelper hijack, launches Defender
disable commands, and runs net user/localgroup commands creating a fixed
password administrator. Its unsigned version resource falsely claims to be
Microsoft Windows Update. These actions precede its debugger exit check.

The subsequent path marks the process critical, injects a small return stub
into notepad through remote allocation/write/thread creation, and starts
recording and command workers. HookCallback (0x21dc) records key codes with
timestamps/window titles. Other workers read changed clipboard text, capture
JPEG screenshots and VFW webcam frames, read Chrome/Edge stores, and enumerate
personal documents and secret-file extensions before calling SendFile.

StartReverseShell (0x39f4) connects a TcpClient to port 5555 and couples its
stream to cmd stdin/stdout with complementary reader/writer loops.
StartCommandExecutor (0x3c48) fetches commands and executes cmd /c, or reads a
requested file. SendToC2 (0x3c78) XORs bytes with the repeating key i XOR 0xaa,
then Base64/URL encodes the result into a GET query.

Limitations: the configured domain already includes `http://`, yet HTTP
helpers prepend another scheme and the TCP constructor expects a hostname.
Successful remote communication is not established. The main thread lacks a
GUI message loop, which may prevent hook callbacks. The PowerShell microphone
helper is not proof of working audio capture. AMSI/ETW and hollowing labels
are not implementations: the injection here is a remote thread, and no
AMSI/ETW patch was found.

Marker: `Windows Update impersonator: cover self-path persistence and file reads`

## edba0aca8f9c — custom .NET locker, chrome variant

SHA256: `edba0aca8f9c195b4d03c16b25cf46048c9d315b5dfa3cd75927b447c7396bcc`

Main (0x2188) creates hidden work directories, starts random mouse activity,
blocks input, disables security services, appends AV domains to hosts, invokes
fodhelper, deletes recovery snapshots, and installs IFEO Debugger hijacks.
It then attempts document-association hijacking, self-copy, persistence and
surveillance. InstallPersistence (0x3450) writes Run keys, a startup copy and
scheduled tasks. HookCallback (0x3720) records keys; the worker also polls
keys 1..255 every 50ms. Clipboard and screenshot workers record acquired data.
File collectors read personal documents and browser data, including copied
credential-manager files. USBWorm (0x3efc) copies the executable to removable
drives and writes executable AutoRun directives. BlockTaskManager (0x671c)
enumerates processes and kills taskmgr/procexp/processhacker targets.

RealEncryption's state machine, launched at 0x463c, attempts replacement only
under Desktop/TestFolder. EncryptAES (0x4680) assigns a 16-byte AES key and a
14-byte IV. The IV setter throws before any encrypted output or source
deletion. Ransom notes, wallpaper, input blocking, registry policies and
recovery deletion remain independent of that failed encryption.

IsPlaceholder (0x277c) unconditionally returns true: rotating beacon URLs
are empty. SendToC2 (0x5ff8) separately appends records locally and attempts
WebClient.UploadString to its literal, malformed-looking `.com2026` domain.
No successful transfer is asserted. Unhandled filesystem errors in the PDF
creation helper can terminate Main before its later workers start. Names
such as RansomwareSimulation and numerous family mutexes do not neutralize
the invoked input blocking, security tampering and extortion effects.

Marker: `Custom .NET locker (chrome): cover collection; consolidate USB traits`

## 4ea4dc29d007 — custom .NET locker, nano variant

SHA256: `4ea4dc29d007de56e9161e0bd29ae080fd8c1c9a5c9eebb47754e981f85223fb`

Main (0x7bd4) invokes the same core disruption, persistence and collection
helpers as the chrome variant. InstallPersistence (0x43ac), HookCallback
(0x4694), USBWorm (0x4dd8) and BlockTaskManager (0x7160) implement their named
operations. Additional code kills AV/analysis processes (0x791c), attempts
random appends to system DLLs, and creates a fixed-password administrator
account (0x79b4). These paths are inside Main's large try block: an earlier
failure can skip later invocations. Privileged operations require sufficient
Windows authority and compatible security settings.

ParseC2Url (0x28c0) sets an empty domain; IsPlaceholder (0x2910) always returns
true. SendToC2 (0x30c8) therefore logs locally and returns before encryption
or upload. Its encrypted beacons and DNS loop are likewise disabled by this
configuration. The separately invoked ping sends constant test data, not
victim secrets. RealEncryption (0x53f8)/EncryptAES (0x543c) share the invalid
14-byte IV and Desktop/TestFolder restriction. DumpLSASS only opens a process
handle and reports a status: there is no implemented LSASS memory dump.
The hollowing helper attempts suspended-process context redirection to a
NOP/RET buffer; it is not an established working replacement payload.

Marker: `Custom .NET locker (nano): cover tool killing; consolidate USB traits`

## Trait changes and controls

- Accept entry-assembly/location references as an alternative self-path form
  in managed keylogger Run-key persistence.
- Detect file acquisition records independently of the HTTP client, using a
  correctly scoped CLR GetFiles name observation instead of a source-only
  qualified method spelling. Collection does not imply successful sending.
- Cover keylogger co-occurrence with process-tool targets and termination
  APIs. The description deliberately does not claim resolved API data flow.
- Consolidate the two USB findings, requiring the union of self-copy,
  drive-type, AutoRun directive and file-write evidence.
- Relocate neutral `.encrypted` suffix and WLAN plaintext-query argument
  observations into filesystem/wireless capability homes. Preserve their
  matchers and scopes. Update the suffix consumer explicitly.
- The extension leaf was already at its 100-rule budget. Consolidate the
  redundant JS executable-suffix observation with the existing source suffix
  check. Its former literal matcher searched for call syntax inside a string
  rather than recognizing an ordinary endsWith expression. The C/Lua/Python
  objective consumer retains its own type scope; the JS grouping remains JS.

`check.py` runs 25 static positive and near-miss controls without executing
any PE. Required-role removals cover recording, self-path, file records,
enumeration, drive type and Kill. Neutral suffix/WLAN stubs cannot satisfy
the objectives; changing the HTTP class leaves collection intact. Two JS
controls cover the consolidated suffix observation. Matcher controls test
static evidence requirements, not specimen reachability or successful harm.

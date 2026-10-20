# Static review, 2026-10-19

All three supplied samples are **MALICIOUS**. Decisions below follow recovered
execution paths, not ML scores or family signatures. No sample was executed.
`atomscan` and `cleave facts` were run on every original file; managed CIL was
decoded with dnfile/dncil and the native program disassembled with Rizin.

## 7adde11b53416cd0ed45502ca8fa415d76d0fb647e50d2646385d3232482a4a8

Unobfuscated VB.NET XWorm client, with encrypted configuration. `Stub.Main.Main`
(RVA 0x227c) decrypts its settings using `AlgorithmAES.Decrypt` (0x5fa4): MD5 of
the mutex text, overlapping digest copies into a 32-byte key, Rijndael ECB and
Base64. Offline decoding recovers an external portmap.host endpoint, port 56058,
an install location of `%Public%`, and an executable install name.

The entry point checks VM manufacturers, Sandboxie and debuggers, adds Defender
exclusions, writes its own bytes into the install path, registers a one-minute
scheduled task and HKCU Run value, and creates a Startup shortcut. Its socket
receive callback hands complete received records to `Messages.Read` (0x38d8).
That routine AES-decrypts and splits commands. `plugin` / `savePlugin` dispatch
decompressed assembly bytes to `Messages.Plugin` (0x41a8), which loads the
assembly and invokes selected methods, including execution/recovery tasks.

`XLogger.HookCallback` (0x5ab4) translates low-level keyboard events with
ToUnicodeEx and appends keys/window titles through a StreamWriter. The
`OfflineGet` command reads that log and sends it to the operator. `$Cap` copies
the desktop, encodes a JPEG into a MemoryStream, compresses/Base64-encodes it,
and calls `ClientSocket.Send`. The DDoS handler fans out threads: its worker
(0x4b78) sends HTTP POST headers promising a 5235-byte body, sends no body,
sleeps 2500 ms, then disposes the socket. USB code copies the implant to
removable drives, hides originals and creates shortcuts chaining payload and
original-file launches.

The original VM-display finding was inaccurate: GPU enumeration (0x3164) is
separate from the manufacturer/model VM check (0x28ac). The rule now requires
virtual display-adapter names rather than generic VM vendors or Microsoft's
ordinary software renderer. The separate anti-analysis gate remains detected.
Added coverage recognizes keyboard recording, screenshot capture and Defender
exclusion commands in the existing plugin-backdoor context. The tasking rule
now requires receive and managed activation references; its mapping no longer
claims HTTP or a command interpreter from unrelated references.

## 893caa36f68a5a9ed4652a555c51c2208ba5273117f26190c303f7ef02967ea4

Native x86 StormAttack installer/injector; the collection filename does not
identify WannaCry. The entry point calls 0x401cb0. Its mode at 0x404120 is 3,
selecting 0x401900: register an HKLM Active Setup StubPath, read its own image
with CRT file APIs, patch/write a copy, and launch the copy. Cleanup at
0x401390 constructs `%COMSPEC% /c del <self> > nul` and launches the shell.

Other installation modes contain concrete malicious code: 0x401260 replaces
LanmanServer's ServiceDLL value, while 0x401150 creates a host process, allocates
remote memory, writes a DLL path, resolves LoadLibraryA and passes that address
to CreateRemoteThread. The resource-extraction path at 0x402460 attempts to
extract resource 101 of type DLL before installation/injection.

All 40960 raw resource-section bytes are zero, so this file cannot supply that
embedded DLL. Service hijacking/injection descriptions remain code profiles,
not assertions of successful installation or observed DDoS. The copied
Microsoft Authenticode material has a mismatching image digest; signer
cryptography does not authenticate the modified executable. Existing traits
already describe the surviving behavior and these limitations: no YAML change
was needed for this sample.

## d5bedc04623f0cb61357898579ee4d60e46c0206052bcc25b9bdf69e1f31097a

C# program self-named `NanoCoreUltimate`; this is not sufficient attribution to
the NanoCore RAT family. Main (0x7bd4) starts both keyboard-hook and key-state
polling recording, clipboard/screenshot/file collection, persistence, input
blocking, Defender/service/firewall disabling, recovery inhibition and policy
lockouts. The helpers contain actual registry writes/process launches, including
ms-settings/DelegateExecute + fodhelper elevation and IFEO Debugger redirection
of system administration tools to the program. These are not just API imports.

Browser helpers read Chromium Login Data and Firefox logins.json bytes; wallet
and Wi-Fi helpers also collect data. `SendToC2` (0x30c8) first appends its input
to local files. Its network path is disabled: `IsPlaceholder` (0x2910) always
returns true and `ParseC2Url` (0x28c0) leaves the domain empty. HTTP/DNS routines
therefore do not establish successful exfiltration. Existing collection traits
accurately report local acquisition instead.

The ransomware state machine (0x5208) targets Desktop/TestFolder, reads files,
calls EncryptAES, writes suffixed output, then deletes the original. However,
its UTF-8 AES key is 17 bytes and IV 15 bytes: setting those values throws
before output/deletion. Existing `managed-ransom-file-replacement-attempt`
correctly describes an attempt. Ransom notes, input blocking, malicious policy
changes and collection remain hostile even with broken encryption and disabled
C2. Existing traits cover this behavior: no YAML change was needed here.

## Checks

Run `python3 testdata/triage/managed-rat-review/run.py [cleave-path]` for two
virtual-display positives and two near misses (software renderer and separate
manufacturer/GPU inventory). New/expanded RAT composites were checked against
the first sample and `testdata/benign/keylog-dropper-controls.exe`. All three
originals were rescanned with this checkout selected through CLEAVE_TRAITS_DIR.

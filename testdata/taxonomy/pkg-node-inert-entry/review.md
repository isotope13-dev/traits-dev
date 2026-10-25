Static first review, 2026-10-25. No Windows specimen or recovered script was
executed. Each input received `atomscan --no-update --analyze local --mode slow
-f json` and `cleave facts`, followed by final local scans of the entire input,
including both embedded PE members of the larger file. Raw reports, facts,
Rizin/Capstone disassembly and forager provenance are retained under
`/usr/local/var/cyclotron/tmp.noindex/cyclotron-e78afdd4/scratch/review`.

| Sample SHA-256 prefix | Identification and judgment | H before/after | S before/after |
| --- | --- | --- | --- |
| 67454523cf4e | Inert PE carrying a serialized V8 cache; BENIGN | 1 / 0 | 1 / 1 |
| c6a9e7f74907 | Another inert PE carrying the same cache structure; BENIGN | 1 / 0 | 1 / 1 |
| b2f5a428690e | Modified XMRig self-replicator with embedded Go downloader and Beacon; MALICIOUS | 5 / 8 | 6 / 7 |

Counts include every analyzed member, rather than only the originally flagged
member. For b2f5a428690e, the outer PE changes from H1/S1 to H4/S2; the Go PE
at 0xbce00 remains H0/S0; Beacon at 0x579001 remains H4/S5. No archive or
embedded-member detection was lost.

The two small files have a single mapped .text section with virtual size one,
containing RET at file offset 0x200 / RVA 0x1000. Their import, export, TLS,
CLR and other data directories are empty. Rizin confirms the entry returns;
there is no native Node runtime, alternate callback or entry-to-overlay path.
The unmapped overlay starts at 0x400 and contains a V8 code-cache header
`28 06 de c0 74 fe da 79`, serialized bytecode and its constant pool. It names
child_process, execSync, decryptPayload, writeFileSync, spawn, ./payload and
./ui/shell, but carries neither the required runtime nor these sidecar modules.
Changing the C:\snapshot source pathname does not supply execution.

The cache's Base64 string decodes to a hidden, no-profile PowerShell command
that uses Add-MpPreference -ExclusionPath for TEMP, ProgramData and two
Microsoft/Windows subtrees, then runs gpupdate /force. This is real embedded
security-control command content; the encoded-PowerShell suspicious finding
and all command/path observations remain. The unsupported claim was that this
RET-only executable runs Defender evasion. The balance of evidence supports
BENIGN inert carriers, regardless of whether their cache originated in a
malicious application. Deployment provenance and the carriers' author's
purpose are unknown; their native execution behavior is established.

The hostile pkg composite was moved from C2/dropper/staging/runtime to
evasion/anti-av/exclusion, since its required evidence establishes no staging
or command channel. Its required observations and hostile severity remain;
the existing precise RET-entry/no-TLS/no-exports observation now excludes
inert carriers. No exact-ID or ancestor-directory consumers selected the
moved composite. A separate TEMP/TMP exclusion-option atom moved to
micro-behaviors/os/security/defender with its regex, scope, confidence and
notable severity unchanged. Its description now states option content rather
than a successful modification. Its two exact consumers were updated; there
were no ancestor-directory consumers requiring preservation. An option alone
does not support the previous inherited T1562.001 mapping.

Before narrowing, the original pkg dropper was recovered with forager by
SHA-256 838c1ecdf14a81a602f8424c3d3d9c6760505ba7f809bfc2645a66cd3b53f1cd.
The original bytes hash correctly and retain .forage.json provenance. This
117,315,002-byte Node 22.23.1 executable has a real runtime, pkg virtual
filesystem, payload module and assets. Its cache has the same header and
function/command structure, with different serialized string hashes and source
pathname. It retains H2/S3 after the corrections, including both hostile
Defender composites. Its raw ML probability changes 0.92289627 to 0.9199581.
Thus the false-positive correction preserves actual attack coverage.

The larger file's ordinary-looking XMRig code is modified at native main
0x14002add4. Following CRT startup reaches a mutex guard and then a self-read
through fopen(argv[0]), fseek/ftell, malloc and fread. At 0x14002aee5 the last
two DWORDs become descendant depth and fan-out. The code decrements depth,
constructs random executable names below C:\Windows\System\, copies its own
image minus the old trailer, appends generated padding and both counters,
closes the output and converts the same RDI pathname for CreateProcessW at
0x14002b01d. Its backedge at 0x14002b03e rechecks the decremented depth before
writing another copy. The actual footer DWORDs are 1,982,999,274 and
171,785,553, both positive signed values: this requests extraordinary
replication and disk/process exhaustion, irrespective of runtime permissions
or whether the first output succeeds. The existing pool configuration and
CryptoNight implementation support the retained miner observation; embedding
them in this self-replicator supports cryptojacking. Ordinary user-directed
mining cannot explain the replication path and huge fan-out.

The existing replica-layout YARA atom gained a UCRT-import compiler variant.
Its first two alternatives are unchanged. The new alternative binds the
self-read to fread, three writes of the same stream to the fwrite IAT,
the output pathname to CreateProcessW, and the backedge to the depth check.
Relocations, generated pathname, padding stride, pool and footer counts do
not identify the routine. Existing objective consumers now detect replication,
million-copy disk impact, and mining in the replicator without new duplicate
behavior rules. The neutral linked-launch atom remains suspicious.

Beacon is a complete 206,848-byte x86 DLL with _ReflectiveLoader@4. Its
XOR-0x69 settings table at file offset 0x2f228 decodes to a five-second sleep,
port 443, ns7/ns8/ns9.softline.top endpoints, an RSA public key, GET/POST
transforms with Amazon-themed Host/URI camouflage, and syswow64/sysnative
rundll32.exe spawn paths. Token-handler code at 0x10009d22 opens an operator
selected process, opens its token, impersonates it and calls DuplicateTokenEx,
retaining the duplicate for subsequent commands. Remote-memory write,
CreateRemoteThread and thread-context code were also inspected. The existing
four hostile and five suspicious Beacon findings are supported and unchanged.
The container does not establish that every embedded Beacon operation runs
on launch; no such claim was added.

The embedded Go program has retained COFF function labels and DWARF source
references. Capstone tracing of main.checkForAdmin, main.main, GetArchive and
Extract shows a PHYSICALDRIVE0 open as the privilege test; a non-admin path
requests ordinary UAC consent with PowerShell Start-Process -Verb runAs.
The privileged path uses a TEMP marker, downloads an S3 ZIP, extracts it into
`C:/G DATA Security Software/`, removes the downloaded ZIP, and starts AVK.exe.
This is staging and execution, not proof of a UAC bypass or independent
credential theft. Existing notable HTTP, ZIP, process and elevation findings
remain. A forager attempt to recover that remote ZIP returned HTTP 404; the
final downloaded application's content and the link between the appended Go
and Beacon stages remain unknown. The supplied Triage web page was
inaccessible. The malicious judgment rests on native replication and decoded
implant evidence, not sandbox labels or the collector-chosen filename.

Regression evidence: 15/15 original-layout controls passed against recovered
SHA-256 717edd476aad82fe7e03719313b3ae4e6287dee36905797e41efeffe39bc8d12;
15/15 inline-layout controls passed against recovered SHA-256
9c36ca6010a751df590bd7dbe026fbd45e5d9a9bdd87ed0b0ac8103e1fb16724.
Both were recovered with forager and verified by hash. The added UCRT suite
passes 16/16 actual-specimen and broken-flow controls. Seven pkg/option
controls pass, including both renamed inert carriers, the recovered original
dropper, positive TEMP/TMP options and query-only near misses. No specimen
was executed. The two new scripts take --sample/--inert, --positive and
--scratch arguments; the earlier scripts remain unchanged.

Final local model bundle v18.18 reports raw probabilities 0.9223401 to
0.9019544 for each inert carrier and 0.995 to 0.995 for the malicious bundle.
The calibrated ML level stays -1 for each carrier and 25 for the malicious
bundle. Thus this local calibrated run does not reproduce the queue's
historical HOSTILE ML label on the inert inputs, although their raw scores
remain high. The retained encoded-command suspicious rule is accurate;
removing it to force an entirely clean report would erase real content.
There is no malicious-sample attack detection loss or unresolved hostile
coverage quota: three additional hostile behaviors now cover the outer
replicator, and the embedded implant's four hostile findings remain.

Judgment marker contents, copied verbatim:

```text
Inert V8 cache PE: RET-only entry; fix Defender execution claim
Inert V8 cache PE: RET-only entry; fix Defender execution claim
Modified XMRig: replica disk bomb and Beacon; extend loop detection
```

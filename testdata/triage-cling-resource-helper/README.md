# Static review: Sleipnir, Cling and res.dll

Each original was scanned with atomscan and cleave facts, including extracted
and decoded strings. The verdicts below follow the requested requirement for
independently established hostile behavior. They do not grade the safety of an
entire distribution from a single module. No original, downloaded installer,
PowerShell payload or native DLL was executed.

| SHA-256 prefix | Identification | Verdict |
| --- | --- | --- |
| 824dab563091 | Sleipnir 3.23, PS2EXE performance utility | BENIGN |
| 3a6927a3399f | Cling MIPS little-endian IoT bot | MALICIOUS |
| a27cafb84876 | res.dll, native network/UI and companion-call helper | BENIGN |

## Sleipnir

dnfile/dncil inspection identifies a conventional PS2EXE wrapper. Entry token
06000072 creates a PowerShell runspace, gets the resource Sleipnir.ps1, reads it
as UTF-8 and supplies the resulting value to AddScript. It also supports writing
the resource to disk. The 364,937-byte resource is readable PowerShell; there
is no additional encrypted executable or hidden loader in that resource.
The large native resource section contains ordinary icon data.

The script implements an actual WPF settings utility. UI button handlers invoke
individual tweaks or preset profiles. Invoke-TweakApply reads current state,
saves it as JSON, applies a change, reads back state and records the result.
Reversion uses the saved state. A separate warning precedes the most aggressive
profile, which disables hypervisor and CPU vulnerability mitigations. Gaming
profiles add Defender exclusions for installed game directories and named game
processes. Those are real security changes and remain notable. Service stops,
startup-item editing, cache deletion, registry changes, process termination,
driver installation and restarting also remain observable capabilities.

Run-key paths belong to startup management, not self-installation. The
FromBase64String call restores previously saved binary StartupApproved data.
The credential dialog and keyboard functions are wrapper host/UI support,
not a demonstrated keylogger or credential stealer. No exfiltration or remote
command listener was found. The IRM/IEX example includes a comment and an
elevation branch whose configured URL is a REPLACE-WITH placeholder; that
branch explicitly rejects the placeholder. The compiled executable requests
administrator consent in its manifest.

The only concrete external download destinations in the script are GPU vendor
sites. NVIDIA resolved to its driver page; AMD resolved to its incomplete
download help page; Intel returned HTTP 403. NVIDIA/Intel silent-install paths
require a valid Authenticode signature, the expected publisher and a restore
point before launching the download. No fetched executable was available to
analyze or run. No package dependencies or working script-host URL were found.

PS2EXE, self-issued signing, Defender exclusions, execution-policy bypass,
service changes and aggressive performance settings plausibly explain generic
Lazy/ML detections. Those detections supply no additional hostile execution path.

## Cling

Rizin disassembly establishes the following reachable chain independently of
the family label:

* Startup at 4001b0 allocates a 66-entry pointer/length table. Calls to 404ac0
  populate it from encrypted read-only data.
* 404ac0 builds a standard ChaCha20 state with sigma constants, a 32-byte key,
  a 12-byte nonce and counter zero. It runs ten double rounds using the
  402650 quarter round and XORs the serialized blocks into table entries.
  The rotation schedule is 16, 12, 8 and 7. The reproducible decoder is
  decode_cling.py; it does not execute the ELF.
* Decrypted entries include wget paths, self-executable access, moving the
  original wget to a .r sibling and a .p forwarding path, copies into hidden
  executable locations, init-script append commands and a bind mount hiding
  /proc/<pid>. These are not inferred from ciphertext entropy.
* 40469c reads the forwarding path, forks and invokes the real wget with the
  caller's argv. Its other branch moves/copies the original utility and
  installs the replacement. Main uses init commands and the hidden copies.
* 4030e4 constructs and sends a 20-byte STUN Binding request: a type/length,
  cookie 2112a442 and a zeroed 12-byte transaction ID. It parses mapped ports.
  The decrypted endpoint table contains thirteen servers; neither those IPs
  nor this build's cipher key are required by the new detections.
* The main receive loop copies packet words at offsets 8, 12 and 16 into the
  command record, then interprets the first transaction byte as an opcode
  from 1 through 8. Paths implement command retrieval/execution, scanning,
  tunneling/relay and flood tasking.
* The task handler at 402324 extracts the target, port, mode and duration,
  forks worker processes, chooses packet-sending functions and kills/reaps the
  worker after the supplied duration. At 40362c, the TCP send worker repeatedly
  sends a 1,000-byte buffer; additional workers implement other flooding modes.
* The scanner at 403bf4 formats decrypted request templates and sends them to
  candidate devices. Recovered payloads include Realtek diagnostic command
  injection and HTTP /shell, shortcut_telnet.cgi and device.rsp command injection
  with downloader/chmod/execution commands. This is propagation, not merely
  a vulnerability name or scanner banner.

One decrypted table entry (index 59) is malformed; the other independently
verified paths suffice for the judgment. The primary
[Nozomi analysis](https://www.nozominetworks.com/blog/a-stunning-disguise-cling-malware-masquerades-as-google-)
corroborates the family and protocol interpretation, rather than establishing
the verdict by itself.

The new hostile traits require STUN construction plus transaction-ID command
dispatch, and that control channel plus a packet-flood loop, respectively.
The atomic cipher, packet parsing and send-loop traits remain neutral. Instruction
patterns tolerate relocated calls, renaming and key changes.

## res.dll

PE inspection and full .text disassembly show three exports: Activate,
InitializeNewSession and DispatchNetworkChain. The HHD Software Device
Monitoring Studio version resource is a provenance claim, not a trusted
identification of these functions.

The CRT entry calls DllMain at RVA 1144. On process attach, that function starts
a thread through RVA 113c into Activate at RVA 1000. Activate initializes COM,
queries system information/current directory and repeatedly passes the current
PID to the imported ElementBlend function in senddmp.resources.dll. An outer
1,680-iteration loop sleeps 49 ms; a nonzero callback result also enters an
812-iteration callback loop with 29 ms sleeps. This automatic companion call
is real. The callee's implementation is not present in the supplied file.

InitializeNewSession constructs STL state and a TCP socket, converts a
caller-provided address/port and calls listen. The constructed sockaddr is not
passed to bind/connect. DispatchNetworkChain primarily manipulates containers,
draws via GDI and calls MCI functions. Neither export provides a demonstrated
remote receive-to-execution path. There is no payload buffer decryptor,
remote-memory write or execution-transfer API in the supplied module.

The apparent extra MZ constant at RVA 279f is part of a RIP-relative call
displacement, not PE parsing. The actual MZ/PE checks at RVA 6894 are CRT
image-section validation. The FNV constants occur in container hashing, not
a recovered API-hash resolver. GetDC without pixel acquisition is not screenshot
collection. These findings refute the initial import-resolution/loader lead.

[Forescout](https://www.forescout.com/blog/romulus-analysis-of-a-new-multi-payload-clickfix-delivery-platform/)
and [Huntress](https://www.huntress.com/blog/chatgpt-custom-gpts-clickfix-rat)
place this exact hash in a malicious installer chain and identify its companion
as an allocation/execution helper. This explains the external malware label,
but is not an independent recovery of the missing callee or a hostile effect
in this module. The judgment therefore follows the task's otherwise-BENIGN
threshold. It does not declare the surrounding installer benign.

Attempts to fetch the reported installers from both 86.109.75.7 and
96.62.224.81 timed out. The public sample retrieval attempts returned
HTTP 401 (MalwareBazaar) and 403 (Triage). No hostile dependency bytes were
obtained. No credentials were used or requested. A mere unsigned res.dll name
plus a .resources.dll reference cannot replace that missing behavior.

## Trait corrections and controls

* PS2EXE host class fingerprints move from process creation/masquerade to
  managed compiler provenance. The composite becomes notable.
* ScriptBlock construction moves out of WSH; credential prompts move out of
  verification; WPF/Process type references become framework references. Run
  key paths move out of installer-specific keys. Hyper-V reference descriptions
  now state the vocabulary match.
* Administrator checks and ordinary RunAs requests move to neutral privilege
  homes. Existing exact consumers follow the move.
* Generic -Value 1 and /d 1 fragments move to process argument options, without
  pass-the-hash mappings. They are components because neither is an operation
  without the surrounding command.
* Microsoft security product-name references move to security-product vocabulary.
  They no longer imply that the analyzed file claims that identity.
* Embedded IRM/IEX pipeline text moves to neutral deployment. Its native
  dropper consumer retains its independent attack-context requirements.
* A resources-library name moves to the library-path reference home. The
  filename/unsigned/sibling-name-only hostile composite is retired.
* MZ detection requires immediate-load instruction forms instead of counting
  matching bytes inside RIP-relative call displacements.
* MIPS socket create/bind/listen, execve and process-signal wrappers move to
  their actual operations. The generic LE syscall atom requires an immediate
  syscall-number load, eliminating its unaligned-byte lead.
* The exec leaf was audited before admitting MIPS. Its existing overlapping
  Perl shell-exec patterns were consolidated with their carrier scopes retained;
  full execution remains notable. Equivalent endian forms of one MIPS execve
  operation share an alternation matcher. The directory stays at 100 rules;
  no taxonomy branch or budget was invented.
* Exact references follow relocations. Broad objective selectors intentionally
  lose neutral observations. Existing syscall aggregates retain their moved
  operation members through explicit references. No new family rule is keyed
  to a filename, address, cipher key or exact file size.

Run check.py with the sample-root path. All twelve static cases passed. It
verifies hashes and exercises
originals, a renamed DLL, a renamed/rekeyed ELF, separate missing-cookie,
missing-command-word, changed-send-loop and changed-rotation controls, ordinary
settings/UAC consent, and overlapping Perl shell-call spellings. No sample
execution is part of the tests. Atomscan is rerun on all three originals;
verified final coverage is two hostile traits on Cling and zero hostile or
suspicious traits on both BENIGN files. Final repository validation follows
the judgment markers.

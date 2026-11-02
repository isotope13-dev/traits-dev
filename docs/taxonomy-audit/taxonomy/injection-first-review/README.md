# Injection branch review

Six legacy subtrees were reviewed by required evidence. Suspended-child APC and section-map/thread-context injection moved to payload execution; an in-process mapping hook moved to the image-map sink. The unsigned version-proxy and API-table combination moved to DLL proxy masquerade. System32 filename references moved to path evidence without labeling the names as injection targets.

Object callback registration and cross-process memory APIs are a driver capability profile; a separate compromised-signer combination remains a hostile code-signing-bypass finding. Atom-table readback plus APC scheduling is an API profile, not proof of atom-bombing; adding a hard-error API reference does not prove a crash. The surveillance combinations retain their stronger collection findings while their names and technique tags describe the evidence.

One existing positive hosts-file sinkhole composite references the entire payload-injection directory. It can now also match the moved APC and section-map findings; those are relevant injection evidence, and the composite still requires an unsigned executable, a hosts-file path and security-vendor localhost redirects. No exclusion directory was broadened.

The PHP procfs shellcode case now separates the interpolated memory path and shellcode write from their likely injection combination. The atom/APC building block is a component, while the hard-error and kernel callback API combinations are notable profiles of independently observable references.

The remaining procfs rules were reviewed by their required evidence: process-memory and environment paths, file-search commands, and injector-related identifiers moved to their observed subjects. Process-memory open plus maps, ptrace and names, and a memory path plus XOR bytes remain evidence profiles rather than confirmed injection. The Lua-search/backdoor-text combination is a suspicious script profile. A Perl LD_PRELOAD composite repeated an environment path already required by its atomic rule and was retired as redundant. The legacy procfs subtree has no remaining rules.

The ptrace subtree was reviewed by required evidence. Calls and attach observations moved to debugger control or attachment; ptrace policy and process-memory paths moved to path observations; function names moved to source naming; and unbound memory, debugger, or identifier combinations moved to evidence profiles. The profiles no longer claim a policy change or injection from paths and references alone. No live YAML references to the retired ptrace namespace remain.

The callback subtree was divided into likely callback deployment, admitted obfuscated local-buffer payload execution, memory and API profiles, and individual API observations. A timer API/resolver combination no longer asserts shellcode execution; its CBC-resource consumer now names the evidence. Thread context API references and their Go trading-type consumer were moved to evidence profiles, without calling ordinary type names a decoy or asserting injection.

The injection toolkit review separated PoolParty module names into an injection-tool reference profile, Cargo feature declarations and unbound API combinations into evidence profiles, Python DLL helpers into the DLL capability, and a KDU mapping command plus detached-injector log into driver exploitation. Their original file-size and section matching scope is preserved. The toolkit general and compatibility files remain.

The toolkit general leaf was retired: assembly call/pop and register-label text now use instruction subjects, managed split-name and thread API combinations use evidence profiles, the APC chain and module-stomp marker use their mechanisms, and a tiny managed layout uses complexity metadata. Two obsolete sentinel strings and the findings depending exclusively on them were removed; an optional sentinel leg was removed without changing its three-evidence threshold. An unused catch-all of unrelated benign tools was retired because its members already have identity rules.

The thread-hijacking review moved DNS-tasked instruction-pointer rewriting to the DNS command channel, remote-write and thread-context combinations to the injection mechanism, and PE context or API combinations to evidence profiles. Descriptions now distinguish instruction and API evidence from proven payload execution. The RC4-resource/thread-context composite moved to payload process injection. A follow-up count found 48 existing rules there; the earlier estimate of 158 incorrectly included nested references, so the directory was not near the rule cap.

Module-stomping rules were split among a staged-shellcode execution finding, an in-process section-map substitution, and memory or DLL evidence profiles. Encoded API names moved to Base64 metadata, with their named process-hollowing combination retained as a payload finding. Harmony-specific reference combinations moved beside Harmony, and debugger/remote-memory API combinations became evidence profiles. Empty legacy subtrees were removed.

The GOT hijack source rules now distinguish named variables from likely code-cave/GOT injection; the Windows hook rules separate loader messages from a likely game-targeting hook; and the XLL and WoW64 combinations moved to payload execution and remote-thread capability respectively.

The iOS branch was divided into named Substrate, Cycript, RevealServer and CBInjection references and neutral mobile profiles. Short or placeholder bundle names and invisible display-name characters moved from masquerade into mobile configuration metadata. A nanopb/CBInjection co-occurrence no longer claims a trojanized library.

The legacy DLL-injection branch was split by remote-thread, DLL-loading, process-discovery and payload behavior. Generic API lookups and naming combinations moved to capability or evidence profiles, and misleading Python DLL-hijacking aggregates and a synthetic sentinel were retired. A shared Go remote-thread API triad moved from the staged legacy namespace to its mechanism.
 The Eldritch fixture is a library wrapper exposing caller-supplied DLL injection and other system functions; it was reclassified as suspicious because it contains no independent attack target or payload.

The staged-injection review moved executable process-parameter pivots, host-reporting injection, and HTTP/decryption remote-thread combinations to payload execution; related API combinations, shared-memory naming, and PE/resource co-occurrences moved to their mechanisms or evidence profiles. The staged tree retains the direct-syscall PE profile and the broader reflective-Windows review.

The remaining staged rules were split into executable image-map and process-injection evidence, PE loader profiles, Go library-build clues, byte-array fragments and naming observations. The zero/outlying timestamp and low-import/non-resource-heavy helpers moved from evasion to binary metadata. The legacy staged tree has no remaining rules.

The native branch review moved WinInet/AutoIt API evidence to remote-thread capability and the silent SFX combination to payload process injection, an IIS PE-loading combination to image mapping, a shim-specific signature to its injection mechanism, and SQLite/native-memory API co-occurrence to a PE profile. The remaining native files need named-family, XOR and shell-byte review.
 The hosts-file composite already referenced the whole payload-injection directory, so its narrower SFX leg became redundant and was removed.

The remaining native branch moved RedShell-specific command grammar and behavior to the named family, generic dlopen help to an observation, and XOR-concealed diagnostics to runtime string decryption. Partial shell-related byte sequences now describe the bytes they actually require; the containing PE profile retains the original conditions with its single-use grouping helpers inlined. Cleave has an exact-ID, exact-matcher exception so the RedShell reference retains whole-file, unbounded coverage.

Runtime-injection rules were divided among in-memory execution, remote process injection, reflective image mapping, inline hooking and evidence profiles. SHA-256, ctypes wrappers, UUID decoding and API names no longer by themselves claim execution; PowerShell and Python rules with complete execution chains retain their behavior.
 The existing hosts-file sinkhole selector references the entire payload process-injection directory and therefore also admits the newly moved remote-process findings; its separate hosts path, security-vendor redirect, and unsigned-PE requirements remain in force.

The VB6 branch was split into native-call capability and evidence profiles. Generic process APIs and an ISO memory-API cluster no longer claim injection or VB6 identity; a generic external endpoint moved out of C2.

The memory-injection review moved the concealed HTTP/decryption and Mach process-write combinations to process injection, while Go WebSocket, NT API and PE-layout combinations remain evidence profiles when their inputs do not establish the claimed downloader or injection. The service-host symbol and moka.dll text are observations rather than service masquerade. The payload-injection directory selector in the hosts-file sinkhole composite also admits the newly moved findings, subject to its other requirements.

Manual export-table evidence moved out of process injection and into an API-resolution subtree, alongside existing PE export-reading rules. Descriptions distinguish field references and labels from established parsing. The signed embedded-PE profile previously accepted any rule in the entire manual-resolution directory; it now requires specific native export-table traversal or API-name comparisons, so the newly added field and label observations cannot trigger it alone.

The remaining RWX review separated debugger checks, process-write/resource API evidence, filename/PDB mismatch context, hotpatch evidence and a source path. The hotpatch name does not itself establish a byte array; the debugger-guard combination does not establish that the debugger check is concealed. Existing inline patch patterns were grouped with the hotpatch finding instead of adding to the crowded interception directory.
 The crowded interception sibling was also divided by moving browser API, DOM and window hooks together; exact consumers follow the moved traits.

The Go-obfuscated and Windows loader-suite review moved explicit remote-thread diagnostics to process injection, probable memory staging and PE-loading combinations to their execution behaviors, and thread-control, allocation and byte-reassembly clues to their capabilities. The descriptions no longer infer Go identity, injection, or an embedded payload from weaker clues alone. Garble-dependent combinations remain under garble with their memory and process context; each requires the existing garble finding. The hosts-file sinkhole's existing whole-directory process-injection selector also admits the moved remote-thread diagnostic, subject to its other conditions.

The C# memory-injection branch now separates injector and shellcode naming observations, DLL lookup, source-level remote-memory API combinations, and the stronger shellcode injection findings. The generic NtWriteVirtualMemory and NtProtectVirtualMemory names and competing write symbol moved out of AMSI and hollowing objectives into memory capabilities. The existing hosts-file sinkhole selector covers the newly moved process-injection findings as well, with its other requirements unchanged.
 A separate suspicious capability now combines the shellcode declaration with remote allocation, write and thread APIs, preserving the VS Code fixture signal without treating the variable name alone as suspicious.

The remaining `hollowing/process` branch was moved to
`objectives/execution/payload/process-inject/hollowing/process` after reviewing
its 69 rules as process-image replacement chains and components. The already
crowded `process-inject` root (84 rules) was organized into technique leaves
for remote-thread, DLL-load, memory-transfer, image-replacement and APC rules;
each leaf is below 80. A redundant exact RunPE selector was removed because
its clause already selects the complete process-injection directory. Runtime,
source and shellcode branches remain under review.

The remaining hollowing runtime and source siblings also moved under
`objectives/execution/payload/process-inject/hollowing/{runtime,source}`. The
complete hollowing branch now has 129 rules in three leaves (69 process, 46
runtime, 14 source), each below 80; the old `evasion/process/injection/hollowing`
namespace is retired. The shellcode branch is the remaining active portion of
that legacy namespace and still needs sink-by-sink review.

The shellcode branch was also split by what the rules establish: register-call
and register-jump patterns moved to binary control-transfer metadata; loaded
module text writes followed by a local thread moved to the memory-branch sink;
remote-process shellcode indicators moved to the remote-thread sink; and the
Signal SQLCipher addon path moved to Signal product identity. The remaining
raw-byte, self-execution, and loader branches still need sink-by-sink review.

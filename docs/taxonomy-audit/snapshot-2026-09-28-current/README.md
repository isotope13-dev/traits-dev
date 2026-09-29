# Current taxonomy audit snapshot — 2026-09-28

Regenerated 2026-09-29 after the archive and HTA sink review. This inventory measures the shared working tree with the uniform inclusive cap
of 100 atomic and composite rules per directory. It has no directory exemptions.

The catalog contains 21,098 YAML files and 118,855 rules
(79,365 atomic and 39,490 composite), across
8,713 rule directories. 71 directories exceed the cap,
containing 8,835 rules and 1,735 rules of excess.
The violations are in 70 `objectives` directories
and 1 `well-known` directory. No rule
directory exceeds depth five. Sparse sibling review uses the
35-rule threshold.

Compared with the preceding 85-rule inventory, this is 143 →
71 violating directories and 3,768 → 1,735 excess rules. Sink corrections in the encrypted-staging cohort moved 29 existing rules
without changing matcher bodies or weakening the conditions. The install-hook environment-secret source move relocates three
composites to their documented source-based home. The TCC classification audit
also moved three composites from memory staging to TCC database manipulation.
Four PowerShell AppDomain chains now live under the runtime `module-load` sink.
The GitHub image-suffix URL clue now lives with neutral HTTP URL evidence; its
two Assembly.Load composites live under the module-load sink.
Two reusable Swift Base64 and Zig shell-argument observations now live in their
capability leaves instead of the anti-static encrypted-payload leaf.
The Swift check-in field marker and its path-corroborated composite now live in
the beacon-format leaf; a path-only clue moved to filesystem path capabilities.
The final three legacy stealer/sweep entries were individually resolved: two
unsupported hostile composites were retired while their capability/channel
signals remain available, and the native credential snapshot composite now
requires source, transfer, and tunnel clues within 128 bytes.
The install-hook cohort moved nine cloud-credential-query rules to
`credential-access/cloud/token/metadata`, routed host-profile evidence by
source and result, and moved cloud provider endpoint references to provider-specific HTTP service
metadata leaves, placed request headers with HTTP headers, and moved the local
GCP credential filename to credential paths. The legacy `supply-chain/recon-exfil/install-hook` leaf
is 178 rules and remains under review. Its combined-cap excess is now 78 rules.
The hidden-payload runtime pass moved three npm composites to reverse-shell,
dropper-pipe, and webshell leaves, plus two supporting Node webshell composites;
the runtime leaf is now 188 rules.
The `dropper/execution` audit inventories 1,749 remaining rules in 41 leaves.
The legacy `exec-download` leaf is empty after archive and HTA rules followed
their required download, process-creation, persistence, file-write, decode and
obfuscation subjects.
The batch pass moved neutral download/process aliases, removed a
misplaced fallback exclusion from BITSAdmin transfer evidence, and routed
architecture, certutil, TEMP and LOLBin profiles by required operation. The
Python/Startup split preserves the original match union; the batch legacy
leaf is now 95 rules. The former HTA/WSH file has also been retired.
The final Ruby `script` cluster and its adjacent update-module path profile
now report neutral HTTP and process-launch context; the `script` leaf is empty.
The mixed Winsock/TEMP profile was split into three exact alternatives;
VM-artifact evidence left debugger-check so that sibling did not grow.
The URLMon stack review placed six stack-string/path atoms and two
co-occurrence profiles in neutral leaves, the Defender-exclusion profile in
Defender evasion, and the distinctive `.zero`/CRC32 delivery signature with
Phorpiex. Seven AMSI composites and one Go injection rule left the oversized
Defender sibling; its 125 remaining rules still require review.
The legacy `execute-download` leaf is empty after routing its final fifteen
rules by the supported activation sink or neutral co-occurrence. Adjacent
supply-chain consumers no longer assert an unbound download-to-execution link.
The adjacent sixteen-rule `download` leaf is also empty after routing macro,
Perl, Python, Ruby, and miner evidence. Seven XMRig command-line argument
rules moved from miner runtime to configuration, resolving that sibling's cap
violation without a language partition or cap exception.
The first nine-rule `exec-download` cohort moved by its actual interpreter,
process or shell evidence; two nearby PowerShell delivery composites now state
their supported IWR/TEMP staging rather than an executed-payload claim.
Three AppData/hidden-process and temp-cleanup profiles then left that leaf
after their unbound payload-execution claims were corrected.
PowerShell decode/write/start, MSI install, native URLMon and managed
HTTP/ZIP/process profiles followed their supported operations, reducing
`exec-download` to 75 rules.
C#, .NET and PowerShell assembly-load chains and VS Code and PyInstaller eval chains moved
to their activation sinks. A Werfault identity rule whose matcher lacks a
staged-code activation sink moved to masquerade; an unrelated copy-plus-HTTP
co-occurrence objective rule was retired. Two Python stdin-interpreter rules now
describe a neutral capability. Three inert loader sentinels and their unreachable
family consumer were removed. Shared-tree edits outside this cohort also changed
the total counts since the preceding snapshot; the global excess change must
not be attributed to these moves alone.
The BOF host API names and runtime cluster moved to a neutral BOF capability
leaf. Their generic COFF import-pointer clue moved to linker facts with a
working prefix matcher; the BOF composite keeps its four-of-nine threshold.
Seven Ruby operation observations moved from the obsolete `ast-script` carrier
leaf to neutral HTTP, decode and filesystem leaves. Four previously inert
receiver-qualified matchers now use syntax queries and match intended Ruby
calls.
The legacy `rename-exec` leaf is empty after resolving its redundant unions,
unsupported download claim, command-execution rules and extconf-context
consumers. Synthetic Ruby and Alpine apk checks preserve the supported
rename-and-command findings. The PyInstaller bytecode audit relocated its
capability clues and removed an unsupported encrypted-.NET-load claim; a
three-rule Rust cluster lacking a download-to-spawn link was retired.
Twenty VB6 loader composites moved to their required capability, staging,
hosts-redirect, obfuscation, or command-execution leaves. Their original
matching clauses were checked against the relocated rules.
The Dark Eye wrapper moved to its family signature, two duplicate section
matchers were consolidated into metadata, and two duplicate WSH ProgID-prefix
matchers became one neutral COM observation. A signer/embedded-PE profile
moved to obfuscation; a Node respawn cluster moved to process lifecycle; an
unsupported Nemucod date-evasion dropper verdict was removed after its
required conditions were inlined into its only consumer. The Elex family
candidate remains for sample-backed section/size scoping.
The legacy integrity and misextension leaves are now empty: SHA-256 context,
runtime-install helper names, COM text, Base64 text and WebClient clues moved
to their neutral homes without changing the atomic matcher bodies.
Three JVM self-relaunch profiles moved to neutral process lifecycle; an
unsupported handoff verdict and its unshared method-name atom were retired.
Go/PowerShell, native DNS TXT, LuaJIT FFI/runtime and JavaScript terminal
launcher contexts moved out of legacy source, DNS, sidecar and launcher
labels. Their retained matcher conditions were compared with the originals.
The legacy `loader` leaf now contains exactly 100 rules after routing its
minizip, IEExec, C# temp-write, Delphi overlay, .NET reflection, resource,
Petite and Gentee evidence to their supported homes.
The first SFX installer pass routes RunProgram directives, progress control
and temporary extraction to neutral capability leaves, and retires a
filename-dependent duplicate and unused umbrella components. The legacy
`installer` leaf falls from 143 to 133 rules. Further Inno, ISAPI, MSI,
YingInstall and NSIS reviews route ten profiles by their required evidence;
the leaf falls to 123 rules. Sixteen Inno profiles and eight macOS observations
then moved by their required technique or characteristic, bringing `installer`
to 99 rules without an exception. WSH host-profile, self-delete, self-read and
fragmentation corrections bring that leaf to 99 rules. Twenty-seven batch
observations now live under their specific transfer, script-evaluation,
process, archive, timing and filesystem capabilities; `batch` is exactly 100
rules. IRM/IEX chains now follow script evaluation, while Perl and Swift
co-occurrence profiles report their neutral capabilities; `fileless` is 99
rules. The two final over-cap execution leaves were reviewed: `exec-download`
is now 96 after moving unsupported downloader claims, ten neutral HTA
observations and Kynix helper names; `script` passed through 40 and is now 3 after routing Ruby,
MSI, MSHTA, Excel COM, Kotlin polyglot, C# command-text, Panos and JScript
obfuscation observations. No execution leaf exceeds the cap; remaining
carrier buckets still need rule-level migration. The follow-up script pass
left three Ruby composites in that carrier leaf, moved macro-trigger profiles
to execution, API-hash DLL profiles to obfuscation, and an OEP/PE-header
profile to binary infection. The WinExec and CHM passes then routed their
security-targeting, process, LSP, extraction and shortcut evidence to the
corresponding subjects, emptying two more legacy leaves. The .NET
concealed-stage and DNS TXT cases remain source-to-sink review items.
The VBS watchdog leaf was emptied by placing its four atoms and one supported
composite with process, path, and timing capabilities; one unsupported watchdog
claim was retired. The legacy persistence leaf was reduced to one Node profile
by routing four supported composites to their persistence or execution sinks
and retiring three unsupported chains. A Defender-naming sibling review placed
three atoms with neutral product and path evidence and narrowed two composites
to the conditions they actually require. Five unlinked decode/launch profiles
left the legacy `decrypt-exec` child for encoded-data, process-creation and
obfuscation leaves, preserving their matcher conditions and effective scopes.
Seven Java and WSH `scriptengine` observations now follow stack, eval,
class-name obfuscation, string-fragmentation, and WSH moniker evidence. Three PowerShell
XMLHTTP/WinHTTP profiles now follow eval, stream-write and process-create
capabilities rather than an unproven download-to-execute chain. Four `.NET`
profiles now follow reflection, hidden-process, or resource-stage evidence.
Four native rules now follow library loading, process creation, Gatekeeper
assessment and quarantine removal. Their modular RAT sibling now reports
neutral socket/module and VM-check clues rather than unsupported command control.
Two further native profiles now follow process detachment and hidden-window
evasion rather than an unbound staged-payload launch. The HTML EXE codebase
attribute and two shared WSH path/ProgID atoms now follow neutral evidence.
Three HTML composites moved by their supported stream, path and codebase
conditions, emptying the legacy HTML leaf. The unbound DNS TXT stage and
its import-time refinement now follow neutral TXT and module-timing evidence.
The desktop-entry launcher leaf was emptied by routing command text,
autostart and document-guise rules to their required subjects and retiring
a redundant wrapper. Six editor-extension installation composites now
follow durable editor-extension persistence, with their matcher clauses and
effective scopes retained. Eleven legacy staging rules now follow temp
paths, checks, process commands, curl/WebClient, or rundll32 evidence without
an unsupported cross-path handoff.
See [PLAN.md](../PLAN.md),
[DROPPER-STAGING-ENCRYPTED.md](../DROPPER-STAGING-ENCRYPTED.md),
[DROPPER-ENCRYPTED-SINK-ROUTING.md](../DROPPER-ENCRYPTED-SINK-ROUTING.md),
[DROPPER-7Z-SPAWN-SINK.md](../DROPPER-7Z-SPAWN-SINK.md), and
[SUPPLY-CHAIN-ENV-SECRET-SOURCE.md](../SUPPLY-CHAIN-ENV-SECRET-SOURCE.md),
[TCC-APPLE-SECRET-MANIPULATION.md](../TCC-APPLE-SECRET-MANIPULATION.md),
and [DROPPER-APPDOMAIN-SINK.md](../DROPPER-APPDOMAIN-SINK.md),
[GITHUB-IMAGE-URL-MODULE-LOAD.md](../GITHUB-IMAGE-URL-MODULE-LOAD.md),
[ANTI-STATIC-SOURCE-COMMAND-ATOMS.md](../ANTI-STATIC-SOURCE-COMMAND-ATOMS.md),
[SWIFT-BEACON-FORMAT-AND-PATH-CLUES.md](../SWIFT-BEACON-FORMAT-AND-PATH-CLUES.md),
[STEALER-SWEEP-RESOLUTION.md](../STEALER-SWEEP-RESOLUTION.md),
[INSTALL-HOOK-HOST-PROFILE.md](../INSTALL-HOOK-HOST-PROFILE.md),
[INSTALL-HOOK-RECON-EXFIL-PLAN.md](../INSTALL-HOOK-RECON-EXFIL-PLAN.md),
[cloud credential placement audit](../CLOUD-CREDENTIAL-REFERENCES.md),
[hidden-payload runtime audit](../HIDDEN-PAYLOAD-RUNTIME-AUDIT.md),
[dropper execution audit](../DROPPER-EXECUTION-AUDIT.md),
plus the CSV files here for directory-level evidence.

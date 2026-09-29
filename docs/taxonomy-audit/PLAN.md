# Taxonomy audit and migration plan

Snapshot: 2026-09-26, traits revision `a8b72b286f0d2ac29e005e151472eaaf701b596e`.
Validator checkout: `../cleave`, based on `a1819d4a488714542871132564b36753722aa3a2`.

The cap measurements below retain that initial snapshot. The follow-up
[implementation-layer audit](IMPLEMENTATION-LAYERS.md) records its own later
snapshot; do not combine the two sets of counts.

## Decision and measured impact

## Current working-tree measurement — 2026-09-29, 100-rule cap

The regenerated [current audit snapshot](snapshot-2026-09-28-current/)
includes the current shared tree and uses the uniform inclusive limit of 100.
Across **21,452 rule-bearing YAML files** and **118,921 rules**, it finds
**0 over-cap directories**, **0 rules in violators**, and **0 excess rules**.
There are 79,414 atomic and 39,507 composite rules. The old atomic-only 75
measurement would still flag 19 directories, and the former combined-80
measurement would flag 182; neither is the enforced policy now. One hundred
directories are at depth five and two DOS leaves are at depth six, which are
soft warnings under the current policy. Sparse sibling output remains an
advisory review at 35 rules and does not flag a single child by itself.

The cap pass completed the technique reorganizations documented below:
source-specific install hooks, network-device exploit cohorts, dropper
download modes, hidden-payload staging and execution, binary masquerade,
scan/port, sensitive-data, hollowing, privilege-escalation vulnerabilities,
eval/scripting, password brute-force, dispatch/shell, and the Elex family.
The leaf-only invariant and reference checks were rerun after each split.
Global matcher inventory contains **418 identical atomic matcher groups**;
identical bodies remain validator review signals until scope, defaults,
constraints, severity, and semantic claim have also been compared.

The [hidden-payload runtime audit](HIDDEN-PAYLOAD-RUNTIME-AUDIT.md) identifies
`runtime` as a legacy lifecycle bucket rather than a concealment technique. Its
SOCKS panel-registration rule and five npm/Node composites moved to their
behavioral homes; the 188-rule leaf remains under rule-by-rule review.

The stealer system-information audit now checks required source and result
against the exact child contracts. A host-profile composite requiring a remote
fix-command and WSS dispatch moved to the WebSocket backdoor leaf; a WMI query
plus an IP literal without a send operation moved to system discovery. Synthetic
positive and negative cases preserve the command-dispatch boundary, and the
PowerShell source-to-upload composite still matches when its upload evidence is
present.

The [dropper/execution audit](DROPPER-EXECUTION-AUDIT.md) now inventories all
1,233 rules in its 19 remaining directories; no leaf exceeds the cap. The
`exec-download` archive pass routed four unbound download/extract/launch
composites to HTTP, process-creation and Run-key persistence subjects. The
remaining 24 HTA/WSH rules then moved by file write, decode, shortcut
creation, eval, hidden execution, process creation and obfuscation evidence;
that leaf is empty. Four dead directory-reference alternatives were removed
from plugin and FTP-banner consumers. The final Ruby `script` rules now follow
HTTP API and process-launch evidence; their `module.bin` sibling follows
URL-path and launch context. The shared tree changed concurrently, so the
current count is not a simple subtraction from the previous checkpoint.
The latest `loader` pass emptied that leaf from 100 rules. Go sandbox
names, ELF HTTP/`execv`, overlay/manual-map clues, Flutter self-read,
PyInstaller pack overlays, managed remote-control/resource profiles,
keylogger/cache paths, sparse import counts, and ConfuserEx trust claims
now follow their supported subjects. One RustDesk and one ConfuserEx
refinement were removed because their added OR condition was already
required by the base; 15 relocated matcher/condition sets and effective
scopes were compared with committed source.
The VB6 follow-up moved ten neutral selfloader clues and five composites by
their supported path, string, crypto, PE-header, and overlay subjects. Two
heterogeneous EOF OR matchers were split by operation. Ten of thirteen
remaining VB6 binary composites now follow required import-obfuscation or
process-hollowing evidence; three ungrounded loader/masquerade wrappers were
retired. The import-obfuscation and hollowing destination leaves already
exceeded the cap and need mechanism-based splits. Eight adjacent VB6 crypter
rules left a language-specific payload-obfuscation leaf and now follow
resource reads, EOF overlay packing, string markers, or resource-stub
concealment. The AES `vb6/` leaf still needs a broader technique-based
sibling audit. The Elex AutoIt/UIMgrBroker wrapper now follows Elex family
identity, while
two unlinked MFC/LuaJIT dropper verdicts were retired. Their component
observations remain, and the shared high-entropy `.rsrc` fact moved to
binary-section metadata with its consumers updated. The seven FASM
assembly-source rules left the legacy loader leaf. Its four
direct observations moved to source, API-resolution, and WinINet leaves;
one heterogeneous include-name OR became four source-import observations.
Two unlinked RunPE dropper verdicts were retired. Thirteen fake-UPX
composites now follow required UPX packing, WindowsUpdate
masquerade, or neutral XOR/Base64 evidence. Loader and encrypted-overlay
claims unsupported by their conditions were removed; matcher clauses were
retained. Two unbounded bitmap/reflection composites were retired because a
proximity-bounded steganography sibling covers the supported technique; the
resource/Base64 PE profile moved to resource concealment. Netz's direct
resource-to-assembly invocation moved to `dropper/module-load`, its CLR calls
to neutral runtime leaves, and its GUID to Siscos/Netz identity. Two native
resource/overlay/process wrappers without linked payload activation were
retired. The managed ZIP follow-up now requires resource access and ZIP extraction in
a neutral capability, retiring three weak loader composites and two dependent
NuGet loader wrappers. The final .NET file sent two family-only name ORs to
Elex identity, nine composites to their required packing/obfuscation/JIT
techniques, and retired a Run-path-only persistence wrapper and unlinked
resource downloader. The legacy `execution/loader` leaf is empty. The small
`native`, `persistence`, and `nezha-dropper` leaves also emptied: unlinked
wrappers were retired, a Go identifier clue moved to neutral string evidence,
and the eooce/ws family consumer now requires Nezha config/flags for its
deployment clue. The `wininet-stage` leaf emptied after six unbound fetch/cache/process
co-occurrences were retired and the ShellExecuteEx/regsvr32 reference moved
to neutral process creation. `binary-native` also emptied: two archive-wide
npm wrappers lacked member-to-launch binding, while four bounded Node and
one newly bounded shell chain now follow probable `file-exec/spawn` evidence.
Their supply-chain consumers were updated. The `kontuke` leaf also emptied.
Its generic PowerShell/conhost/curl/tar
observations now follow their mechanisms, while the exact EndpointDLP
sidecar profile follows a family marker under known Kontuke malware.
The `platform-branch` leaf emptied after its hash-prefix checks, process
co-occurrences, bounded file-launch profile and exact Node self-delete
conditions moved to their respective subjects. Two unlinked supply-chain
wrappers were retired. The `sqlserver` leaf also emptied: ten observations
now describe database configuration, CLR stored code and database-mediated
shell calls, while three composites follow their exact SQL execution method.
The `stego-loader` leaf emptied after marked-file evaluation, encoded-command,
LSB and rundll32 contexts followed their supported mechanisms. Two image and
execution co-occurrences lacking concealed-image evidence were retired; the
Rust test-fixture consumer now separates its stronger remote-shell branch.
Sixteen `vb6-shell` rules now follow their required socket, string, HTTP,
process, registry, masquerade, rundll32 or sparse-import subject. Four
concealment/credential contexts remain for over-cap destination restructuring;
none supports its former dropper claim.
The nineteen-rule WMI leaf emptied after its complete process-creation set
moved to `objectives/execution/wmi`; no rule established a staged payload
handoff, so none remained under dropper.
The twenty-three-rule `encoding` leaf also emptied: representation and
evaluation contexts moved under anti-static taxonomy, while the one complete
uuencoded self-extractor moved to dropper file execution.
The twenty-four-rule `payload` leaf emptied after its FTP self-reconstruction,
JSONKeeper worker evaluation, Electron extraction, compiler, concealment,
LaunchAgent and neutral process clues followed their behavioral homes. No
generic payload label remains as a taxonomy axis.
Three unsupported
macro-dropper verdicts now follow
WSH execution and document-trigger evidence, emptying the macro child. The
sibling review moved four API-hash profiles to native API-hash obfuscation and
an OEP/PE-header profile to binary infection, emptying two more legacy leaves.
WinExec security-targeting and LSP profiles now follow their behavioral
subjects, while the CHM/curl/LNK pass retired a redundant HTML Help finding
and routed its remaining observations to their direct capabilities.
The VBS watchdog leaf was emptied by routing its process, path, and timing
observations and one supported composite to their evidence homes; its other
composite was retired. The legacy persistence leaf now holds one Node profile:
four composites moved to persistence or execution sinks, and three unsupported
chains were retired. The Defender sibling review moved three bare naming clues
to neutral leaves and narrowed two masquerade composites to their required
evidence. Five unlinked decode/launch profiles left the legacy `decrypt-exec`
child for encoded-data, process-creation, and obfuscation leaves; their
matcher conditions and effective scopes are unchanged. The seven Java and
WSH `scriptengine` observations moved to stack, eval, class-name obfuscation,
string-fragmentation, and WSH moniker leaves because their matchers do not
establish a staged script handoff. Three PowerShell XMLHTTP/WinHTTP
profiles now follow eval, stream-write, and process-create capabilities
because their execution sinks were not bound to the retrieved response.
Four `.NET obfuscated-loader` profiles now follow their required reflection,
hidden-process, or resource-stage subjects. Four native rules moved by
library-load, process-create, Gatekeeper and quarantine-removal evidence;
their modular RAT sibling now describes supported socket, module and VM-check
clues. The archive/detached-launch and ChaCha/hidden-PowerShell
profiles now follow process detachment and hidden-window evasion. The HTML
EXE codebase attribute and two shared WSH path/ProgID atoms now follow
neutral evidence; three HTML composites moved by their supported stream,
path, and codebase conditions. The unbound DNS TXT stage and its import-time
refinement now follow neutral TXT and module-timing evidence. The desktop-entry
launcher leaf was emptied by routing command text, autostart and document-guise
rules to their required subjects and retiring a redundant wrapper. Six
editor-extension installation composites now follow durable editor-extension
persistence, with their matcher clauses and effective scopes retained. Eleven
legacy staging rules now follow temp paths, checks, process commands,
curl/WebClient, or rundll32 evidence without an unsupported cross-path
handoff. The inventory is structural; individual evidence review remains for
the 1,233 remaining legacy rules. The final fifteen `execute-download` rules have now
been routed by their required sink or supported co-occurrence; that leaf is
empty. Its dependent supply-chain profiles were adjusted where they claimed
an unbound fetched-payload execution. The adjacent sixteen-rule `download`
leaf is also empty after routing macro, Perl, Python and Ruby evidence. Seven
XMRig argument rules moved from miner runtime to configuration, reducing the
global over-cap count by one.
Nine `exec-download` rules with unbound HTTP-to-eval or download-to-file-launch
claims moved to neutral interpreter, process and shell-command leaves. Two
related PowerShell delivery siblings moved to neutral IWR/TEMP download, and
their Mark-of-the-Web consumer now states its supported context.
Three more `exec-download` profiles moved by AppData process creation,
hidden PowerShell execution, and temp-script cleanup; an RDP consumer now
states enablement near download clues without asserting a staged implant.
Eight more PowerShell, MSI and URLMon `exec-download` profiles with no bound
download-to-launch handoff moved by their required operation. The managed
.NET HTTP/ZIP/process-API profile moved to neutral HTTP-client evidence.
The adjacent batch pass moved four shared neutral aliases and one
BITSAdmin transfer matcher out of the legacy batch leaf, then routed four
unsupported dropper composites by their required download, TCP stage-query
and TEMP-launch evidence. A two-profile Python/Startup split preserved all
32 Boolean combinations; the old `exec-download` batch file is empty.
The final mixed Winsock/TEMP profile now has separate overlay, self-read
and debugger alternatives with the same union semantics. The debugger sibling
remains at 149 rules after a VM artifact moved to VM detection.
The latest URLMon pass separated six neutral stack-string/path observations,
two AppData/URLMon profiles, and one Defender-exclusion context from the
Phorpiex family signature. Primary threat research and matching CRC32 API
hashes establish the Phorpiex attribution; the old Elex directory mixed a
Phorpiex infector with a host-family label. Seven AMSI composites and a Go
process-injection rule left the overloaded Defender sibling. The uniform cap
remains enforced without an exemption; Defender is now 125 rules and needs
further technique review.
The sibling analysis shows that the legacy `loader`,
`script`, `batch`, and transfer/phase names are not exclusive subtechniques.
Initial evidence-based moves put C#, .NET and PowerShell assembly activation under
`module-load`, VS Code and PyInstaller source evaluation under `script-eval`,
and a Werfault identity composite under masquerade because its matcher lacks
a staged-code activation sink. One copy-plus-HTTP co-occurrence rule without
payload activation was retired. Two Python stdin-interpreter composites now
state their supported neutral capability, and three dead compatibility
sentinels plus the unreachable family rule they guarded were removed after
consumer repair. The BOF host API cluster now lives under neutral interpreter
capabilities, while the COFF import-pointer clue lives with linker facts; its
prefix matcher was corrected and tested. The Dark Eye wrapper now lives under
its malware family, with reusable section measurements in metadata; Sysbot's
identical section matchers were consolidated. Two identical WSH `MSXML2.XML`
atoms became one neutral COM-prefix observation, with the narrower size guard
on its consumer. The Elex UIMgrBroker family candidate remains in the legacy
leaf until its section and size scope can be established from evidence. The
signed embedded-PE/API-resolution profile moved out of `loader`; its evidence
supports obfuscation, not certificate abuse or staged-code activation.
The reentrancy-guard leaf moved to neutral process lifecycle: the matcher
does not check a guard or link a fetched payload to the child. The standalone
Nemucod date-evasion verdict was retired after its three required legs were
inlined into its only full-chain consumer, preserving that consumer's match.
The nine-rule `integrity` leaf is empty after separating SHA-256 context from
runtime-install helper names into their neutral technique leaves.
The five-rule `misextension` leaf is empty after relocating its PNG/text
carrier clues to COM, Base64 and WebClient capabilities. It never required
an extension mismatch or a payload launch.
Three JVM self-relaunch profiles now live in neutral process lifecycle;
the unsupported stage-handoff verdict and its unshared method-name atom were
retired. The legacy `jvm-relaunch` child is empty.
The two Go/PowerShell source composites now report neutral hidden-process
context: their required launch targets PowerShell, not the downloaded or
decoded file. The `source` child is empty.
Two native DNS-TXT/write/exec composites moved to neutral DNS context because
the TXT response was not bound to the written or launched path.
The Lua sidecar leaf is empty after separating FFI declarations and Lua
runtime/file-argument context; no rule required an actual sidecar load.
The JavaScript terminal-launch cluster left `launcher` for the neutral shell
bridge; the desktop-entry launcher rules remain for sink review.
The minizip ZIP-in-data cohort moved out of `loader`: a source filename clue
belongs to provenance, recognized minizip content to its library identity,
and packed/checksum combinations to anti-static binary-metrics. No retained
rule requires the ZIP to be extracted or executed, and the old signature
claims lacked signer evidence.
The C# temp-write/Shell profile moved to neutral process-create context; its
ping-delay variant moved to anti-analysis timing. No matcher bound the written
temp path to the Shell argument.
IEExec, Delphi overlay, tiny .NET reflection, RWX resource overlay, Petite/VB6
and Gentee profiles left `loader` for their provenance, packing, reflection,
runtime or masquerade homes. The `loader` leaf is now exactly 100 rules, with
no cap exception or implementation-language split; remaining entries still
need individual sink review.
Per-rule review remains open for the rest.
The seven generic Ruby operations from `ast-script` now live with their
neutral subjects; four previously inert receiver-qualified symbol matchers
were corrected with AST queries and checked against positive and unrelated
method-call examples.
The eight-rule legacy `rename-exec` leaf is now empty: redundant union
composites were inlined, unsupported fragmented-download inference retired,
and rename-plus-command and extconf-context rules moved to their supported
execution and build-hook homes. Rubygems and Alpine package consumers were
updated and checked on synthetic Ruby and apk examples.

The first 100-cap audit cohort (historical snapshot before the later splits)
combined the largest excess and coherent nearby
sibling reviews: `supply-chain/hidden-payload/runtime` (188),
`dropper/execution/loader` (100), `dropper/staging/encrypted` (188 after its
sink review), `dropper/staging/embedded` (186), and
`anti-static/obfuscation/imports` / `anti-static/obfuscation/payload/encrypted`
(183 each). The legacy `supply-chain/recon-exfil/install-hook` leaf is now 178
after source-based migrations. These remain inspection
priorities, not preselected split designs. For each, check the 63 exact matcher
overlap groups touching violators, then compare every proposed child with its
parent and siblings. Consolidate duplicate evidence first; split only along a
single stable technique question whose children each narrow the parent. The
remaining 74 directories should then be reviewed by shared parent/cohort so
that moves account for destination capacity and sibling meaning together.

The install-hook cohort has a dedicated
[source/result audit and migration plan](INSTALL-HOOK-RECON-EXFIL-PLAN.md).
Its legacy leaf is **178** rules after source-based relocations and remains
78 over cap. The plan records sibling destination capacity and rule-file
cohorts; it rejects language/phase subdirectories because the trigger is
context rather than a behavior subtype.

## Implementation checkpoint: close the legacy stealer/sweep leaf

The [sweep disposition audit](STEALER-SWEEP-RESOLUTION.md) resolves its final
three entries. Two unsupported hostile composites were retired from the
stealer tier, preserving their independent capability/channel findings. The
native credential-snapshot composite now requires a sensitive-data clue, a
protocol-neutral upload/send/post clue, and a Cloudflare tunnel within 128
bytes; the split matcher passes two positive and three counterexample cases. The sweep
leaf has no YAML rules. The full audit remains at **79 over-cap directories**
and **1,983 excess rules** under the single 100-rule limit; these changes do
not add a cap exception.

## Implementation checkpoint: encrypted staging sink correction

The [encrypted staging audit](DROPPER-STAGING-ENCRYPTED.md) moved the Electron
ASAR decrypt/write/launch chain to `dropper/file-exec/spawn` and the two
CryptoAPI executable-memory staging rules to `dropper/staging/memory`. Both
files are byte-identical to their prior definitions; the two consumers of the
CryptoAPI composite now reference its new ID. The encrypted leaf first fell **217 → 211** through the earlier sink corrections; the passworded 7z stdout launch then moved to `file-exec/spawn`, bringing the current encrypted leaf to **210** and spawn to **69**. Memory rose **131 → 133** during the earlier moves. The
available prebuilt engine reports the same known benign `pyaigis-top10.tar.xz`
false positive after the moves, but my attempted before/after check used
hard-linked files and was contaminated by concurrent edits; I do not treat it
as detection-parity evidence. Current source validation remains open because
`cleave` has shared `filefacts`/`stng` API mismatches.

## Implementation checkpoint: passworded 7z launch follows its sink

The [7z sink audit](DROPPER-7Z-SPAWN-SINK.md) moves the passworded 7z stdout
extract, PE validation, temp-path and `Start-Process` chain from
`staging/encrypted` to `file-exec/spawn`. Its YAML hash is unchanged and no
rule-ID consumer required an edit. A live synthetic JavaScript positive matched
the relocated ID with all four conditions satisfied. The encrypted staging
cohort falls **211 → 210**; spawn rises **68 → 69**. This does not change the
global number of rules, cap violators or total excess.

## Implementation checkpoint: encrypted-stage chains follow their sinks

The [encrypted sink-routing audit](DROPPER-ENCRYPTED-SINK-ROUTING.md) moved ten
PowerShell eval chains to `dropper/script-eval`, two PowerShell assembly loads
to `dropper/module-load`, and seven direct file-launch chains to
`dropper/file-exec/spawn`. Rule fields and inherited defaults were compared
before and after; local and external references now resolve at the new paths.
Synthetic PowerShell AES/IEX and VS Code write/spawn samples matched their new
canonical IDs. The encrypted leaf fell **210 → 191**; script-eval is **26**,
module-load **18**, and file-exec/spawn **76**. No rules were removed or
weakened.

## Implementation checkpoint: GitHub image-suffix URL and assembly-load sink

The [GitHub image URL audit](GITHUB-IMAGE-URL-MODULE-LOAD.md) moves the
image-suffix URL atom into the neutral `communications/http/url/github` home:
the suffix is endpoint text and does not establish image bytes or encryption.
Both composites now live in `dropper/module-load`, where Assembly.Load is the
required activation sink; the URL clue is referenced there. Their matcher legs,
scope and 4 KiB proximity bound are preserved. Synthetic PowerShell positives
match both composites. The encrypted leaf falls **191 → 188**, module-load
rises **18 → 20**, and catalog-wide excess falls **1,991 → 1,988**; no
directory crosses the 100-rule cap as a result.

## Implementation checkpoint: neutral atoms leave the anti-static payload leaf

The [source-command atom audit](ANTI-STATIC-SOURCE-COMMAND-ATOMS.md) moves the
Swift Base64 API reference to `micro-behaviors/data/decode/base64` and the Zig
`/bin/sh -c` argument clue to
`micro-behaviors/process/create/shell/command-string`. Their matcher conditions
are retained, all four consuming composite references resolve, and synthetic
Swift and Zig source samples match at the new IDs. The Swift capability scope
now covers the Unix/macOS context required by its consumers. The anti-static
encrypted-payload leaf falls **188 → 186**; its remaining Swift path/check-in
atoms need further evidence-based placement review.

## Implementation checkpoint: Swift beacon fields and path clues

The [Swift beacon/path audit](SWIFT-BEACON-FORMAT-AND-PATH-CLUES.md) moves a
field set that contained no DNS evidence into `command-and-control/beacon/format`,
with its path-corroborated composite, and moves the `/tmp/.system_logs` literal
to `micro-behaviors/fs/path/temp`. The path atom keeps its matcher, Swift/Unix
scope and suspicious criticality; the beacon composite keeps its conditions
and hostile tier but now has beacon-format mappings and a name that describes
the evidence. A synthetic Swift sample matches the relocated composite. The
anti-static encrypted-payload leaf falls **186 → 183**; two remaining composites
there still need path-to-action review.

## Implementation checkpoint: install-hook environment-secret source

The [source-routing audit](SUPPLY-CHAIN-ENV-SECRET-SOURCE.md) moves the
three-composite install-hook environment-secret file from
`supply-chain/recon-exfil/install-hook` to `exfiltration/stealer/env`. Its
matchers and settings are byte-identical; it had no external rule-ID consumers.
The move follows the documented source-first rule: the acquired data is
process-environment secrets, while install time is referenced context. The
source leaf falls **198 → 195** and the destination rises **61 → 64**; the
current 100-rule inventory therefore remains at 79 violating directories and
falls **2,029 → 2,026** in excess. The sibling audit also confirms that
`supply-chain/credential-theft/env` is legacy duplication called out in
`TAXONOMY.md`; its atomic source rules and two source-to-exfil composites still
need coordinated migration or retirement.

## Implementation checkpoint: Telegram profile follows its source

The [Telegram profile source audit](SUPPLY-CHAIN-TELEGRAM-PROFILE-SOURCE.md)
moves the canonical host/user profile-to-Telegram composite and its npm
preinstall wrapper into `exfiltration/stealer/system-info/profile`. Telegram
is transport; installation is contextual evidence. Effective defaults and
matching conditions are preserved, along with both existing suppression legs
where the package rule had been referenced. The install-hook source falls
**195 → 194**, and the destination rises **84 → 86**. A direct JS positive, an
npm `.tgz` preinstall positive, and a same-payload package without the hook
control verify the source and lifecycle distinction.

## Implementation checkpoint: TCC manipulation leaves memory staging

The [AppleScript TCC audit](TCC-APPLE-SECRET-MANIPULATION.md) moves three
composites that write or save macOS TCC grants from `dropper/staging/memory`
to the existing `evasion/tcc-manipulation/db` leaf. Descriptions, settings,
conditions, and references to the existing AppleScript evidence are preserved;
source defaults remain `applescript`/`macos`. The staging leaf falls **133 → 130 →
126** and the TCC leaf rises to **19**. The current-source soft validator,
built with a temporary patch to the adjacent `stng` working tree, found no
broken references; it reports 84 issues, including the 79 cap
violations, and the same three benign `pyaigis-top10.tar.xz` fixture matches.

## Implementation checkpoint: PowerShell AppDomain activation sink

The [AppDomain sink audit](DROPPER-APPDOMAIN-SINK.md) moves four unchanged
PowerShell composites from `dropper/staging/memory` to `dropper/module-load`.
Each requires an AppDomain assembly load, so the runtime loader is the precise
activation technique even though the code remains in memory. The source leaf
falls **130 → 126**; the destination rises **12 → 16**. The latest 100-rule
inventory has 79 over-cap directories and 2,010 excess rules. A full soft
validation against the current source, built with a temporary Cargo patch to
the adjacent `stng` worktree, reports no broken references and the known three
benign archive fixture matches; it also reports 84 validation issues, including
all 79 over-cap directories.

## Implementation checkpoint: socket-backed shell classification and wallet source

The [ASP.NET socket relay audit](WEBSHELL-REQUEST-FD-REDIRECT.md) moves the
reverse-shell composite and both defining atoms to their semantic homes. The
webshell request leaf falls **86 → 83**; `fd-redirect` rises **35 → 37** and
neutral socket creation **61 → 62**. The direct socket-to-stdio technique stays
hostile; the standalone socket-creation clue is notable capability evidence.
All **1,842 controlled corpus fixtures** pass, including a benign Telegram path
control that rejects path mention as proof of acquisition.

The [wallet-keyring source audit](SENSITIVE-DATA-WALLET-KEYRING.md) moves seven
unchanged rules from generic `sensitive-data` into `stealer/wallet`. The wallet
leaf is **48**; the legacy source falls **141 → 134** and remains over cap for
further source-by-source review. Live strict validation reports **98 issues**
and **144 over-cap directories**; an independent new schema-object sibling is
90 rules. The broader migration remains open.

The [JavaScript credential-source audit](SENSITIVE-DATA-JAVASCRIPT-SOURCES.md)
moves nine rules: wallet seed/mnemonic/password export to `stealer/wallet`, and
generic private-key export to `stealer/credential`. The generic `sensitive-data`
directory falls **134 → 125**; wallet rises **48 → 54**, credential **37 → 40**.
An unsupported supply-chain “library theft” duplicate is merged into the
canonical wallet-seed classifier, preserving its ATT&CK mapping. All **1,842
controlled corpus fixtures** pass. The source leaf remains over cap and needs
further source/technique review; no exception was added.

The [source-classification audit](SENSITIVE-DATA-EXFIL-SOURCES.md) continues
that migration. Six JavaScript/Go source-to-HTTP classifiers now follow
`env`, `file`, and `system-info/profile`; process-only export moves to
`system-info/process`; a required browser-plus-network identity export moves to
`multi-source`. The legacy source falls **125 → 119**. Every receiver remains
within 85, with `system-info/profile` exactly at the cap. All **1,842 controlled
corpus fixtures** pass. Live strict validation still reports **144 over-cap
directories**; the broader audit remains open.

The [DNS source-classification audit](DNS-EXFILTRATION-SOURCE-CLASSIFICATION.md)
moves **18 rules** whose matchers already require AWS/netrc credentials,
credential stores, account databases, SSH material, or sensitive identity files
from `exfiltration/dns/tunnel` to their source-defined stealer leaves. Hostname
and user identity DNS exports now follow `system-info/identity`. A follow-up
moves neutral DoH endpoint observations to `communications/dns/doh` and the
DoH-to-C2 composite to `command-and-control/dns/tunneling`. An explicit DNS TXT
command-execution rule also moves from exfiltration to that C2 leaf, and the
Go PAN-OS DNS heartbeat moves to `command-and-control/beacon/network/periodic`.
The DNS exfil leaf and C2 tunneling leaf are now **100** and **85** rules; the
beacon periodic receiver has **81**. The DNS exfil leaf falls **125 → 100**;
every receiver remains within the current 100-rule cap. A related
system-information review moves a host/user-only
export from `system-info/profile` to `system-info/identity`; the leaves are now
84 and 38 rules. All **1,842 controlled corpus fixtures** pass. At the current
100-rule limit, the DNS exfil leaf is within cap; 79 directories remain over
cap catalog-wide, and other C2-versus-theft rules need individual review.

## Implementation checkpoint: ASP.NET socket-backed shell relay

Moved `aspnet-callback-reverse-shell` from `webshell/request` to
`reverse-shell/fd-redirect`: it attaches the same outbound socket to all three
child-process standard streams, which is the documented direct descriptor
redirection technique. `webshell/request` falls from 86 to 85; the receiver rises
from 35 to 36. Matcher conditions, scope, criticality, confidence and mappings
remain equivalent, and all three directory references were reviewed. The move
preserves all **1,841 controlled corpus fixtures**. See
[the boundary audit](WEBSHELL-REQUEST-FD-REDIRECT.md).

The refreshed live validator reports **103 existing issues**, including **143
over-cap directories**; the shared tree has other concurrent changes. The
taxonomy migration remains open.

## Implementation checkpoint: credential UI and application references

The [wallet-UI audit](WALLET-UI-BOUNDARIES.md) records **44 moves, one merge and
two unsupported hostile wrapper retirements**. Desktop-wallet falls from 24 to
17; objective mnemonic from 41 to 33. Product references leave artifact/library
identity, generic secret-entry UI follows credential controls, and process/service
observations follow their capabilities. Every receiver remains a strict leaf
within 85. The MetaMask union preserves prior scope and removes a duplicate vote.

The proof protects **541 definitions**; **653 affected directory references in
475 consumers** have recorded dispositions. **127 focused assertions** pass across
37 files. The complete controlled corpus passes
**1,841 fixtures** with 46 affected files overlaid on the previous passing snapshot.
Exact seed-export expectations replace stale hierarchy assertions without changing
score thresholds. Strict validation remains at 110 diagnostics and 144 oversized
directories; the unrelated live RAT matcher still blocks loading.

The ledger contains **1,674 implemented dispositions out of 1,683**, six
retirements and three sweep reviews. Four outside changes are recorded separately.
Residual wallet catalogs, recovery UI, decryption and staging claims need further
review. The full taxonomy migration remains unfinished.

## Implementation checkpoint: filename search and source-specific export

The [wallet-search audit](WALLET-SEARCH-BOUNDARIES.md) records **29 moves**, one
unsupported hostile wrapper retirement, and two explicit composite additions.
Desktop-wallet falls from **44 to 24**. The six-rule `fs/enumerate/extension`
branch is removed; predicates share `fs/search` across languages and file forms.
Dotenv interpretation leaves filesystem search for configuration loading.

Wallet and generic `id.json` search exports now have separate source-required
classifiers. Their union preserves the original Telegram classifier; a compiled
control demonstrates that generic search options no longer imply a wallet.
Traversal-dependent consumers retain the relocated bundle search explicitly.
The old hostile wrapper around a JSON filter is retired, while its suspicious
underlying observation remains unchanged.

The proof protects **69 original definitions**, with **39 directory references in
32 consumers** reviewed and 22 repair records (20 consumers plus the source split).
**82 focused assertions**, **32 Boolean union comparisons**, and all **1,841
controlled corpus fixtures** pass. Strict validation reports 110 diagnostics and
144 over-cap directories; an unrelated live RAT matcher still blocks loading.
Eight outside changes are recorded separately. The ledger contains **1,629
implemented dispositions out of 1,636**, four retirements and three sweep reviews.
Residual desktop UI, application interference, decryption, catalog and staging
cohorts remain open, as does the full cap and semantic migration.

## Implementation checkpoint: wallet stores and exported secrets

The [desktop-wallet audit](DESKTOP-WALLET-BOUNDARIES.md) records **83 moves**,
reducing the desktop leaf from **120 to 44**. Store paths, installed applications,
product references, prompts, DPAPI and messaging follow their actual subjects.
Six completed exporters follow their required source; a generic private key or
secret phrase cannot by itself require a wallet category. Every receiver remains
an existing strict leaf within 85. No exception or new depth was needed.

The proof protects **144 definitions**, reviews **48 directory references in 42
consumers**, and records **11 explicit repairs**. **126 focused assertions** and
all **1,841 controlled corpus fixtures** pass. The corpus comparison uses the
previously passing snapshot plus only the migration's 35 changed files, with no
excluded fixtures. Live loading is blocked by an unrelated new RAT definition;
23 outside changes are recorded separately. See the verification/isolation records.

The ledger contains **1,600 implemented dispositions out of 1,606**, plus three
retirements and three sweep reviews. Mnemonic retains 41 rules; blockchain-library
retains 63. The audit lists file-selection, recovery-UI, application-interference,
secret-container, broad-catalog and staging cohorts still needing semantic fixes.
The desktop size violation is resolved; the full taxonomy migration remains open.

## Implementation checkpoint: mnemonic capabilities and recovery interfaces

The [mnemonic audit](MNEMONIC-BOUNDARIES.md) records **77 moves**, reducing
`credential-access/wallet/mnemonic` from **91 to 46**. Seed representations and
wordlists now share `crypto/mnemonic`; WIF/private-key evidence, derivation paths,
UI recovery controls and keystore locators follow their documented subjects.
All receivers remain strict leaves within 85; 63 blockchain-library rules remain.

The proof protects **147 definitions**, with **33 directory references in 30
consumers** reviewed. Five explicit repairs retain relevant source/encryption
clues and remove a blanket mnemonic exemption. Local seed-entry code no longer
counts as sensitive-file targeting merely through directory membership.
**84 focused assertions** and all **1,841 isolated corpus fixtures** pass.
Live soft validation still fails the unrelated PyAigis shell-decoder regression;
strict validation reports **107 diagnostics** and **145 over-cap directories**.

The ledger contains **1,517 implemented dispositions out of 1,523**, plus three
retirements and three sweep reviews. Fifteen outside changes are recorded
separately. The audit lists remaining private-key/UI alternatives, wallet export
classifiers, three generic wallet remnants and the provider/exchange cohorts.
The full taxonomy migration remains unfinished.

## Implementation checkpoint: blockchain operations and library exclusions

The [blockchain audit](BLOCKCHAIN-OPERATION-BOUNDARIES.md) records **87 moves**
into transaction, key/signature/hash, endpoint, payment-interface and UI homes.
All receiving leaves stay within 85. Query and reward observations leave the
library layer; **93 rules remain** there for explicit follow-up.

**34 blanket blockchain exclusions are removed**, fixing the reproduced
`wallet.dat` profiler false negative and preventing wallet vocabulary from
hiding ordinary process/deserialization capabilities. One redundant ZIP
alternative from the previous batch is also removed. Moved matcher/settings
semantics are preserved; consumer changes are separately recorded.

The proof protects **204 definitions** with no outside changes, reviewing
**70 directory references in 66 consumers**. **57 focused assertions** and all
**1,841 isolated corpus fixtures** pass. Live soft validation still fails the
unchanged PyAigis shell-decoder regression; strict validation reports **91
diagnostics** and **146 over-cap directories**. The ledger contains **1,440
implemented dispositions out of 1,446**, plus three retirements and three sweep
reviews. The full migration remains open.

## Implementation checkpoint: HTTP upload follows source and channel

The [HTTP-upload audit](HTTP-UPLOAD-BOUNDARIES.md) records **98 moves**,
reducing HTTP upload from **176 to 85** combined rules. Required source data
selects the stealer leaf; otherwise archive, encrypted payload and encoded
transport have documented precedence. Local HTTP construction, paths, archive
creation and crypto operations follow their neutral capabilities. Three hybrid
crypto observations move up a level; all receivers remain strict leaves within 85.

All moved matcher/settings semantics are preserved. Four consumer rewrites retain
appropriate moved evidence; the proof protects **276 definitions** and reviews
**151 directory references in 130 consumers**. **83 focused assertions** and
**128 Boolean comparisons** pass. All **1,841 corpus fixtures** pass with only
the unrelated shell-decoder regression isolated. Live validation still fails;
strict validation reports **92 diagnostics** and **146 over-cap directories**.

The ledger has **1,353 implemented dispositions out of 1,359**, plus three
retirements and three sweep reviews. The later preservation proof records 17
outside changes and 118,811 rules; the inventory above is a separate checkpoint.
The audit records remaining upload classifiers and a blockchain-library
exclusion that mistakes generic wallet terminology for a library identity.
The cap migration and semantic audit remain open.

## Implementation checkpoint: browser locations and access mechanisms

The [browser-access audit](BROWSER-ACCESS-BOUNDARIES.md) records **95 moves**,
resolving two cap violations: Chromium **136 → 82**, multi-target **106 → 85**.
App-Bound Encryption and DevTools become sibling techniques, with no added depth.
Neutral paths, JSON fields, executable names and keyring references follow their
capabilities. All receivers remain strict leaves within 85.

The proof protects **205 definitions** and records **37 affected directory
references in 36 consumers**. Six consumer repairs retain relocated technique
alternatives. Two dead defanged-IP matchers are repaired explicitly; all other
moved matcher/settings semantics are preserved. **1,032 Boolean comparisons**
and **63 focused assertions** pass. All **1,841 corpus fixtures** pass with only
the unrelated shell-decoder regression isolated; live validation remains failing.
Strict validation reports **91 diagnostics**, including **147 over-cap leaves**.

The ledger has **1,248 implemented dispositions out of 1,251**, with three sweep
reviews. Remaining browser export, generic-capability and mixed-target rules are
listed in the audit; passing a cap is not a semantic certificate.

## Implementation checkpoint: keychain sources and local credential access

The [keychain audit](KEYCHAIN-SOURCE-BOUNDARIES.md) records **11 moves**:
five local observations leave export, and six classifiers follow their common
authentication-data source in `credential`. Keychain export has **11** rules;
credential export **33**. Every receiver remains a strict leaf within 85.
Matchers and settings are preserved. The Python collector explicitly retains
its former DPAPI source, with an unchanged eligible candidate set.

The proof protects **25 definitions**, and **16 affected directory references in
12 consumers** are reviewed. **59 focused assertions** pass. All **1,841 corpus
fixtures** pass in the documented temporary copy restoring only the unrelated
shell-decoder regression; the live tree still fails on PyAigis. Strict validation
retains **89 diagnostics** and the cap backlog stays at **149 directories**.
The ledger has **1,153 implemented dispositions out of 1,156**, with three sweep
reviews. Remaining weak transfer/store claims are recorded explicitly.

## Implementation checkpoint: mail sources and client operations

The [mail audit](MAIL-SOURCE-BOUNDARIES.md) records **89 moves**, reducing
email-harvest from 103 to **45**. Mailbox access, sending, address parsing, audit
records and account secrets now follow distinct subjects. Schema-object has
**77** rules after its own cleanup; every receiver is a strict leaf within 85.
Browser request-history export replaces mailbox reconnaissance in the 85-rule
browser leaf. No matcher or effective detection setting changed.

The proof protects **189 definitions**; the consumer report covers **72 changed
references in 66 consumers**. All **45 focused assertions** pass. The live corpus
has an unrelated pre-existing PyAigis shell-decoder regression. An isolated copy
restoring only that rule to its previous definition passes **1,841 fixtures**;
the repository rule remains unchanged. Strict validation retains **89 diagnostics**.
The audit records the isolation and outside edits explicitly.

The shared tree has **149 oversized directories**. The ledger contains **1,142
implemented dispositions out of 1,145**, with three sweep reviews. Contacts,
message-export claims, campaign audit provenance, and remaining browser/keychain
alternatives still need semantic review. The migration remains unfinished.

## Implementation checkpoint: browsing records and storage boundaries

The [history audit](BROWSER-HISTORY-BOUNDARIES.md) records **13 moves**, four
retired wrappers, and one new neutral tab-event helper. Ten history/navigation
exports now follow their browser source. Browser export has **85** rules,
activity/browser **53**, and tracking **45**. No receiver exceeds the cap.

Local storage now requires a storage interface; encryption alone no longer
satisfies it. The source-and-send classifier remains available. Payload evidence
is explicit in its consumers, and recognized cookie helpers no longer supply
false theft evidence. **8,192 Boolean comparisons**, **42 focused assertions**,
and all **1,841 corpus fixtures** pass. Strict validation retains **89
diagnostics**. The audit distinguishes the 39-definition move-preservation
proof from intentional refinements and retirement effects on broad consumers.

The shared tree now has **150 oversized directories**: an independent CFML
webshell addition raised its receiver to 86 during the pass. The ledger records
**1,054 implemented dispositions out of 1,057**, with three sweep reviews;
retired mixed observations have no fabricated single replacement. Remaining
browser acquisition, mailbox, keychain and HTTP-report classification is listed
in the audit. The overall taxonomy migration remains unfinished.

## Implementation checkpoint: browser sources and HTTP request facets

The [browser-source audit](BROWSER-SOURCE-BOUNDARIES.md) records **55 moves**:
stealer/browser falls from 106 to **78**, request/client from 96 to **85**, and
the duplicate HTTP body branch is retired. The catalog has **149 oversized
directories**, down from 151. Every receiver is a strict leaf within 85.

An ordinary JSON POST no longer supplies false cloud-theft evidence through a
misplaced helper. Distinct Go method groups replace invalid occurrence counts.
All **1,841 corpus fixtures** and **73 focused assertions** pass on the shared
tree without exclusions; strict validation still reports **88 diagnostics**.
The audit separates the matcher-preserving moves from intentional method-count
and loader repairs, records **377 protected definitions**, and documents
**92 changed directory references in 83 consumers**.

The ledger has **1,036 implemented dispositions out of 1,039**, with three sweep
reviews and a broader semantic backlog. Next, reconcile remaining browser helper
and source claims, route the history/navigation exports from collection, and
audit keychain alternatives. Passing the cap does not certify those classifiers.

## Latest checkpoint: browser observation and neutral instrumentation

The [113-rule manifest](activity-routing-moves.csv) reduces activity/browser from
100 to **62** and monitor/tracking from 125 to **50**, resolving two cap
violations. Generic event labels, JSON serialization, URL observation, storage,
cookies, and lifecycle callbacks move to their neutral subjects. All receivers
remain leaves within 85. The [activity audit](ACTIVITY-TELEMETRY-BOUNDARIES.md)
records **208 protected definitions**, **66 affected directory references in 62
consumers**, and a separately repaired JVM directory-observation regression.

All **82 focused assertions** pass. An isolated YAML copy excluding one new
post-baseline Go wallet file passes **1,841 corpus fixtures**. The actual shared
tree remains failing: strict validation reports **85 diagnostics**, and the new
file's regex-alternation count checks prevent even soft loading. The audit and
snapshot manifest state that verification boundary explicitly; no repository
exceptions were introduced. Twenty-eight outside changes are recorded separately.

The cumulative ledger has **981 implemented dispositions out of 984**, plus its
three sweep reviews. The broader semantic backlog is separate. Next, reconcile
the overfull **106-rule stealer/browser** leaf before routing history/navigation
exports out of collection; do not fill an already oversized destination.

## Latest checkpoint: input devices, notifier hooks, CSS export, and touch

The [34-rule sibling manifest](input-siblings-moves.csv) retires the overlapping
keylog/evdev leaf, moves kernel notifier collection into hook, and routes CSS
input oracles by exported source. Generic routes, paths, buffers and device
interfaces become capabilities. Direct-device collection has **9** rules,
hook **60**, and input export **54**. Touch collection has its own documented
source category; raw coordinates are not classified as keystrokes.

The [sibling audit](INPUT-SIBLING-BOUNDARIES.md) records **66 protected
definitions**, **32 changed directory references in 30 consumers**, and the
remaining classifier review. All conditions and effective settings are
preserved. The cumulative ledger has **868 implemented dispositions out of
871**, with three sweep reviews; the broader semantic backlog is separate.
The cap backlog remains **153**, with no exceptions or new depth.

## Latest checkpoint: keyboard collection and neutral input

The [200-rule manifest](keylog-routing-moves.csv) separates acquisition methods,
input export, general input handling, and synthesis. Keylog/capture falls from
193 to **53**, resolving one cap violation. The receiving hook leaf stays at
**59** after its generic primitives leave. Mouse synthesis/simulate synonyms
are consolidated, and MouseInfo leaves the misleading robot category.
Every receiver is a strict leaf within 85. No additional depth is introduced.

The [input audit](KEYLOG-INPUT-BOUNDARIES.md) documents the contracts, **386
protected definitions**, and **76 affected directory references in 70 consumers**.
One tested exclusion repair prevents `event` from also matching `System Events`.
All **1,840 verdict fixtures**, **38 source-routing assertions**, and **14 new
input assertions** pass. Strict validation still reports **77 diagnostics**,
including **153 oversized directories**. Eight concurrent definition changes
outside this migration are recorded separately.

The cumulative [837-row ledger](stealer-source-dispositions.csv) contains **834
implemented dispositions** and **three sweep reviews**. Those review counts cover
the ledger, not the whole remaining taxonomy backlog. The 53-rule capture
remainder and adjacent device/evdev/kernel/CSS leaves need the precision review
detailed in the input audit. Earlier checkpoints retain their own measurements.

## Latest checkpoint: recording sources and acquisition mechanics

The [68-rule manifest](surveillance-moves.csv) separates sound/camera exports,
local acquisition, and source-neutral recording APIs. Monitor/capture falls from
83 to **29** rules and surveillance from 14 to **6**; these leaves were already
within the cap. The pass improves semantics without claiming another cap fix.
All receiving leaves remain within 85. Source categories are registered in the
validator, with no exemptions. The whole catalog preserves moved definitions;
one collector follows the new sources and one covered OR leg is removed.
The rebuilt CLI passes **1,840 verdict fixtures** and **38 focused assertions**.
Strict validation initially retained 70 diagnostics; the reconciled run has 79,
with nine additional diagnostics from concurrent edits outside this migration.

The [recording audit](RECORDING-SOURCE-BOUNDARIES.md) records evidence contracts,
38 affected directory references across 34 consumers, validation, and unresolved
source/control distinctions. The [637-row ledger](stealer-source-dispositions.csv)
has **634 implemented** dispositions and **three sweep reviews**. There remain
154 cap violations. The snapshot includes concurrently added AMOS rules and
Java/native matcher cleanup, recorded separately in the audit. The next
oversized collection sibling is keylog/capture (**193**), whose atoms mix input
observation with input synthesis.

## Latest checkpoint: capture sources and redundant depth

The [181-rule manifest](capture-routing-moves.csv) separates screen/image export,
local capture, and neutral graphics/device/path observations. Screenshot
collection now has **58** rules and monitor/capture **83**, resolving two cap
violations. With screen streams moved to export, the redundant screenshot/capture
child is collapsed into the screenshot leaf. The implementation-form
native-capture directory is retired. No new depth or exceptions are added.

Whole-catalog comparison preserves every moved rule's effective definition;
the Python collector additionally follows the new screen/image directories.
All **1,837 verdict fixtures** and **29 focused assertions** pass. Strict
validation retains 70 issues, with oversized directories reduced to **154**.
The [capture audit](CAPTURE-SOURCE-BOUNDARIES.md) documents 52 changed broad
references across 46 consumers and the remaining surveillance, display, and
monitor reviews. The [569-row ledger](stealer-source-dispositions.csv) records
**566 implemented** dispositions and **three remaining sweep reviews**.
Historical checkpoints below retain their earlier measurements.

## Latest checkpoint: HTTP capability boundaries

The [82-entry manifest](http-capability-moves.csv) records 81 moves and one
inlined helper. HTTP upload now has **66** rules and HTTP collect **83**, resolving
two cap violations through semantic relocation into existing categories. Every
receiver is strictly leaf-only and at or below 85. The whole catalog passes
normalized comparison with explicit exceptions for equivalent helper inlining
and making Yarn bundle identity notable. Form construction, headers, suffixes,
Blob construction, and package identity no longer supply generic upload votes.

All **1,837 verdict fixtures** and **18 focused assertions** pass. Strict
validation retains 70 reported issues; only the oversized-directory diagnostic
improves, from 158 to 156. See [the HTTP audit](HTTP-CAPABILITY-BOUNDARIES.md)
for source contracts, remaining scope-sensitive duplicate candidates, and
preservation limits. The [389-row ledger](stealer-source-dispositions.csv)
records **385 implemented** dispositions and **four remaining sweep reviews**.
Broader semantic and cap work remains, including screenshot capture and
surveillance. Path changes still need downstream model assessment.
Historical checkpoints below retain their earlier measurements.

## Latest checkpoint: sweep sources and evidence roles

The [67-rule manifest](stealer-phase4-moves.csv) separates required independent
datasets (`multi-source`, **22**) from authentication-store alternatives
(`credential`, **15**), local acquisition, and neutral capabilities. Every moved
rule initially passed definition-preserving comparison. One Node composite then
received a separately tested precision repair: endpoints alone and source paths
alone no longer satisfy secret export; source plus either endpoint still does.
The source/destination helper adds one rule to the existing 121-rule HTTP collect
violator, increasing excess by one without adding an exemption.

All **1,837 verdict fixtures** and **8 source-routing assertions** pass. Strict
validation retains **70 issues**, including 158 oversized directories; no new
migration diagnostics remain. See [the checkpoint and remaining cohort](STEALER-SOURCE-PLAN.md)
for source contracts, exact preservation limits, and validator candidates.
Remaining catalog-wide cap, surveillance, transport, and semantic work is tracked
in the snapshot CSVs and ledgers. Path changes still require downstream model
assessment. Historical checkpoints below retain their earlier measurements.

## Latest checkpoint: host-information sources and capability boundaries

The [206-rule manifest](stealer-phase3-moves.csv) covers the host-information
split and receiving-leaf audits. All moved definitions retain matcher bodies
and effective settings after ID normalization. User-agent evidence and
schema-object each contain **85** rules; discovery/system/profile contains
**77**. The focused regression check passes all four assertions, and soft
validation passes **1,837/1,837 fixtures**. Strict validation still reports
70 issues, including 158 oversized directories; no broken references or
leaf-only violations remain from this migration. An unrelated login-items
addition is included in the working-tree measurements. The source contracts,
intentional broad-consumer grouping changes, and remaining work are documented
in [the implementation checkpoint](STEALER-SOURCE-PLAN.md).

## Latest checkpoint: capability helpers and captured input

Thirty rules moved with matcher bodies and effective settings preserved:
sixteen out of system-info, all twelve out of phish, and two input exporters
out of surveillance. Phish has no rules left; its exports now follow input,
and local capture/staging remains in the respective objectives. Every receiving
leaf remains within 85. The [manifest](stealer-phase2-moves.csv) records exact
IDs and definition hashes. Soft validation passes **1,837/1,837 fixtures**;
strict validation retains the same 69 reported entries. The backdoor consumer
retains applicable relocated members. Python infostealer intentionally excludes
three telemetry/startup helpers from source counting instead of promoting them
to independent proximity legs. Four dedicated finding assertions pass: a real
multi-source export matches, while telemetry observations remain visible without
an infostealer finding. The broader source-equivalence audit remains unfinished;
see [the implementation checkpoint](STEALER-SOURCE-PLAN.md).

## Latest checkpoint: PowerShell decompression is encoded staging

Five composites in `dropper/staging/encrypted/powershell-data.yaml` required
Base64 and/or Deflate reconstruction evidence without requiring encryption or
an activation sink. They moved to `dropper/staging/encoded/powershell-data.yaml`
with their IDs, conditions, scope, criticality, confidence, and attack mappings
unchanged. A synthetic generic-data sample matches two moved composites;
soft validation retains all **1,837/1,837 fixture** verdicts. Strict validation
still reports the same **60 existing validation issues**, including 160 cap
violations, with no stale-reference or unknown-directory issue for this move.
Encrypted staging falls from 223 to **218 rules**; encoded staging rises from 28 to **33** and
remains below the 85-rule cap. The refreshed audit records **160** over-cap
directories and **4,485** excess rules. The remaining PowerShell cohort stays
for individual review; this checkpoint does not assume that HTTP/image
retrieval, anti-static string clues, or a culture-derived key are encryption.
See [the focused disposition](DROPPER-POWERSHELL-COMPRESSED-DATA.md).

## Latest checkpoint: HTTP exfiltration follows its source

Four composites moved from `exfiltration/http/upload` into `stealer/cloud`,
`stealer/env`, or `stealer/file`: cloud/Kubernetes secrets with hybrid
encryption, environment credentials sent to a router endpoint, file-content
records with a harvested npm token, and environment-secret evidence near
encoded GitHub writes. Matcher conditions were retained; the GitHub write
description was narrowed to state the proximity the matcher actually
establishes. One deaddrop consumer now references the moved cloud-source rule.
A matched/miss synthetic pair confirms the router rule still requires an
environment-exfil leg, and the file-source rule matches its synthetic
GitHub/token/file pattern. Soft validation passes **1,837/1,837 fixtures**;
strict validation remains at **60 issues**. The refreshed cap audit remains at
160 over-cap directories and falls to **4,480 excess rules**. HTTP upload is
now **196 rules**; the destination leaves contain 26 cloud, 53 environment,
and 50 file-source rules, all below the cap. See [the focused
source-routing audit](EXFIL-HTTP-SOURCE-ROUTING.md); the remaining HTTP-upload
rules still need individual source and transfer review.

## Latest checkpoint: HTTP exfiltration follows credential sources

Moved three JVM composites that require developer-credential file reads plus
HTTP/curl transfer from `exfiltration/http/upload` to
`exfiltration/stealer/dev-secret`. Moved the Swift iOS Keychain marker and its
HTTP-exfiltration composite to `exfiltration/stealer/keychain`, retaining the
HTTP POST capability atom in the upload directory. Matcher bodies, IDs,
effective scopes, criticality, confidence, and ATT&CK settings are preserved;
there were no external consumers of the moved IDs. Upload falls from 196 to
191 rules; `dev-secret` rises from 73 to 76 and `keychain` from 19 to 21.
The refreshed audit remains at 160 over-cap directories and reduces excess
rules from 4,480 to 4,475. Strict validation reports no broken references from
these moves; the catalog-wide cap and policy errors remain.

## Latest checkpoint: HTTP exfiltration follows SSH, capture, token, and wallet sources

Moved Swift SSH-key marker/exfiltration rules to `stealer/ssh`, the browser
camera/microphone-recording upload composite to `stealer/surveillance`, the
device-code OAuth token forwarding composite to `stealer/token`, and the Sui
wallet archive upload composite to `stealer/wallet`. The OAuth phishing
consumer now references the token-source rule. Generic MediaRecorder plus
upload-route evidence stays under HTTP upload because it does not establish a
sensitive capture source or theft intent. Rule matcher bodies and effective
scopes, criticalities, confidence, and tags were retained. Soft validation
passes **1,837/1,837 fixtures**. The refreshed audit measures 160 over-cap
directories and **4,467 excess rules**; HTTP upload falls from 196 to 183.
Strict validation still fails on catalog-wide policy and cap findings.

## Latest checkpoint: HTTP upload evidence follows screenshot and sweep sources

Moved the browser-extension visible-screenshot JSON upload to
`stealer/surveillance`, the Swift authorized-key upload to `stealer/ssh`, and
the Swift composite requiring both shadow/SSH-path and shell-history evidence
to `stealer/sweep`. The shared Swift collect-endpoint atom remains in HTTP
upload because it is also used by cloud exfiltration and a degradation rule
and does not identify a payload source. Matcher bodies and effective rule
settings are preserved. Soft validation passes **1,837/1,837 fixtures**. HTTP
upload now has 180 rules, 95 above its cap; `stealer/sweep` has 83 rules and
remains under cap. The full audit records **4,464 excess rules** across 160
over-cap directories.

## Latest checkpoint: HTTP transport follows appliance and required sweep sources

Moved ESXi credential/configuration material sent over HTTP to
`stealer/appliance-config`. Moved the Objective-C BSD credential export to
`stealer/sweep`: its matcher requires the master-passwd source and at least
one additional credential-source clue before the send. Both composites keep
their source, transport, scope, criticality, confidence, and matcher settings;
local transport references now use canonical fully-qualified IDs. Soft
validation remains **1,837/1,837 fixtures**. HTTP upload is 178 rules, 93
over cap; appliance-config is 33 and sweep is 84. The full audit measures
**4,462 excess rules** across 160 directories.

## Latest checkpoint: HTTP source files follow the file source

Moved two Python composites from HTTP upload to `stealer/file`: one requires
enumeration of System32 driver text/log files plus a POST content field; the
other reads local Python source and sends it to a specific transform endpoint.
Both already express file collection in their ATT&CK mappings, and their
matcher bodies, scope, criticality, confidence, and file-type settings are
unchanged. Soft validation passes **1,837/1,837 fixtures**. HTTP upload now has
176 rules, 91 over cap; `stealer/file` has 52. The refreshed full audit records
**4,460 excess rules** across 160 directories.

## Latest checkpoint: miscategorized system-info exports follow their source

Moved Go global-input export and its anti-debug wrapper to
`stealer/surveillance`; a browser/network-identity export to `stealer/sweep`;
and JVM and Swift process-inventory exports to `stealer/process-list`. Their matchers and
effective settings remain unchanged. The browser/network composite requires
both source classes and brings `sweep` to exactly 85 rules. Soft validation
passes **1,837/1,837 fixtures**. `stealer/system-info` falls from 169 to 164
rules but remains over cap; its broader contents need technique-based
subdivision before routing more host-profile exports there. The refreshed
full audit records **4,454 excess rules** across 160 directories. See the
[focused source audit](SYSTEM-INFO-EXFIL-SOURCES.md) for the complete mapping
and remaining system-info disposition.

## Latest checkpoint: cloud credential exfiltration follows its source

`aws-shared-credentials-http-exfil` requires AWS credential-file contents to
enter an HTTP request. It moved from `exfiltration/http/upload` to
`exfiltration/stealer/cloud`; its matcher and effective rule settings are
unchanged, and its supply-chain consumer now uses the canonical source ID. The
consumer now admits `tar`, `whl`, and `pyproject.toml` types so it can evaluate
source-distribution and wheel containers. The hostile AWS-upload control still matches and the
benign unrelated-body control stays negative. Soft validation passes
**1,837/1,837 fixtures**. The current audit reports 160 over-cap directories
and 4,484 excess rules. The full PyPI archive sample remains unmatched because
its `Path.read_text()` to `json=` flow is outside the source atom's current
`open().read()` to `data=` matcher; that separate coverage gap is documented in
[the focused audit](EXFIL-CLOUD-CREDENTIAL-HTTP.md).

## Latest checkpoint: install-hook host profiling follows the result

[Host-profile audit](INSTALL-HOOK-HOST-PROFILE.md) moves a JavaScript host/CI
query aggregate to `discovery/system/profile`, and moves install-time
host-profile transmissions to `exfiltration/stealer/system-info`. The install
declaration is retained as evidence in the exfiltration composites. This
removes one trigger-based duplicate home, but exposes existing breadth debt:
`recon-exfil/install-hook` is **199 rules**, `stealer/system-info` **169**, and
`discovery/system/profile` **93**. No per-directory exception is proposed;
these leaves need their own precise cohort audits. Strict validation remains
at **60 issues** and **164 over-cap directories**; soft validation passes
**1,837/1,837 fixtures**.

## Latest checkpoint: parsed archive properties leave capabilities

[Archive fact audit](ARCHIVE-FILE-FACTS.md) moves five parser-derived
observations—member naming/separators, duplicate paths, and encrypted-member
counts—from `micro-behaviors/data/archive/member` to the corresponding package
and file metadata leaves. These rules describe the analyzed archive, not code
that manipulates archives. Matcher bodies, effective scopes, confidence, and
criticality remain intact. `TAXONOMY.md` now states this boundary. Soft
validation passes **1,837/1,837 fixtures**; strict validation remains at **60
issues** and **164 over-cap directories**.

## Latest checkpoint: APK package-member facts leave dropper staging

[APK member-fact audit](DROPPER-APK-MEMBER-FACTS.md) moves 17 parsed APK
member-path observations from `dropper/staging/archive` to
`metadata/package/files/mobile-package`. Their evidence establishes package
contents, not packing or staging; package scopes and matchers are preserved,
while inappropriate inherited `T1027.002`/`B0024` labels are removed. The
device-admin plus lock-screen resource composite now lives under Android UI
harassment and references the canonical package facts. DEX content references
remain for separate review. The taxonomy now documents package-specific versus
generic archive-member boundaries and how capability/objective composites
consume member facts. Soft validation passes **1,837/1,837 fixtures**. The
archive-staging directory falls from **97 to 79 rules** after the member move;
two later asset-staging composites bring it to **81 rules**. Strict validation
still reports catalog-wide issues, including **164 over-cap directories**.

The same audit relocated 14 APK member observations out of encrypted staging,
plus six composites whose evidence did not establish encrypted staging. The
LibGDX/network-module composites now describe package contents, and
non-encrypted asset staging sits with archive staging. One encrypted-core
composite remains in the encrypted leaf. Its count falls from **243 to 223**;
soft validation remains **1,837/1,837**, and strict validation is back to the
existing **60 issues**. The encrypted leaf remains over cap and requires a
separate technique-level subdivision; see the expanded
[APK member-fact audit](DROPPER-APK-MEMBER-FACTS.md).

## Latest checkpoint: Node Python bootstrap remains a capability signal

[Node Python-bootstrap audit](DROPPER-NODE-PYTHON-BOOTSTRAP.md) moves the
file-scoped URL, write-stream, and `execSync` conjunction into the shell-bridge
capability leaf. The duplicate objective-only `get-pip.py` text leg was
removed because the URL matcher already covers that bootstrap URL. The rule is
now named as co-occurrence and scored notable because it does not link fetched
bytes to execution. Soft validation passes **1,837/1,837 fixtures**.
`execute-download` falls from **134 to 133 rules**. Strict validation remains
at **60 issues**, including **165 over-cap directories**. See the
[mapping ledger](dropper-node-python-bootstrap-mapping.json).

## Latest checkpoint: crypto provider references leave encrypted staging

[Crypto API audit](DROPPER-CRYPTO-API.md) moves 13 rules out of
`objectives/command-and-control/dropper/staging/encrypted`. Their evidence is
Python cryptography imports near BCrypt/libcrypto references and API-name
strings; it does not establish payload staging or conditional fallback
selection. The rules now describe probable native crypto API references and
co-occurrence in `micro-behaviors/crypto/native/`, preserving matcher bodies and
effective scopes. Soft validation passes **1,837/1,837 fixtures**. I rebuilt
cleave against the sibling `filefacts` working tree with a one-command Cargo
patch; `make validate` now reports the established 60 issues and 165 over-cap
directories, with no unknown-directory error. The encrypted-staging directory
remains over the 85-rule cap and needs further cohort-by-cohort audit.

## Latest checkpoint: .NET RAT configuration leaves encrypted staging

[.NET RAT-config audit](DROPPER-DOTNET-RAT-CONFIG.md) moves the MD5 provider
and ECB/zero-padding clues to their crypto capability leaves, while the
RAT-specific field cluster and crypto co-occurrence move to
`command-and-control/backdoor/rat/config`. The composite no longer claims that
decryption occurred. Two consumers now use the canonical crypto IDs; matcher
bodies and effective scopes are preserved. Soft validation passes
**1,837/1,837 fixtures**. Encrypted staging loses five rules but remains over
the cap; strict validation reports the existing 60 issues, including 165
over-cap directories.

## Latest checkpoint: Electron sidecar chain follows its module-load sink

[Electron sidecar audit](DROPPER-ELECTRON-SIDECAR-MODULE-LOAD.md) moves the
AES-decrypt/`Module._compile` chain from encrypted staging to `dropper/module-load`,
the required activation sink. Its matcher legs, scope, confidence, criticality,
tags, and exclusions are preserved; three masquerade consumers use the
canonical path. Soft validation passes **1,837/1,837 fixtures**. Encrypted
staging loses one additional rule and remains over cap.

## Latest checkpoint: archive containment is separate from encrypted staging

[Archive disk-image audit](DROPPER-ARCHIVE-UNENCRYPTED-DISK-IMAGE.md) moves two
composites that never require archive encryption from `staging/encrypted` to
`staging/archive`. The taxonomy now distinguishes an archive-contained disk
image from encrypted archive staging and from a mounted image-disk activation.
Matchers and effective metadata are preserved; no external consumer needed an
ID update. Soft validation passes **1,837/1,837 fixtures**. Encrypted staging
falls to 243 rules; archive staging is 97 and remains over cap for further
cohort review.

## Latest checkpoint: JavaScript temp-environment clue uses the shared capability

[JavaScript environment audit](DROPPER-JAVASCRIPT-ENVIRONMENT.md) moves the
`process.env.TEMP` observation from `execute-download` to the shared
`os/env/read` capability and updates the Node downloader consumer. The shared
matcher now covers JavaScript and TypeScript alongside other source forms.
`execute-download` falls from **135 to 134 rules**. See the
[mapping ledger](dropper-javascript-environment-mapping.json).

## Latest checkpoint: hidden scratch-stage patterns use one technique leaf

[Hidden-stage audit](DROPPER-HIDDEN-STAGE.md) moves 17 language-neutral hidden
scratch-stage rules from the generic download-execute directory into the
existing `delivery/hidden-stage/` leaf, and updates six consumers. The move
keeps carrier formats together under the behavior they evidence; it does not
create language/filetype branches. The hostile CI fixture now expects the new
canonical leaf, and the benign shell control explicitly forbids it. Soft
validation passes **1,837/1,837 fixtures**. `execute-download` falls from **152
to 135 rules** and remains over the 85-rule cap. Strict validation remains at
**60 issues**, including **165 over-cap directories**. See the
[mapping ledger](dropper-hidden-stage-mapping.json).

## Latest checkpoint: Windows HTTP APIs are explicit delivery techniques

[Windows HTTP API audit](DROPPER-TRANSFER-API-LEAVES.md) moves 13 more WinHTTP,
URLMon, and WinINet rules beside the 17 API-specific rules moved earlier.
Their effective scopes, matchers, and rule metadata are preserved, with
canonical IDs updated for external consumers. The `TAXONOMY.md` disambiguation
defines each child by its transfer API, not language or filetype.
`execute-download` falls from **165 to 152 rules**, so it remains over the
single 85-rule cap and needs further technique-level audit. See the
[mapping ledger](dropper-wininet-urlmon-mapping.json).

## Latest checkpoint: PowerShell download clues use capability leaves

[PowerShell atom audit](DROPPER-POWERSHELL-ATOMS.md) relocates four capability
observations from the oversized dropper leaf to WebClient download, MSI
installer, and GitHub URL capability leaves. Their exact consumers now use the
canonical IDs; the download/installer objective composites remain in their
sink leaves. Their `[powershell, batch, pe]` scopes are preserved, while
inherited dropper tags are removed where the atom does not establish transfer
or installation. A filename-only MSI date heuristic was retired in favor of
requiring the actual package verb. See the expanded
[mapping ledger](dropper-powershell-cooccurrence-mapping.json). The full soft
fixture suite passes **1,837/1,837**. Strict validation remains at **60 issues**
and **165 directories over the 85-rule cap**; this migration adds no strict
issues.

## Latest checkpoint: PowerShell fetch and launch evidence stays capability-level

[PowerShell co-occurrence audit](DROPPER-POWERSHELL-COOCCURRENCE.md) moves one
atom and two unsupported dropper composites into the corresponding process and
download capability leaves. SCCM, MSI, and Defender consumers now use the
canonical capability IDs. The fetch composite and the hidden request/launch
co-occurrence are notable, not hostile, because neither proves payload
activation. A fixture review also repaired PowerShell backtick-newline handling
in the existing `iwr-outfile-download` matcher, restoring a separately
evidenced quiet-MSI installer chain. Soft validation passes **1,837/1,837
fixtures**. See the [mapping ledger](dropper-powershell-cooccurrence-mapping.json).

## Latest checkpoint: PowerShell rules use installer and spawn sinks

[PowerShell sink audit](DROPPER-POWERSHELL-COMPLETED-SINKS.md) moves three MSI
chains to `file-exec/installer` and two downloaded-executable launch chains to
`file-exec/spawn`. Their source atoms remain available through canonical
references. Matchers and effective scopes are unchanged. `execute-download`
falls from **195 to 190 rules**, installer grows from **10 to 13**, and spawn
from **60 to 62**. See the
[mapping ledger](dropper-powershell-completed-sinks-mapping.json).

## Latest checkpoint: .NET launch chains use file-exec/spawn

[.NET spawn audit](DROPPER-DOTNET-SPAWN.md) moves five C#/.NET composites
with required process-launch evidence to `dropper/file-exec/spawn/`. The one
C# source-scoped rule keeps that scope, the other four remain PE scoped, and
the sandbox-gated composite retains its helper dependency through a canonical
cross-directory reference. Matcher semantics and effective scopes are
unchanged. `execute-download` falls from **200 to 195 rules** and spawn grows
from **55 to 60**. See the
[mapping ledger](dropper-dotnet-spawn-mapping.json).

## Latest checkpoint: URLMon launch chains use file-exec/spawn

[URLMon spawn audit](DROPPER-URLMON-SPAWN.md) moves ten composites requiring
`WinExec`, `ShellExecute`, `ShellExecuteEx`, or process-creation evidence into
`dropper/file-exec/spawn/`. Their dependent browser-UA and sandbox-gated rules
moved with the rules they reference. Matchers and effective scopes are
preserved, including PE-only scope for the two signed-downloader rules. The
source leaf falls from **210 to 200 rules** and spawn grows from **45 to 55**.
See the [mapping ledger](dropper-urlmon-spawn-mapping.json).

## Latest checkpoint: VBScript MSI chains use file-exec/installer

[VBScript MSI audit](DROPPER-VBS-MSI-FILE-EXEC.md) moves three rules requiring
an `msiexec` transaction to `dropper/file-exec/installer`. The delayed RMM
composite moved with its referenced base rule. Matcher bodies, effective
scopes, criticalities, and tags are unchanged. The two non-installer findings
from the same source file remain for separate review. `execute-download` falls
from **213 to 210 rules** and `file-exec/installer` grows from **7 to 10**.
See the [mapping ledger](dropper-vbs-msi-file-exec-mapping.json).

## Latest checkpoint: URLMon launch rules use file-exec/spawn

[URLMon sink audit](DROPPER-URLMON-FILE-EXEC.md) moves two composites that
require a branded URLMon downloader and `ShellExecuteEx` or `CreateProcessW`
to `dropper/file-exec/spawn`. Their matcher bodies and effective scopes are
unchanged; no exact consumers needed updates. The two adjacent staging-only
profiles stay in the source leaf because they do not establish a launch sink.
`execute-download` falls from **215 to 213 rules** and `file-exec/spawn` grows
from **43 to 45**. See the [mapping ledger](dropper-urlmon-file-exec-mapping.json).

## Latest checkpoint: Node download/interpreter co-occurrence is a capability

[Node co-occurrence audit](NODE-INTERPRETER-COOCCURRENCE.md) moves three rules
from the dropper source leaf to
`micro-behaviors/process/create/shell/interpreter/`. A generic `run()` call
with an interpreter name remains a lower-confidence capability clue; the
download/interpreter composite is now named and scored as co-occurrence because
its 320-line window does not link downloaded bytes to interpreter input. Both
supply-chain consumers use the canonical capability ID. The dropper leaf falls
from **218 to 215 rules** and the interpreter leaf now has **12**. Soft
validation passes **1,837/1,837 fixtures**; strict validation remains at **59
issues**, including **165 over-cap directories**. See the
[mapping ledger](node-interpreter-cooccurrence-mapping.json).

## Latest checkpoint: remote-thread activation uses process-inject

[Download sink audit](DROPPER-EXECUTE-DOWNLOAD-SINKS.md) moves one WinHTTP
composite requiring remote-process memory APIs and remote-thread creation to
`dropper/process-inject`. Its matcher and execution scope are preserved.
`execute-download` falls from **219 to 218 rules**. See the
[mapping ledger](dropper-execute-download-sinks-mapping.json).

## Latest checkpoint: neutral WebClient retrieval stays in communications

[DownloadString reference audit](DROPPER-EXECUTE-DOWNLOAD-HTTP-REFERENCES.md)
moves six WebClient type/download findings out of
`dropper/delivery/execute-download`. Their match predicates are preserved; the
three DownloadString composites and the executable-download-to-writable-path
composite are now notable communications capabilities because no rule linked
the fetched content to evaluation or launch. One impossible PE scope was
removed from the DownloadString composite. `execute-download` falls from
**225 to 219 rules**. The taxonomy now states the
retrieval-versus-activation admission test. See the
[mapping ledger](dropper-execute-download-http-references-mapping.json).


### Latest checkpoint: archive-adjacent eval and module loading use their sinks

[Archive eval/module-load audit](DROPPER-ARCHIVE-EVAL-MODULE-LOAD.md) moves
the remote PowerShell `IEX` chain to `script-eval` and the Dalvik reflective
invocation chain to `module-load`. The APK asset helpers remain in archive
staging, with one dependent reference updated. The original PowerShell matcher
was restored exactly, and its process-start legs were removed from the archive
extraction aggregate. `staging/archive` drops from **97 to 95 rules**. Soft
validation passes **1,837/1,837 fixtures**. See the
[mapping ledger](dropper-archive-eval-module-load-mapping.json).


### Latest checkpoint: completed archive launches follow the spawn sink

[Archive file-execution audit](DROPPER-ARCHIVE-FILE-EXEC.md) moves six
PowerShell archive chains whose matchers require payload process launch into
`dropper/file-exec/spawn`. The helper rules remain in archive staging, and the
extraction-only composites stay there. `file-exec/spawn` grows from **78 to
84 rules**; the external ClickFix consumer now references the canonical rule
path. Matchers and effective scope are unchanged. Soft validation passes
**1,837/1,837 fixtures**. Strict validation still reports **165 over-cap
directories** and existing catalog debt. See the
[mapping ledger](dropper-archive-file-exec-mapping.json).


### Latest checkpoint: file-exec is refined by activation mechanism

[File-execution subtechnique audit](DROPPER-FILE-EXEC-SUBTECHNIQUES.md)
reorganizes all rules in `dropper/file-exec` into strictly leaf-only
`command` (**41**), `spawn` (**43**), and `installer` (**7**) directories.
Shell/interpreter-evaluated command text, direct process creation, and installer
transactions each have one admission test. Exact rule references point to their
canonical child paths; parent-directory references remain valid aggregate
references. No matcher or effective rule scope changed. Soft
validation passes **1,837/1,837 fixtures**. Strict validation still reports
**165 over-cap directories** and existing catalog debt. See the
[85-rule mapping ledger](dropper-file-exec-subtechniques-mapping.json).


### Latest checkpoint: encrypted payloads follow injection and image-map sinks

[Injection/image-map audit](DROPPER-ENCRYPTED-INJECT-IMAGE-MAP.md) moves the
CryptoAPI manual-PE mapper to `dropper/image-map`, and three composites with
required remote memory-transfer, remote-thread, or thread-hijack evidence to
`dropper/process-inject`. Two exact consumers now use the canonical image-map
ID; the other moved rules had no external consumers. `staging/encrypted` drops
from **268 to 264 rules**. Matchers, effective scope, and criticality remain
unchanged. The directory contract now explicitly distinguishes process
injection, current-process image mapping, and generic executable-memory
staging. Soft validation passes **1,837/1,837 fixtures** with no new migration
warnings. Strict validation still reports **165 over-cap directories** and
other catalog debt. See the
[mapping ledger](dropper-encrypted-inject-image-map-mapping.json).


### Latest checkpoint: completed source-evaluation chains use script-eval

[Encrypted script-eval audit](DROPPER-ENCRYPTED-SCRIPT-EVAL.md) moves the
Python base64/zlib `exec` chain, Ruby Base64/zlib `eval` chain, and PowerShell
hex-XOR `IEX` chain from encrypted staging to `dropper/script-eval`. The Ruby
atomic pattern moved with its composite; decoder-only evidence and the
PowerShell ScriptBlock-construction rule remain in staging. No external
consumers needed reference updates. `staging/encrypted` drops from **272 to
268 rules** (four definitions, including the Ruby atom); script-eval remains
below the 85-rule cap. Matchers, scopes,
and criticality are unchanged. See the
[mapping ledger](dropper-encrypted-script-eval-mapping.json).


### Latest checkpoint: remaining completed encrypted stages follow their sink

[Encrypted-stage sink audit](DROPPER-ENCRYPTED-REMAINING-SINKS.md) moves the
.NET decrypt-and-reflective-assembly-load chain to `dropper/module-load` and
the PowerShell hex-XOR chain that downloads and launches an executable to
`dropper/file-exec`. Decoder and ScriptBlock evidence remains in encrypted
staging and is referenced by exact ID. The injection-configuration composite
stays in encrypted staging because its strings do not establish process
injection. `staging/encrypted` drops from **274 to 272 rules**, module-load
grows from **9 to 10**, and file-exec grows from **84 to 85**, at the shared
cap. Rule matchers and effective scope are unchanged; one dependent .NET
reference now uses the canonical ID. See the
[mapping ledger](dropper-encrypted-remaining-sinks-mapping.json).


### Latest checkpoint: IoT raw-IP chmod launch chains use file-exec

[ELF chmod/file-exec audit](DROPPER-ELF-CHMOD-FILE-EXEC.md) moves three
Linux ELF composites whose raw-IP download evidence is joined to explicit
chmod and local-launch evidence. One cleanup consumer now references the
canonical rule path; the other two composites had no external exact-ID
consumers. Rule matchers, effective scope, and criticality are unchanged.
`delivery/execute-download` drops from **228 to 225 rules** and file-exec
grows from **81 to 84**. Soft validation passes **1,837/1,837 fixtures**.
Strict validation retains the existing unknown `micro-behaviors/os/application`
directory and catalog-wide over-cap debt, including **165 over-cap
directories**. See the [mapping ledger](dropper-elf-chmod-file-exec-mapping.json).


### Latest checkpoint: IoT download-to-shell pipes use interpreter-stdin

[ELF stdin audit](DROPPER-ELF-INTERPRETER-STDIN.md) moves two ELF chains
whose downloader output is piped directly into the shell: the hex-encoded NVMS
stager and the raw-IP IoT shell stager. Their activation sink is interpreter
stdin; the shared native pipe marker remains in the legacy leaf by exact ID.
No external references to the moved composites needed updates. Matcher bodies
and scopes are unchanged. `delivery/execute-download` drops from **230 to 228
rules** and `interpreter-stdin` grows from **1 to 3**. Soft validation passes
**1,837/1,837 fixtures**. Strict validation retains catalog-wide debt,
including **165 over-cap directories**. See the
[mapping ledger](dropper-elf-interpreter-stdin-mapping.json).


### Latest checkpoint: PHP and TFTP local launches use file-exec

[PHP/TFTP file-exec audit](DROPPER-PHP-TFTP-FILE-EXEC.md) moves the bounded
PHP download/chmod/local-exec chain and the one-command TFTP-to-local-shell
launch into `dropper/file-exec`. The TFTP exploit consumer now uses the
canonical exact ID; no PHP exact-ID consumers needed updates. Matcher bodies
and effective scopes are unchanged. `delivery/execute-download` drops from
**232 to 230 rules** and file-exec grows from **79 to 81**. Soft validation
passes **1,837/1,837 fixtures**. Strict validation retains catalog-wide debt,
including **165 over-cap directories**. See the
[mapping ledger](dropper-php-tftp-file-exec-mapping.json).


### Latest checkpoint: ELF download/chmod/execute chain uses file-exec

[ELF file-exec audit](DROPPER-ELF-FILE-EXEC.md) moves the
`download-permission-execute-chain` composite to `dropper/file-exec`. Its
required legs combine a native download/chmod marker with chmod-then-local-exec
behavior. Eight consumer files now use the canonical exact ID (nine reference
occurrences); the supporting download marker remains in the legacy source leaf.
The matcher and effective scope are unchanged. `delivery/execute-download`
drops from **233 to 232 rules** and file-exec grows from **78 to 79**. Soft validation
passes **1,837/1,837 fixtures**. Strict validation retains the catalog-wide cap
and quality debt, including **165 over-cap directories**. See
the [mapping ledger](dropper-download-permission-file-exec-mapping.json).


### Latest checkpoint: WinINet hollowing follows process-inject sink

[WinINet hollowing audit](DROPPER-WININET-PROCESS-INJECT.md) moves the
retrieval-plus-process-hollowing composite from `delivery/execute-download` to
`dropper/process-inject`. Its matcher body and criticality are unchanged, and
there were no exact-ID consumers. The legacy leaf drops from **234 to 233
rules**; `process-inject` now contains one rule. Soft validation passes
**1,837/1,837 fixtures**. Strict validation retains the catalog-wide cap and
quality debt, including **165 over-cap directories**. See the
[mapping ledger](dropper-wininet-process-inject-mapping.json).


### Latest checkpoint: PowerShell executable/MSI launch chains use file-exec

[PowerShell file-exec audit](DROPPER-POWERSHELL-FILE-EXEC.md) moves three
chains from legacy `delivery/execute-download`: a writable-path EXE launch, a
country-gated executable launch, and a ProgramData MSI install. Their matcher
bodies and criticalities remain unchanged; source helper traits stay in the
legacy leaf and the moved composites reference them by exact ID. No external
references to the moved composites needed updates. The legacy leaf drops from
**237 to 234 rules** and file-exec grows from **75 to 78**. Soft validation
passes **1,837/1,837 fixtures**. Strict validation still has catalog-wide cap
and quality debt, including **165 over-cap directories**. See the
[mapping ledger](dropper-powershell-file-exec-mapping.json).


### Latest checkpoint: Go and Java temp-file launches use file-exec

[Go/Java launch audit](DROPPER-LANGUAGE-FILE-EXEC.md) moves the Go encrypted
payload temp-file launcher and the Java XOR-decoded temp-shell launcher to
`dropper/file-exec`. Their supporting observations remain in encrypted staging;
the moved composites now reference those traits by canonical exact IDs. The
OrgSearch consumer now points to the Go rule at its new home. No matcher bodies,
scopes, or criticalities changed. Encrypted staging drops from **277 to 274
rules** and file-exec grows from **72 to 75**. Soft validation passes
**1,837/1,837 fixtures**. Strict validation retains the catalog-wide cap and
quality debt, including **165 over-cap directories**. See the
[mapping ledger](dropper-language-file-exec-mapping.json).


### Latest checkpoint: native encrypted loaders follow activation sink

[Native loader audit](DROPPER-NATIVE-LOADERS.md) moves the XChaCha/native
section-map chain to `dropper/image-map` and the write-then-`LoadLibraryA` DLL
loader to `dropper/module-load`. The crypto and transport evidence remains part
of each existing composite, and neither matcher body was changed. The encrypted
staging leaf drops from **279 to 277 rules**; image-map gains one rule and
module-load grows from **8 to 9**. Soft validation remains **1,837/1,837
fixtures**. Strict validation retains the catalog-wide cap and quality debt,
including **165 over-cap directories**. See the
[mapping ledger](dropper-native-loaders-mapping.json).


### Latest checkpoint: JavaScript encrypted eval rules follow sink and capability

[JavaScript eval audit](DROPPER-JAVASCRIPT-EVAL.md) moves the completed
hardcoded-decrypt/eval chains into `dropper/script-eval` and classifies a
standalone generator/eval source indicator with the interpreter-eval capability.
That source indicator alone does not establish encryption, staging, or a dropper.
The encrypted-staging leaf drops from **287 to 279 rules**; `script-eval` grows
from **4 to 11**, and JavaScript direct-eval grows by one. Soft validation
passes **1,837/1,837 fixtures**. Strict validation still reports the existing
catalog-wide taxonomy and quality debt, including **165 over-cap directories**. See the
[mapping ledger](dropper-javascript-eval-mapping.json).


### Latest checkpoint: encrypted dropper rules follow their activation sink

[Encrypted sink audit](DROPPER-DECRYPT-EVAL-SINKS.md) splits completed
decrypt-and-execute chains into `script-eval`, `module-load`, and `file-exec`.
It leaves unbounded or sink-ambiguous zero-IV rules in the staging leaf until
their matchers establish a launch relationship. Soft validation passes
**1,837/1,837 fixtures**; the encrypted staging leaf drops from **293 to 287
rules**, while the new script-eval leaf has **4**, module-load **8**, and
file-exec **72**. Strict validation remains at **59 issues**, including **165
over-cap directories**, without new migration-specific warnings. See the
[mapping ledger](dropper-decrypt-eval-sinks-mapping.json).

### Earlier checkpoint: encrypted Node activation uses module-load

[Encrypted module-load audit](DROPPER-ENCRYPTED-MODULE-LOAD.md) moves four
Node composites with a required dynamic `require` sink from
`staging/encrypted` to `dropper/module-load`. The decryption method remains
referenced evidence; eval chains and ciphertext without an established sink
stay in their own technique homes. Three supply-chain consumers now use
canonical IDs. Soft validation passes **1,837/1,837 fixtures**. The encrypted
staging leaf drops from **297 to 293 rules** and module-load grows from **3 to
7**. Strict validation still reports catalog-wide cap and quality debt. See
the [mapping ledger](dropper-encrypted-module-load-mapping.json).

### Earlier checkpoint: remote MSI activation uses file-exec

[MSI file-exec audit](FILE-EXEC-MSIEXEC.md) moves three remote MSI-install
composites and their shared non-ASCII-switch fragment from
`delivery/execute-download` to `dropper/file-exec`. The URL-backed package
install activates the staged file through its installer handler; a generic
`msiexec` invocation remains insufficient. Soft validation passes
**1,837/1,837 fixtures**. The source leaf drops from **241 to 237 rules** and
`file-exec` grows from **67 to 71**. Strict validation retains catalog-wide
quality and cap debt, including **165 over-cap directories**. See the
[mapping ledger](file-exec-msiexec-mapping.json).

### Earlier checkpoint: Node activation follows the required sink

[Node sink audit](NODE-DROPPER-SINKS.md) moves eight complete Node file-launch
chains to `dropper/file-exec` and a decoded dynamic-`require` loader to
`dropper/module-load`. It leaves a broad download/interpreter co-occurrence in
the old leaf because its matcher does not tie the downloaded file to the
interpreter input. FTP-banner aggregation already includes both sink leaves;
five exact supply-chain references now use the canonical IDs. Soft validation
passes **1,837/1,837 fixtures**. `delivery/execute-download` drops from **250
to 241 rules**, `file-exec` grows from **59 to 67**, and `module-load` from **2
to 3**. Strict validation still reports catalog-wide cap and quality debt. See
the [mapping ledger](node-dropper-sinks-mapping.json).

### Earlier checkpoint: Regsvr32 scriptlet execution has a technique-specific home

[Regsvr32 audit](REGSVR32-LOLBIN.md) moves the seven-rule Squiblydoo set out of
the generic staged-download leaf and consolidates it with the two existing
Regsvr32 LOLBin rules in `objectives/execution/lolbin/regsvr32`. The new
boundary distinguishes remote scriptlet activation from a staged file launch;
the Equation Editor, DLL-hijacking, Windows LOLBin, and FTP-banner consumers
now use the canonical rules. Soft validation passes **1,837/1,837 fixtures**.
`delivery/execute-download` drops from **257 to 250 rules**; the new
Regsvr32 leaf has **9 rules**. Strict validation retains the catalog-wide
quality and cap warnings, including **165 over-cap directories**. See the
[mapping ledger](regsvr32-lolbin-mapping.json).

### Earlier checkpoint: Node activation chains use file-exec or module-load

[Node activation audit](DROPPER-NODE-ACTIVATION.md) moves five complete staged
payload composites according to their sink: four process launches to
`dropper/file-exec` and one dynamic `require` loader to
`dropper/module-load`. FTP-banner consumers now include both activation leaves
and the remaining legacy delivery directory. Soft validation passes
**1,837/1,837 fixtures**. `delivery/execute-download` drops from **262 to 257
rules**; `file-exec` grows from **55 to 59**, and `module-load` from **1 to 2**.
Strict validation still reports catalog-wide quality and cap warnings,
including **165 over-cap directories**. See the
[mapping ledger](dropper-node-activation-mapping.json).

### Latest checkpoint: Python file activation uses the file-exec leaf

[Python file-exec audit](FILE-EXEC-PYTHON.md) moves four composites joining
remote file acquisition or writing to a process launch. Python/platform scopes
remain in the rule file; matchers, effective scope, and proximity are unchanged.
Soft validation passes **1,837/1,837 fixtures**. The oversized
`delivery/execute-download` leaf drops from **266 to 262 rules**; `file-exec`
grows from **51 to 55 rules**. Strict validation remains at **59 issues**,
including **165 over-cap directories**. See the
[mapping ledger](file-exec-python-mapping.json).

### Latest checkpoint: .NET file activation uses the file-exec leaf

[.NET file-exec audit](FILE-EXEC-DOTNET.md) moves six PE-scoped composites
that link downloaded or written files to process/file-handler activation. The
PE scope remains in the rule file, and two external consumers now use canonical
IDs. Soft validation passes **1,837/1,837 fixtures**. The oversized
`delivery/execute-download` leaf drops from **272 to 266 rules**; `file-exec`
grows from **45 to 51 rules**. Strict validation remains at **59 issues**,
including **165 over-cap directories**. See the
[mapping ledger](file-exec-dotnet-mapping.json).

### Latest checkpoint: piped shell payloads use interpreter-stdin

[Interpreter-stdin audit](INTERPRETER-STDIN.md) moves the raw-IP downloader
fallback rule out of file execution because the payload is piped into a newly
launched shell. Matcher and effective scope are unchanged; the fallback atom
remains in the neutral HTTP capability leaf. Soft validation passes
**1,837/1,837 fixtures**. `delivery/execute-download` drops from **294 to 293
rules**; strict validation remains at **59 issues**, including **165 over-cap
directories**. See the [mapping ledger](interpreter-stdin-mapping.json).

### Earlier checkpoint: shell file activation uses the file-exec leaf

[Shell file-exec audit](FILE-EXEC-SHELL.md) now includes thirty-five shell
download/permission-change/launch composites in the canonical activation leaf.
The latest twenty-one rules retain their matchers and scopes; cross-rule and
external consumers use canonical IDs. The FTP-banner consumers also include
both activation leaves alongside the remaining legacy directory. Soft
validation passes **1,837/1,837 fixtures**. `delivery/execute-download` drops
from **293 to 272 rules**, while `file-exec` remains under cap at **45 rules**.
Strict validation still reports **59 issues**, including **165 over-cap
directories**. See the
[mapping ledger](file-exec-shell-mapping.json).

### Earlier checkpoint: shell download fallback is a capability

[HTTP fallback audit](HTTP-DOWNLOAD-FALLBACK.md) moves two shell matcher atoms
and their cascade composite out of the dropper objective into
`communications/http/download/fallback`. The two raw-IP droppers retain the
same fallback evidence through canonical references; fallback alone does not
imply payload activation. Soft validation passes **1,837/1,837 fixtures**. The
oversized execute-download leaf drops from **306 to 303 rules**. Strict
validation remains at **59 issues**, including **165 over-cap directories**.
See the [mapping ledger](http-download-fallback-mapping.json).

### Latest checkpoint: Rust file-execution chains use the activation leaf

[Rust file-exec audit](FILE-EXEC-RUST.md) moves four composites whose evidence
joins remote file staging to a process or file-handler launch into
`dropper/file-exec`. Effective Rust/platform scopes, proximity limits,
metadata, and consumers are preserved. Soft validation passes all
**1,837/1,837 fixtures**. The oversized `delivery/execute-download` leaf drops
from **310 to 306 rules**; `file-exec` grows from **11 to 15 rules**. Strict
validation remains at **59 issues**, including **165 over-cap directories**.
See the [mapping ledger](file-exec-rust-mapping.json).

### Earlier checkpoint: PowerShell file-execution chains use the activation leaf

[PowerShell file-exec audit](FILE-EXEC-POWERSHELL.md) moves five composites
whose evidence joins remote staging or archive extraction to a process
launch or installer sink into `dropper/file-exec`. Matchers, scopes, confidence, and criticality
are unchanged; the encrypted-stage and timing consumers now reference the new
canonical IDs. Soft validation passes all **1,837/1,837 fixtures**. The strict
quality/cap debt remains catalog-wide; the oversized
`delivery/execute-download` leaf drops from **315 to 310 rules**. The new
`file-exec` leaf contains **11 rules**, well below the cap. See the
[mapping ledger](file-exec-powershell-mapping.json).

### Earlier checkpoint: shell file activation moves to its canonical leaf

[Shell file-exec audit](FILE-EXEC-SHELL.md) moves five download/chmod/launch
composites out of `delivery/execute-download` into `dropper/file-exec`, with
matchers and scopes unchanged. Four same-file references and one external
consumer were remapped. Positive local, BusyBox temp, and raw-IP checks pass;
a >30-line locality negative remains negative. The oversized delivery leaf
drops from **320 to 315 rules**; the 85-rule debt remains. See the
[mapping ledger](file-exec-shell-mapping.json).

### Earlier checkpoint: cloud credential strings classified as capabilities

[Cloud credential reference audit](CLOUD-CREDENTIAL-REFERENCES.md) moves
provider endpoint paths into their HTTP-service leaves, environment-name sets
to `os/env/cloud`, and local credential/config paths to `fs/path/credential`.
Three GCP endpoint strings leave `metadata/file/string/cloud`; Rust-specific
credential clues leave the attacker-objective leaf or reuse existing neutral
HTTP atoms. The Rust hostile composites keep their provider and compiler
constraints, and the benign MongoDB ELF retains capability markers without a
Rust credential-sweep finding. Exact fixture assertions now use explicit
`required_traits`/`forbidden_traits` fields instead of malformed path prefixes.
The soft fixture gate passes **1,837/1,837**; strict validation still reports
**59 quality/cap issues**, including **165 directories** above the 85-rule
combined cap.

### Earlier checkpoint: C# file activation and .NET XOR module loading

[C# file-exec audit](FILE-EXEC-C-SHARP.md) moves the complete C# download and
launch composite into `dropper/file-exec`, replaces four duplicated objective
atoms with canonical HTTP, process, environment-read and process-configuration
evidence, and requires the evidence to cluster within 512 bytes. Three
FTP-banner consumers retain the migrated C# rule explicitly. A nearby positive
fixture still matches; the same signals split across distant methods do not.

The .NET XOR-loader composite now lives under `dropper/module-load`, selected
by its assembly-loading sink. Its shared hex-conversion evidence moved to
`micro-behaviors/data/decode/hex`; the old mixed “assembly, temp, entry point or
process start” atom was retired. The old `delivery/execute-download` leaf
remains at **315 rules** after these partial migrations, so the 85-rule debt is
not resolved. The new activation leaves are still being populated. See the
[mapping ledgers](file-exec-csharp-mapping.json) and
[.NET module-load ledger](dotnet-module-load-mapping.json).

### Earlier checkpoint: move the remaining clear network-interface misplacements

[Network-interface cleanup](INTERFACE-CLEANUP.md) moves seven rules or
composites: best-interface route selection to `os/network/route`, domain-join
status and host-network profile composites to `os/sysinfo`, Android VPN route
configuration to `os/network/tunnel`, and Node mapped-drive enumeration to
`os/network/share`. At that checkpoint the interface leaf decreased from **59 to 52**
rules; the route leaf grows from **8 to 9**, tunnel from **27 to 29**, and share
by one.
Five broad host-profile/exfiltration consumers retain their former member sets.
All seven effective definitions compare equal modulo IDs, except that the
host-network composite description was corrected to match its existing
three-of-twelve matcher.

Soft validation passes the current **1,829 fixtures** (including 530 benign
fixtures). Strict `make validate` still reports **57 issues**, including **165
over-cap directories**; the moved rules add no reference or scope errors. The
two Google Play package-name literals were subsequently moved to
`micro-behaviors/os/application/target`; see
[APPLICATION-TARGET.md](APPLICATION-TARGET.md). The interface leaf now has 50
rules after that move.

### Latest checkpoint: separate route and neighbor-table operations

[Route/neighbor audit](ROUTE-NEIGHBOR.md) relocates ten rules from generic
interface and socket-route leaves to `micro-behaviors/os/network/route` and
`.../neighbors`. The 5 route APIs and their composite, plus route queries, now
describe routing-table behavior; ARP/IP neighbor queries and cache flushes share
the neighbor-table leaf. The source `communications/socket/route` leaf is retired.
The interface/route/neighbor boundary and the rule that a route-cache flush is
neighbor management are now documented in TAXONOMY.md.

All ten moved definitions retain their effective matcher and scope. Five
host-profile/exfiltration consumers preserve the three members moved out of the
interface leaf. Seven broad communication-directory consumers intentionally no
longer count route-table APIs as communication evidence; the consumer audit
records why. Exact route and neighbor references were updated. Soft validation
passes **1,827/1,827 fixtures**, with **165 oversized directories and zero mixed
nodes**. Strict validation still fails on catalog-wide cap and quality debts.

### Latest checkpoint: OS tunnel interfaces leave generic interface/proxy leaves

[Tunnel/interface audit](TUNNEL-INTERFACE.md) moves 27 rules with unchanged
effective matching semantics and 50 documented reference decisions. All twelve
affected directory-consumer member sets are preserved. Interface has **62 rules**,
application proxy tunnels **80**, and the new OS tunnel-interface leaf **27**.
All **330 focused verdicts** match the pre-move baseline; soft validation passes
**1,827/1,827 fixtures**. There are **165 oversized directories and zero mixed
nodes**. Strict validation remains unresolved. Preserving an Empire consumer's
conjunction required one OR helper, increasing that already oversized family
leaf from 89 to **90**; this remains cap debt without an exemption. The audit
also records semantic cleanup still needed in the now-under-cap network leaves.

### Earlier checkpoint: wireless capabilities leave the generic interface leaf

[Interface/wireless audit](INTERFACE-WIRELESS.md) moves 14 rules to the existing
wireless-network leaf, preserving their matchers, effective scopes, and all
original consumers. Interface decreases from **94 to 80 rules**; wireless
increases from **47 to 61**. Four consumer member sets and the webhook's
94-member network group are preserved; its field alternatives are explicitly
grouped without losing the 512-byte constraint. The ledger records 14 moves
and 31 reference decisions. All **136 focused verdicts** match the captured
baseline, and soft validation passes **1,827/1,827 fixtures**. There are
**166 oversized directories and zero mixed nodes**. Strict `make validate`
still reports size, scope, suppression, regex, and description debts.

### Earlier correction: classify probable capabilities from content

Distinctive strings and other static indicators belong with the probable
capability they support; proof of execution is not required. `veth` and bridge
interface references now live in `micro-behaviors/network/interface`, with
unchanged matchers and effective scope. That checkpoint left 94 interface rules;
the wireless cohort above reduces this to 80. Re-audit prior semantic-content moves into
`metadata/file/string`, starting with the pending container and port cohorts;
string counts and other real artifact measurements remain metadata. Do not
expand metadata to absorb content merely because an operation is uncertain.
The correction passes 16 focused verdicts and all 1,826 fixtures under soft
validation. There are zero mixed nodes and 167 oversized directories; strict
validation remains unresolved. The namespace audit records the five affected
directory consumers and the intentionally broadened interface evidence.

### Latest checkpoint: put interface capabilities under an OS-neutral path

The generic interface capability leaf moved from `micro-behaviors/os/network/interface`
to `micro-behaviors/network/interface`; all 61 YAML files that referenced the
old IDs now use the canonical path. Three JavaScript shell-command observations
(`ifconfig`, `ip addr`, and `ip a`) moved out of `objectives/discovery/network/interface`.
Their matcher bodies, descriptions, confidence, criticality, filetype, and
platform scopes are unchanged; their `T1016` objective tags were removed because
each atom describes a capability clue, not adversarial intent. The host-system
consumer now references a type-scoped capability composite, preserving those
command alternatives without retaining a discovery objective for a single
query. The obsolete three-leg objective helper was retired.

The capability leaf now contains **54 rules** (46 atomics and 8 composites).
The directory validator admits `network/interface` as a neutral resource home.
Focused JavaScript samples match all three moved atoms, and `test-rules` confirms
the replacement composite and host-system consumer match. Soft validation passes
all **1,837/1,837 fixtures**. Strict `make validate` still reports the
catalog's **60 issues**, including **160 over-cap directories**; it
reports no unknown-directory or stale-reference issue for this migration.

### Latest checkpoint: separate namespace behavior from runtime identity

[Container namespace audit](NAMESPACE-CLEANUP.md) moves container-runtime
identity, interface names, and host-root changes to their matching metadata or
filesystem techniques, and retires unsupported roll-ups. Namespace operations
remain in the platform-neutral `namespace` leaf, with Linux/Unix in rule scope;
the syscall-specific matcher file shares that leaf. Five port-reference and
service-table rules moved to a new `network/port` leaf, removing a mixed
parent/child node while preserving seven references from six consumers.
Focused inert controls verify relocated characteristics and retained
operations. Two filename-as-directory references in a separate .NET ransomware
composite were repaired so validation can load the catalog. Before the capability
placement correction above, soft validation completed with **1,826/1,826 passing
fixtures** and **zero mixed nodes**; **167 directories still exceeded the 85-rule
cap**. Those results do not establish acceptance of the pending semantic moves
or a passing strict validation run.

### Latest checkpoint: distinguish Kubernetes references from namespaces

[Kubernetes namespace audit](KUBERNETES-NAMESPACE.md) relocates three API/env
references, retires two unsupported/unconsumed roll-ups, and requires actual
environment-access evidence in a catalog consumer. Seven ledger entries and 30
reference decisions accompany **1,824/1,824 passing fixtures**, 30 targeted
verdicts and 12 updated regression verdicts. Namespace has 45 rules;
**167 oversized directories and zero mixed nodes** remain. Names-only catalogs
lose their false access finding; actual access and namespace controls retain coverage.


### Latest checkpoint: separate Kubernetes path prefixes from imports

[Kubernetes prefix audit](KUBERNETES-PREFIX.md) moves two directory-prefix
observations to general secret-store paths and removes the Go path shortcut
from a renamed package-import aggregate. Seven ledger entries and 14 reference
decisions accompany 16 targeted verdicts and **1,820/1,820 passing fixtures**.
Runtime has 65 rules and credential paths 37; **167 oversized directories and
zero mixed nodes** remain. The namespace aggregate's other unsupported client
identity alternatives are recorded for follow-up.


### Latest checkpoint: generic secret mounts are not token stores

[Secret-mount audit](SECRET-MOUNT.md) moves two generic directory observations
to general credential paths, preserving effective matchers and nine consumers.
The generic-mount/config control no longer manufactures a token/config pair;
a defined token/config pair retains coverage. Eleven ledger entries, 21
reference decisions and 16 targeted verdicts accompany **1,818/1,818 passing
fixtures**. Runtime has 67 rules, token paths 38, credential paths 35;
**167 oversized directories and zero mixed nodes** remain.


### Latest checkpoint: separate service-account tokens, namespace and CA files

[Service-account resource audit](SERVICEACCOUNT-RESOURCES.md) retires the
paths-as-access aggregate, moves public/configuration resources to their own
filesystem homes, and requires token evidence in credential consumers. Fifteen
ledger entries and 28 reference decisions accompany **1,816/1,816 passing
fixtures**, 20 new targeted verdicts and 15 updated regression verdicts.
Runtime has 68 rules; **167 oversized directories and zero mixed nodes** remain.
CA/namespace controls lose the false token-abuse finding; token controls retain
coverage. Remaining path-only objective claims are explicitly documented.


### Latest checkpoint: remove context-as-path evidence and repair cardinality

[Container context audit](CONTAINER-CONTEXT.md) retires the misplaced tooling
aggregate while preserving its only direct downgrade use. A second repair
replaces matching-rule counts with six explicit credential-category pairs and
updates two exfiltration consumers. Nine targeted verdicts and **1,814/1,814
fixtures** pass. Eleven ledger entries and 18 reference decisions are recorded;
**167 oversized directories and zero mixed nodes** remain. The intentional
single-category/app-data coverage changes and remaining aggregate debt are explicit.


### Latest checkpoint: Kubernetes token references follow their resource

[Kubernetes token-path audit](KUBERNETES-TOKEN-PATH.md) relocates two path atoms
with unchanged effective matchers and updates six exact consumers. Twenty
reference decisions and 15 targeted verdicts accompany **1,812/1,812 passing
fixtures**. Runtime has 71 rules, token paths 38; **167 oversized directories and
zero mixed nodes** remain. The audit records the surviving service-account
aggregate and a demonstrated context-as-secret-path cardinality defect.


### Latest checkpoint: token filename text does not establish Kubernetes

[Container token-read audit](CONTAINER-TOKEN-READ.md) relocates one mislabeled
member-reference atom to file-text metadata, preserving its exact predicate and
apply-composite consumer. Five reference decisions, ten targeted verdicts and
**1,810/1,810 fixtures** pass, including two new benign controls. Runtime has
73 rules; **167 oversized directories and zero mixed nodes** remain. The cap
count was already 167 at this cohort's start in the shared worktree. The audit
records the remaining token/namespace/CA/mount and credential-access migrations.


### Latest checkpoint: privilege vocabulary requires container context

[Container privilege audit](CONTAINER-PRIVILEGE.md) relocates four generic
observations, tightens Docker configuration evidence and repairs enabled-flag
boundaries. Six ledger entries and 14 consumer decisions are recorded. Twelve
targeted checks and **1,808/1,808 fixtures pass**, including six new benign
controls. Runtime contains 74 rules; **166 oversized directories and zero mixed
nodes** remain. Changed files introduce no remaining hygiene errors.

### Latest checkpoint: container port vocabulary and duplicate consolidation

[Container port audit](CONTAINER-PORTS.md) moves four port observations into
network metadata and retires an equivalent discovery-tier port-pair rule. Five
consumer changes and 14 reference decisions preserve contextual uses without
claiming Docker, authentication or TLS from numbers alone. Four new controls
pass; the full suite is **1,802/1,802**. Runtime contains 77 rules; **166 oversized
directories and zero mixed nodes** remain.

### Latest checkpoint: container socket references share a filesystem home

[Container socket audit](CONTAINER-SOCKETS.md) relocates seven endpoint-path
rules, updates nine consumers and records 27 reference decisions. Matchers,
scopes and exclusions are preserved; container-reference context remains where
justified, without treating paths as trusted tooling. Eight new fixtures pass;
the full suite is **1,798/1,798**. Runtime is now 81 rules, leaving **166 oversized
directories and zero mixed nodes**. Remaining runtime/image/OCI misplacements
are recorded separately from cap compliance.

### Latest checkpoint: inline fetch contents-write coverage

[GitHub fetch audit](GITHUB-FETCH.md) restores destination-bound inline fetch
PUTs without accepting method overrides or unrelated calls. Two rule changes
and 22 consumer decisions are recorded; **1,790/1,790 fixtures pass**. GitHub
contains 84 rules; **167 oversized directories and zero mixed nodes** remain.
Variable-held options remain unsupported pending a current-value contract;
mutation/spread counterexamples and a quantified-query discrepancy are recorded
for engine follow-up.

### Latest checkpoint: contents URLs separated from write evidence

[GitHub write audit](GITHUB-WRITE.md) requires write-specific evidence in the
create-and-write combination and adds a PUT atom bound to its own destination.
Eight targeted checks distinguish direct writes from reads and unrelated PUTs;
**1,790/1,790 fixtures pass**. Two rule changes and 22 consumer decisions are
recorded. GitHub contains 83 rules; **167 oversized directories and zero mixed
nodes** remain. Unsupported write implementations and the older proximity-based
write-flow rule remain explicit follow-up work.

### Latest checkpoint: repository creation requires operation evidence

[GitHub creation audit](GITHUB-CREATION.md) removes bare-path and field-only
creation shortcuts, retires two unsupported rules, and updates the affected
exfiltration consumer. Five effective changes and 37 consumer decisions are
recorded. Seven exact creation controls pass; the full fixture gate passes
**1,790/1,790**. GitHub contains 82 rules; **167 oversized directories and zero
mixed nodes** remain. Unresolved helper and obfuscated field-only coverage
changes are intentional and documented rather than hidden by a weaker claim.

### Latest checkpoint: generic options removed from GitHub activity

[GitHub options audit](GITHUB-OPTIONS.md) relocates three provider-neutral
observations and updates four exact consumers, with 23 consumer decisions.
Generic recursion, pagination and GraphQL text no longer suppress unrelated
environment uploads. Nine new fixtures pass; the full suite is **1,790/1,790**.
GitHub is now 84 rules, leaving **167 oversized directories and zero mixed
nodes**. The audit records remaining service/sibling placement and inference
issues rather than treating cap compliance as semantic completion.

### Latest checkpoint: parsed PowerShell helper identity

[PowerShell library audit](POWERSHELL-LIBRARY.md) replaces three text matchers
with parsed assignments and bound encoder/launch relationships. The actual helper
and a renamed parameter retain recognition; commented and mismatched controls
do not activate its exception. **1,781/1,781 fixtures pass**. The library
description/regex failures are resolved; **168 oversized directories** and the
separate suppression/description debt remain.

### Latest checkpoint: bound HTTP hostname transfer and definition-aware dedup

[Shell hostname-flow audit](SHELL-HOST-FLOW.md) binds identity output through
hex encoding into the next HTTP hostname, adds single-line pipeline coverage,
and rejects seven negative flow/shadowing cases. The objective moves from DNS
to HTTP hostname transport; three unsupported/redundant composites retire.
Ten ledger entries and 58 consumer decisions include a canonical shared curl
definition guard. The engine now preserves function definitions when comparing
cross-type matchers: **14 validator tests pass**. The rebuilt engine passes
**1,781/1,781 fixtures**. **168 oversized directories** and zero mixed nodes
remain; strict validation additionally reports separate PowerShell, WASM,
Silver Sparrow description/regex issues and suppression-count debt.

### Latest checkpoint: literal limit separated from DNS truncation

[DNS limit audit](DNS-LIMIT.md) relocates a numeric assignment and curl URL
shape, retires a false truncation/exfiltration inference and its one-leg roll-up,
and updates three consumers. Seven ledger entries and 33 ancestor decisions
record the change. **1,771/1,771 fixtures pass**; an ordinary service request is
neutral and a multiline hex-identity hostname transfer remains hostile.
**168 oversized directories** and zero mixed nodes remain, along with the
concurrent PowerShell strict-validation failures. The retained `xxd` matcher
misses single-line pipelines; repair its data relationship before broadening it.

### Latest checkpoint: domain preparation claims separated from transfer

[DNS preparation audit](DNS-PREPARATION.md) relocates three neutral observations,
retires four unsupported/redundant composites and updates three consumers.
Seventeen ancestor decisions record the changed support. Two ordinary-settings
controls lose false hostile verdicts; actual DNS identity egress remains
unchanged. **1,769/1,769 fixtures pass**. **168 oversized directories** and zero
mixed nodes remain. Strict validation still also reports the concurrent
PowerShell description/regex-length and suppression-count failures.

### Latest checkpoint: analyzer-based DNS AST leaf retired

[DNS AST closure](DNS-AST-CLOSURE.md) moves domain-like formatting to string
construction and retires its unsupported packing/exfiltration profile. Three
ledger entries and four ancestor decisions record the change. An ordinary
configuration control loses a false hostile verdict; actual host-identity DNS
egress retains identical findings. **1,767/1,767 fixtures pass**. The `dns/ast`
directory and production references are gone; **168 oversized directories**
and zero mixed nodes remain. Strict validation also reports concurrent
PowerShell description/regex-length and suppression-count failures, separately
from this DNS migration.

### Latest checkpoint: DNS construction requires coherent labels

[DNS construction repair](DNS-CONSTRUCTION.md) replaces generic two-of packing
inference with a bound label/length encoder and corroborating construction
evidence. Two neutral primitives leave `dns/ast`; its loose manual-label profile
is retired. Six effective-definition changes and 20 consumer decisions record
the intentional coverage changes. Three benign controls require correct
construction and reject arbitrary framing/mismatched lengths. **1,765/1,765
fixtures pass**; strict validation still reports **168 oversized directories**.
Two `dns/ast` rules remain, as do co-occurrence-based downstream intent claims.

### Latest checkpoint: binary packing separated from DNS identity

[DNS packing audit](DNS-PACKING.md) relocates six generic packing observations
to integer framing and binary serialization, with unchanged predicates and four
exact consumer rewrites. Ten ancestor decisions document the semantic narrowing
of communications/exfiltration directories. Two controls retain identical
findings modulo IDs. **1,762/1,762 fixtures pass**; strict validation still reports
**168 oversized directories**, with zero mixed nodes. The control exposes an
unchanged DNS-construction composite that accepts generic packing alone; repair
that evidence boundary next. The remaining five `dns/ast` rules also need audit.

### Latest checkpoint: fabricated DNS construction chain retired

[DNS placeholder audit](DNS-PLACEHOLDERS.md) removes two sentinel-string atoms,
their tunneling roll-up and a dependent exfiltration composite. Three optional
consumers and six ancestor references are audited. A sentinel-only negative
control loses the false verdict; a real encoded-label egress control retains
its complete findings. **1,762/1,762 fixtures pass**. Strict validation reports
**168 oversized directories**, with zero mixed nodes; DNS tunneling is 83 rules.
Overlapping DNS C2 and exfiltration branches remain open for semantic migration,
including unsupported name-only claims and an analyzer-based `ast` directory.

### Latest checkpoint: native-host fixture evidence corrected

[Native-host fixture review](NATIVE-HOST-FIXTURE.md) retains the retirement of
the unsupported setup-as-staging detector. The original archive is preserved
byte-for-byte as a negative control; a new inert remote-tasking/native-execution
control requires the positive objective. The shared checkout now passes
**1,760/1,760 fixtures**, resolving the discrepancy below without restoring the
detector. Strict validation still reports **169 oversized directories**.

### Latest checkpoint: TLS initialization separated from connection

[TLS initialization audit](TLS-INITIALIZATION.md) moves five setup observations
to one `tls/initialize` leaf and retires a connection roll-up that accepted
constructors. Nine ledger entries and eight ancestor decisions preserve primitive
matching and exact consumers. Five control scans agree modulo IDs. **1,759/1,759
fixtures pass in an isolated copy restoring only the pre-existing native-host
detector**; the shared suite currently has one native-host fixture failure from
concurrent detector retirement. That discrepancy is not repaired by reverting
the unrelated work. Strict validation reports **169 oversized directories**;
zero mixed nodes. The shared fixture discrepancy and broader migration remain open.

### Latest checkpoint: unbound API argument-byte claims repaired

[Call-argument byte audit](CALL-ARGUMENT-BYTES.md) reproduces six false OpenSSL
operation claims on inert ELF controls whose calls target a local return stub.
Six observations move to metadata; a beacon consumer retains its predicate
under a corrected name. Seven ledger entries and ten ancestor decisions record
the changes, including two intentional profile criticality corrections.
**1,755/1,755 fixtures pass**; strict validation reports **169 oversized
directories**, with zero mixed nodes. Actual call-target binding remains a
requirement before these byte shapes can support an API-operation claim.

### Latest checkpoint: warning suppression consolidated

[Warning suppression audit](WARNING-SUPPRESSION.md) moves general urllib3
warning control to diagnostics, merges a narrower matcher into the existing
canonical rule, and retires a redundant OR roll-up. Twelve ancestor decisions
remove warning suppression as HTTP/communications evidence. Three fixtures
separate warning controls from disabled verification. **1,753/1,753 fixtures
pass**; **169 oversized directories** remain. The literal option/guard observation
and other legacy TLS operations still need audit.

### Latest checkpoint: canonical TLS verification-disable operation

[TLS verification consolidation](TLS-VERIFICATION.md) moves nineteen rules from
HTTP/socket branches to `communications/tls/verify/disable`, retiring `http/ssl`.
All moved effective predicates are unchanged. Fifty ledger entries and seventeen
ancestor decisions cover the moves and consumers; five controls retain identical
findings modulo IDs. **1,750/1,750 fixtures pass** on the rebuilt engine; strict
validation reports only **169 oversized directories**, with zero mixed nodes.
Remaining TLS observations still need operation-based placement and precision
repairs described in the preceding boundary audit.

### Latest checkpoint: TLS evidence boundaries

[TLS boundary audit](TLS-BOUNDARIES.md) moves generic NSPR I/O and domain-intel
vocabulary out of socket TLS, preserves the corroborating I/O composite, and
removes an unsupported word-only exclusion from disabled-verification detection.
Three controls and eight ancestor decisions cover the changed boundaries.
**1,745/1,745 fixtures pass**; socket SSL is **85 rules**, leaving **169 oversized
directories** and zero mixed nodes. The report records the operation-based
reorganization needed across socket/ssl, http/ssl and http/tls.

### Latest checkpoint: accounting literal claims corrected

[Accounting literal audit](ACCOUNTING-LITERALS.md) moves eleven rules whose
matchers detect quoted text, not the source declarations their old names claimed.
Before/after traces preserve all eleven literal matches and reject actual syntax.
The ledger and 89 ancestor decisions document intentional removal of vocabulary
from compiled-language suppression. **1,742/1,742 fixtures pass**; **170 oversized
directories** remain. The account/accounting sibling-name advisory is reviewed
as distinct subjects, without a validator exemption. The engine now makes
shared-stem reviews non-blocking; strict validation reports only cap debt.
Remaining compiled-source
and runtime observations still require audit.

### Latest checkpoint: WebAssembly declarations separated from attribution

[WASM observations](WASM-OBSERVATIONS.md) moves seven parsed export/producer
facts to existing metadata subjects and preserves three attribution profiles.
The ten-entry ledger and 105 ancestor decisions document effective predicates
and intentional removal of weak suppression evidence. Three inert controls test
exports, name-only text, and isolated-helper attribution. **1,740/1,740 fixtures
pass**; **170 oversized directories** remain, with zero mixed nodes. Strict
validation reports only cap debt. `lang/compiled` is now 79 rules but still
contains misplaced source/runtime observations requiring further audit.

### Latest checkpoint: graphics vocabulary and provider identity

[Graphics audit](GRAPHICS-VOCABULARY.md) moves nine observations, retires three
weak library-reference aggregates, and replaces word-only Mesa identity with
provider-name/interface evidence. Four controls distinguish vocabulary, identity,
and each missing requirement. The 30-entry ledger and 74 ancestor decisions
record the migration and associated duplicate/hygiene repairs. **1,737/1,737
fixtures pass**, with **171 oversized directories** and **zero mixed nodes**.
Strict validation still fails on that cap debt; the overall plan remains open.

### Latest checkpoint: ABI recognition repaired with consumer cleanup

[ABI repair audit](ABI-REPAIR.md) fixes two normalization-sensitive regexes,
removes unsupported library identity and exception-obfuscation inferences,
and consolidates sparse-string predicates and redundant wrappers. The 21-entry
ledger excludes unrelated concurrent archive edits; 95 ancestor occurrences
are reviewed. A directory-reference cycle is avoided by retaining system-fn's
five original primitive alternatives. **1,733/1,733 fixtures pass**; **172
oversized directories** remain, with zero mixed nodes. The previously recorded
ABI matching gap is closed; broader library and binary-metric audits continue.


### Latest checkpoint: binary declarations and string counts separated from intent

[Binary observation audit](BINARY-OBSERVATIONS.md) relocates eleven observations
and records twenty-seven consumer updates in a verified 38-entry ledger.
Thirteen ancestor occurrences are audited. Binary-metrics/shape falls **88→85**,
reducing cap violations to **172** with zero mixed nodes. **1,730/1,730 fixtures
pass**. A pre-existing ABI-symbol normalization gap is reproduced before and
after migration and remains open; its library-family exclusions must be audited
when repairing those regexes. Remaining Mesa references and other binary metrics
still need precise placement.


### Latest checkpoint: runtime-indirection directory retired

[Runtime profile audit](RUNTIME-PROFILES.md) moves three observations, retires
two unsupported aggregates and preserves three specific exclusions in an
eight-entry ledger. Thirteen ancestor consumers are audited. Neutral conversion
no longer receives an obfuscation verdict, and package tests no longer supply
exfiltration evidence. Four controls bring the gate to **1,728/1,728 passing
fixtures**; strict validation still reports **173 oversized directories**, with
zero mixed nodes. Binary string-count/graphics dependencies, remaining
code-metrics, source/syntax and retry branches still require work.


### Latest checkpoint: runtime-indirection atoms separated from decoding claims

[Runtime observation audit](RUNTIME-OBSERVATIONS.md) moves two neutral atoms to
identifier metadata and character conversion, updates their composite and
preserves a conservative helper exclusion. The four-entry ledger and five
ancestor decisions document preserved matching and intentional concealment
boundary corrections. **1,724/1,724 fixtures pass**, with **173 oversized
directories** and zero mixed nodes. The three remaining runtime-indirection
composites still require a semantic audit; this checkpoint does not endorse
their existing category or intent claims.


### Latest checkpoint: source/array leaf retired into semantic subjects

[Array operation audit](ARRAY-OPERATIONS.md) relocates all eighteen rules and
updates fourteen exact consumers in a verified [32-entry ledger](array-operations-mapping.json).
The obsolete source/array directory is removed with no remaining YAML references.
Four new controls include standalone Rust zero initialization.
**1,722/1,722 fixtures pass**; strict validation reports only **173 oversized
directories**, with zero mixed nodes. Remaining source/syntax, runtime-indirection,
retry and composite-relationship audits remain in scope.


### Latest checkpoint: hexadecimal notation separated from operations and concealment

[Hexadecimal observation audit](HEX-OBSERVATIONS.md) relocates nine observations
and updates eighteen consumers in a verified [27-entry ledger](hex-observations-mapping.json).
Twenty-one ancestor consumers were audited. Matchers, scopes and criticalities
are preserved; names no longer invent mixed radices, arrays, string operations
or decoding. The hex obfuscation leaf falls from **30 to 23 rules**.
**1,718/1,718 fixtures pass** with four new controls; strict validation reports
only **173 oversized directories**, with zero mixed nodes. Remaining composite
relationships and source-array, runtime-indirection and retry siblings are
recorded for continued migration.


### Latest checkpoint: function shape and computed access placed in neutral subjects

[Neutral function-shape audit](NEUTRAL-FUNCTION-SHAPE.md) moves six observations
to function metadata, property access and dispatch; six exact consumers and five
ancestor consumers are recorded in a [12-entry ledger](neutral-function-shape-mapping.json)
and accompanying inventory. Threshold-distinct metadata siblings remain separate.
**1,714/1,714 fixtures pass**, including three new controls. Strict validation
reports only **173 oversized directories**, with zero mixed nodes. The report
records a standalone debugger stall and the remaining runtime-indirection,
retry and hexadecimal sibling audits.


### Latest checkpoint: archive regression repaired; full fixture gate restored

[Archive validation audit](ARCHIVE-VALIDATION.md) repairs cross-member
retroactive suppression and a separately reproduced container-evaluation
starvation bug. **29 unit tests** pass, and the encrypted-stage fixture again
retains three hostile findings and its required staged-payload observation.
The rebuilt checkout engine passes **1,711/1,711 fixtures** with unchanged
expectations. Strict validation fails only on **173 oversized directories**.
Resume the remaining neutral-obfuscation and oversized-leaf migration work.


### Latest checkpoint: capture-free AST queries repaired and misclassified observations moved

[AST capture audit](AST-CAPTURES.md) repairs five canonical observations from six
inert queries, consolidates the nested-array duplicate, and moves unsupported
encoding/timing/family claims to neutral homes. A [12-entry ledger](ast-capture-mapping.json)
and seventeen ancestor consumers were verified. Five direct positive and five
negative query checks pass, as do six new fixture controls. Strict validation
reports only **173 oversized directories**, with zero mixed nodes.

**Historical verification failure, resolved above:** the then-newly rebuilt checkout engine
loses an existing encrypted-stage archive finding with both the before and
after rules. The installed engine retains it with both. The report records
this isolated engine regression; fixture requirements remain unchanged.


### Latest checkpoint: computed dispatch and member access classified by evidence

[Computed-dispatch audit](COMPUTED-DISPATCH.md) relocates thirteen neutral
observations, retires one redundant aggregate and records ninety-three consumer
updates in a [107-entry ledger](computed-dispatch-mapping.json). Seventy-five
ancestor consumers were audited. An inert AST query now captures indexed
addition with a verified negative boundary. Five new fixtures bring the corpus
to **1,705/1,705 passing**; strict validation reports only **173 oversized
directories**, with zero mixed nodes. Syntax remains oversized at 101 rules.
Remaining neutral obfuscation measurements, six capture-free AST queries and
relationship-sensitive composites are documented for the next audit.


### Latest checkpoint: property operations migrated and reference validation corrected

[Property operation audit](PROPERTY-OPERATIONS.md) completes retirement of
`data/source/property`, with **53 relocations** and a verified
[113-entry ledger](property-operations-mapping.json). An overlooked ancestor
consumer now retains all **74** former alternatives. The attributes matcher is
repaired, and the validator no longer requires widening partial `any` lists or
replacing `all` conjunctions. **75 validator tests** and **1,700/1,700 fixtures
pass**; strict validation reports only **173 oversized directories**, with zero
mixed nodes. The report records the local dependency used for engine validation
and remaining computed-call, loop-duplicate and relationship audit work.


### Latest checkpoint: property identity split and false exfiltration helper corrected

[Property audit](PROPERTY-IDENTITY.md) retires the historical identity/read leaves,
classifies twenty-eight observations by their supported subjects, and preserves
consumer alternatives in a [53-entry ledger](property-identity-mapping.json).
A field/dot-join helper is now neutral; this removes a reproduced suspicious
MCP-injection false positive (archive/member scores **42/41→5/4**). Direct traces
verify its 2,048-byte proximity behavior. Eighteen engine directory tests and
**1,697/1,697 fixtures pass**. **173 oversized directories** and zero mixed nodes
remain; the report identifies the remaining property-sibling and relationship
work. The wider migration remains incomplete.


### Latest checkpoint: account vocabulary receives a canonical home

[Account vocabulary audit](ACCOUNT-VOCABULARY.md) moves nineteen observations
from relational schema, serialization and telemetry to neutral account naming.
The [26-entry ledger](account-vocabulary-mapping.json) verifies preserved matching
conditions and consumer references. Four archive/member controls preserve
findings and criticalities; their aggregate scores fall by one point, documented
as a classification effect. **1,693/1,693 fixtures pass**, with **173 oversized
directories** and zero mixed nodes. The report identifies the remaining
source-property, telemetry and relationship-consumer audit work.


### Latest checkpoint: SQL mutation operations separated

[SQL operation audit](SQL-OPERATIONS.md) moves fifteen syntax observations into
row-write, row-delete and schema-delete leaves while preserving predicates and
consumer alternatives. The [31-entry ledger](sql-operations-mapping.json)
verifies against current definitions. Three new controls preserve findings and
scores across six archive/member comparisons; **1,691/1,691 fixtures pass**.
SQL falls from **78 to 65 rules**; **173 oversized directories** and zero mixed
nodes remain. Editor/API fragments, account fields and catalog siblings are the
next documented precision work; the wider migration is incomplete.


### Latest checkpoint: SQL-based suppression dependency removed

[SQL suppressor audit](SQL-SUPPRESSORS.md) moves eleven language/vocabulary
observations to neutral homes, removes unrelated SQL exclusions and retires a
string-pattern-only dropper verdict. The [22-entry ledger](sql-suppressors-mapping.json)
verifies. The metadata section-filter recommendation is now advisory as its
validator contract intended; five related tests pass. Six archive/member checks
exercise SQL-present and SQL-absent controls, and **1,688/1,688 fixtures pass**.
IRC bot falls from **90 to 81 rules**, oversized directories from **174 to 173**,
with zero mixed nodes. SQL operation regrouping and wider migration remain open.


### Latest checkpoint: database mutation claims corrected

[Mutation-claim audit](DB-MUTATION-CLAIMS.md) replaces an unsupported
telemetry-deletion conclusion with accurate method/symbol observations, adds
a receiver-specific row-truncation observation, and corrects the plaintext-
password claim. The [five-entry ledger](db-mutations-mapping.json) verifies.
Three new controls reproduce the old errors and check actual truncation syntax;
all six archive/member checks and **1,686/1,686 fixtures pass**. SQL contains 78
rules; strict validation reports **174 oversized directories**, with zero mixed
nodes. SQL mutation regrouping and the wider migration remain open.


### Latest checkpoint: SQL schema observations relocated

[SQL/schema audit](SQL-SCHEMA.md) moves ten observations to existing relational,
introspection and stored-code leaves. The [20-entry ledger](sql-schema-mapping.json)
records those relocations and consumer updates. An ADO consumer now explicitly
requires the catalog its comment promised; the report documents this intentional
tightening and the directory-counting ambiguity behind it. **1,683/1,683 fixtures
pass**. SQL falls from **89 to 79 rules**, oversized directories from **175 to
174**, and mixed nodes remain zero. The report lays out remaining SQL/editor/API
and schema-sibling corrections; the wider migration is incomplete.


### Latest checkpoint: generic DOM operations separated from browser UI

[DOM operation audit](DOM-OPERATIONS.md) moves 24 observations into the generic
DOM leaf, preserves the sole parent-subtree consumer's original alternatives,
and fixes a local consumer reference. The [26-entry ledger](dom-mapping.json)
verifies unchanged relocation conditions and current definitions. A new control
retains identical findings modulo renamed IDs and identical scores.
**1,682/1,682 fixtures pass**, with **175 oversized directories** and zero mixed
nodes. Generic DOM contains 25 rules. Parser/HTML/browser sibling boundaries and
the wider cap migration remain open, as detailed in the report.


### Latest checkpoint: Base64 backend partition retired

[Base64 symbol consolidation](BASE64-SYMBOLS.md) migrates 19 observations into
15 canonical rules and removes `decode/symbol-base64`. Five Go API variants
share their exact predicate union; compiled decoder identity now requires the
Base64 package. The [156-entry ledger](base64-symbols-mapping.json) accounts for
those observations and 137 updated consumers, including three deliberately
broadened Go consumers. Ten archive/member checks distinguish hexadecimal from
Base64 decoding. **1,681/1,681 fixtures pass**, with **175 oversized directories**
and zero mixed nodes. The unified Base64 leaf contains exactly **85 rules**.
Generic DOM siblings, remaining predicate precision issues, and the broader
cap migration remain open.


### Latest checkpoint: XML observations separated from codec direction

[XML codec audit](XML-CODECS.md) relocates ten observations by DOM operation,
XML parsing or XML typing; corrects the Base64 aggregate; and adds bound
JavaScript encode/decode sequences. Two consumers retain their requirements
under names that do not assert unproven conversion flow. The
[15-entry ledger](xml-codec-mapping.json) verifies. Four new archives test both
directions and unrelated receivers/types; all 17 archive/member exact-ID checks
pass. **1,679/1,679 fixtures pass**, with **175 oversized directories** and zero
mixed nodes. Base64 decoding is at 70 rules. Generic DOM siblings, symbol-backend
consolidation, and the wider cap migration remain open. The report documents
the intentionally bounded directional coverage and remaining consumer risks.


### Latest checkpoint: arithmetic separated from codec claims

[Arithmetic audit](ARITHMETIC.md) relocates 25 observations, retires one
unsupported decoder aggregate, and narrows the Base64 umbrella. The
[27-entry ledger](arithmetic-mapping.json) verifies that all relocated matching
conditions are preserved. Ordinary shifts and binary formatting retain their
specific findings without claiming Base64 decoding. **1,675/1,675 fixtures
pass**; strict validation reports only **175 oversized directories**. There are
zero mixed rule directories, and Base64 now contains 78 rules. The validator's
18 directory tests pass with the documented arithmetic category admitted.
XML conversion direction, the symbol-backend partition, and the wider cap
migration remain open; this checkpoint does not complete the plan.


### Latest checkpoint: mixed encoded-data branch retired

[Format-branch migration](DECODE-FORMATS.md) moves six observations into existing
format/assembly leaves and retires `data/decode/encoded`. Its mixed transformation
umbrella is expanded into the same named alternatives in three consumers. The
[ten-entry ledger](decode-formats-mapping.json) verifies; a control exercises all
six moved observations. **1,674/1,674 fixtures pass**, with **175 oversized
directories** and zero mixed rule directories remaining. Base64 is at 82 rules.
Symbol-backend consolidation, XML directionality, and the wider cap audit remain
open; the report records the proximity/span-grouping limit of this migration.


### Latest checkpoint: Buffer calls and JSON conversion

[Computed-call and JSON audit](BASE64-CALLS.md) relocates generic Buffer dispatch
and JSON conversion observations, replaces a nearby-token test with a structured
Base64-to-JSON relationship, and corrects the parenthesized-eval classification.
The [ten-entry ledger](base64-calls-mapping.json) verifies. **1,673/1,673 fixtures
pass**; the Base64 leaf is now **80 rules**, with **175 oversized directories**
and zero mixed rule directories overall. XML directionality, the symbol-backend
partition, and the remaining format cohort are still open work, documented in
the report. This checkpoint does not complete the migration.


### Latest checkpoint: Base64 supporting observations

[Base64 cohort audit](BASE64-SUPPORT.md) moves eleven import, alphabet and file-
write observations to their actual subjects, updates consumers, and corrects
an umbrella that treated supporting observations as decoding. The
[13-entry ledger](base64-support-mapping.json) verifies. The decoding leaf drops
from 90 to **84**, and oversized directories drop from 176 to **175**. Three new
controls distinguish imports/constants, decoding and encoding; **1,670/1,670**
fixtures pass, with zero mixed rule directories. The report records remaining
symbol-backend, XML, computed-call and format sibling work; fitting this one
leaf under the cap does not complete that cohort or the broader migration.


### Latest checkpoint: encoded reverse-shell leaf retired

[Final encoded-leaf audit](ENCODED-FINAL.md) retires the Python import/shell and
PHP label verdicts, places six neutral observations in their semantic homes,
and removes `reverse-shell/encoded`. The [eight-entry ledger](encoded-final-mapping.json)
verifies. New stored-text controls score 12 as an archive, and an encoded Python
relay retains stream-bridge coverage. **1,667/1,667 fixtures pass**; strict
validation still reports **176 oversized directories**, with zero mixed nodes.
The audit also records a reproduced PHP decoded-snippet parsing gap, which labels
cannot repair. This checkpoint does not finish the cap migration or sibling audit.


### Latest checkpoint: encoded Unix/JVM carriers

[Encoded carrier audit](ENCODED-UNIX.md) retires four unsupported Perl, Elixir
and Kotlin reverse-shell verdicts, relocates three neutral shell observations,
and removes the related decode/exec proximity verdicts and dependent wrappers.
The [17-entry ledger](encoded-unix-mapping.json) verifies; two new benign
archives score 4 and 5, while all three real encoded payloads retain hostile
`dev-tcp` detections. The full soft suite passes **1,665/1,665** fixtures.
Strict validation still fails only on **176 oversized directories**; no mixed
rule directories remain. Three Python/PHP rules remain in `reverse-shell/encoded`.
This is an intermediate checkpoint, not completion of the cap migration.


### Execution revision: simplify placement before expanding the tree

The directory policy remains **strictly leaf-only**. Mixed parent/child YAML
was tried previously and gave similar rules multiple homes. Broad evidence
must be resolved by its actual shared operation, metadata claim, or independently
meaningful alternatives; an opaque broad capability needs a defensible leaf
partition before migration. An unresolved placement is recorded rather than
hidden in a generic bucket or an invented narrower claim. Follow the
[placement procedure](../../TAXONOMY.md#directory-budgets-and-placement-contracts).

Leaf-only recheck (2026-09-27): scanning 19,940 YAML files found one mixed
directory, `metadata/package/documentation`, with parent rules in
`npm-readme-anomalies.yaml`. Audit those rules against its documentation
children and package-description metadata before moving them; their README
claims, manifest-description observation, and filename observation do not all
have the same subject. Parent composites and aliases are not exceptions to
the leaf-only requirement. This live finding supersedes earlier zero-mixed
snapshots; the migration remains incomplete.

That mixed node is now resolved: see [Documentation leaf repair](DOCUMENTATION-LEAVES.md)
and its [10-entry mapping](documentation-parent-mapping.json). A fresh four-tier
scan finds **zero mixed rule directories**. All destination leaves fit the cap
(36, 27, 10, and 13 rules), and every ledger destination matches its recorded
effective definition. No stale moved IDs remain in rules, fixtures, or engine
sources. The final soft run passes **1,631/1,631** fixture checks, including
four new controls capped at 5; local atomscan scores those controls at 1–4.
Strict validation still reports **176 oversized directories**, plus **six
four-platform scope findings** inherited from the migrated definitions. The
report explains why retaining Android/iOS coverage requires resolving that
separate validator heuristic. No scope exception or coverage reduction was
used to make the migration appear complete.

Work in this order:

1. Resolve broad-evidence destinations and nearest-sibling boundaries in each
   proposed split. Keep the author-facing decision procedure short; put
   historical rationale in this audit rather than repeating it in contracts.
2. Fix duplicate normalization and the reproduced scope/confidence blind spot.
   Compare effective scopes and constraints before recommending a merge;
   retain genuinely different quantitative observations.
3. Finish retiring `reverse-shell/socket-exec`, including its references and
   positive/negative fixtures. Use the completed migration as the pilot.
4. Coordinate boundaries across dropper, obfuscation, injection, exfiltration,
   and supply-chain, then migrate bounded batches with all dependent references
   updated together. Do not make the entire cross-domain audit one edit batch.

Review outcomes separately: fewer competing destinations, preserved or
explicitly corrected detections, and measured model effects. A move from
`obfuscation/string/encoding` to `obfuscation/string-encoding` does not by itself
change the current direct prefix `objectives/anti-static/obfuscation`.
Use independent placement reviews on representative unfamiliar matchers to
check whether contracts actually give authors the same destination.

The implemented policy is **one inclusive cap of 100 total rules per directory**,
counting atomic traits and composite rules together, with **no exemptions**.
There is **no hard physical-depth limit**. Depth above five directories below
any tier receives a soft, non-blocking validation warning; the tier and YAML
filename do not count. Prefer breadth when sibling techniques remain equally precise;
retain depth when it gives a matcher one unambiguous semantic home. The current
path-presence/max-criticality model feature uses the tier plus two descendants,
so deeper distinctions are not guaranteed direct features; the taxonomy must
record that model limitation without forcing lossy flattening. The validator
now reports sparse sibling cohorts as an advisory. A first path-resource
migration tranche is recorded in the [implementation-layer audit](IMPLEMENTATION-LAYERS.md);
cap and semantic taxonomy audits remain active work.

| Measurement | Result |
|---|---:|
| YAML files containing rules | 20,798 |
| Atomic traits / composites | 79,333 / 39,475 |
| Total rules / directories containing rules | 118,808 / 8,724 |
| Directories exceeding the current 100-combined cap | **79** |
| Violators by tier | 78 objectives, 1 well-known |
| Rules in violating directories | **9,861** |
| Sum of excess above 100 | **1,961** |
| Violators plus sibling subtrees inventoried | 1,176 rule directories / 29,643 rules |
| Identical atomic `if` bodies touching violators | 63 groups / 142 rules |

1,961 is the minimum number of rules that must leave their *current* oversized
directories or be removed; it is not a proposed deletion count. Reclassifying
all contents of a retired directory will move more. Destination capacity must
also be measured; moving 20 rules into an 80-rule sibling simply moves the error.

The released/default binary initially enforced the old atomic-only policy.
The sibling engine checkout already contained uncommitted combined-counting
work at 80. That work was preserved, its threshold was later raised to 100, and
the reverse-shell exemption removed. The old exemption concerned `reverse-shell/dup`,
which currently has only 52 rules. The actual reverse-shell violator is
`reverse-shell/socket-exec`, with 151. Removing the exemption therefore creates
no additional failure at this snapshot, but prevents future bypasses.

Validation evidence:

- Before the cap policy changed, `make validate` passed all 1,583 fixtures.
- The latest `make validate` using the available prebuilt v2.12 binary exits
  with the expected **79 over-cap directories** and also reports **18** clauses
  containing a directory plus a trait already covered by that directory. It
  reports no unknown subdirectories or broken references for the current
  moves. Building the current adjacent engine source remains blocked by its
  unrelated call to `stng::decode_xor_fat_macho`, which the locked `stng`
  revision does not expose; the current-source build therefore remains
  unverified.
- Synthetic npm, PowerShell, and Java-class cases cover the current
  system-information reclassifications: remote command execution is required
  for the WebSocket dispatch rule; host-profile discovery without upload does
  not trigger the stealer rule; adding `Out-File` and `curl -T` does; and the JVM
  profile-marker rule requires both byte patterns.
- Boundary tests now cover all-atomic, all-composite and mixed 100/101 limits,
  76 atoms without an atomic cap,
  separate-directory budgets, the former exempt path, and depth counting.
  The two focused current-source tests for combined counting and the former
  exemption pass when built against the adjacent working-tree `stng` API.
- The available prebuilt release was used for the taxonomy move smoke check;
  it still reports the existing benign `pyaigis-top10.tar.xz` false positive.
  Its 100/101 boundary behavior is verified separately, but current-source
  build and full strict corpus validation remain open.

## Current migration progress

**Latest batch (2026-09-27):** the
[Windows encoded-launcher audit](ENCODED-WINDOWS.md) moves command flags, hidden
Run arguments and encoded TCP type references to their actual subjects, reuses
canonical Run observations, and retires four unsupported reverse-shell verdicts.
An explicit creation-name observation moves from TCP to socket/create, keeping
every destination within 85. All **1,661/1,661** fixture checks pass, including a
genuine decoded command channel. The 11-entry ledger verifies; no mixed rule
directories remain. Strict validation still fails only on **176 oversized
directories**. Seven encoded rules and the broader cap/implementation cohorts
remain open; carrier-decoding limits are documented in the report.

**Preceding batch:** the
[C# stream audit](CSHARP-STDIO.md) consolidates four source verdicts around
bound bidirectional transfers, retires an unsupported CLR-name aggregate, and
moves named dispatch/TCP observations to their neutral subjects. The nine-entry
ledger verifies. `reverse-shell/stdio` is now empty and removed; socket/tcp is
exactly **85** rules. All **1,657/1,657** fixture checks pass, with zero mixed
directories. Strict validation again fails only on **176 oversized directories**.
The earlier independent exception/suppression findings no longer appear. Source
coverage limits, other relay siblings, and the broader cap migrations remain open.

**Preceding batch:** the
[Telnet relay audit](TELNET-RELAYS.md) consolidates overlapping FIFO verdicts,
requires a shell in two-channel pipelines, and retires a persistent-shell
aggregate reproduced by printing four strings. Genuine FIFO and two-channel
forms belong in stream-bridge, not PTY. All **1,653/1,653** fixture checks pass;
the six-entry ledger verifies and no mixed directories remain. Strict validation
reports **176 oversized directories** plus one exception-member error in a
separate live PyPI credential-reference edit, recorded in the report. Two C#
rules remain in stdio; the broader sibling and cap migrations remain open.

**Preceding batch:** the
[Python stdio migration](PYTHON-STDIO.md) replaces three overlapping verdicts
with one stream-bridge composite requiring explicit input/output transfers and
shell creation. It retires unsupported receive/send and PTY aggregates, renames
keyword-argument observations honestly, preserves the blockchain consumer, and
repairs a TCP-profile placement found during the connection audit. All
**1,644/1,644** fixture checks pass. The 11-entry effective-definition ledger
verifies, every destination fits 85, and no mixed rule directories remain.
Strict validation still fails only on **176 oversized directories**. Three
C#/FIFO rules remain in stdio. Callback identity/data-flow limitations and the
remaining sibling/cap migrations are documented as unfinished work.

**Preceding batch:** the
[unsupported stdio audit](UNSUPPORTED-STDIO.md) retires five verdicts that lacked
their claimed relay or gating evidence and moves the self-deletion composite
to its existing subject leaf, now exactly **85** rules. The local computed-code
false positive is verified by restoring the old rule in an isolated snapshot:
the archived control scores 126 with the old hostile finding, versus 8 under
the current rules. This avoids a fixture-path exclusion that masked the plain
source regression. All **1,641/1,641** fixture checks pass; there are zero mixed
directories, and strict validation still fails only on **176 oversized leaves**.
Seven Python/C#/FIFO rules remain in `stdio`; encoded and the other planned
cohorts remain open.

**Preceding batch:** the
[JavaScript pipe-endpoint follow-up](JAVASCRIPT-PIPE-ENDPOINTS.md) replaces
independent pipe co-occurrence in seven relay composites with a neutral atom
requiring matching peer and child identifiers. The reproduced local-file-pipe
false positive disappears; mismatched children also fail, while output-first
and comma-separated genuine relays remain detected. All **1,640/1,640** fixture
checks pass, including 24 reverse-shell controls. All seven effective mappings
verify; `fd/stdio` holds 71 rules and there are zero mixed rule directories.
Strict validation still fails only on **176 oversized directories**. This
syntactic matcher does not resolve aliases or prove the peer's network type;
those coverage limits and the opaque-obfuscation verdict remain explicit audit
work alongside the remaining reverse-shell siblings.

**Preceding batch:** the
[JavaScript stdio audit](JAVASCRIPT-STDIO.md) fixes a reproduced four-verdict
false positive on independent networking and local shell execution. Three
overlapping relay composites merge with explicit input/output pipe requirements;
the variable-shell and extension wrappers gain the missing evidence. Neutral
environment/pipe observations have canonical homes, and reviewed relay rules
move into `stream-bridge`. All 21 recorded dispositions verify. The three new
controls preserve genuine JS/TS and extension relays while rejecting independent
local operations. All **1,636/1,636** fixture checks pass; zero mixed directories
remain. Strict validation still fails only on **176 oversized directories**.
Next: cross-call peer/child binding checks, the opaque-obfuscation verdict, and
the remaining Windows/.NET, Python, FIFO and encoded siblings.

**Preceding batch:** the
[Go/JVM stream and scope follow-up](STDIO-STREAM-OBSERVATIONS.md) moves three
neutral observations out of reverse shells and merges four overlapping Go
stdio definitions into one canonical atom. Nine effective mappings verify;
destination leaves hold 70 and 31 rules. The platform-count heuristic is now
a non-blocking review across all tiers, without directory exemptions or reduced
coverage. Its boundary regression passes and the release build succeeds.
All **1,633/1,633** fixture checks pass, including two new neutral-stream
controls. Strict validation again fails **only on 176 oversized directories**.
The remaining `stdio` and `encoded` rules still need semantic reconciliation.

**Preceding batch:** the
[documentation leaf repair](DOCUMENTATION-LEAVES.md) removes the remaining
mixed node and consolidates a duplicate advisory statement. All 1,631 fixture
checks pass. Strict validation retains 176 oversized directories and flags six
preserved platform scopes; the platform-policy conflict remains unresolved.

**Preceding completed batch:** the
[parser/DOS consolidation](PARSER-DOS-CONSOLIDATION.md) resolves the final two
original duplicate pairs. The validator reports no shared-matcher reviews;
all 1,627 fixture checks pass in soft mode. Parser guards now describe real
member structure, and DOS query evidence is neutral. The new value-field
constraint check passes 17 pattern-validation tests. Strict validation still
fails on 176 oversized directories; `stdio`/`encoded` reconciliation is next.

**Preceding member-name batch:** the
[member-name consolidation](MEMBER-NAME-CONSOLIDATION.md) resolves three more
duplicate pairs and moves eight adjacent filename observations out of the
retired `files/credentials` leaf. Twelve of the 14 original pairs are resolved;
the parser-error and DOS-call pairs remain. Platform-equivalence diagnostics
now distinguish Unix coverage from Linux/macOS; all 144 duplicate-related
tests pass. The name leaf has 19 rules and remains leaf-only.
All 1,623 fixtures pass in soft mode. Strict validation still reports two
shared-matcher pairs and 176 oversized directories.

**Preceding canonical-observation batch:** the
[canonical-observation consolidation](DUPLICATE-CONSOLIDATION.md) merges nine
of the 14 shared-matcher pairs. Dependency, runtime-variable, path and metric
observations now have one canonical home; contextual composites retain their
additional requirements. All **1,623 fixtures pass** in soft mode. Five pairs
remain under review, and 176 directories remain over the cap. All destination
leaves remain at or below 85, with no mixed nodes or exemptions.

**Preceding descriptor batch:** the
[descriptor mechanism migration](DESCRIPTOR-MECHANISMS.md) removes `dup` and
`syscall`: 27 more rules moved, two retired. Neutral descriptor observations
have operation-specific homes; outbound and accepted socket shells have
separate objective evidence. All **1,619 fixtures pass** in soft mode, including
five new controls/positives; copied controls also pass outside the benign
fixture path. All destination leaves stay within 85. Strict validation still
reports 176 oversized directories and 14 shared-matcher review pairs.
`stdio` and `encoded` remain to be reconciled before the reverse-shell audit
is complete. The policy remains strictly leaf-only.

**Previous completed batch:** see the
[socket-shell pilot report](SOCKET-SHELL-PILOT.md). The remaining 43 rules in
`socket-exec` were resolved and that directory was removed. Including necessary
destination cleanup and Perl descriptor observations, 60 rules moved and 11
unsupported verdicts were retired. The duplicate-validator changes pass 142
tests and surface 14 previously missed shared-matcher pairs. Soft validation
passes **1,614/1,614 fixtures**; strict validation still reports **176** oversized
directories, the shared-matcher findings, and unrelated authoring issues.
This batch completes `socket-exec` retirement, not the entire reverse-shell
family audit; subsequent descriptor work is recorded above. All directories remain
strictly leaf-only.

The following progress notes preserve earlier checkpoints; their counts are
historical and must not override the completed-batch report above.

The current worktree is based on traits revision `31568d2bbf`; the table above
is the preserved initial cap snapshot and has not been silently rebased. The
latest `cleave version` reports **79,242 atomic traits and 39,502 composites**;
strict validation reports **177** cap violators. A fresh behavior-tier path
inventory has 253 YAML files at depth 2, 8,452 at depth 3 and 5,560 at depth 4
(levels below the tier, excluding filenames). Depth is not a policy violation.
The validator currently reports **88** sparse sibling cohorts under its
35-rule advisory threshold; this is a review signal, not a directive to
flatten. `validate --soft` preserves all **1,610/1,610** fixtures.
These current measurements are distinct from the preserved initial cap audit
table above.

### Depth and breadth are semantic choices, not physical limits

Collimator's `_finding_paths` currently emits the tier and first two directory
prefixes for direct path-presence/max-criticality features; Scan uses the same
vocabulary. A third taxonomy level below the tier is therefore not guaranteed
its own direct feature. Full paths may appear in higher-order features when
trained vocabulary supports them. The previous physical limit of three
subdirectories was not aligned with this implementation and did not measure
misorganization. A future feature-limit change can make more levels directly
visible without changing semantic taxonomy.

Audit each path by what its hidden fourth segment means:

- **Prefer a broader sibling placement** when it stays equally exact and
  disambiguates the behavior in a visible level. For example,
  `objectives/anti-static/obfuscation/string/encoding/` and its sibling
  `.../string/fragmentation/` both currently feature as
  `objectives/anti-static/obfuscation` as direct path prefixes. Candidate
  sibling subjects such as `anti-static/obfuscation/string-encoding` and
  `.../string-fragmentation` should be used only if each has a clear, unique
  placement contract and doesn't merge neighboring behavior.
- **Promote a useful protocol distinction** only when it changes the behavior
  being learned. For example,
  `micro-behaviors/communications/email/access/imap/` shares direct path
  features with MAPI and ManageSieve. Decide whether protocol-specific behavior
  merits a separate visible subject, or whether the operation is the desired
  shared signal; do not infer bad organization from depth alone.
- **Collapse redundant or implementation-only levels** when the segment adds
  no behavior meaning. Move the rule to its semantic parent and keep language,
  platform, or sample-specific distinctions in filenames and scopes.

Do not add an artificial intermediate node just to satisfy a fixed path shape.
The goal is to expose distinctions the model should learn while retaining a
single, semantically defensible placement for each behavior. Prefer breadth
over depth only when that does not reduce taxonomy precision.

Behavior-preserving migration tranches now cover path resources, bind shells,
string APIs and technique-specific library fingerprints:

- **Path-resource placement:** 12 rules formerly under
  `micro-behaviors/fs/path/library` now live in cache, system recovery, font,
  application-data, system-log and metadata-store subjects. Eight composite
  reference occurrences follow those IDs. The six remaining rules in
  `fs/path/library` point to shared-library files. Their effective matchers,
  scopes, criticalities and confidence are preserved.
- **Bind-shell placement:** all eight rules in
  `objectives/command-and-control/backdoor/dispatch/bind-shell` moved under the
  canonical `backdoor/bind-shell` subject. Two Ruby bind-shell composites also
  moved out of `reverse-shell/socket-exec`; three supporting observations moved
  to neutral socket-listener and process-stdio capabilities. Their matchers
  and the two composites' effective predicates are unchanged after reference
  remapping. `socket-exec` was still oversized at 146 rules before the current
  reverse-shell audit tranche.
  This is a pilot rather than completion of the nine-leaf reverse-shell cohort.
- **String and path-operation placement:** the 21 string API rules formerly
  under `micro-behaviors/data/string/library` now live under operation leaves.
  Three reference-only Java code-generation framework fingerprints moved to
  `micro-behaviors/metaprogramming/generation`, and all reflection exclusions
  and the cglib fixture expectation follow the new IDs. The .NET `Combine`
  and `GetDirectoryName` API-name tokens moved to pathname join and parse
  leaves. Matcher bodies and effective scopes remain unchanged; the codegen
  names state only that a library is referenced, not that code generation ran.

The `micro-behaviors/metaprogramming/{ast,generation,reflection}` contract is
now language- and filetype-neutral. AST operations and reflection are code
techniques, not a `data/source` or language subcategory. Existing
`data/source/` contents still need a rule-by-rule semantic migration; the path
is closed to new rules until that audit is complete.

The Go parser/source-generator example is now a concrete migration: parser
calls and their composite live in `metaprogramming/ast`; formatting generated
source and the composite that additionally requires a file write live in
`metaprogramming/generation`. Its matcher bodies and effective composite
predicate are unchanged. The boundary guide distinguishes a program's AST
behavior from an analyzer's internal AST and from ordinary data parsing.

The existing `micro-behaviors/process/interpreter/reflection/` collection also
needs a rule-by-rule placement audit: actual reflective discovery or invocation
maps to `metaprogramming/reflection`, while indirect dispatch, evaluation, and
loading must go to their own technique leaves. Keep language names in rule
scopes and filenames, not as taxonomy branches. Do not bulk-move this
collection based on its current `reflection` path name.

The current audit tranche moves Go AST parsing into `metaprogramming/ast`,
separates source generation into `metaprogramming/generation`, moves Node
socket/child-stream shell bridges into `reverse-shell/stream-bridge`, and moves
the native ELF socket/`dup2`/shell composites into `reverse-shell/fd-redirect`.
Ruby's receive → command execution → socket response loop now lives under
`remote-command/dispatch`, and its VM-aware consumer follows the relocated ID.
The Node library/extension consumers now require one of the stronger bridged
shell composites instead of socket-plus-exec co-occurrence. Zig's host/port
literal and shell-launch facts now live in neutral socket-endpoint and process
capability paths, and its reverse-shell composite requires the `dup2` link.
The Lua fixture is classified as remote-command dispatch and now requires
connect, receive, shell execution and response send. The weak WSH object
co-occurrence verdict was removed; its TCPClient and stream-object observations
now live as neutral capabilities. After these changes, the retired
`reverse-shell/socket-exec` directory contains 51 rules
and is below the cap, but is not empty. At that checkpoint, strict validation
reported 177 unrelated oversized directories and soft validation preserved all
1,610 fixtures (243 hostile, 338 benign, 175 does-nothing, 45 drop-exec, 572
supply-chain, 66 impact-wipe, 82 obfuscation, 24 reverse-shell, 65 simple-stealer).

- **Direct-socket HTTP correction:** the Bash `/dev/tcp` + HTTP-token rule was
  hostile despite proving no shell I/O over the socket. Its shell-specific
  observations and neutral notable composite now live in
  `micro-behaviors/communications/http/direct-socket`; the existing raw HTTP
  capability was moved there and its three consumers remapped. The taxonomy
  distinguishes protocol-first raw HTTP, HTTP client APIs, and socket-only
  behavior. A benign health-check fixture guards against restoring the false
  reverse-shell claim.

- **Reverse-shell precision and method placement:** HTTP polling agents now
  live under `remote-command/http-poll`, and netcat remains the specific
  `reverse-shell/netcat` technique (14 rules; invocation children are not
  justified at this size). Java, Kotlin and Scala stream-bridge composites
  moved to `reverse-shell/stream-bridge`; generic Java transfer and Kotlin
  shell-process observations live under neutral process capabilities. Socket
  plus shell co-occurrence without stream evidence no longer qualifies as a
  reverse shell in Java, Kotlin, Scala or Swift. Swift's separate stdio-wiring
  composite remains. Reverse-shell fixtures now require one confirmed hostile
  finding each instead of a second, weaker co-occurrence result. The former
  140-rule `socket-exec` violator is now below the cap at 51 rules, as reported by strict
  validation; all 24 reverse-shell fixtures pass. The remaining JavaScript
  HTTP GET-command/POST-result composite moved from `socket-exec` into
  `remote-command/http-poll`; its legs prove polling and task dispatch, not a
  persistent socket-coupled shell. A Node hosted-reverse-shell curl-pipe
  composite was removed after confirming it was a strict branch duplicate of
  the existing `dropper/delivery/pipe` composite. The canonical dropper rule
  already requires the same three facts, so detection remains and now retains
  both JavaScript and shell ATT&CK facets. The retired `socket-exec` catch-all
  now has 51 rules and is no longer a cap violator, but its remaining rules still
  need routing to the documented mechanisms before the directory can be removed.
  The native ELF socket+`dup2`+shell rules now live in
  `reverse-shell/fd-redirect`, where their required evidence identifies the
  inherited-descriptor mechanism.
The full reverse-shell fixture group still passes.

- **PHP socket-shell and staged-eval placement:** PHP socket setup, shell
  creation and descriptor-spec stdin mapping now live as neutral socket,
  process and fd capabilities. One nearby composite under reverse-shell
  `fd-redirect` requires all three; the weaker socket-plus-shell co-occurrence
  rule was removed, and the existing webshell composite now references the
  stronger reverse-shell result. Network-order length unpacking, buffer
  reassembly and `eval($b)` moved to framing, buffer-transfer and direct-eval
  capabilities. Their socket-delivered stage composite moved to
  `remote-command/dispatch`; a new hostile fixture confirms the whole chain.
  Both PHP fixtures pass against their relocated composites. JSP's socket
  read-to-exec loop moved to `remote-command/dispatch`. Swift's former
  endpoint-plus-shell/stdio co-occurrence composite was tightened to require
  Network.framework connection, start, send and receive facts plus shell-pipe
  wiring, then moved to `reverse-shell/stream-bridge`. Its endpoint literals,
  connect state, send and receive observations now live in neutral socket
  capability subjects. Python's shell invocation facts and AppleScript's
  interactive Bash fact also moved to neutral process capabilities; AppleScript
  reverse-shell composites still match under `dev-tcp`. Objective-C shell
  launch and interactive-argument observations moved to neutral process
  capabilities. Its socket/dup2 reverse-shell composite now requires an actual
  connect; socketless shell/dup2 co-occurrence no longer receives a hostile
  reverse-shell verdict. The systemd unit's dev-tcp shell composite moved to
  the `dev-tcp` technique and reuses canonical persistence/restart facts; a
  hostile fixture confirms it.

- **Certificate metadata ownership:** script signature-block observations
  moved into the existing `signed/certificate/signature` subject, and direct
  signer-subject observations moved into the new `signed/certificate/subject`
  subject. Authenticode integrity and verification facts moved out of the mixed
  identity file into `signature/pe-chain`; 91 YAML reference owners were
  remapped without changing predicates. Moving the three script markers brought
  `certificate/identity` from 88 to the inclusive 85 cap and removed one
  violator; subsequent subject moves made the residual identity set smaller.
  The mixed PE certificate matcher was then separated by the field or property
  it reads: `subject`, `issuer/name`, `issuer/chain`, verified issuer sets
  (`issuer/microsoft`, `issuer/attestation`), certificate security properties,
  and signature validity/integrity. A Microsoft CA name string remains only an
  issuer-name observation; platform trust requires a verified-chain thumbprint.
  The forged-name and genuine-chain fixtures both pass after this split.

Current strict validation remains **red only on the known 177 oversized
directories**. Soft validation reports all **1,610 current fixtures passing**
(245 hostile, 338 benign, 175 does-nothing, 45 drop-exec, 572 supply-chain, 66
impact-wipe, 82 obfuscation, 22 reverse-shell, 65 simple-stealer); it also checks
parsing and rule quality while allowing that cap policy failure.
The destination leaves created or extended by these migrations remain below
85. The minimum cap excess is now **4,848**, down from 4,920 in the earlier
pre-migration inventory; there are no new violating directories. The broader
cohort ledger below remains open.

## Evidence and audit coverage

- [oversized.csv](oversized.csv): every violator, with atomic/composite counts,
  excess, source-file count, and physical depth.
- [disposition.csv](disposition.csv): every violator assigned to a migration
  cohort, with the proposed organizing question, action, and source examples.
- [siblings.csv](siblings.csv): all rule-bearing leaves under each violating
  directory's parent, including siblings' descendants. Overlapping audit scopes
  are counted once. Both YAML rule kinds were parsed, not counted by regex.
- [matcher-overlaps.csv](matcher-overlaps.csv): identical `if` bodies and their
  effective surrounding settings. These are **candidates**, not equivalent
  detections: file types, platform, size, confidence, criticality and exclusions
  can differ. For example, the same `exec` symbol means different things in
  Python and PHP. Do not merge it across those scopes merely because text agrees.
- [reference-impact.csv](reference-impact.csv): distinct YAML reference owners
  per violating directory, including references to its ancestor directories.
  Counts overlap between rows and are not additive. Tests, external consumers,
  and engine-emitted IDs need the additional migration checks below.
- [structure.csv](structure.csv): whole-tree depth, single-child, mixed-leaf,
  and broad-parent inventory. Structural review flags are not proof of semantic
  errors or a new validator policy.
- [summary.json](summary.json): machine-readable totals and scope roots.
- [IMPLEMENTATION-LAYERS.md](IMPLEMENTATION-LAYERS.md): technique-first placement
  of embedded library evidence, all 15 literal `library` nodes, related
  implementation terminology, and the artifact-identity boundary.

The inventory covers every rule. The semantic audit inspected a spread of rule
IDs/descriptions and source files in **each of the 180 violators**, the sibling
structures, and actual matcher/composite bodies for the conflicts documented
below. It does **not** claim line-by-line adjudication of all 61,219 rules in
those subtrees, or all 8,637 directories. The migration must produce a complete
old-ID → new-ID disposition before moving each cohort. Proposed child sizes are
not yet measured and must not be represented as guaranteed to fit.

Reproduce the structural reports with PyYAML available:

```sh
python3 scripts/audit-taxonomy.py --out /tmp/taxonomy-audit
make validate
```

`disposition.csv` and this plan are reviewed recommendations; the inventory
script does not manufacture semantic classifications.

## Duplicate-validator findings and proposed improvements

**Implemented checkpoint:** exact and scope-only atomic passes now share
matcher/default normalization, normalize set ordering, and retain architecture
and downgrade constraints. The logic pass reports file-scope differences and
confidence differences below 0.1, checks architecture overlap, and retains
different quantitative observations. The reproduced DOS pair now appears in
the 14-pair review output. Diagnostics request a scope/verdict review rather
than asserting that every shared matcher can safely be merged. Seven new
regressions cover these boundaries; all 142 duplicate-related tests pass.
Further candidates below remain proposals unless explicitly covered here.

Identical matcher bodies should enter a common duplicate review, but a merge
must preserve the **effective predicate**: inherited defaults, file type,
platform, architecture, bounds, exclusions and conditional verdict changes.
The 128 groups in `matcher-overlaps.csv` are body matches, not 128 confirmed
validator defects. Confidence alone is not a different observation.

### Confirmed missed merge: overlapping scope plus a small confidence difference

Two existing rules in `objectives/impact/infect/binary/dos` have exactly
`if: {type: hex, pattern: "B4 52 E8"}`:

| Rule | Effective file types | Confidence |
|---|---|---:|
| [`dos-list-of-lists-call`](../../objectives/impact/infect/binary/dos/com-bytes.yaml) | `dos_com`, `static-lib` | 0.88 |
| [`dos-get-list-of-lists-near`](../../objectives/impact/infect/binary/dos/direntry.yaml) | `dos_com`, `static-lib`, `data` | 0.80 |

Both have `crit: notable`, `platforms: [windows, unix]`, and `size_max: 65536`,
with no differing exclusions or other matching constraints. Their scopes
overlap, and they assert the same DOS observation. Merge into one canonical
observation after reviewing the broader `data` scope and choosing one supported
confidence; rewrite both sets of consumers.

The current engine's `src/capabilities/validation/duplicates.rs` lets this pair
fall between three checks:

- `find_duplicate_atomic_traits` includes `for` in its fingerprint, so the
  different lists separate the pair.
- `find_for_only_duplicates` includes confidence to two decimal places, so the
  different confidences separate the pair again.
- `find_atomic_logic_duplicates` checks that the file types overlap, but does
  not count a differing `for` list as a metadata difference. It only treats a
  confidence difference of at least 0.1 as different. This pair is skipped on
  the assumption that the exact checks handled it.

**Reproduced against the rebuilt binary:** isolating these two rules with their
effective defaults produces no duplicate diagnostic with all validators enabled
(`validate --exclude ''`). Changing only 0.80 to 0.88 produces the existing
“trait groups differ only in scope (should be merged)” error. The tiny isolated
bundles also report unrelated whole-tree allowlist/default-style errors; this
experiment compares the duplicate diagnostics, not overall exit success.

**Priority 1:** group by normalized matcher independently of confidence, then
compare effective predicates and report the actual differences. Do not make
one check assume another handled a pair without checking its equivalence
criteria. Add this exact pair as a regression, plus overlapping and disjoint
file/platform scopes with equal and slightly different confidence.

### Additional patterns to cover, without erasing precision

- **Report mergeable disjoint scopes as an advisory.** The former
  `execution/script::msi-scheduled-task-action` and neutral
  `os/autorun/scheduled::new-scheduledtaskaction` had the same
  `New-ScheduledTaskAction` text matcher. Their effective `for:` lists were
  disjoint (`oledoc` versus `powershell`), so overlap-only duplicate checks
  need not reject them, but the atom had no MSI-specific predicate. The
  neutral rule now owns both file types and the MSI composite references it.
  A same-body, same-subject advisory should propose this sort of scope union
  while spelling out confidence and verdict differences for review.
- **Share normalization across duplicate passes.** Currently only the logic
  pass normalizes `count_min: 1` and an explicit `exists: true` spelling. Its
  “exact check handled this” shortcut deserves regressions for those variants
  with otherwise identical settings. Canonicalize set-valued scopes after
  defaults/group expansion; do not sort ordered ranges or other ordered data.
  These are source-review candidates, not additional reproduced failures.
- **Account for architecture and conditional verdicts.** The exact and
  scope-only fingerprints omit `arch` and `downgrade`; the logic pass compares
  downgrades but does not test architecture overlap. Add disjoint-architecture
  and differing-downgrade regressions before recommending automatic merges.
  The diagnostic must distinguish shared matching work from equivalent output.
- **Explain why identical bodies were retained.** In
  [`fetch-exec/shell.yaml`](../../objectives/command-and-control/dropper/delivery/fetch-exec/shell.yaml),
  `spl-payload-names--rx-7` and `arch-args-arm--rx-18` both match the word
  `splarm`, but require six and two occurrences respectively. Several adjacent
  payload-name pairs repeat this pattern. These are different quantitative
  observations, and the logic pass deliberately skips unequal bounds. Report
  such groups as shared-matcher review candidates with the threshold difference,
  not mandatory merges. Factor matching work only if the reference mechanism
  preserves each count constraint. The stale comments in that function which
  recommend merging overlapping bands should also be reconciled with its code.
- **Give scope-only and logic-duplicate findings dedicated diagnostic IDs.**
  The reproduced scope-only merge appears under generic `qual/validation`.
  Stable IDs and explicit skip reasons would make audit reports and regression
  assertions distinguish a missed check from an intentional exception.
- **Report composite overlap with effective-predicate differences.** The Node
  reverse-shell collection had two rules sharing socket-connect, shell-bridge
  and `/bin/sh` requirements; one required `exec` without proximity, while the
  other allowed `exec` or `spawn` within 4096 bytes. They overlapped but neither
  predicate implied the other. The broad non-proximity branch was retired after
  review because it had no consumer and could join unrelated functions; this
  was an accuracy judgment, not a proven duplicate. A validator could surface
  common required legs and the exact differences after expanding directory
  references and normalizing `all`/`any`/`needs`, proximity, file/platform/
  architecture scope and verdict modifiers. Keep it a review warning:
  overlapping rules can be intentional, and shared legs are not permission to
  merge or remove either rule.

Implement these as a separate validator change with focused regressions. The
current implementation changes only the directory cap/depth policy; it does
not silently alter duplicate semantics during the taxonomy inventory.

## Taxonomic contract

The normative [behavioral directory contracts](../../TAXONOMY.md#behavioral-directory-contracts)
now document domain ownership, admission predicates and ordered disambiguation.
They apply before the legacy illustrative tree or existing directory placement.
The [implementation contract](../../TAXONOMY.md#implementations-and-library-fingerprints)
also applies to every software-identity recommendation below: embedded library
evidence goes to its supported technique or capability group; `well-known` is
for the independently identified artifact, not every application containing it.

Linnaean containment is a useful discipline: every child must be a narrower
kind of its parent. Security observations also have independent facets, so
containment alone cannot ensure unique placement. **Ordered evidence tests**
must resolve intersections. The directory owns one claim; cross-references
express other claims without duplicating their matchers.

For each parent, document: its admission predicate, the single question its
children answer, positive and negative examples for each child, and the first
matching placement test. The full path must read as a narrowing statement.
Classification follows required evidence, not the rule's name, author intent,
language, sample label, optional corroboration, or whichever directory has room.

Apply these tests in order:

1. **What does this matcher actually establish?** A neutral API/path/field goes
   to its capability or metadata subject. Embedded implementation evidence goes
   to its supported capability; independently identified artifacts go to their
   identities. Neither acquires attack intent from a consuming composite.
2. **What result must a composite prove?** Sensitive source plus transmission
   belongs in exfiltration; source access without transmission belongs with
   collection/credential access. An install hook or archive is context, not a
   second copy of that result. Persistence requires a durable activation change.
3. **Which required mechanism distinguishes the result?** Use the ordered
   contracts below; place a mechanism-neutral rule at a genuinely defined
   broader claim only when it cannot truthfully assert any child.
4. **Does it require several independent outcomes?** Factor canonical outcome
   composites. Keep a higher composite only when the conjunction establishes a
   distinct documented claim. Do not create `combined/`, `behavioral/`, or
   `multi/` overflow directories whose only definition is “several things.”
5. **Is it a suppressor?** `crit: exception` remains the composite-only
   suppression role from RULES.md. Its placement is the documented exception
   to evidence-tier placement; it still counts toward the 85-rule budget.

Do not lower criticality to disguise misplacement. Conversely, moving a falsely
hostile neutral observation does require correcting the overstated finding:
preserving a wrong verdict is not a migration invariant. Record such semantic
changes separately from moves and test them explicitly.

### Breadth, depth, and the ML distinction

The current Collimator and Scan implementation extracts direct path features
from the tier plus the first two path segments below it. No downstream
feature-limit change is part of this taxonomy audit.

The current behavior-tier inventory has 253 rule files at depth 2, 8,452 at
depth 3, and 5,560 at depth 4. Only the first two levels below the tier are
currently guaranteed direct path-presence/max-criticality features. Prefer
breadth over depth when the sibling names remain equally precise, but don't
flatten distinctions that need separate canonical homes. Any feature-depth
change should be a separate extractor/model-schema migration with retraining
and evaluation.

Whole-tree structural findings:

- **Single-child parents.** Keep their count as an inventory statistic, not a
  validation warning. The leaf-only rule permits an internal parent with one
  child and no YAML of its own; it forbids mixing YAML and subdirectories.
  A meaningful refinement does not become redundant because it is the only
  subtype currently represented. Child count, depth, and identical current
  descendant sets cannot establish that the parent and child mean the same thing.
  Use existing name-restatement and duplicate-matcher checks where applicable.
  Broader semantic redundancy needs evidence that the documented admission
  predicates are equivalent, not merely that one name looks generic. The
  sparse-sibling advisory reports a parent only when at least two child
  branches together contain fewer than 35 rules; it does not warn on a
  single-child parent by itself.
  Candidates for that semantic review include `trigger/activation`, `self-modify/runtime`,
  `fs/quota/control`, `mem/advise/hints`, and `hardware/block/device`.
  After confirming redundancy, remove the unnecessary level while preserving
  the leaf-only rule, references, and capacity limit. If moving YAML to
  the parent, remove the obsolete child directory; do not leave a mixed node.
  Do not flatten `trigger/activation`'s 97 rules into another oversized leaf;
  identify actual mechanisms instead.
- **Retain real refinements** such as `crypto/symmetric/gost/cbc`,
  `os/compat/wow64`, and `persistence/system/wmi/subscription`: CBC, WOW64, and
  permanent subscriptions answer a specific question about their parents.
  Do not add a taxonomy level merely to satisfy a minimum path-depth rule.
- **Promote/merge duplicate subjects:** `process/fork/clone` with
  `process/create/fork`; `process/script/wsh` by actual execution mechanism;
  `discovery/host/browser/identity` with browser discovery subjects;
  `collection/app-data/notes/app` loses the final `app` word. Account for the
  existing siblings rather than blindly renaming a path.
- **Remove wasted identity layers:** `tool/development/cli/dev-cli/<tool>`
  repeats CLI; use `tool/development/cli/<tool>`. Under
  `tool/development/agent/ai-cli/<tool>`, keep either a defined agent function
  or CLI role, not both grouping words by habit. `.../elex/dropper/elex` repeats
  the family; classify identity facets under the one canonical Elex family.
- **Breadth pressure exists before 150:** `well-known/lib/development` has
  149 immediate children, `well-known/app/system` 139, `well-known/lib/web`
  134, `well-known/tool/development/vscode-extension` 131,
  `well-known/lib/format` 129, and `well-known/lib/network` 127. Subdivide the
  broad catalogs by primary function, e.g. development → compiler, testing,
  linting, build; consolidate into existing function homes first. For identities
  spanning functions, use their documented primary purpose, never alphabetical
  chunks. A product directory still has one canonical home.
- `metadata/package/documentation` is the one inventory entry with both rules
  and descendants. Investigate its direct rules and migrate to their document
  subjects. This inventory observation was not an additional hard error in
  the engine run.

## Cohort 1: neutral subjects and software identities

This work goes first because objective migrations depend on canonical atoms.

| Current violator(s) | Organizing question and disposition |
|---|---|
| `metadata/binary/{framework,vendor}` | Is this a format part, vendor claim, signer, or product fingerprint? Keep format anatomy under `binary`; move signer evidence to `signed`, OS vendor claims to `vendor`, and product/framework identity to existing `well-known` homes. Audit `binary/{bundle,license,signing,toolchain}` too. |
| `metadata/lang/compiled` | What language/toolchain does the artifact prove? Move source-language syntax to `lang/source`, compiler provenance to `lang/compiler`, and independent runtime/library artifact identity to `well-known/lib`. Embedded implementation markers go with their supported capabilities: `rust-zstd-library-marker` is not a language. Split residual language evidence by compilation model only if necessary. |
| `metadata/package/files/system-package` | Which package property is read: container format, member layout, declared fields, or signature? Route into format/member/field/signature subjects, with APK/RPM/container implementation in filenames. Compare all ecosystem siblings, including BSD, MSI and wheel/sdist. |
| `metadata/package/testing/presence/fixture` | Does the matcher prove a fixture's role/location, a testing framework identity, or a generic token? Keep fixture location/content-shape facts; merge path overlap with `presence/path`, move framework identities and certificate facts to their subjects, and keep suppressors explicit. |
| `metadata/permission/host` | What host authority is declared? Split by grant breadth (`all-origins`, `domain-pattern`, `explicit-origin`), then resource category where needed. Distinguish content-script scope in the rule/file. Move extension name/description claims out; provider identity does not establish a grant. |
| `metadata/signed/certificate/identity` | Which certificate role/property is asserted: subject, issuer, timestamp authority, or revocation endpoint? Split those roles and compare with existing `signed/leaf`, `signed/unknown`, and `certificate/signature`; a timestamp issuer must not establish the leaf signer. |
| `micro-behaviors/dylib/library/family` | Loaded-library reference, named-software identity, or API operation? Route each accordingly; a `XCreateWindow` reference belongs with window creation and GDB identity with tools. Retire `family` as a mixed library bucket. |
| Six oversized `well-known` leaves | Keep family/product-specific evidence only. Remove generic `memcpy`, archive-size and API flags, preserving scope through references. For residual overflow, use genuine family components or identity facets, not languages. |

Concrete checks: `metadata/binary/vendor::glarysoft-ltd` reads a certificate
subject; `...::hwmonitor-product-marker-rsrc` reads `HWMonitor`.
`well-known/malware/stealer/amos::memcpy-symbol-macho` matches exactly `memcpy`
and already has a neutral matcher counterpart. It is not AMOS identity.

`well-known/tool/detection/security-scanner` mixes product identities with
generic defensive pattern catalogs. Merge identifiable tools into their named
sibling homes; generic catalogs belong with the documented content/build
subject or a suppressor, not in a purported specific-software identity.
`security-scanner-identity` is a competing sibling to audit together.
`powershell-empire` should retain Empire-specific module/protocol names;
`daemontools-cc` should separate the actual implant components from generic
Toolhelp/API atoms; `elex/worm` needs reconciliation with the other Elex leaves;
`tenorshare` must distinguish product identity from evidence of a trojanized
copy. Product identity alone must not be treated as malware identity.

## Cohort 2: process creation and reverse shells

### Process creation

Apply the existing TAXONOMY process-creation decision table to the *whole*
`process/create` family. The overfull leaves are `agent`, `direct`, `spawn`,
`shell/bridge`, and `shell/spawn`. Siblings `exec`, `execv`, `spawnv`, `system`,
`api-system`, `popen`, `subprocess`, `launch`, `local-exec`, and `shell/lang`
show the same competing axes.

Required shell parsing → `create/shell`; interpreter source argument →
`create/eval`; a child-process object → `create/subprocess`; desktop handler →
`create/shellexec`; native argument-vector launch → `create/exec`. API spelling
and language go in filenames. A bare shell pathname belongs with interpreter
identity, a pipe with IPC/process I/O, and imported `child_process` does not
prove a shell. Agent permission/configuration text does not prove creation of a
process; move it to its configuration/authority subject.

Retire `direct` and `spawn` as competing synonyms, and retire `shell/bridge`
as a JavaScript bucket. Under `shell`, use required command form: interactive
session, command text, script file, or pipeline; encoded text is represented by
canonical decoding atoms plus the executing composite, not another generic
shell directory. More specific forms win over unspecified forms. If only a
shell-capable API is observed, the description and directory must say that;
do not pretend its optional shell argument was present.

### Reverse-shell contract

Strict validation reports 128 rules in the over-cap `socket-exec` subtree.
Netcat currently has 14 rules, so direct-exec and FIFO/pipeline forms remain
together. Netcat has its own technique directory because its utility invocation
is a sufficiently specific shell-relay method; split it by invocation only if
a meaningful subtechnique distinction or directory size requires it. Three
HTTP-only `/dev/tcp` rules moved to neutral HTTP mechanics.

First establish direction and behavior. A listening server is a **bind shell**;
an HTTP request parameter passed to a command is a **webshell/remote-command**
surface. Receiving independent commands is **remote-command dispatch** unless
the rule requires a persistent shell session. Reverse-shell admission requires
an outbound connection and evidence connecting it to the shell's I/O. Socket
plus shell existence alone is not that relationship.

For admitted reverse shells, use the first required mechanism in this order:

| Evidence required | Canonical destination | Exclusion / counterexample |
|---|---|---|
| Shell pseudo-device creates the connection and redirects shell I/O | `reverse-shell/dev-tcp` | `/dev/tcp` used to send HTTP alone is neutral networking. |
| Netcat directly owns the shell relay | `reverse-shell/netcat` | A netcat banner/import alone is not a shell. |
| Pseudoterminal explicitly carries the session | `reverse-shell/pty` | Merely opening a PTY does not meet admission. |
| Socket is installed as inherited standard descriptors | `reverse-shell/fd-redirect` (merge `dup` and applicable `stdio`) | An arbitrary file `dup2` is neutral descriptor manipulation. |
| Explicit read/write/copy loop joins socket and persistent child streams | `reverse-shell/stream-bridge` | A per-command request/result loop goes to remote-command dispatch. |

`encoded` and `syscall` are evidence representations, not competing shell
mechanisms: route their rules using the same table. The three HTTP polling
command agents moved from `reverse-shell/http-poll` to
`remote-command/http-poll`; this directory requires repeated fetch/dispatch
and does not represent a persistent shell session. Retire `socket-exec` after
redistributing, not by adding another
generic child. If a rule proves a reverse shell but its bridge mechanism cannot
be inferred, strengthen it or document that missing mechanism before deciding
a new child; do not manufacture a catch-all to clear the cap.

Verified examples in `socket-exec`:

- The Ruby listener plus shell composites now live at canonical
  `objectives/command-and-control/backdoor/bind-shell`; their server-loop,
  client-accept and descriptor-redirection atoms live with socket/process
  capabilities. The old `backdoor/dispatch/bind-shell` sibling was merged into
  this canonical bind-shell directory.
- `ruby-http-query-command-shell` is not a reverse shell. Determine from the
  surrounding server/client evidence whether it is a webshell endpoint or a
  remote-command client before moving it.
- `objc-connect-call`, `csharp-tcpclient-host-port`, and
  `swift-process-launchpath-bin-sh` are neutral socket/process capabilities;
  `open3-popen` still needs a matcher-level audit before final placement because
  one variant is a string-literal API token rather than a proven call.
- The Objective-C connect call, C# `TcpClient(host, port)`, Swift shell launch
  path, and Node RFC1918 address observations have been moved to their neutral
  socket, process-creation, and IP-literal capabilities with consumer
  references remapped. Their matcher predicates, scopes, confidence, and
  criticality are preserved. The reverse-shell leaf is smaller by six rules;
  remaining objective composites still need admission review.
- `objc-systemd-wantedby-default` only matches `WantedBy=default.target`;
  it is a service configuration fact. `any-shell-exec` is a neutral aggregate.
- `dev-tcp::shell-dev-tcp-http` required only TCP redirection plus an HTTP
  GET/Host token. It now lives as a neutral notable direct-socket HTTP capability;
  the benign `/dev/tcp` health-check fixture forbids any reverse-shell finding.
- The shell and PowerShell HTTP poll agents moved to
  `objectives/command-and-control/remote-command/http-poll`. Their matched
  fetch/evaluate/post-or-loop predicates and verdicts are unchanged; their
  descriptions now identify task polling rather than a reverse shell.

## Cohort 3: payload delivery, hiding, and loading

Audit **all** `command-and-control/dropper` siblings with
`anti-static/obfuscation/payload`, `evasion/fileless`, and
`evasion/process/injection`. The largest leaf has 324 rules, so moving whole
files or renaming one node is inadequate.

`delivery/execute-download` (324), `delivery/fetch-exec` (133),
`execution/exec-download` (now 96 after evidence routing), `execution/execute-download` (15),
`delivery/fetch-eval` (129), `execution/eval` (78), and `execution/fileless`
(now 99) demonstrate duplicate concepts across delivery and execution. The
current four-phase dropper tree puts full-chain composites under whichever
phase the author happened to emphasize.

**Proposed change to TAXONOMY:** put complete payload-activation chains directly
under `dropper/<activation-mechanism>`. The child question is “how does staged
payload become running code?” Apply required sink precedence:

1. execution in a different process → `process-inject`;
2. same-process native image mapping → `image-map`;
3. runtime module/assembly loading → `module-load`;
4. source evaluated in the current interpreter → `script-eval`;
5. source fed through stdin to a new interpreter → `interpreter-stdin`;
6. a staged file launched through a process/file handler → `file-exec`.

These are proposed paths, to be reconciled with the canonical evasion and
execution atoms/composites, not six new copies of them. Dropper admission
requires a demonstrated payload-staging/activation relationship. Evasion
composites which merely establish an injection technique stay in evasion;
the delivery-chain composite references that one technique. A carrier file
shape alone is metadata. Document a narrower child only when its necessary
evidence refines the activation mechanism; fifth-level room is available for
such a refinement.

`staging/{encrypted,embedded,memory,archive}` overlaps source, transform, and
storage axes. Retire full-chain rules from those branches into activation
homes. Put standalone decryption/decoding/archive mechanics into capabilities;
concealment *objectives* into anti-static; neutral section/entropy/layout facts
into metadata. A remote encrypted assembly therefore has one complete-chain
home (`module-load`), with cipher and download evidence referenced.

Likewise retire language/container buckets `execution/{batch,script,wsh}` and
`node-bootstrap`; classify their actual chains. `execution/installer` contains
SFX, MSI custom actions, signed overlays and scripts—installer identity is not
an execution mechanism. `builder` contains neutral compiler/build settings
alongside malware-generator templates; separate build facts from actual
payload construction.

Evidence: `staging/memory` includes a temporary AppleScript file path and
file-writing launchers; `payload/encrypted` includes plain large-data-section
measurements. The former `execution/script::msi-scheduled-task-action` searched
only for `New-ScheduledTaskAction`; it has been merged into a neutral scheduled
task observation. Neither an MSI nor that API proves a dropper.

The first `execution` cap pass is complete without an exception: 2,001 rules
across 59 leaves, with `exec-download` at 96 and `script` at 40. This is a
capacity checkpoint, not a completed semantic migration. MSHTA execution,
npm preinstall, MSI custom actions, VBS/Excel COM, Kotlin polyglot, Panos Ruby,
C# command text and JScript obfuscation have now been routed by their required
evidence. Next require a matched source-to-sink relation before a Ruby
HTTP-body/Open3 combination claims execution of the downloaded response.
Audit the remaining Python and JScript profiles and then reconcile the
overlapping `exec-download`/`execute-download` and
`script`/`dropper-script` siblings by the required activation sink.

Capacity planning is deliberately deferred to the rule-by-rule map. These
large families may need real submethods and composite consolidation even
after neutral atoms leave. Do not promise that these six leaves alone fit 85.

## Cohort 4: HTTP, protocols, and system capabilities

| Family | Required boundary and sibling reconciliation |
|---|---|
| HTTP `post`, `upload`, `request/client` | Method evidence stays in `post`; attachment/multipart/file-source mechanics in upload; method-unspecified client request in client. A GET belongs in existing GET handling, a header token in its header subject. Split upload by attachment mechanism, not SDK; raw body writes are not automatically uploads. |
| HTTP `oauth` | Separate authorization request, code exchange, token refresh, and token use; move fields/scopes to their field/authority subjects. Reconcile `auth`, `token-auth`, `device-code`, `authorization-header`, `idp`, `jwt`, and `login`. Token refresh must not also be classified merely as token exchange. |
| HTTP `services/{github,microsoft}` | Endpoint presence and an actual operation are different claims. File named-service endpoints under service/resource purpose and neutral operations under their behavior. Compare existing `sharepoint`, `dataverse`, `entra-directory`, `devops-azure`, GitHub URL and CLI siblings before creating anything. A CLI call is not HTTP evidence merely because its vendor has an API. |
| HTTP `url/query`, `user-agent` | Separate constructing/parsing query parameters from particular field meanings; separate setting/reading a User-Agent from comparing it and spoofing/rotation intent. Reconcile `http/query`, `request/params`, `url/telemetry`, `fingerprint`, and header siblings. Campaign labels are not generic query operations. |
| MCP | Protocol negotiation, tool registration/listing/call/result, and resource access are legitimate children. Config-file presence and product identity leave the protocol bucket; filesystem/shell APIs exposed as tools remain canonical capabilities referenced by the MCP composite. |
| TLS / proxy | Reconcile `socket/ssl`, `http/{ssl,tls}`, proxy `tunnel`, `relay`, `socks`, `reverse`, and C2 tunnels. Separate handshake, certificate validation, and encrypted I/O. TLS verification disabling needs its own factual validation-setting observation and an intent composite where appropriate. Move cloudflared/ngrok identities to their existing software homes. |
| Blockchain / SQL | `crypto/library/blockchain/client` mixes transaction semantics, payment services, identities and address decoding. Keep a neutral `communications/blockchain/client` composite for actual chain queries and transaction behavior, while relocating atoms to RPC, transaction, crypto and wallet/provider operation homes; imports, endpoint strings and offline key operations alone do not establish client use. SQL divides query/execute/schema/connection; Entra credential-table targeting leaves generic SQL, tool fingerprints leave capabilities. |
| Base64 decoding | Consolidate equivalent variants before a split. Compare `symbol-base64`, `native-base64`, `reflection-base64`, `request-base64`, `environment-base64`, `repeated-base64`, and `quartet-base64`. Input origin and matcher implementation are not alternate meanings of Base64 decoding. A required repeated decode is a refinement; a decoder reached by a symbol matcher is not. |
| Registry | One operation axis: open, read/query, write, create key, delete, enumerate, watch; key/hive references have distinct factual homes. Retire mixed `access`/`manipulate` buckets by routing to existing siblings first. A write API alone is not persistence. |
| Scheduled tasks | Task definition, registration, launch, query, deletion, and trigger properties are different facts. Reconcile `scheduled`, `task-trigger`, and `task-xml-scheduled`; a scheduled-task API is neutral. Durable malicious task installation is a persistence composite. |
| Container / network interface | Split container lifecycle, inventory, image, exec, namespace and authority facts with existing siblings. Split interface enumeration, address queries and configuration; saved WLAN credentials leave interface handling. `android-play-store-package-literal` matches `com.android.vending`, not an interface. |

## Cohort 5: observations and objective boundaries

All oversized directories in these groups are enumerated in disposition.csv.

| Group | Canonical axis and required corrections |
|---|---|
| Debugger / sandbox / VM detection | Classify the probe mechanism: debugger API, process status, tracing interference, debug registers; sandbox resource/user/artifact/timing gates; VM instruction/firmware/device probes. Remove bare APIs/vendor strings to neutral observations. `check`, `script` and `vendor` mix these axes. Compare `combined-checks`, `artifact`, `dmi`, `process`, `registry`, `instruction`, `timing` before splitting. |
| Self-modification | `runtime` restates the parent. Separate required code rewrite, import-table rewrite, and decoder self-update; relocate ordinary memory protection and GOT hook observations. Reassess anti-analysis placement when static-analysis obstruction or production interposition is the actual effect. |
| Obfuscation / packing | Separate required concealment mechanism: API hash resolution, escaped import names, dynamic dispatch, string selection/permutation/concatenation, runtime decryption, bytecode/VM dispatch, runtime unpacking. Reconcile string `reconstruct`, `fragmentation`, `concat`, `array`, `reverse`, and `recovery`; do not leave synonymous subsets. `binary-metrics`, `code-metrics/structure`, `section-anomaly`, and `detect` are rule-form/judgment buckets. Their neutral metrics go to the part measured. Named packer identity goes to well-known; actual unpacking/concealment stays objective. |
| Keylogging / screenshot / monitoring | Classify capture source/mechanism: keyboard hook, device input, DOM input, terminal; screen/display capture; camera; microphone. Generic capture APIs are capabilities; objective composites must establish surveillance context. Collection plus transmission goes to stealer. `monitor/capture` must not duplicate screenshot/keylog. `go-empty-recover` only matches empty panic recovery, not a screenshot. |
| Browser activity / messaging / email | Distinguish browsing/history collection, message/mailbox content, contacts, and credential/session stores. Route cookie/session theft to credentials, source-plus-send to exfiltration. `email-harvest::mailitems-accessed-operation` is an audit event fact; `monitor/tracking::sentry-self-hosted-dsn` is a telemetry endpoint shape, not proof of covert tracking. |
| C2 dispatch / RAT / webshell | One request-to-action axis for remote-command dispatch; polling/socket/HTTP are channel facts. Retire duplicate `control`, `tasking`, `rat/multi`, and parallel `backdoor/tasking` placements after mapping actual required operations. Keep server request-to-command webshells separate from an outbound reverse shell. Memshell intercept splits by required installed hook: request filter, listener, handler/route; plain framework registration is a capability. |
| Botnet / IRC / tunnels | `iot` is a deployment platform, `irc/client` contains protocol mechanics and malicious actions. Move neutral protocol evidence, family names, DDoS and propagation to their subjects; retain fleet-control evidence. C2 tunnels must show control/relay intent beyond proxy capability. DNS command retrieval and DNS data exfiltration are different required directions. |
| C2 trigger / infrastructure | Replace `trigger/activation` with packet knock, message/content gate, or local artifact gate when attacker activation is required. `ci-abuse` mixes ordinary Jenkins/Groovy references with credential theft, pipeline tampering, persistence and C2: retire it by effect. Brand impersonation is deception/phishing unless C2 role is independently established. `groovy-package-json-rewrite` matches only `package.json`. |
| Browser credentials / system dump / SSH / wallets | Filepaths and neutral store APIs leave objective buckets. Classify actual extraction by store and bypass/decryption mechanism. Browser source/store contracts should reconcile Chromium, Firefox, multi-target, DPAPI and session hijack. SAM/NTDS/shadow/LSASS are distinct system stores. SSH key harvesting is not host-key validation bypass. Wallet mnemonic entry phishing is not a local-wallet-store read. |
| Phishing | Deceptive prompting, form harvesting, origin/proxy relay and session interception have distinct admission predicates. `credential`, `lure`, and `mfa-relay` must not each own the same full harvest chain. Complete phishing source-plus-send chains go to `exfiltration/stealer/phish`; the deception/relay composite is referenced. |
| Discovery | `network/scan/port` requires active probing/enumeration, not a literal port or generic socket. Distinguish connect, SYN and protocol-response probing; compare `banner`, `utility`, `http`, `ics`, and distributed scanning. Host profile requires multi-property reconnaissance, with plain hostname/interface APIs in capabilities. |
| Defender / EDR | Stealth bypass/exclusion belongs in evasion; process termination, service disabling, update teardown and driver-assisted killing in impact/degrade. Reconcile `platform/defender`, `amsi`, `teardown`, `terminate`, `driver`, `targeting`, and `autostart` by required action. |
| Injection / fileless / rootkits | Require target and execution transfer for injection; hollowing, APC, thread hijack, module stomping, and remote-thread creation are distinct mechanisms. Same-process shellcode execution is not cross-process injection. A userspace LD_PRELOAD rootkit is not a kind of kernel hiding: move to an evasion concealment parent with distinct userspace-interposition and kernel-manipulation children, and reconcile existing preload/hook leaves. |
| Masquerading / logs | Classify deception by the identity surface actually falsified: process title, filename, version metadata, signer claim, or format. Retire `identity/fabricated` and reconcile `binary`, `file/lure`, `process/name`, `process/title`, `identity/process-title`. Log removal, truncation, selective record removal and disabling audit production must reconcile `logs`, `log-removal`, `audit`, `application-logs`, and `accounting`. |
| LLM prompt abuse / automation | Classify the violated boundary: instruction authority, tool arguments, policy/config mutation, sensitive export, or output disclosure. Prompt wording/carrier alone is evidence, not a unique attack. Reconcile `prompt`, `override`, `persona`, `output-steering`, and `sandbox`; neutral agent configuration must not imply code execution. |
| Destruction / ransom / infection | Destructive deletion vs overwrite vs encryption vs host infection are different effects. DOS API calls go to OS capabilities; DOS/source are not infection techniques. Split infection by append, prepend, entrypoint replacement, cavity/section insertion, or script insertion. Ransom notes/config are evidence for ransom, not necessarily encryption. Reconcile filesystem encryption with `bulk-encryption`, `hybrid` and runtime wrappers. |
| DDoS / rival removal / ICS | Protocol flood mechanism, target-disabling action and industrial control mutation define children. Botnet tasking alone is C2; neutral protocol/config methods leave impact. Merge rival `competitor` with applicable `killer`/`scan-terminate` rules. An industrial read is not sabotage. |
| Brute force / exploits | Separate credential guessing strategy (spray vs per-account dictionary vs fixed defaults) from service transport, with ordered precedence. Neutral SSH authentication leaves brute-force. Split exploit claims by exploit primitive or affected boundary, retain specific CVE context in rule metadata/files. `vulnerabilities` restates `exploit`; `network-device` mixes provisioning, discovery and exploitation. |
| Persistence | Put durable activation mechanism before platform. Merge Run-key rules in `login/startup/registry` into `login/registry/run-key`, but route Active Setup/Winlogon separately. Reconcile shell `config`, `rc`, `profile`; service `install`, `systemd`, and sibling `system/systemd`. User services/timers are not necessarily OS-boot persistence. Backdoor account creation grants continued access; it is not code executing at login. Revise the boot/login-only parent rubric accordingly. |

## Cohort 6: exfiltration and supply chain

For exfiltration, the existing `stealer/<source>` contract is already the best
canonical home for complete chains. Route the full chains in HTTP `upload`
(201), `collect` (120), `agent` (95), and `sensitive-data` (142) there; neutral
HTTP atoms leave objectives. DNS transport does not override the source of a
complete theft chain. Keep transport-specific objective leaves for transport
abuse whose required evidence does not identify a narrower source, rather than
duplicating every source under every transport.

Split the oversized stealer sources semantically: browser → cookie/session
versus saved-login versus browser history/content; system-info → host identity,
hardware/platform profile, account profile, or a required joint host profile.
Define precedence when a single chain steals several: a mandatory multi-store
sweep uses the existing sweep contract; optional extra sources do not move a
browser stealer. Network configuration already has its own source sibling.
Whether these distinctions should replace the third-level source or sit one
level below it is an explicit ML-schema choice, not an accidental overflow fix.

The supply-chain tree has the same dimensional duplication at larger scale:

- `recon-exfil/install-hook` (209) and `npm-install-targeting` (88) duplicate
  source-plus-send chains; use canonical stealer source directories and reference
  the install/build/import trigger. `install-hook/build/behavioral` (134) and
  `install-hook/dropper/hook-setup` (94) duplicate payload activation chains.
- `hidden-payload/{runtime,package,exec,staging,trojan}` mixes carrier, lifecycle,
  concealment and result. Move neutral facts to metadata/capabilities; full
  theft/delivery chains to their existing objective; keep supply-chain-specific
  concealment only when the package trust boundary is required.
- `trojanized/{package,app/package}` overlaps itself. Require unauthorized
  modification/substitution of a legitimate component. Separate dependency
  substitution, build-input/output replacement, update substitution, and
  configuration/extension poisoning. A package that is simply a loader is not
  evidence that a previously legitimate application was modified.
- `trojanized/app/config-injection` needs distinctions between instruction-file
  poisoning, tool-server configuration, authority changes and endpoint swaps.
  Reference the resulting behavior; avoid reproducing the entire attack tree
  below “agent”. `build-pipeline` should retain boundary crossings such as
  untrusted PR code under privileged credentials, not generic curl/build facts.
- `impersonation/{package/wheel-sdist,registry/manifest,registry/snapshot,
  registry/wheel-sdist}` is organized by evidence container. Move manifest and
  registry observations to metadata; retain deception comparisons by the thing
  misrepresented (name, provenance, functionality, declared contents). Registry
  versus artifact remains a source/scope distinction in the matcher. A tiny
  package, version churn, or self-disclosed security purpose is not itself
  impersonation. `cargo-dep-litcrypt` is a manifest dependency identity.

This resolves a contradiction already inside TAXONOMY.md: the “trigger is not
an objective” passage criticizes install-hook duplication while the main tree
still prescribes install-hook/recon-exfil branches. The migration must replace
that tree and its examples with these canonical ownership rules in the same
change that moves each cohort.

## Migration sequence and acceptance criteria

0. **Establish placement contracts first — documented.** Use TAXONOMY's
   level-1–3 contracts and technique-first implementation test. Before each
   migration, complete any missing leaf admission predicates and disambiguate
   overlapping siblings. Planned paths in the guide are not already migrated.
1. **Canonical atoms and metadata/identity cleanup.** Start with registry,
   process creation, HTTP, binary metadata, then source/store observations.
   Retire implementation-only layers alongside these canonical subjects,
   following the implementation-layer audit. Refine the documented contracts
   when a concrete matcher reveals an unresolved boundary.
2. **Reverse shells as the first complete pilot.** Map all 342 rules across the
   nine sibling leaves, including neutral atoms and bind/HTTP counterexamples.
   Use its reference and fixture migration as the pattern for later cohorts.
3. **Coordinate dropper/obfuscation/injection boundaries; migrate bounded batches.** Produce all
   old-ID → new-ID mappings and destination counts before moving. Fold redundant
   complete-chain composites only after comparing scope, required evidence,
   proximity and exclusions. Do not preserve a stale parent to host aliases.
4. **Exfiltration and supply-chain chains together.** Otherwise each migration
   repopulates the other's old buckets. Move trigger/context facts first, then
   route result composites and update package/archive scope deliberately.
5. **Remaining objective cohorts and broad identity catalogs.** Follow the
   disposition ledger; use the structure report to prune redundant depth and
   introduce primary-function breadth where required.

For **every** cohort:

- Materialize a mapping for every old rule: keep, move, merge into named
  canonical rule, or retire with evidence. Record inherited defaults before
  splitting YAML files. Language-specific matchers may remain separate within
  one directory; collapsing them must preserve supported scopes.
- Compute destination counts including incoming rules and existing residents.
  All must be ≤100, with no exemptions, and every internal directory must be
  free of YAML leaves. Do not choose an arbitrary “misc” remainder.
- Rewrite local references, fully-qualified references, positive directory
  references, `unless`, `downgrade`, fixture expectations, source/docs examples,
  and engine consumers. Compare the **resolved member sets** of directory refs
  before/after; a syntactically valid reference can still change meaning.
- Snapshot match results before moves. For pure relocations, compare detections
  modulo the ID map, including criticality, scope, exclusions, confidence and
  evidence. For semantic repairs, document expected verdict changes and add
  targeted positive/negative cases: HTTP-over-dev-tcp vs reverse shell,
  bind vs connect-back, legitimate registry writes vs persistence, ordinary
  installers vs payload activation, and authorized telemetry vs theft.
- Require all focused tests and `make validate` before declaring the migration
  complete. Until all cohorts fit, track the exact remaining oversized set;
  `--soft` is diagnostic, never the final acceptance check.
- Update the feature schema/mapping supplied to downstream consumers. A path
  migration changes ML features even when runtime findings are equivalent;
  retraining/evaluation is needed before claiming improved ML accuracy.

The outcome should be fewer overlapping concepts and stronger canonical
observations. Passing a numeric cap alone is not evidence of a defensible
taxonomy or better model performance.

### Latest checkpoint: notebook identity cues leave the generic profile bucket

Moved the Colab project/version identifier observations and their notebook
metadata-harvest composite from `objectives/discovery/system/profile/` to
`objectives/discovery/system/fingerprint/notebook/`. The rules are gated on a
Colab callback plus a notebook-specific identifier; that subject is narrower
than generic host profiling and now has an explicit place in the discovery
tree. Also moved Swift host/system field pairs to `fingerprint/info/`: the
fields establish profile content, while the existing exfiltration composite
adds the transfer evidence. Its ATT&CK mapping is now T1082 at the discovery
atoms and remains T1041 on the exfiltration composite. Finally, moved the Node
process-snapshot path clue into `objectives/discovery/process/enumerate/` and
renamed its description to identify it as a path reference rather than claim
the program creates the file. The relocated matchers retain their criticality
and scope; the process clue's ATT&CK mapping now reflects process discovery
rather than network exfiltration. Repository search found and updated the
Swift exfiltration consumer and all three consumers of the process-snapshot
clue. The source profile bucket falls
from 93 to 87 rules from those subject relocations, then to 84 after moving
Go's `ps`, `netstat`, and `df` command clues into process enumeration, network
status, and disk-information capability homes. The host-profile command-set
composite now references those generic capability atoms. Reused shared
BusyBox-source and apko identity exclusions in the new atoms to avoid
duplicating inline suppression logic. Strict validation remains at its
pre-change 60 issues, while over-cap directories fall from 164 to 163; the
profile leaf is no longer over cap. The larger taxonomy audit and global cap
migration remain incomplete.

### Latest checkpoint: browser bundleware is separated from browser discovery

Moved the seven-rule AVG/SlimWare bundleware chain from
`objectives/discovery/host/browser/identity/` to
`objectives/impact/ui/manipulation/browser/`. The installer clues, homepage
offer, toolbar identifier, tracking/PDB clues, and hostile bundleware composite
describe unauthorized browser-setting manipulation; they do not describe
learning which browsers are present. The browser-discovery sibling keeps its
browser identity, installed-browser, and data-location rules. Matcher bodies,
scopes, criticalities, and composite membership are unchanged; repository
search found no external references. The taxonomy tree now defines the browser
manipulation leaf. This reduces browser identity from 88 to 81 rules and the
global over-cap count by one; it does not complete the broader cohort audit.

### Latest checkpoint: VBScript payload execution leaves document delivery

Split `delivery/document/vba-embedded-pe.yaml` by the behavior each rule
requires. The two VBScript drop-and-run composites moved to
`dropper/file-exec/spawn/`; the reconstructed hard-coded PE payload and its MZ
string evidence moved to `dropper/staging/encoded/`, because they establish a
payload but no activation sink. The descendant leaf is now documented with
that admission rule. Matchers, effective VBS/Windows scope, confidence,
criticality, and composite legs are preserved; the only reference update is
the hidden-run composite's link to the moved drop-and-execute rule. This takes
`dropper/delivery/document` from 86 to 82 rules without removing detection and
reduces the global over-cap count by one. The full migration plan remains open.


### Latest checkpoint: browser export is separated from incidental capabilities

Implemented [the browser-export audit](BROWSER-EXPORT-BOUNDARIES.md): seven
moves, three unsupported hostile wrapper retirements, and no matcher changes.
The browser-export leaf stays at 85; its three incoming export chains have
positive and local-only controls. Cookie-reader and cookie-jar modules follow
their HTTP capabilities, a TLS reference follows TLS writing, and the archive
footer diagnostic follows custom archives. Sixteen exclusions retain that
archive-specific evidence explicitly. Existing acquisition consumers retain the
exporters' required source evidence without new aliases or redundant wrappers.

The audit covers 59 directory references in 53 consumers and protects 64 original
definitions. New and established controls pass 71 assertions across 31 files.
All 1,841 corpus fixtures pass with only the documented pre-existing shell-decoder
regression isolated in a temporary copy. Live soft validation still fails that
regression; strict validation reports 96 diagnostics and 147 oversized directories
in the shared tree. A concurrently introduced filename-bearing CPUID reference
was corrected so validation could load the catalog. The broader taxonomy plan
remains open; remaining PyInstaller contents and browser-export evidence chains
need further semantic review.

### Latest checkpoint: self-extract leaves follow activation and staging evidence

Audited all 24 rules in the legacy `dropper/execution/self-extract` leaf.
AutoHotkey FileInstall/Run, IExpress/AutoIt, and the MSI wrapper now follow
`dropper/file-exec/spawn`; fixed-offset self-reading C code follows
`dropper/staging/stub` without claiming an unbound activation handoff. The
background local-tool probe moved to neutral shell launch, and the
Windows-System self-read/process profile moved to path masquerade. All external
references were updated. The legacy leaf is empty; the dropper inventory is
113 files, 1,233 rules, and 19 rule-bearing directories, with no leaf over 100.

### Latest checkpoint: HTTP is a transfer source, not a taxonomy level

Audited all 28 rules in `dropper/execution/http`. JVM, Python, and the
path-based Rust launch follow `dropper/file-exec/spawn`; Rust
`curl|shell` follows `dropper/delivery/pipe`. PHP response writes and
variable includes now live with filesystem-response and PHP auto-exec
capabilities. Kotlin and PHP decode profiles remain staging context without
an asserted response-to-sink relationship. A duplicate Hermit archive
bootstrap rule was retired, and the Block FTL archive refinement moved to
supply-chain manifest evidence. The legacy HTTP leaf is empty.

### Latest checkpoint: network-stage is split by bound behavior

Audited all 28 rules in `dropper/execution/network-stage`. The one compact
fetch/write/chmod/spawn chain follows `dropper/file-exec/spawn`; the npm
wrapper follows install-hook context. Other rules now describe neutral Node
process, hidden execution, archive, temporary-file, wallet, obfuscation and
path-masquerade evidence. Fetch/write/launch co-occurrences without a value or
path handoff no longer claim a dropper. All old consumers were updated and the
legacy leaf is empty.

### Latest checkpoint: JPHP carrier evidence leaves dropper execution

Audited all 29 rules in `dropper/execution/jphp`. Runtime markers moved to
the neutral runtime-interpreter capability; process, archive, hidden-form and
Defender-context rules follow their actual subjects. The JPHP name is now
scope evidence rather than an activation technique. All rule IDs were
preserved and the legacy leaf is empty.

### Latest checkpoint: markup and masquerade-loader leaves are behaviorally split

The 29-rule HTML markup leaf was divided between clipboard-lure PowerShell
evidence and blockchain-delivery staging evidence. The SQLite proxy profile
moved to the DLL-proxy masquerade leaf, while its exact Native API injection
duplicate was removed in favor of the existing definition. Three additional
identity profiles moved from `masquerade-loader` to version-resource, versioninfo
and brand-wrapper leaves. The remaining COM, timer, signer and LaoMaoTao rules
then followed their process, timing, trust and identity leaves. The reflective
leaf also closed: batch/.NET reflective chains moved to `dropper/module-load`,
and the stripped batch crypter moved to `dropper/file-exec/command`. The Deno
bring-your-own-runtime cohort then moved from `runtime-eval` to the existing
standalone JavaScript-runtime technique, with its two supply-chain consumers
updated. Android DEX wget staging and netcat stream-to-shell delivery moved
from the pipe carrier to the existing Android staged-loader and dropper pipe
techniques. Miner configuration hijacking moved to cryptojacking configuration
and the inline Python listener moved to neutral socket-listen evidence. The
dropper subtree now contains 113 files and 1,233 rules across 19 rule-bearing
directories. The reflective, runtime-eval and these pipe subcohorts are now
resolved; the shell pipe file now retains only generic pipe, installer and
fetch-loop evidence after its three misplaced atoms moved to specific leaves.

### Latest checkpoint: staged-loader remains one leaf and platform names stay in filenames

The Android DEX pipe rules had been placed under a platform-named child
directory while the parent also contained YAML, violating the strictly
leaf-only and platform-neutral directory policies. The child was flattened
to `dropper/staged-loader/android-pipe.yaml`; the filename preserves the
Android scope while the directory continues to describe the staged-loader
technique. Matcher bodies, IDs, scopes and conditions were preserved.

The validator now reaches catalog-wide policy checks: the staged-loader
structure and platform-directory errors are gone, and two stale references
were repaired to their existing neutral traits. The current shared catalog
still reports 107 issues, dominated by 69 oversized directories and six
micro-behavior-to-objective references; those are separate taxonomy debts and
remain queued for their own evidence review.

### Latest checkpoint: objective composites leave capability directories

The six obfuscated Node hidden-stage composites were objective in substance:
they combine hidden process creation with obfuscation, dynamic loading and
staging context. They moved from `micro-behaviors/process/create/hidden` to
`objectives/evasion/process/hidden/execution`, and the plugin-loader consumer
was updated. Three Node archive/staging composites likewise moved from the
archive capability file to `dropper/staging/archive`; the neutral archive
constructor atom remains in `micro-behaviors/data/archive/library`.

The hostile JVM bytecode temp-execution composite moved to the Java file-exec
objective with its original scope and ATT&CK mapping preserved. The Rust and
Classic ASP composite scopes were corrected so every required leg can match
the declared file type. OpenWrt kprobe composites now declare only source or
ELF types supported by their kprobe evidence; the invalid outer scope was
removed. These changes eliminate six capability-to-objective errors, the
hostile capability error, and all composite file-type errors.

The generic shell-spawn leaf was reduced from 101 to 96 rules by moving the
five batch start/temporary-execution observations into the existing
`process/create/shell/batch` technique leaf and updating all consumers. The
batch child now holds 17 rules and remains below the cap. The validator now
reports 95 catalog issues, with 66 oversized directories and seven
suppression-limit findings still requiring broader evidence audits.

The 42-rule payment-document executable lure cohort then moved from the broad
`masquerade/file/lure` leaf to the technique-specific sibling
`masquerade/file/payment`. Its local composite references were preserved, and
external cabinet, installer and medical-lure consumers now use the new
directory ID. The generic lure leaf is 63 rules; the new payment leaf is 42.

The Linux system-process name cohort then moved from the broad
`masquerade/process/name` leaf to the technique-specific sibling
`masquerade/process/system-name`. The parent retains 59 rules and the new leaf
holds 52. Both splits are behavior-based boundaries rather than platform or
language partitions, and the current catalog has no broken trait references.

The broad anti-static imports leaf was also split at a real technique boundary:
the 91 API-hash and additive-hash rules now live under
`anti-static/obfuscation/imports/api-hashing`; the remaining 100 import-
obfuscation rules now live under the sibling `imports/concealment` leaf. The
category node is YAML-free, so the strict leaf-only rule remains intact. The
validator's oversized-directory count is now 64; the remaining cap failures
still need evidence-led technique splits.

The 188-rule `dropper/staging/embedded` leaf was then flattened into four
depth-five technique leaves: `staging/runtime` (runtime carriers),
`staging/native` (native binary carriers), `staging/script` (script and registry
carriers), and the existing `staging/archive` leaf (archive carriers). The
moved cohorts contain 94, 46, 39, and 9 rules respectively; the archive cohort
joins the pre-existing archive rules. This preserves the carrier
mechanism in the path, avoids a sixth level, and removes the mixed parent.

After this flattening, the shared validator reports 64 oversized directories;
the remaining failures are independent of the dropper staging move. The move
also leaves no broken references in the staging subtree.

The encrypted-staging audit found that the 88-rule `7z-aes-exe` cohort was
archive staging rather than a general encrypted-payload category. It now lives
in the depth-five `dropper/staging/encrypted-archive` leaf; the generic
`dropper/staging/encrypted` leaf retains 96 rules and the existing archive leaf
is unchanged. This is a carrier distinction, so it remains platform and
language neutral. The validator now reports 63 oversized directories.

The latest `make validate` run reaches all catalog policy checks with 23
issues: 61 oversized directories, six suppression-limit findings, twelve
long-regex or three nested-regex reviews, and one duplicate matcher warning in
each of the literal-covered and cross-surface categories. Broken references,
impossible file-type composites, mixed leaf directories, and micro-to-objective
cap references are now clear. The hidden-payload runtime audit then routed
remote loader cohorts to `hidden-payload/remote-loader`, native extension and
plugin cohorts to their mechanism leaves, package obfuscator evidence to
`anti-static/obfuscation/obfuscator-supply-chain`, and telemetry composites to
their data-source stealer leaves. Runtime is now 94 rules and the catalog has
61 oversized directories remaining. These remaining warnings are
matcher-quality work and independent cap audits, not unresolved references.

The encrypted-payload audit then split three concrete carrier mechanisms:
the 35-rule source-level command cohort moved to
`anti-static/obfuscation/payload/encrypted-source`, 33 executable-loader
rules moved to `payload/encrypted-loader`, and 27 key/placeholder-key rules
moved to `payload/encrypted-key`. The parent encrypted leaf is now 83 rules;
all consumers were retargeted and validation reports no broken references or
YAML parsing errors. The current validator total is 23 issues with 59
oversized directories; the shared-default reuse warnings were folded into
file defaults during the same quality pass.

The debugger-detection audit then reduced the broad 148-rule
`anti-analysis/debugger-detect/check` leaf to exactly 100 rules. Twenty-three
loader-bound rules moved to `debugger-detect/loader`; 22 multi-signal
profiles moved into the existing `debugger-detect/combined-checks` leaf,
which now holds 49 rules; and three exception-trigger profiles moved to the
new `debugger-detect/exception` leaf. All external and local references were
retargeted, and validation again reports no broken references or YAML parsing
errors. The catalog now has 60 oversized directories remaining.

The process-injection audit then reduced
`evasion/process/injection/memory` from 147 to 94 rules. Thirty-three
ptrace/procfs rules moved into the existing `injection/ptrace` leaf, seven
in-memory module-loading rules joined `injection/native`, and 19
code-cave/GOT-hijacking rules moved into the new `injection/hijack` leaf.
References were retargeted and validation reports no broken references or YAML
parsing errors. The catalog now has 59 oversized directories remaining.

The trojanized-application package audit reduced
`supply-chain/trojanized/app/package` from 148 to 40 rules. Eighty-three
agent-skill rules moved to the new `app/agent-skill` leaf; native-agent,
remote-agent, installer, and vendor-repack cohorts moved to their existing
`native-loader`, `remote-command`, `installer`, and `replace` leaves,
which now hold 9, 9, 18, and 37 rules respectively. All known consumers were
retargeted. The taxonomy files parse cleanly; the full validator is currently
blocked before taxonomy checks by an untracked benign fixture lacking an
expectations entry, so the next run must re-establish that fixture baseline
before measuring the cap count.

The build-pipeline audit moved the 95-rule CI workflow and pull-request
tampering cohort into the new `supply-chain/trojanized/ci-pipeline` leaf. The
residual `build-pipeline` leaf is 49 rules, and three external consumers were
retargeted. This is a CI authority boundary rather than a provider or language
split; the catalog has 58 oversized directories remaining.

An isolated validation overlay (with a temporary expectation only for the
untracked Tor benign fixture) confirms the post-move tree loads and resolves
all references. It reports 24 catalog issues and 57 oversized directories;
the extra quality findings are seven suppression-limit warnings and one
binary-section validation warning. The repository's direct `make validate`
remains blocked by that untracked fixture's missing expectations entry, so the
overlay result is the authoritative taxonomy check until the fixture manifest
is reconciled.

The dropper staging audit then split the 128-rule `staging/memory` leaf by
carrier mechanism: 46 managed-runtime memory loaders moved to the existing
`staging/managed` leaf and 44 script/interpreter stages moved to
`staging/script`. The residual `staging/memory` leaf now has 38 rules. All
references were retargeted, and the taxonomy guide now makes these carrier
boundaries explicit while keeping HTTP, encryption, and language as matcher
context rather than extra taxonomy levels.

The persistence service audit reduced `persistence/system/service/install` from
133 to 99 rules. Twenty-five kernel-driver registration rules moved to the new
`persistence/system/driver` leaf, seven SafeBoot-only rules moved to the new
`persistence/system/safeboot` leaf, and two `svchost` service-DLL loader rules
joined the existing `persistence/system/service/loader` leaf. References were
retargeted, and the taxonomy guide now distinguishes service installation,
kernel-driver activation, SafeBoot startup, and service-DLL loading.

The kernel-hide audit moved the 57-rule `kernel-hide/userspace/ld-preload`
legacy file into the existing `hijack-execution-flow/env/preload` leaf. LD_PRELOAD
is environment-based execution-flow hijacking, so this removes a duplicate
userspace branch without introducing a language or operating-system split.

The packing audit moved the 89-rule `anti-static/pack/section-anomaly/loader-noise`
cohort into a new sibling `anti-static/pack/loader-noise` leaf. The residual
`section-anomaly` leaf now contains only section-layout measurements and
ownership anomalies; all consumers were retargeted.

The string-obfuscation audit moved four mechanism-specific files out of
`obfuscation/string/encoding`: HTA and C octal source syntax moved to
`obfuscation/syntax`, rolling-XOR moved to `string/crypto`, and browser-target
substitution moved to `string/conceal`. The encoding leaf is now 96 rules, and
the taxonomy guide records the mechanism boundaries.

The tunnel audit moved 23 SOCKS-specific rules out of the 118-rule
`command-and-control/channel/tunnel/proxy` leaf into a new sibling
`channel/tunnel/socks` leaf. The generic proxy residual is 95 rules, and the
taxonomy guide now distinguishes protocol-specific SOCKS tunneling from generic
relay behavior.

The Defender audit moved eight telemetry/scanning-suppression rules from
`anti-av/platform/defender` into the existing `anti-av/blinding` leaf. The
Defender leaf is now exactly 100 rules; exclusions, service changes, and
product-control settings remain there, while notifications, MAPS/sample
reporting, behavior, IOAV, and archive-scanning suppression use `blinding`.

The string-reconstruction audit moved the 38-rule indexed-character cohort
from `obfuscation/string/reconstruct` into a new sibling
`obfuscation/string/index-select` leaf. Generic reconstruction remains 75
rules, and references were retargeted.

The latest isolated validation overlay resolves all references after these
moves and reports 50 oversized directories. The remaining non-taxonomy findings
are the pre-existing unknown `objectives/execution/database` tier, three
quality description/validation issues, and seven suppression-limit warnings;
the direct validator is still blocked by the untracked Tor fixture noted above.

The subsequent overlay sees a partial count of 49 oversized directories, but
its final load is interrupted by two concurrent YAML parse errors in
`objectives/evasion/process/injection/cluster/traits.yaml` and the untracked
Tor browser fixture. The post-Defender count of 50 was reference-clean; a final
cap measurement must wait for those shared-file changes to be reconciled.

The direct validator now reports 41 oversized directories after the fileless,
SysV-init, shell-sink delivery, and kernel-module splits. It resolves the moved references;
remaining hard failures are the unrelated quality findings and the existing
Tor-browser reference issue.

The fileless audit moved the 33-rule anonymous-file-descriptor cohort from
`evasion/fileless/memory` to a new sibling `evasion/fileless/memfd` leaf. The
generic fileless memory leaf now contains 74 rules; references were retargeted
and the taxonomy guide distinguishes `memfd` execution from other in-memory
mechanisms.

The kernel-module audit moved the three-rule VxWorks module/task-table hiding
profile into the existing `kernel-hide/rootkit` leaf. The generic
`kernel-hide/module` leaf is now 99 rules, with the taxonomy guide documenting
the coordinated rootkit boundary.

The dropper delivery audit moved the 92-rule shell-sink cohort out of
`dropper/delivery/fetch-exec` into the sibling `delivery/fetch-exec-shell`
leaf. The general `fetch-exec` residual is 41 rules; references were
retargeted and the taxonomy guide makes shell an activation mechanism rather
than a source-language branch.

The persistence boot audit moved the two-rule `runlevel-self-install` cohort
from `persistence/system/init/boot` into the existing `init/script` leaf. The
boot leaf is now 99 rules; the taxonomy guide records SysV runlevel scripts as
the mechanism-specific child.

The persistence timer audit moved the nine-rule `user-timer-source` profile
from `persistence/system/service/systemd` into the existing
`persistence/system/cron/schedule` leaf. Systemd service installation remains
under `service/systemd`; the schedule leaf owns the required timer trigger.

The script-infection audit moved the three-rule AutoLISP self-replication
profile from `impact/infect/script/self-copy` into the existing
`impact/infect/macro` leaf. The self-copy residual is now 104 rules, so further
splitting is still required there.

The follow-up infection audit moved the four-rule Go embedded-shell infector
into `impact/infect/script/inject`, where the matcher establishes code written
into an existing script host. `script/self-copy` is now exactly 100 rules.

The EDR teardown audit moved four mechanism cohorts: Java security-tool kills
to `edr/terminate`, AppRemover and BTR vulnerable-driver profiles to
`edr/driver`, and the driverless WFP silencer to `edr/network`. The residual
`edr/teardown` leaf is 97 rules; references were retargeted and the taxonomy
guide records the mechanism boundaries.

The phishing audit moved 11 passkey/WebAuthn rules from
`credential-access/phishing/mfa-relay` into a new sibling
`credential-access/phishing/passkey` leaf. MFA relay is now exactly 100 rules;
the guide distinguishes passkey spoofing/downgrade from challenge relaying.

The ICS audit removed the mixed parent leaf by moving the 44-rule safety-
parameter matcher set from `impact/degrade/ics` into
`impact/degrade/ics/parameter`. The existing PLC-disruption and device-recovery
leaves now sit beside it, so the parent is a strict grouping node and each
child names a distinct OT-impact action. The taxonomy guide documents the
boundary between process/setpoint mutation, controller/project disruption,
recovery interference, neutral protocol mechanics, and discovery.

The botnet audit moved the Android TV raw-packet flood composite from
`impact/dos/attack/botnet` into the existing `impact/dos/attack/flood` leaf.
Its evidence establishes a flood implementation, but no botnet coordination,
so the move removes a one-rule overflow without using the implementation
platform as a taxonomy level.

The RAT-control audit moved the UPnP-exposed remote-control composite and the
Android accessibility/VNC surveillance composite into the existing
`backdoor/rat/remote-agent` leaf. Both establish an exposed or interactive
remote agent rather than RAT tasking control signals; the former control leaf
therefore drops to the 100-rule cap without a platform split.

The CI-abuse audit moved the generic Groovy shell-command atoms into
`micro-behaviors/process/create/shell/command-string` and the dynamic-evaluate
atom into `objectives/execution/interpreter/eval/dynamic`. CI composites now
reference those neutral capability leaves, leaving the CI directory for
context-specific behavior instead of using Groovy as a taxonomy axis.

The indicator-removal audit moved the six-rule PowerShell ETW provider-disable
cohort from `indicator-removal/logs` into the existing
`anti-av/blinding` ETW leaf. ETW telemetry suppression now has one home beside
the native patching profiles; ordinary log deletion remains under `logs`.

The log-removal audit separated shell-history truncation into
`indicator-removal/history` and moved the remaining auth/lastlog and journal
cohort into `indicator-removal/log-removal`. The cross-purpose composite now
references the history atom explicitly; the general `indicator-removal/logs`
leaf is at the combined cap.

The appliance-tasking audit moved six NetScaler/Citrix ADC command-control
profiles into `command-and-control/remote-command/appliance`, alongside the
existing PAN-OS appliance profiles. Their required control surface is an
appliance remote-command technique rather than generic HTTP tasking; references
were retargeted and the HTTP tasking leaf is now within the cap.

The follow-up appliance audit moved the QNX, RouterOS, and remaining NetScaler
tasking profiles from `backdoor/tasking/poll` into the same appliance leaf.
Their platform names describe the controlled appliance surface, while the
required command channel remains remote-command/appliance; the poll leaf is
now within the combined cap.

The RAT-tasking audit moved the 75-rule Windows RAT command vocabulary into
`backdoor/rat/command-set`. It contains explicit task names spanning discovery,
collection, credential access, evasion, and lateral movement, so it is a RAT
control-surface technique rather than generic remote-task transport. The
generic `remote-command/tasking` leaf remains direct and reference-clean.

The package-impersonation audit moved the scoring composite file from
`impersonation/package/wheel-sdist` into the existing `impersonation/package/scoring`
leaf. Wheel/sdist remains the home for package-summary and archive evidence;
scoring composites now have a distinct inference-function home.

The LLM prompt audit partitioned the former mixed prompt leaf into `mcp`,
`carrier`, `egress`, and `override` leaves. MCP tool poisoning, propagated
prompt carriers, network-control directives, and direct behavior overrides now
have distinct homes; the parent holds no rules and all references remain valid.

The fabricated-identity audit moved named application identities into
`masquerade/identity/app`, security-product identities into `.../product`, and
installer/NSIS/driver-installer identities into `.../installer`. The former
fabricated leaf now retains only identities without a more specific artifact
class.

The destruction audit moved container-store and privileged host-root wipes into
the new `impact/destroy/container` leaf, and LLM-directed destructive deletion
into `impact/destroy/agent-directed`. The ordinary file-deletion leaf is now at
the combined cap.

The dropper audit retired the mixed `delivery/fetch-eval` leaf as a destination.
Remote response-to-interpreter rules now live under `dropper/script-eval/response-eval`
or the more concentrated `remote-code` profile; the `response-eval` name avoids
the ambiguous sibling stem that the validator flagged. Embedded decoded-source
evaluation lives under `script-eval/embedded`. References were retargeted by
rule ID. This separates the activation sink from the transport or package
carrier and removes one combined-cap violation without a language branch.

The remote-command audit partitioned the legacy `control` leaf into ADB,
WebSocket, SSH, MCP, interactive-terminal, hosted-service, and generic
dispatch mechanisms. Generic task profiles were added to the existing
`remote-command/dispatch` leaf; the mechanism leaves retain their control
surface evidence without turning implementation languages into taxonomy levels.

The encoded-payload audit split `anti-static/obfuscation/payload/encoded` by
its required sink: exactly 100 decoded-to-execution rules now live in
`encoded/exec`, while 24 carrier/decoder observations live in `encoded/carrier`.
This keeps encoded content from being treated as execution merely because a
decoder or dynamic API is present.

The install-hook audit migrated the cloud-metadata cohort out of the legacy
trigger bucket. Cloud theft now uses `exfiltration/stealer/cloud`; database
software discovery uses `discovery/host/software`; database query collection
uses `collection/database/query`; file, environment, developer-secret, and
database-recon results use their source-specific stealer leaves. The install
hook remains a referenced lifecycle fact rather than a second objective axis.

The Cargo package audit moved neutral dependency and feature presence facts to
`metadata/package/dependencies/manifest/presence/cargo.yaml`, keylogging
profiles to `collection/keylog/capture`, ransomware profiles to their impact
leaves, and two multi-source theft profiles to `exfiltration/stealer/multi-source`.
The remaining Cargo package profile is exactly 100 rules, so the package leaf
meets the inclusive cap without a Cargo-specific directory level.

The latest cap pass completed the remaining reorganizations. Technique cohorts
now live in leaves under `botnet/iot`, network-device exploit, dropper download,
hidden-payload staging/exec, binary masquerade, scan/port, sensitive-data,
hollowing, privilege-escalation vulnerabilities, eval/scripting, password
brute-force, dispatch/shell, and the Elex family. The child names answer the
documented technique question; source languages and platforms remain filenames
or matcher scope. References were retargeted by directory and the leaf-only
invariant was rerun after each cohort.

The authoritative audit (`scripts/audit-taxonomy.py --cap 100`) now reports
**0 violating directories, 0 rules in violators, and 0 excess rules** across
**118,901 rules** (79,410 atomic and 39,491 composite). It finds 109 depth-five
directories and four depth-six leaves; depth above five remains a soft warning.
The 75-atomic historical count still identifies 19 directories, but the
inclusive combined cap is the enforced policy. The legacy
`dropper/execution` tree is empty after its final sink-based migration.
`make validate` reaches the taxonomy checks without cap, leaf-directory,
meaningless-segment, YAML, or broken-reference errors; its remaining failures
are independent quality, deduplication, and suppression checks already present
in the tree.

The global matcher inventory contains 418 identical atomic matcher groups. The
validator should continue flagging identical matcher bodies, but the audit must
include scope, defaults, constraints, severity, and the semantic claim before
suggesting a merge. A neutral atom and an objective composite may intentionally
share a matcher; identical text alone is a review signal, not an automatic
deduplication.

Future taxonomy work should use the same sequence: state the result and the
deciding child question in `TAXONOMY.md`, split only into technique-bearing
leaves, retarget every reference, and rerun both validation and the authoritative
audit. Sparse sibling output remains advisory at 35 rules; depth above five is
the soft warning. Neither should override a precise, defensible placement.

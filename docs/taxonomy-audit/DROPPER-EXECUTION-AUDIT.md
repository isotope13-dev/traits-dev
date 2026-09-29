# Legacy `dropper/execution` taxonomy audit

The `execution/` partition is a historical phase bucket, not a subtechnique of
dropper. Its 41 remaining rule-bearing children mix activation sinks, programming
languages, file types, transfer protocols, concealment methods, triggers,
program roles and unrelated objectives. A rule can satisfy several of those
labels, so the old tree cannot give it one reliable home. New rules should use
the activation-sink contract in [TAXONOMY.md](../../TAXONOMY.md#remote-access-reverse-shells-and-droppers).

The reproducible [rule inventory](dropper-execution-rules.csv) lists every
remaining rule with its matcher, references, effective scope and source file.
[`scripts/audit-dropper-execution.py`](../../scripts/audit-dropper-execution.py)
regenerates it and the [summary](dropper-execution-summary.json). This is a
complete structural inventory, **not** a claim that every rule has yet passed
individual evidence review. Keep the source rule visible in this checklist
until its matcher and consumers have a supported destination.

At this checkpoint: **190 files, 1,749 rules, 41 directories**. No leaf
exceeds the inclusive 100-rule cap. The last two former violators now hold:

| Leaf | Rules | Excess | Remaining precision question |
|---|---:|---:|---|
| `script` | 0 | 0 | Retired after Ruby launch and HTTP evidence review. |
| `exec-download` | 0 | 0 | Retired after rule-level HTA/WSH review. |

The cap determined review order; it does not justify language, carrier or
`loader` subdivisions. These are still legacy audit sources, not final
taxonomy destinations.

## Directory-level diagnosis

The groups below record the historical audit sources, including leaves now
empty. They name the original organizing axis, not a destination for all their rules. A leaf can contain
several actual sinks and requires per-rule disposition.

| Historical axis | Original children under review |
|---|---|
| Activation or loader role, often mixed with stage or concealment clues | `binary-native`, `eval`, `fileless`, `inject`, `loader`, `masquerade-loader`, `native`, `reflective`, `self-extract`, `stealth-spawn`, `stego-loader`, `vb6-shell`, `windows-loader`, `wmi` |
| Carrier, host, language, file format or application | `batch`, `browser`, `clickfix`, `dropper-script`, `installer`, `jphp`, `markup`, `msi`, `resource`, `script`, `shell-chain`, `sqlserver`, `wsh`, `wsh-reconstruct` |
| Acquisition, staging or transfer route | `exec-download`, `http`, `network-stage`, `payload`, `pipe`, `wininet-stage` |
| Orthogonal feature or other objective | `build`, `encoding`, `kontuke`, `nezha-dropper`, `persistence`, `platform-branch`, `runtime-eval`, `string-reconstruct` |

`exec-download` and the now-empty `execute-download` were synonymous phase labels; `script`
and `dropper-script` overlap by carrier; `loader`, `windows-loader`,
`dotnet-obfuscated-loaders`, and `masquerade-loader` overlap by program role.
Neither these sibling names nor their current paths distinguish one specific
activation mechanism. `inject` is closer to a mechanism, but its members must
still establish cross-process transfer before entering `process-inject`.

## Rule-level findings verified so far

- `csharp-download-base64-assembly-invoke` requires WebClient fetch, Base64
  decode, `Assembly.Load`, and reflective invoke within 1,024 bytes. Its
  supported sink is `dropper/module-load`; its YAML moved intact.
- `vscode-hidden-terminal-remote-eval` requires an adjacent VS Code terminal
  `sendText` command with `iwr` piped to `iex`. Its sink is
  `dropper/script-eval`; its YAML moved intact.
- `pyinstaller-runtime-source-loader` combines one-file extraction, XOR
  decoding and a Python compile/exec bytecode tail. The supported sink is
  `dropper/script-eval`; its YAML moved intact.
- `dotnet-shipped-key-reflective-load` requires static-key decryption near
  `Assembly.Load` of a buffer. Its supported sink is `dropper/module-load`;
  its YAML moved intact.
- `powershell-inmemory-reflective-dotnet-loader` requires memory copy,
  `Assembly.Load` and reflected method invocation. It moved to
  `dropper/module-load`. Its process-injection ATT&CK mapping was removed:
  no cross-process transfer is required by the matcher.
- The two Python stdin-interpreter composites required no relationship between
  the HTTP response and the child process. Both now live under the neutral
  `process/create/subprocess` capability. The HTTP variant says that response
  handling and a stdin-reading Python child coexist; it no longer asserts
  fetched code reached that pipe. The original `all`/`any` matcher legs and
  confidence are unchanged. A synthetic Python sample with response access
  matches both rules; the same child without response access matches only the
  detached-child rule.
- The old `werfault-assemblyresolve-stage-loader` required a fabricated
  Werfault identity, `AssemblyResolve` registration, and a CreateProcess API
  name, but no staged assembly load or staged-file launch. It now describes
  the supported identity claim under `evasion/masquerade/identity/fabricated`
  as `werfault-identity-assemblyresolve-hook`; the six matcher legs are intact.
- The retired `copy-stage::unsigned-copyfile-http-post` required `CopyFileA` and an HTTP
  POST request line. Its comment claims a copy-plus-spawn dropper, but no
  spawn or relation to the HTTP body was matched. It had no consumers; the
  two neutral component findings remain available.
- The seven `ast-script` observations moved into neutral HTTP-client,
  Base64-decode, file I/O mode, chmod and file-rename leaves. Their consumers
  now use the new IDs. The old `ruby-ast-base64-dns` matcher established only
  `Base64.decode64`, and `ruby-ast-chmod-777` did not inspect the chmod mode;
  both claims were corrected. Four old symbol matchers could not match normal
  receiver-qualified Ruby calls because Cleave's Ruby call facts store bare
  method names. Receiver-aware syntax queries now match the intended
  `Net::HTTP`, `Base64`, and chmod calls. The positive Ruby fixture matches
  all seven moved rules; a file with unrelated `get_response`/`decode64`
  methods and a non-executable rename matches none of the five tested
  discriminating rules.
- The three `loader/compat_missing.yaml` sentinels were removed. Two were
  optional impossible clauses: the Flying Windows rule now requires its two
  real corroborators directly, and the execution-methods rule keeps its real
  alternatives. The third sentinel was required by
  `hijack-gen-dotnet-shellobject-loader`, making that family rule unreachable;
  the inert rule was retired. Restoring it needs a real, family-specific
  matcher, not a generic .NET loader cluster. No other rule referenced it.
  Validator improvement: report a required reference to a sentinel literal
  such as `__cleave_missing_*` as unreachable, and report the incompatible
  effective file types of required producer and consumer where possible.
- The `loader` leaf still contains 25 atomic rules, including a ConfuserEx
  banner and PE import-count metrics. The remaining
  75 composites need sink and claim review; moving the entire leaf to
  `module-load` would misclassify these other subjects.
- The 19-rule PyInstaller bytecode file mixed API names, Run-key clues,
  cryptography names, AMSI context, and an embedded PE profile under
  `dropper/execution/loader`. Its 11 atomic clues now live in registry,
  path, AMSI, memory, timer, CLR, and crypto capability leaves. The
  `SetValueEx` name moved to registry access: a synthetic `.pyc` check showed
  that the existing boundary-based bytecode winreg matcher and the old exact
  matcher miss strings adjacent to marshaled bytes. A substring matcher detects
  it. The same issue affected `CreateTimerQueueTimer`; its bytecode marker
  now uses a substring matcher. The Run-key composite moved to
  `persistence/login/registry/run-key` and now requires that write clue;
  its old AppData-or-Base64 alternatives did not support a write. The AMSI
  and timer/memory clusters moved to neutral leaves: API-name co-occurrence
  does not prove patching, shellcode execution, or cross-process injection.
  The AES/CBC and CLR/Invoke clusters likewise report names, not decryption
  or a .NET load. The Base64 PE/temp/subprocess cluster reports co-occurring
  clues without claiming that the subprocess launches that PE. The old
  `encrypted-dotnet-loader` composite was retired because it never required
  `Assembly.Load`, a decrypted assembly, or another payload activation sink.
  Its component findings remain. `crypto/cipher` is documented as the home
  for generic cipher API/name clues before an algorithm family is supported;
  the Cleave directory whitelist was updated alongside the taxonomy.
  Validator improvement: flag bytecode-scoped `text exact`/word-boundary
  API-name matchers for fixture review. Marshaled names can abut adjacent
  bytes and silently miss without changing the apparent API name.
- The BOF host file's seven `Beacon*` name observations, execution-status
  message and runtime cluster moved to `micro-behaviors/process/interpreter/bof`.
  Names formerly labeled “exports” now say “API name”, because their matchers
  search text rather than parsed exports. The generic `__imp_` clue moved to
  `micro-behaviors/os/linker/import-symbol`. Its old whole-word matcher could
  not match an actual `__imp_Resource` prefix; the new substring matcher does.
  The runtime cluster still needs four of the same nine observations. Its
  Tailscale consumers reference the renamed BOF API facts. A synthetic C
  source with three Beacon names and `__imp_Resource` now matches; the
  two-name counterexample does not.
- `loader/rust.yaml` was retired after matcher review. Its `client.get`
  atom searched a string literal rather than a Rust call; `.write(&body)`
  did not identify a file or a downloaded response. A separate spawn gave
  no source-to-sink link. None of the three rules had external consumers.
- The five `go-wasm-stealth.yaml` rules moved to neutral WASM-host,
  module-load and filename leaves. The old "random-named WASM payload"
  matcher saw only a quoted long lowercase filename; the old "silent catch"
  matcher allowed any catch handler. Their names and descriptions now state
  those observations. The composite still requires `new Go()`,
  `WebAssembly.instantiate`, an empty catch, and one long asset/sidecar name,
  but does not claim that named asset reaches `instantiate`. Synthetic
  JavaScript with a long `.wasm` name and an empty catch matches; the same
  host using `tree-sitter.wasm` does not. A long `require("./...js")` sidecar
  also exercises the alternative branch. The taxonomy now states when a
  WASM host becomes a linked staged-payload module load.
- The C# AES-stage source file moved its Common AppData path expression,
  `Assembly.Load(method())` call shape and `GetMethod` assignment to neutral
  path, module-load and reflection leaves. Its literal
  `File.WriteAllBytes(path, Convert.FromBase64String("TVqQ...` matcher actually
  describes a decoded PE write and now lives under `staging/encoded`.
  The composite remains a staging profile with its original three required
  legs, four alternatives and confidence; it no longer claims that AES
  decryption feeds `Assembly.Load`, because that relationship is not matched.
  DarkComet and .NET resource-loader consumers reference the new IDs.
  Synthetic C# with the PE write matches the staging profile; a same-file
  `Assembly.Load`, KDF and `GetMethod` control without the write does not.
- The Elex AutoIt UIMgrBroker rule is a family wrapper assembled from a
  distinctive path, compiled AutoIt context, self-install profile and
  network-capable wrapper. Its matcher has no staged-payload activation sink.
  It remains in the legacy loader leaf pending a supported, section-scoped
  family fingerprint: moving a broad path string into `well-known/malware`
  would require a justified section and size scope, and moving the dependent
  persistence composite there would otherwise break objective-tier
  dependencies. Do not invent those bounds to silence validation.
- The Dark Eye fake-UPX rule is a family wrapper fingerprint, not evidence
  that staged bytes reach an in-memory loader. Its project-path atom moved
  from generic provenance to `well-known/malware/trojan/dark-eye`, and its two
  PE section measurements moved to neutral `metadata/binary/section/size`.
  The family composite retains its nine required observations and all three
  alternatives. Sysbot's size-band composite now references that wrapper
  instead of repeating the two identical section predicates. The project
  path's 1.8 MB minimum follows from the two required section-size minima;
  no arbitrary maximum was introduced. A source-to-destination comparison
  verified the atomic matcher bodies and composite clause sets. This exposed
  a validator opportunity: flag identical `if` bodies even when inherited
  file-size guards differ, then identify the guards so one shared observation
  and consumer-level restrictions can replace the duplicates.
- Two `wsh-reconstruct` atoms matched the same bare `MSXML2.XML` text, with
  one guarded at 50 KB and the other unguarded. The matcher is now a single
  `micro-behaviors/os/com/automation` ProgID-prefix observation. The 50 KB
  restriction moved to its specific consumer; the other consumer remains
  unbounded. Neither atom actually proved token-array reconstruction or an
  HTTP client, because `MSXML2.XML` is only a prefix. The matcher itself,
  platform and file-type scope are retained.
- Four `loader` files need evidence-linked dispositions before any
  sink move. `dotnet-stage.yaml` can satisfy its ZIP "loader" with resource
  access, extraction and reflection namespace but no launch or module load;
  its admin-batch variant inherits that missing sink. `dotnet-bitmap.yaml`
  requires pixel access plus reflection, but does not connect extracted pixel
  bytes to the invoked method; its third rule supports encoded PE staging,
  not activation. `windows-resource-process-loader.yaml` requires resource
  APIs and `CreateProcessA` but not the resource's output path as the process
  target; its overlay variant does not require overlay decoding.
  `pyinstaller-stage.yaml` combines onefile/overlay, debugger and process
  clues without requiring a staged payload at a sink. Review their
  existing consumer and sample coverage, then route supported staging,
  reflection, process, and signing observations separately.
- `signed-anomalous.yaml` moved to
  `anti-static/obfuscation/binary-metrics/profile`. Its matcher requires signer
  evidence, an AssemblyResolve hook, multiple embedded PEs and manual API
  resolution, plus either a resource-carrier or AES clue. It does not establish
  certificate abuse or payload activation. The matcher clauses and exclusions
  are unchanged; the description now states the profile, criticality is
  suspicious, and the unsupported `T1553.002` mapping was removed.
- `zip-launcher.yaml` contained one `launcher.cpp` filename clue and three
  minizip/ZIP-in-data profiles. None required extraction or execution of the
  embedded ZIP, and two asserted a signature without any signer leg. The
  filename clue now lives in binary source provenance; the minizip plus
  ZIP-in-data profile lives with the recognized library identity; and the
  two packed/checksum profiles live in anti-static binary-metrics. The
  `masquerade-loader` consumer uses the new minizip ID. The atomic matcher,
  required/alternative clauses, thresholds, exclusions and downgrade were
  compared with the originals. Names and criticalities no longer claim a
  signed loader or staged-payload activation.
- The C# temporary-payload file required `WriteAllBytes`, a randomized temp
  path and a VB Shell call, but did not bind the written path to the Shell
  argument. That profile now lives in neutral `process/create/vb-shell` as a
  temp-write/Shell context. Its ping-delay variant now lives with
  anti-analysis timing, and the Poison Ivy family consumer uses that new ID.
  Required legs are preserved; the unsupported temp-payload execution claim
  and inherited execution mapping were removed.
- Two IEExec name/PDB atoms moved to binary provenance; their dominant-overlay
  profile moved to anti-static binary-metrics. Its Pinball/registry variant
  moved to overlay decoy masquerade. The same atomic matcher bodies and
  composite conditions remain, but the names no longer claim a downloaded
  or launched payload.
- The Delphi embedded-PE/dominant-overlay profile moved to `pack/overlay`;
  the tiny .NET byte-array-load profile moved to reflection obfuscation; the
  duplicate-RWX-resource/overlay/API-resolution profile moved to anti-static
  binary-metrics; and the Petite/VB6 memory-API profile moved under Petite
  packing. None required a staged payload reaching an activation sink. The
  NJRat and Phantomgate family consumers were updated. The Gentee runtime
  API/temp-DLL profile moved to neutral Gentee interpreter capability, while
  its Chrome-brand/dominant-overlay profile moved to Chrome version-resource
  masquerade. Required/alternative matcher clauses were compared after the
  moves. The `loader` leaf is now **exactly 100** rules; its remaining entries
  still require individual claim and sink review.
- The 7-Zip SFX bundle mixed config directives, a basename, overlay utilities
  and execution claims in `installer`. Its RunProgram observations now live
  under neutral installer process creation, the `Progress="no"` control under
  UI controls, and the `%TEMP%` extraction destination under archive extraction.
  Five retained atomic matchers preserve their matcher, count, size, explicit
  scope and confidence; twelve retained composites preserve their condition
  clauses after reference rewrites. The outer installer-themed basename was
  removed because it can be assigned by a collector and its only composite
  was a subset of the existing silent 7-Zip SFX profile. A large-overlay
  wrapper was replaced at its only consumer by the same canonical overlay
  observation. Two unused `component` unions of signer and installer markers
  were retired. The `installer` leaf falls **143 → 133**; its remaining rules
  still need sink and claim review.
- Five more `installer` profiles moved without changing matcher clauses: the
  oversized sparse Inno composite now describes binary code complexity; the
  ISAPI-capable opaque-content composite now describes packing rather than a
  deployed IIS extension; the managed MSI custom action profile now describes
  VM-aware context rather than a VM-gated child; and the two YingInstall
  overlay profiles now describe packing and accompanying API clues rather
  than a staged RAT. Their required/alternative clauses, thresholds,
  exclusions and confidence were compared with the originals.
- Five NSIS composites moved to their required capability or objective:
  elevated INetC/WinINet context to HTTP client capability, a dominant opaque
  overlay to packing, self-extraction plus process API to anti-static
  self-read, a self-issued security-product claim to certificate masquerade,
  and reboot plus clipboard APIs to shutdown context. The old “encrypted”,
  “payload reconstructed”, “dropper” and “loader” assertions exceeded the
  matcher evidence. All five retain their required/alternative clauses,
  thresholds, exclusions, effective file scope and confidence; consumers
  reference the new IDs. The `installer` leaf is now **123** rules. The
  remaining Inno/NSIS carrier profiles require a source-to-sink audit before
  any `dropper/file-exec/installer` destination is justified.
- Sixteen Inno/Delphi composites then moved from the carrier leaf: eight
  overlay profiles to `anti-static/pack/overlay`, the standard dbk export pair
  to binary symbols, PBKDF2/SafeArray context to neutral crypto, privilege
  context to token manipulation, two driver-claim profiles to vendor-brand
  masquerade, a NVIDIA version-resource claim to NVIDIA masquerade, a signed
  self-read profile to trust masquerade, and encrypted overlay/thread context
  to packing. All sixteen kept their condition clauses, thresholds, exclusions
  and confidence after reference rewrites. Unsupported staged-loader, RAT,
  process-injection and transfer claims were removed from names, descriptions,
  criticality and mappings. The Inno source still holds a driver-banner atom
  and three composites needing separate evidence review.
- Eight macOS installer atoms moved to their actual observations: a `.pkg`
  filename reference, installer root target, two HTTP endpoint URLs, a
  background osascript shell command, a package hook path, and two curl/bash
  command forms. Their matchers, filters, exclusions, confidence and effective
  file scope were compared with the originals; the thirteen remaining macOS
  composites kept their condition clauses. Generic endpoint strings no longer
  claim C2, and a Scripts path no longer claims preinstall execution.
  `installer` is now **99 rules**; its remaining composites still need
  individual activation-sink review.
- The WSH leaf fell **106 → 99** after routing a bare machine/user field pair
  to format-neutral host-profile data, a POST plus those fields to
  system-information exfiltration, a self-deleting hidden EncodedCommand
  relay to self-deletion, a self-read/write/hidden-run combination to
  anti-static self-read, and ActiveX/MSI plus VBA split-dispatch profiles to
  string fragmentation. A response-body/file-save method co-occurrence moved
  to the WSH interpreter leaf; it does not bind the response bytes to the
  saved file. The atom's matcher and six composites' condition clauses,
  exclusions and effective scopes were compared with the originals. The
  remaining WSH rules still need individual source-to-sink review.
- The `batch` leaf fell **127 → 100** by moving 27 atomic observations to
  HTTP transfer and WebClient, script evaluation, process creation and
  respawn, timing, temporary paths, file rename/copy/delete, RAR extraction
  and WebDAV current-directory capabilities. A bare `DownloadFile` name and
  curl/wget near TEMP no longer assert a completed download to that path;
  the Python `requests.get` → Base64 decode → `exec` and PowerShell
  `irm | iex` matchers retain their linked script-evaluation sink. Every
  moved atom kept its matcher, guard, confidence and effective scope; all
  50 retained batch composites kept their condition clauses, thresholds and
  scopes after reference rewrites. The remaining batch rules still need
  individual claim and sink review even though the leaf is within cap.
- Eleven `fileless` rules moved by their required sink or capability. Two
  IRM/HTTPS URL atoms moved to neutral HTTP download evidence and their four
  IRM/IEX composites to `dropper/script-eval`. A Perl Base64 decoder moved to
  neutral decoding; its Base64/Python-inline/fork combination moved to
  process-create context because it did not link decoded bytes to the Python
  command. Two Swift URLSession/stdin observations and their composite moved
  to neutral shell-pipeline context for the same missing source-to-stdin link.
  All eleven retained their matcher or composite clauses, thresholds,
  exclusions and effective scopes. `fileless` is now **99 rules**, and the
  remaining rules still require individual sink review.
- The `reentrancy-guard` atom matches a Node interpreter spawn with a cloned
  environment; it does not require a guard value or guard check. Its composite
  permits a file-download handler, chmod, **or a URL clue**, so it cannot claim
  that a fetched payload reaches the spawned child. Both rules now live in
  neutral `process/lifecycle/respawn` with evidence-limited descriptions and
  no unsupported execution-guardrail or payload-transfer mapping. Their
  matcher bodies, proximity, exclusions and alternatives are unchanged.
- The `date-evasion::nemucod-dropper` composite required string obfuscation,
  a date check and an MZ-header array check, but no download or activation.
  Its one consumer, `nemucod-full-chain`, now requires those same three legs
  directly; the unsupported standalone dropper verdict was retired. The
  `date-evasion` legacy child is empty.
- The `integrity` leaf's seven atoms were SHA-256 manifest fields and Node
  helper names; its two composites required SHA-256 digest/hash variables or
  runtime download/install/validation helper names. Neither required a
  malicious payload or activation sink. The hash atom and composite moved to
  `crypto/hash/digest`, and six helper atoms plus their cluster moved to
  `os/package-manager/runtime-install`. The SHA-256 composite now states
  co-occurring expected-hash context, since it does not compare hashes; the
  runtime cluster now states helper **names**, since it does not call or order
  them. Matcher bodies, proximity and scope are preserved. Two
  `stealth-spawn` suppressors formerly pointed at the entire `integrity/`
  directory, so any single hash or helper-name atom could suppress a dropper
  verdict. They now point only to the complete runtime-install helper-name
  cluster. The legacy child is empty.
- The `misextension` leaf was scoped to PNG/text input but did not test an
  extension mismatch or execute a staged file. Its four text matchers moved
  to COM automation, Base64 decode, WebClient client and WebClient download
  capability leaves with the same matcher bodies and input scope. The
  composite now reports a PNG/text carrier with WebClient/decode clues; it
  remains a conjunction of the same four observations but is no longer a
  hostile dropper verdict. The `impact/degrade` consumer of `WScript.Shell`
  text now references the neutral atom. The old child is empty.
- `jvm-relaunch` required a self-JAR path and Java process-launch clues in
  three supported profiles, but no acquired payload or stage-to-sink link.
  Those profiles now live in neutral `process/lifecycle/respawn`, and their
  game-mod and archive-loader consumers reference the new IDs. The fourth
  composite inferred staged-code handoff from a `stageWithContext` method
  name plus a decoder descriptor; neither proves a handoff. That verdict and
  its unshared method-name atom were retired. Match conditions on the three
  retained composites are unchanged; criticalities now describe a relaunch
  capability rather than a hostile dropper.
- The two `source/go-powershell` composites require a Go process-create clue,
  a PowerShell download-to-file literal, a hidden argv flag, and a
  `Start-Process` **of PowerShell itself**. The certutil variant also requires
  a PS1 decode command; neither rule connects the downloaded file or decoded
  PS1 to that launch. Both moved to neutral hidden-process context with
  descriptions limited to their co-occurring download/decode clues. Their
  `all` matcher legs and benign-test exclusion were preserved, and the
  original first-rule exclusion still selects the richer variant. The
  language-specific `source` child is empty.
- The two native `dns-txt` composites join a TXT lookup with file-write,
  detached process and, in one variant, LaunchAgent clues. Neither binds TXT
  response bytes to the written or executed path. They moved to neutral
  `communications/dns/txt` context with their original required legs and
  scope; the unsupported payload-write/install verdicts were removed. The
  remaining Node import-time rule still depends on a preexisting DNS-stage
  objective whose own source-to-file-to-spawn relationship needs audit.
- `lua-sidecar` combined LuaJIT FFI declarations, Lua DLL name text and an
  executable-file argument. Those observations did not show that a sidecar
  file existed, was loaded, or was executed. The three FFI rules moved to
  neutral `dylib/load/ffi`; the Lua runtime name and two context composites
  moved to `process/interpreter/lua`. Atomic matchers and the original FFI
  profile's required/alternative/proximity conditions are unchanged; names
  and criticalities now state the supported context. The legacy child is
  empty.
- `launcher/javascript.yaml` needed two of a cmd-start clue, terminal-launch
  clue, or osascript terminal reference. It required no acquisition or staged
  payload, so its complete matcher moved to neutral
  `process/create/shell/bridge` as a terminal-launch clue cluster. The
  desktop-entry launcher rules remain for separate sink and persistence
  review.
- The seven-rule desktop-entry `launcher` leaf is empty. Its `wget -O /tmp`
  and chmod/pipe command-text atoms moved to HTTP CLI download and process
  launch capabilities with identical matcher bodies, confidence and effective
  scope. Two composites requiring XDG autostart moved to login persistence;
  two requiring a document guise moved to document masquerade. Their required
  and alternative clauses and confidence are preserved, while criticality
  and descriptions no longer assert an unbound downloaded-payload handoff.
  `weaponized-launcher` was retired: it added only Type/Exec/Terminal metadata
  and a non-autostart exclusion to the existing desktop delivery finding,
  without a distinct activation mechanism. No external consumer referenced
  any of the seven old IDs. The underlying desktop delivery rule remains a
  separate sink review item.
- `chm-lolbin` has three direct command-pattern atoms and two composites.
  The `curl`-to-`hh -decompile` matcher supports CHM acquisition/extraction;
  the `hh -decompile`-then-LNK matcher supports a command chain but does not
  compare the decompiled output path with the launched LNK. The composite
  combining those atoms should not claim a complete downloaded-CHM-to-LNK
  payload chain until the path relationship is checked. The separate HTML
  Help Shortcut composite already depends on `delivery/chm` and extraction;
  compare its required sink with that delivery sibling before moving it.
- `platform-branch` mixes three hash-prefix gate atoms, cross-platform branch
  composites, shell/file-exec clues, self-delete, npm install-hook context and
  source decoding. Platform branching is a condition shared by those
  techniques, not a dropper subtechnique. Route each composite by its required
  sink or other objective; specifically, `platform-branched-dropper` currently
  requires a download directory and a process-create alternative but does not
  bind the fetched bytes to that process, while
  `hash-gated-second-stage-download-execute` joins HTTPS GET and execFile
  without a source-to-target relation. These names overstate their matchers.
- `kontuke` mixes a generic PowerShell character-array eval wrapper with
  headless conhost, curl, tar and rundll32 commands, plus Endpoint DLP names
  and a PE-family profile. The first wrapper's regex contains no
  family-specific literal, so its `Kontuke-specific` description is too
  strong. The conhost/curl/tar/rundll32 chain supports a staged-file launch;
  the Endpoint DLP profile belongs in family identity only if its DLL/export
  pair is sufficiently distinctive. Split the generic command techniques
  from the family identity instead of retaining a `kontuke` dropper child.
- `nezha-dropper` requires Axios, a write stream, chmod, detached background
  command and one Nezha/domain clue, but no relation connecting response
  bytes to the stream or written path to the spawned command. Its two variants
  add npm masquerade or unlink evidence without repairing that link. Keep the
  named Nezha artifact under `well-known/app/system/nezha`; a canonical
  dropper rule needs the missing source-to-file-to-launch evidence.
- `persistence` contains one stronger downloaded-file execution plus autorun
  profile and seven weaker combinations of URL, BITS, Startup keywords,
  scheduled-task creation, tunnel and rundll32 clues. The latter do not all
  prove durable registration or link the downloaded content to a launched
  target. Route proven durable activation to `objectives/persistence` by the
  trigger, and file execution to its dropper sink only when the staged path is
  linked to launch; retire mere URL-plus-keyword verdicts after retaining
  their neutral observations.
- `loader/vb6-binary.yaml` began as a 33-composite cross-product, not 33
  loader mechanisms. Twenty rules have moved: hosts redirection to its
  channel leaf; two overlay-stub profiles to staging; two URLMon contexts
  to the HTTP client; shell, file-write, Run-key, key-poll, watchdog and
  ShellExecute conjunctions to their neutral capabilities; numbered-identifier
  file-write and shell contexts to string junking; and two cmd.exe `/c` clues to command
  execution. Required matcher legs and exclusions were preserved, apart from
  local IDs updated to their new homes. A source-to-destination comparison
  confirmed the same `all`, `any`, `needs`, and `unless` clauses for the first 19;
  the twentieth kept its two required legs and exclusions.
  The old dropper descriptions had
  claimed writes, downloads, or launches that those legs did not link.
  Thirteen rules remain in the file. The embedded-PE shell cluster lacks
  evidence that the embedded PE is used as a stage and needs more than a
  rename. The URLMon/hollowing cluster belongs with process hollowing if
  its required injection leg proves transfer; the two IE-name rules follow
  process-name masquerade; and the nine obfuscated/concealed API-context
  rules follow their actual import-concealment mechanism. Those destination
  leaves already exceed the cap. Audit their existing siblings and partition
  them by mechanism before completing these moves; do not create a VB6 child
  merely to hide the overflow.
- The broad `Net::HTTP` method observation and the specific
  `Net::HTTP.get_response` observation can both match one call. They express
  nested breadth in the same neutral leaf; review their consumer roles before
  suppressing the broader finding. An overlap advisory that distinguishes
  broad/specific matchers from identical bodies would help here.
- `rename-exec` had no rule that linked a renamed staged path to the launched
  command. Two one-use union composites were inlined into their consumers,
  preserving those conditions. Five composites moved to
  `execution/interpreter/command` or the extconf build-hook leaf with
  descriptions limited to rename, HTTP and command clues. The sixth,
  `extconf-fragmented-download`, was retired: an extconf filename plus any
  `Net::HTTP` method did not establish fragmentation or a download, and its
  component findings remain. The leaf is now empty.
- The Rubygems `extconf-dropper` and Alpine apk wrapper followed their
  command-execution result; three more Rubygems rename-and-exec variants were
  likewise moved out of the install-hook trigger branch. An extconf Ruby
  fixture matches the relocated rules. A synthetic Alpine apk with `.PKGINFO`
  and that extconf script matches the package-context rule; a package with a
  plain non-executable rename does not. None of these descriptions claims the
  renamed file is the command target.
- `script/xmlhttp::ps-xmlhttp-downloader` and
  `xmlhttp::ps-xmlhttp-downloader` have identical local composite clauses but
  resolve `xmlhttp-clsid-any` to different local definitions. Both use
  response-text and IEX as separate co-occurring legs; neither directly
  connects the response bytes to IEX. A validator comparison must resolve
  local IDs before calling these identical, and both objective claims need
  relation review.
- `exec-download` is **115 → 96**. Six rules claiming a downloader were
  reclassified by their required evidence: a Ruby extconf with IP-tracker
  clues, two WebClient/ScriptBlock or scheduled-task profiles, two obfuscated
  Node profiles, and a WebSocket control/file-transfer profile. Their
  matcher clauses remain intact; unsupported download, payload-activation
  and supply-chain claims were removed from descriptions and mappings. Ten
  HTA-file atoms moved to their actual string-fragmentation, WSH process,
  stream-write/read, gzip, batch-run, COM, shortcut or eval subjects. Their
  matchers and effective scopes were retained, and composite references now
  point to the new homes. The `ruby-extconf-ip-tracker-clues` rule lists the
  existing tracker clues explicitly because a directory reference from the
  same directory would recursively include the rule itself. The Kynix
  `download_wininet` and `execute_stealth` helper-name observations moved to
  their neutral WinInet and process homes; their unconsumed full-chain
  composite was retired because names plus anti-analysis clues do not link
  downloaded bytes to execution. The family signature keeps referencing the
  two neutral observations.
- `script` is **126 → 40**. Ruby string literals naming `uri`, `resolv`,
  `open-uri` and `pty`, plus their unused import rollups, were retired:
  neither a bare literal nor an `any:` of such literals proves a `require`.
  A commented chmod example was also retired as non-executable evidence.
  Six Ruby capability atoms moved to their write, archive, build, HTTP,
  process and named-tool homes; WScript execution and a benign HTML-preview
  exception moved to their process homes. The TCP socket/shell profile moved
  to `backdoor/shell/reverse` with a description limited to its actual
  co-occurrence. Its `TCPSocket` clue was corrected from socket listening to
  connection; `UDPSocket` moved to the UDP subject. The one-use XMLHTTP CLSID
  union was inlined into its PowerShell consumer, preserving its Boolean
  condition without a redundant separate finding. The MSI pass merged an
  identical `New-ScheduledTaskAction` matcher with its neutral capability,
  widened that rule to MSI/OLE scope, and moved Run-key references and task
  registration to registry and scheduled-task capabilities. MSI PowerShell
  command clues and launch profiles moved to installer process creation.
  Three unconsumed MSI/dropper composites that required only a Run-key path,
  task-action API or process-hunter clue were retired; none established a
  persistent write or linked payload stage.
- The MSHTA pass routes remote host invocation profiles to
  `execution/interpreter/script/mshta`, two encoded fragments and their pair
  to string encoding, and the npm preinstall profile to the install-hook
  remote-fetch subject. A remote MSHTA command does not by itself establish
  a separately staged dropper payload. The JavaScript, Python and batch
  co-occurrence profiles were reduced to `suspicious` where the matcher did
  not link a download or decoded buffer to the invoked process.
- The VBS/Excel file had no staged payload activation: its four observations
  and workbook-open profile now report Excel COM automation and a quoted
  XLSM path. A second unsupported document-delivery verdict was retired.
  Kotlin marker/compile-run/hex-descriptor observations moved to format,
  process-build and decoder subjects; an unlinked FTP/hex-payload verdict
  was retired. C# PowerShell command strings, a generic `Upload` call and a
  batch percent-variable literal moved to their neutral subjects; their two
  profiles now describe co-occurring command clues rather than uploading a
  stager. The Panos Ruby shell call, fragment assembly and composite moved
  to process and data capabilities. JScript structural and Syriac/ActiveX
  profiles moved to anti-static obfuscation because neither requires a staged
  payload sink.

Four more unconsumed Ruby verdicts were retired after claim review:
`ruby-obfuscated-c2` needed any three of generic Base64/DNS/HTTP clues,
`ruby-ast-obfuscated-c2` needed only Base64 and DNS, and two generic
download/write/execute rollups did not require a staged-to-activation link.
Their neutral component observations remain.

The `script` leaf has **3 rules** after an evidence-bound review. Six Python
atoms moved to their direct HTTP, chmod, pipeline and eval capabilities; eight
unlinked Python profiles moved to the required capability leaves. The `curl … |
bash` literal kept the interpreter-stdin claim; a redundant stricter Python
composite was retired. The AppData/startfile profile now sits beside its
required GitHub write/startfile rule under `dropper/download`; it is suspicious
because no matcher binds the AppData path to the launched argument.

The nine JScript profiles now follow their required WSH, rundll32, ActiveX,
rename/engine or string-encoding evidence. The rundll32 profile no longer
accepts obfuscation alone in place of a write clue. Seven batch Unicode/JS
rules now follow ComSpec invocation, script encoding/eval, batch file call or
COM GetObject evidence. The duplicate PowerShell XMLHTTP rule was retired after
inlining its three CLSID alternatives in the sibling rule; that sibling still
asserts only co-occurring response-text and IEX clues. Two Ruby composites
moved to Open3 process creation and binary file writing
capabilities. Their required clauses, exclusions, proximity and confidence
were preserved; names, descriptions and hostile verdicts were corrected to
stop claiming an unbound response is launched. The third Ruby Windows rename
profile was a strict subset of the existing
`objectives/execution/interpreter/command::ruby-image-rename-with-exec` rule:
the latter already accepts the same Windows check plus image-to-EXE rename
and Ruby exec. The redundant profile was retired; the sibling verdict is now
`suspicious` because it does not bind the renamed path to the command.
The `Open3.capture3` atom and its HTTP-body proximity profile now live under
`process/create/subprocess`: the matcher names a subprocess API, not a shell
parser. This also removes an otherwise misleading `shell/lang` sibling home.
This subset escaped the identical-matcher check because one rule was a
composite with an extra Windows gate in another directory. A validator review
could report candidate cross-directory composite containment after resolving
local IDs and effective scopes. Treat it as a review warning: exclusions,
thresholds and proximity can make apparent supersets behave differently.

The remaining three rules in `script/ruby.yaml` are a recognized-benign
suppressor, an HTTP-client/message union, and
`ruby-http-write-process-cluster`. The latter has an exact-ID consumer in
`staging/temp/ruby-unix.yaml`, but it does not require a temporary path or bind
the HTTP response, write target and launched argument. Its component and
exception rules cannot be rehomed by language alone. The next pass should
inspect representative Ruby samples and either require a matched path/data
handoff or retire this cluster and recompose its consumer from canonical
capabilities. Until then, the source remains an explicit unresolved audit
item, not a recommended destination for new rules.

The three rules in `execution/macro` had no acquired or staged payload. The
junk-decoder/hidden-Run profile moved to the WSH interpreter leaf; the two
auto-open/CreateProcess profiles moved to the document-trigger leaf. Their
required matcher legs were preserved, while names and verdicts now describe
the observed co-occurrence rather than asserting a downloaded command or
hidden payload. The empty macro child was removed.

The four `api-hash-loader` composites have no staged payload or load sink.
They now share the existing `anti-static/obfuscation/native-api-hash` subject
with the DJB2 hash profile. The small-DLL predicates, local dependencies,
suppression, confidence and size limits were preserved. A sparse string table
and API-hash resolver cannot establish PlugX identity or DLL sideloading, so
those names and hostile verdicts were removed. The empty `api-hash-loader`
child was removed. Its closest sibling, `dotnet-obfuscated-loaders`, still has
four rules requiring separate review: each combines resource/entropy,
reflection or network clues with write/process APIs, but the current
conditions do not bind the concealed or fetched bytes to the child launch.
Their IDs, descriptions and criticality now state co-occurrence rather than
a completed loader handoff; unsupported execution and transfer mappings were
removed. They remain in the legacy audit source until a supported primary
technique can be selected for each profile.

The two `embedded-pe` rules also lacked an embedded-payload write or launch.
Its API-name comparison matcher moved to manual API resolution; the composite
requires an OEP-restoration byte pattern, PE-header scan and those API-name
comparisons, so it now lives with binary infection/rewrite profiles. Matcher
bodies, exclusions, scope and confidence were preserved. The description and
ATT&CK mapping no longer assert an embedded PE drop or user execution. The
empty `embedded-pe` child was removed.

The five `winexec` composites did not require a copied file to be the
WinExec argument. The rule with multi-vendor EDR targets and Run-key/copy
clues moved to `impact/degrade/edr/targeting`; its `needs: 2` alternatives
can be satisfied by registry writes without process termination, so it no
longer claims to kill security processes. An unsigned single-export WinExec
profile moved to process execution. Three LSP enumeration/path/connect
profiles moved beside their LSP capability, with WinExec as supporting
context. Required clauses, exclusions, confidence and scope stayed intact;
unsupported download and execution mappings were removed. The empty
`winexec` child was removed.

The five `chm-lolbin` rules were not one linked download-to-LNK chain.
The HTML Help composite only added a decompile clue to the existing
`delivery/chm::htmlhelp-shortcut-process-dropper` rule, so that redundant
stricter finding was retired. The headless conhost/curl observation moved to
hidden process creation; curl-output near `hh -decompile` moved to CHM
extraction; and decompile followed by a LNK launch moved to the LNK execution
subject. Their three-part profile now reports those clues as co-occurrence,
without asserting that the fetched CHM supplied the launched LNK. The
atomic matcher bodies, scopes and confidence were preserved, and the empty
`chm-lolbin` child was removed.

`vbscript-watchdog` had four neutral observations and two unlinked hostile
composites, with no acquired payload. Its AppData `WshShell.Run` call now
follows direct process creation, the two executable-name references follow
executable paths, and its repeated `WScript.Sleep` follows sleep intervals.
The first composite keeps its WMI survey, Run, sleep and optional name clues
as a notable process-supervision profile. The second was retired: it required
only a hash-shaped EXE name, sleep loop, WMI enumeration and a
`WScript.Shell` literal, without a Run call or a link to that EXE. No external
consumer referenced it. Atomic matcher bodies, scopes and confidence were
preserved. The empty legacy child is removed. The two existing
`process/create/shell/{wsh,script-host}` leaves still overlap; the process
creation contract now distinguishes direct WSH Run, explicit shell handoff,
COM-object references and host executable names for their later migration.

The five `decrypt-exec` composites failed that source-to-sink test and left
that legacy child. The MFC profile has an encoded resource and a concrete
transformed-stack-buffer call, but no resource-to-buffer link; it now follows
encoded-payload obfuscation at `suspicious`. The Node rule joins AES, write
and detached-spawn APIs within 80 lines without a common value or path; it
now describes that context under process spawn at `suspicious`. The PyC rule
required only an embedded blob, a cipher-module reference, `tempfile` and a
subprocess-module reference; it now follows encoded-data evidence at
`notable`. The user-folder rule accepted a char-code helper instead of a
Function-constructor sink, so its path/XOR/eval-context observation moved to
custom decoding at `suspicious`. The Zig rule paired an XOR operator and byte
array with shell/Child.init references without passing the decoded command;
it now follows shell process creation at `suspicious`. All five retained their
conditions, effective scopes and confidence, and none had external exact
consumers. Unsupported dropper execution mappings and descriptions were
removed. A sample-backed chain can later add a linked objective rule at the
proper sink.

The seven `scriptengine` rules likewise did not form a single loader
subtechnique. A bare `LinkageError`/`StackTraceElement` text matcher now lives
with neutral stack-debug evidence; it no longer claims to decode a string.
The Java resource-plus-ScriptEngine profile requires no stream-to-eval dataflow
and now reports eval context at `suspicious`. Three further Java composites
require an obfuscated class name with an eval, resource-access, or engine-setup
clue; they now follow class-name obfuscation at `suspicious`. The two WSH
GetObject profiles require a variable moniker plus split URL fragments, or a
literal `script:` URL plus a GetObject shape. Their alternatives do not bind
the reconstructed URL to the call, and a direct URL-moniker GetObject already
has its own neutral atom. The split-scheme profile now follows string fragmentation, and the
literal-URL profile follows neutral WSH moniker context, both at
`suspicious`.
All seven kept their required and alternative clauses, effective scopes and
confidence; no exact external consumers depended on them. The legacy
`scriptengine` child is empty.

The three PowerShell `xmlhttp` composites also left their carrier leaf.
The XMLHTTP response-text plus IEX profile does not require the response to
be passed into IEX, so it now follows interpreter eval as a `suspicious`
context signal. The ADODB rule does require a response-body stream write,
but does not bind the saved file to `Start-Process`; it now follows stream
writing at `suspicious`. The WinHTTP rule requires request/response handling
and `Start-Process` but no response-to-command handoff; it now follows
process creation at `suspicious`. Their required and alternative conditions,
effective scopes and confidence remain; no exact external consumers depended
on their old IDs. The legacy `xmlhttp` child is empty.

The four `dotnet-obfuscated-loaders` profiles have distinct required
subjects and no staged-byte-to-child link. The reflection/dense-region/write
profile moved to reflection-invoke obfuscation; the NetworkStream/dense-region
hidden-child profile moved to neutral hidden process creation. Two AES
resource-stage profiles moved to resource staging because their required
resource-stage leg is supported, while Pastebin, DownloadString or a hidden
child are unlinked context. All four retain their clauses, effective scopes
and confidence; no external exact consumers referenced them. The legacy
`dotnet-obfuscated-loaders` child is empty.

The four `html` rules left their carrier leaf after tracing two shared WSH
atoms. The object-tag EXE `codebase` matcher is an HTML-format reference,
not an observed load. A bare `ADODB.Stream` ProgID in HTML now follows COM
automation, and a UNC EXE string follows executable-path evidence; these two
atoms also had WSH, CHM, HTA and webshell consumers, which now use the neutral
IDs. Their matcher bodies, exclusions, confidence and effective scopes were
preserved. The three HTML composites retain their required clauses but now
report stream-write, UNC-path or object-codebase context at `suspicious`,
`notable` and `suspicious` respectively. None requires the HTTP response to
be written at the named path or the saved file to be the `codebase` target.
The legacy `html` child is empty.

The six `ide-extension` composites now follow editor-extension persistence.
Every rule requires the editor CLI to install an extension; download,
obfuscation and editor-fork enumeration are context for that durable result.
The native GitHub-release profile and the HTTP/write/force-install and fork-
sweep profiles now report `suspicious` installation clues. The two profiles
that additionally require obfuscated download/install chains retain `hostile`
criticality. All six kept their `all`/`any`/`unless` clauses, confidence and
effective scope. The trojanized-application consumer now references the new
editor-extension home. A fetched VSIX path is not always bound to the CLI
argument, so the old dropper descriptions were narrowed. The legacy
`ide-extension` child is empty.

The eleven-rule `staging` leaf is empty. Three EXE/DLL/data path atoms
moved to temp-path evidence; a batch `if not exist` atom moved to path checks;
a bare Temp batch-command atom moved to shell process creation. The curl
`-o ProgramData` atom and its three-clue composite moved to curl download
context. Two WebClient composites now describe HTTP method, temp-path,
delete/shell or paired EXE/data-path context. Two rundll32 composites now
follow that named execution mechanism. The original matcher bodies, clauses,
confidence and effective scopes were retained; the two batch consumers of
the Temp-script atom use its new neutral ID. The ProgramData curl output and
Temp script command are different paths, so their composite no longer claims
a single downloaded-and-executed batch stage. No other external consumer
referenced the old staging IDs.

The seven `binary-native` composites also need value/path review rather than
a carrier-based home. Their shell and Node conditions combine network fetch,
chmod, detached launch and sometimes postinstall or cleanup, which is a
strong suspicious cluster. The YAML clauses mostly require these APIs or
commands to coexist; they do not equate the fetch output, chmod target and
launched path. In particular, the npm postinstall/configurable-release
profile has no required response-to-file write, and a self-respawn
alternative in the Node stealth rule need not launch a downloaded binary.
Keep the corroborating facts, but move a full-chain verdict to
`dropper/file-exec/<mechanism>` only after its actual path handoff is
established. A verified install-hook trigger remains a referenced fact,
not a second dropper taxonomy branch.

Four `native` rules moved by required evidence. The C/C++ temp-write,
`LoadLibrary` and export-lookup profile now follows dynamic library loading;
it did not bind the written path to the loaded module. On macOS, curl plus a
temp path and task/shell launch now follows process creation, while `spctl`
assessment with codesign/MIME clues follows neutral Gatekeeper assessment.
The curl plus quarantine-removal composite now follows the required evasion
action; it no longer claims downloaded-payload execution. The same matcher
clauses, effective scopes and confidence were retained. The archive
fetch/extract/chmod/detached-launch cluster also moved to
neutral process detachment, and an encrypted temp-script plus hidden
policy-bypassed PowerShell profile moved to hidden-window evasion. Both keep
their clauses and effective scopes without claiming a staged-script handoff.
Three native rules remain for source-to-sink review: a Go `PayloadContainer`
name with Zstd, write and exec APIs, and a memory-loader profile beside
WinHTTP and shell calls. Neither establishes its full claimed payload path.

The C/C++ library-load profile had two exact consumers in a modular RAT sibling.
That sibling required only library-load, a pipe-delimited string, socket
connect, a 32-byte array, and optional VM checks; it did not establish command
dispatch, encrypted transport or an operator access surface. The socket/string
cluster now lives under neutral socket connection, its module-plus-socket
profile under dynamic loading, and the VM-check alternative was split between
process-based and CPUID-vendor VM detection. The split preserves the old
alternative logic while dropping unsupported hostile RAT verdicts. No external
consumer referenced the sibling's four old IDs.

The eight-rule `persistence` child is down to one unresolved Node profile.
BitsAdmin plus the word `Startup`, an HTTP IP URL plus a WSH object name, and
an HTTP IP URL plus the word `Startup` did not establish a persistence write
or a linked payload, so those three unconsumed verdicts were retired. A
`schtasks /create` profile moved to scheduled-task CLI persistence; two
Startup-script writes with Cloudflare/IWR/curl clues moved to Startup-folder
persistence. The latter's `any:` can be satisfied by another Startup-write
clue without curl, so its name and description no longer claim a curl
dropper. Cloudflare-tunnel and rundll32 co-occurrence moved to rundll32
execution without a download claim. All four moved rules retain their
required/alternative clauses, exclusions, effective scope and confidence;
supported persistence/rundll32 ATT&CK mappings remain. The Node profile
retains its exact consumer in Defender masquerade, but neither its temp-file
launch nor its autorun alternative is path-bound to the HTTP write. It now
reports that co-occurrence as `suspicious` pending a mechanism-specific split.

That Defender consumer also exposed three bare names stored as objective
atoms. Two executable-name literals moved to
`micro-behaviors/fs/path/application/executable`, and the bare Defender
product name moved to `micro-behaviors/os/security/product`; matcher bodies,
effective scopes and confidence were retained. The Defender composites stay
with fabricated identity but now describe name, copy, HTTP-write and launch
co-occurrence at `notable`, without claiming a proven System32 install or
downloaded-payload handoff. Their LuaJIT and Bundlore consumers use the new
neutral IDs. Bundlore's two-product-name rollup likewise no longer claims
AV targeting. These are accuracy corrections to a sibling, not additional
dropper rules removed from the branch count.

The one-rule `execution/dns-txt` child is empty. Its import-time composite
required the `dns/tunneling::node-dns-txt-binary-stage` profile, but that
profile only joined indexed TXT decoding, file write, chmod and detached
spawn within 8,192 bytes. It did not bind decoded bytes to the written file
or that file to the launched path, and it did not establish a DNS command
channel. The shared stage profile now follows neutral DNS TXT evidence; the
import-time refinement follows neutral module-execution timing. Both retain
their clauses, proximity, confidence and effective scopes, with `suspicious`
criticality and descriptions limited to the supported co-occurrence. No other
consumer referenced the old TXT-stage ID.

The `nezha-dropper` leaf also remains under sink review. Its base rule requires
Axios and stream-write capabilities, executable chmod, a detached shell
command, and Nezha identity or endpoint clues; it does not bind an HTTP
response to the written file or the chmod/command target. The npm-named
follow-ons add a literal write path, then a matching launch path plus unlink,
but lack a proximity or response-to-write relation. All three now report
deployment co-occurrence as `suspicious` without unsupported transfer or
execution mappings. The Eooce family rule references the renamed base
profile. A matched sample must establish the missing handoff before these
profiles move to `dropper/file-exec`; until then the legacy leaf is an audit
source, not a placement precedent.

The `execute-download` leaf is now empty after individual review of its last
fifteen rules. A million-iteration loop beside `chrome.runtime.connect` indicates
extension-port resource exhaustion, and its loop bound is a neutral
control-flow clue. Two clipboard-write profiles beside curl-to-zsh or IEX
commands now describe execution lures; the matcher does not bind clipboard
contents to the command. The direct `exec(urlopen(...).read())` Python atom and
its contextual composite follow `dropper/script-eval`, because the response
reaches the evaluation sink in the atom. Two Python HTTP/write/exec and
HTTP/temp/chmod/subprocess profiles moved to neutral file-write and executable
permission leaves because no response or file path is bound to their sinks.
Two HTTP/memfd and HTTP/execve profiles likewise report their supported
co-occurrence, not a fetched binary reaching a process. The five rules in
`python-remote-source.yaml` were the final leaf members: URL read near a
script-path write follows neutral HTTP download/write; importlib near that
profile follows neutral module load; response-write near a variable-path
interpreter and urllib/write/chmod/process clues follow neutral process
creation. Their clause sets, confidence, proximity and effective scopes were
compared to the old rules. The unsupported download-to-activation descriptions
and criticality were corrected.

The consumer audit followed these moved Python profiles into adjacent
supply-chain leaves. An agent-skill archive composite now states the observed
response-write and variable-interpreter context under package metadata.
A request-wrapper atom moved to neutral HTTP-client evidence, and its
write/chmod/launch composite to neutral process creation. A decoded-exec
consumer now follows its actual obfuscated-evaluation objective while
describing HTTP response writing as context. The PyPI metadata-plus-write
consumer now reports a neutral package response-write profile. These
consumers no longer claim that the response was executed, that the package
install triggered execution, or that the payload was hidden without evidence.
No rule refers to the retired `execute-download` IDs; validation reports no
new broken references from these moves.
The executable-chmod profile stays outside the subprocess leaf because its
directory-wide subprocess reference would otherwise include itself, making
the composite recursive and unreachable.

The adjacent `download` leaf is also empty after review of its sixteen rules.
Two Office macro profiles moved by their actual shell and `mshta` actions;
three document profiles moved by auto-open or curl download evidence. None
established that a saved file reached the invoked command. Perl hidden-HOME
path and encoded chmod atoms moved to neutral path and executable-permission
leaves; their LWP/write composite follows neutral HTTP download/write because
it never requires launch. A Python Discord executable URL plus setup fetch and
an unbound subprocess call follows the supply-chain install-hook remote-binary
context at `suspicious`.

Four Windows Ruby rules now describe NetHTTP/temp-EXE context, response-body
writing, HTTP/write/spawn co-occurrence, and temp-EXE write context. The
GitHub REST releases atom was consolidated into the existing neutral endpoint
matcher by adding Ruby to its file scope; its canonical exclusions now apply.
The Ruby XMRig/pool composite follows miner runtime evidence, with fetch,
extract and local exec recorded as context rather than a linked dropped miner.
Its hidden RubyGems consumer and the Windows extconf consumer use the new
IDs and accurate descriptions. The source-to-destination comparison covered
all sixteen atomic matchers or composite clauses, confidence, proximity and
effective scopes. The consolidated GitHub matcher retains its `if` body and
adds the canonical exclusions. Validation reports the same 21 pre-existing
broken references, with none to the emptied leaf.
The adjacent miner audit found seven XMRig and SilentXMRMiner command-line
argument rules under `miner/runtime`; those define configuration, so their
file moved intact to `miner/config` and the masquerade consumer was updated.
This reduces the already-over-cap runtime leaf from 104 to 97 without a
language partition or cap exception. TAXONOMY.md now distinguishes miner
configuration from runtime and pool evidence.

The first `exec-download` cohort moved nine rules. BAT's minimized PowerShell
launch and VBScript's bypass/hidden flags follow neutral process creation.
`ScriptBlock::Create` near `Invoke-WebRequest` follows interpreter compilation:
the regex does not pass the HTTP response into the ScriptBlock call. CMD curl
near a PowerShell `-File` invocation follows shell command context without a
matched output-to-argument path. The batch TEMP curl plus script-call profile
is bounded to eight lines but likewise does not require the same file path.
Two hidden PowerShell/EXE URL profiles require process-start clues, but one
has no downloader and the other does not bind `saps` to IWR's TEMP output.
Their two sibling delivery rules now report IWR/TEMP download and hidden-window
context under neutral HTTP download; the Mark-of-the-Web consumer reports
ADS removal near these clues without claiming the downloaded file was
launched. The eleven moved rules retain matcher bodies or composite clauses,
effective scope, confidence and proximity. No dependent rule keeps an old ID.

Three further `exec-download` composites moved by their required operations.
The PowerShell AppData IWR/start profile does not bind `OutFile` to the
`Start-Process` argument; it follows neutral process creation. Its embedded
hidden variant follows hidden-process evasion. The JavaScript temp-script
profile requires cleanup, but its fetch, temp path and child-process clues
are not an ordered or path-bound run; it follows indicator cleanup. The RDP
consumer now describes enabled RDP near AppData download/start clues rather
than a staged implant. All three moved composites retain their clauses,
effective scopes, confidence and proximity.

Eight more `exec-download` composites require download/decode/write and process
or installer clues, but no value or path handoff. Their PowerShell base
profile follows neutral process creation, its hidden variant follows hidden
execution, and its self-deleting variant follows script cleanup. Two bounded
batch IWR/`msiexec` profiles follow neutral installer process creation; their
12-line bound does not identify IWR's `OutFile` as the installer argument.
Three native URLMon profiles follow the required HTTP client APIs, with nearby
process and XOR-URL clues described as context. The managed .NET profile also
follows HTTP-client evidence: three download API names, Base64, ZIP extraction
and a CreateProcess API name do not bind an extracted member to launch. The
nine moves retain all matcher clauses, scope, confidence and proximity. No
new broken references or cap violations were introduced.

## Latest `exec-download` and adjacent review

A PE TEMP-write/process-API composite moved from `staging/temp` to a neutral
file-write context: it does not bind the written file to the process target.
Six exact-ID consumers now use the new canonical rule. Three Winsock/self-read
profiles also left `exec-download` for the payload self-read subject; the
remaining Winsock/TEMP rule has a mixed overlay/self-read/debugger alternative
and still needs an exact split before its objective location can be settled.

Two obfuscation rules from the `syntax` leaf followed their actual subjects:
a social-platform message bomb to denial-of-service and JSON key/value padding
to document whitespace. A Nemucod decimal-XOR profile moved into `syntax`;
that leaf is now exactly 100 rules without a cap exception. The NSIS
INetC/TEMP/process-API scaffold now reports a neutral HTTP-client profile.
The WinINet TEMP/CMD profile was split into a neutral variant and an API-hash
variant. Exhaustive evaluation of its five alternatives confirmed that their
union preserves the former two-of-five rule.

The Nemucod `fragmented-url-dropper` rule required neither a URL nor a staged
payload handoff. Its ADODB SaveToFile and WSH Run/computed-member alternatives
now report a neutral co-occurrence profile. The polluted-Base64 atoms and
composites, plus the evasion-heavy multi-clue signature, now live with the
recognized Nemucod family. Their predicate legs and scope are preserved;
descriptions and unsupported download/execute mappings were corrected.
The `bat-archive-loader` atomic that claimed an extracted launch has also
moved to neutral TEMP-path process creation: it matches `start` on a TEMP/TMP
EXE, not extraction. Its archive consumers still require a same-path handoff
review. Five atomics from `batch-lolbin` now report Python interpreter arguments, a
Python runtime ZIP filename, a generic `-k` text-file argument, and
curl-to-executable output paths in neutral capability leaves; all exact-ID
consumers were updated. A filename reference
is not a download URL, so the old `python-embed-zip-url` description was
corrected. A comparison against the committed source confirmed matcher and
condition parity for all 14 relocated Nemucod/batch rules; the earlier
Nemucod date-evasion wrapper was expanded into its three exact required legs.
`make validate` reports no new errors for these files.

Seven JavaScript composites left `exec-download`: three unbound HTTP,
curl or IP/write/shell combinations now report neutral shell-process context;
one TLS-disable/write/shell combination reports neutral TLS-disable context; two
obfuscator-driven HTTP/TEMP and HTTP/write/opener profiles now follow the
obfuscation technique; and the obfuscated COM SaveToFile/computed-call profile
now follows syntax obfuscation. An unrelated `.split()` matcher that did not
require obfuscation moved from the full syntax leaf to neutral string splitting,
keeping that leaf at exactly 100 rules. Two consumers were updated to avoid
claiming a delivered shell stage from co-occurrence. All seven composite
conditions and the split matcher's `if`/`not` bodies match their prior forms;
unsupported download/execute mappings and criticalities were corrected.

The remaining `windows-urlmon-stack` file is empty. Six atomic patterns
that construct only `%appdat`, `http://`, `pei.exe`, `%s:Zone`, `windrx.txt`, or
`%appdata%` now live in their neutral path, URL, and stream-name leaves. Two
URLMon/AppData/windrx co-occurrence profiles also moved to a neutral AppData
leaf; Needle's Twizt consumer uses the canonical profile. The GitHub-release,
URLMon and Defender-exclusion composite now follows Defender evasion with its
unsupported dropper verdict removed. Sibling review moved a Go injection rule
from Defender to process injection and seven AMSI bypass composites to the
AMSI leaf, reducing Defender from 132 to 125 rules even after the URLMon move.

The distinctive `.zero` stub, original-entry bytes and API-hash cluster now
identify Phorpiex in `well-known/malware/worm/phorpiex`. A
[Phorpiex delivery analysis](https://www.bitsight.com/blog/ransomware-twizt-inside-phorpiex-botnet)
documents the `.zero` entrypoint, stack strings, `windrx.txt`,
`Zone.Identifier`, URLMon and CRC32 API resolution;
[URLhaus](https://urlhaus.abuse.ch/host/thaus.top/) associates `pei.exe`
with Phorpiex. The six four-byte hash patterns were independently checked
against little-endian CRC32 values: they name `LoadLibraryExA`,
`ExpandEnvironmentStringsW`, `GetFileAttributesW`, `URLDownloadToFileW`,
`DeleteFileW`, and `CreateProcessW`, correcting the former A-suffix labels.
All 15 migrated family rules retain their matcher and condition bodies and
effective size bounds. The Elex iTorrent consumer now requires the complete
Phorpiex delivery/hash profile as optional mixed-bundle context instead of
letting any one four-byte hash imply Elex identity. The family signature
reports identity rather than asserting a payload-to-launch link that its
matcher does not capture.

The last Winsock/TEMP rule was a union of overlay, self-read and debugger
corroborators. It is now three profiles in neutral file-write, self-read
obfuscation and debugger-check leaves, each retaining the two shared required
legs, size guard and exclusions. An exhaustive three-bit truth table verified
that their union matches the original alternatives. A VM-artifact shell matcher
moved from debugger-check to VM detection, so the already oversized debugger
leaf did not grow; it remains at 149 rules for a separate technique audit.

The batch `exec-download` file is now empty. Its archive-independent
profiles moved by required evidence: architecture-aware downloads to neutral
HTTP download context, certutil plus raw-IP TCP stage query to C2
infrastructure, curl output near TEMP launch to neutral process creation, and
generic download/path/launch co-occurrence to neutral download context. The
shared `download-tool`, `exec-cmd`, `payload-exec-cmd` and PowerShell `-File`
observations moved from the 100-rule batch sibling to capability leaves; that
leaf is now 95 rules. `bitsadmin /transfer` also moved to neutral downloads,
and its exclusion for fallback-download objectives was removed: a fallback
transfer is still a download. A synthetic positive batch sample matches the
canonical BitsAdmin rule, while a `/list` control does not. The LOLBin
co-occurrence profile now reports neutral download/launch clues. The Python
bin/key launcher became a neutral profile plus a Startup-folder refinement;
all 32 combinations of its original five alternatives show that the two
profiles preserve the original match union. The shared alias matcher bodies
and numeric conditions were checked against their committed versions.

The four `bat-archive-loader` composites did not tie an extracted member to
their launched TEMP path. Their matcher clauses now follow the actually
required subject: HTTP download with hidden/extraction context, TEMP process
creation with archive context, TEMP script-host process creation, and Run-key
persistence. Descriptions no longer say the launched file came from the
archive. Three underlying extraction-command atoms and their `any` alias
left `dropper/staging/archive` for neutral archive-extraction capability;
their matchers, confidence, platforms, and file-type scopes were retained.
The PowerShell file-exec and batch consumers use the new IDs. An adjacent
`powershell-download-archive-execute` objective still has no same-path handoff
and remains for sibling review. `make validate` found no new errors in the
archive files; the global check still fails on existing taxonomy debt.

Seven `hta.yaml` composites also moved by their supported operations. An HTA
markup/FSO pair follows file writing; a hex-XOR decoder plus HTA markup follows
decoding. A computed ActiveX, shortcut target and shortcut save combination
now reports shortcut creation: its matcher has no Startup-folder or Run-key
evidence, so the former persistence verdict was unsupported. `ExecuteGlobal`
with MSXML and a hidden window follows VBScript evaluation, while a hidden
TEMP batch launch and a hidden ActiveX/ADODB ProgID cluster follow hidden
execution. A Fisher–Yates string shuffle with hidden-window clues follows the
JS-obfuscator technique. Their required predicate clauses and effective
file-type/platform scopes were retained; unsupported staged-payload and
persistence wording and mappings were removed. Two outside consumers of the
HTA hex-XOR decoder now use its new neutral ID.

The final **17 HTA rules** were then routed by their required evidence. Their
matching clauses, proximity, confidence and effective file-type/platform
scopes were checked against the pre-move YAML; only the claims and severity
or ATT&CK mappings that depended on an unproven handoff were changed.

| Former rules | Evidence actually required | Disposition |
|---|---|---|
| `cloudflare-tunnel-url`, `epub-hta-stage-url`, `hta-media-decoy-lure` | Split substrings for a domain or the word `epub`, and an HTML media element referencing a media file | String-concatenation and HTML-document leaves. The `"ep" + "ub"` clue remains a low-severity component of the mshta-fragment profile, not a remote-stage verdict. |
| `offscreen-obfuscated-wsh-downloader`, `wsh-archive-download-execute`, `offscreen-wscript-download-launch` | Off-screen window, curl output or WebClient call, extraction/EXE-path or process-launch clues | Hidden execution or detached-spawn profile with network/archive context. No rule binds the fetched bytes or extracted member to the launched target. |
| `hta-embedded-batch-dropper`, `hta-base64-gzip-tempbat-loader`, `hta-obfuscated-com-tempbat-loader`, `vbs-base64-gzip-tempbat-loader`, `hta-obfuscated-wscript-file-runner` | Text-file or gzip write plus batch/script-host launch | Hidden execution or neutral process-creation profiles. The gzip writer matches `SaveToFile tempZip`, while the launcher matches `Run tempBat`; those variable names alone do not bind archive contents to the batch file. |
| `hta-encoded-eval-loader`, `hidden-hta-remote-reflective-loader`, `hta-hidden-powershell-decode-stager`, `hta-decoy-lure-obfuscated-dropper` | Eval or reflective-load operations near decoding, HTTP, concealment, or media clues | Direct eval, dynamic eval or hidden-execution profiles. The media element no longer claims to be a decoy. Require the decoded/fetched value to be the eval/load argument for a dropper verdict; `powershell-keyword` alone is not a launch. |
| `hta-mshta-remote-stage`, `hta-charcode-activex-stager` | Split `mshta` or char-code/ActiveX clues with WSH/HTA context | String fragmentation and char-code encoding profiles. The `mshta` rule does not require a URL argument, and the ActiveX rule does not require a download or staged payload. |

The `exec-download` leaf is empty. Four broad directory consumers in the
plugin-loader and FTP-banner siblings had referenced it; those now-dead
alternatives were removed without changing their other branches. Their
broader plugin and FTP payload-link claims remain separate sibling audits.

The three-rule `script` leaf is empty too. Its Ruby HTTP/message API alias
now lives with neutral HTTP request-client evidence, and its exception
remains beside the process-launch profile it suppresses. The profile still
requires the same HTTP, file-write, and launch alternatives within 2,048
bytes, but now says they coexist rather than claiming the fetched response
is executed. The `has-dynamic-exec` consumer points to this exact new profile.
An adjacent `staging/temp` sibling had matched `payload_url` near
`/update/module.bin` without a TEMP path or fetch-to-launch relationship.
Its path clue and composite now report URL-path and Ruby-launch context.
The catalog changed concurrently during this pass, so the current inventory
has seven more legacy rules than the prior 1,742-rule checkpoint despite the
three-rule `script` retirement.

The `installer/nsis-overlay-loader` and two `windows-loader`
profiles still mix
loader words with unbound process/section evidence. Review their required
relationships and consumers before choosing destinations; neither language,
installer format, nor generic `loader` is a valid split axis.

## Placement and migration procedure

The next review should start with the ten largest legacy leaves: `loader`
(100), `fileless` (99), `installer` (98), `wsh` (97), `batch` (95),
`shell-chain` (89), `wsh-reconstruct` (82), `eval` (76),
`dropper-script` (72), and `clickfix` (72). Together they hold **880 of the
1,749 remaining rules**. Their names mix program role, language, carrier and phase; none is
an admission criterion for a new rule. Review exact matcher bodies and
consumers in each leaf, beginning with rules that assert a download-to-sink
or decode-to-sink handoff, then route neutral atoms and remaining profiles.
The directory inventory already covers every rule, but the 1,749 entries
still require individual evidence decisions. The priority is precision, not
reducing the directory count for its own sake.

For each rule, first identify the fact supported by its actual condition.
Move generic atomic facts to their neutral subject, preserving their scope and
updating every consumer. For a composite, require payload acquisition or
staging **linked** to activation before keeping it under dropper. Choose the
required payload sink: `process-inject`, `image-map`, `module-load`,
`script-eval`, `interpreter-stdin`, or the proper `file-exec` child. A helper
process that eventually loads staged code does not make the helper launch the
payload sink. If two independently staged payloads reach different sinks,
split the claims rather than copying one chain into two leaves.

When the matcher supports staging but no sink, use the specific staging
mechanism. When it supports only a download, ordinary execution capability,
build step, concealment, persistence, or identity fraud, place that fact under
its corresponding subject outside dropper. Retire a composite whose asserted
relationship is absent and already covered by its component findings. For
every move, check exact-ID and directory consumers, preserve effective
defaults and matcher bodies unless the audit explicitly repairs a claim, and
run validation plus a representative positive and counterexample where the
matcher changes.

Review the remaining legacy leaves and their closest siblings next. Close `execution/` only after every rule
has one evidence-supported destination and no directory or exact-ID consumer
depends on the retired path.

`make validate` still fails on catalog-wide debt, including 71 over-cap
directories and one unrelated broken `os-release-open` reference in system
discovery. It reported no broken references for these dropper moves. The
relocated C#, VS Code, PyInstaller and shipped-key YAML bodies match their
original committed bodies; the Werfault rule retains its six matcher legs
while its identity claim and ATT&CK mapping were corrected. The new audit
script compiles; its generated summary is the current directory inventory.

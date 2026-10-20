# greatnesscoming HTA triage

Analysis date: 2026-10-20. All payload inspection was static: literal folding,
Base64 decoding, AES decryption, ILSpy decompilation, and native disassembly.
No HTA, JavaScript, PowerShell, managed assembly, or native payload was launched.

## Recovered chain

1. The HTA uses mixed-case VBScript, 240-space token padding, long variable
   names, character-code reconstruction of WScript.Shell and %ComSpec%, and
   WSH Run with window style 0. It invokes a Base64 UTF-16LE PowerShell command.
   The parent WSH Run argument 0 requests a hidden window. PowerShell also
   specifies `-W 1`: its CLI converts the value to ProcessWindowStyle, whose
   value 1 is Hidden ([PowerShell parser](https://github.com/PowerShell/PowerShell/blob/master/src/Microsoft.PowerShell.ConsoleHost/host/msh/CommandLineParameterParser.cs),
   [Microsoft enum reference](https://learn.microsoft.com/en-us/dotnet/api/system.diagnostics.processwindowstyle)).
2. Decoded PowerShell downloads a JavaScript file into APPDATA and invokes it.
   Its U+201D quotes are accepted by PowerShell, although the current source
   facts parser does not recover them as ordinary quoted literals
   ([Microsoft quoting rules](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_quoting_rules?view=powershell-5.1)).
3. The fetched UTF-16LE WSH script contains thousands of numeric junk
   assignments. Its core uses synchronous ServerXMLHTTP GET, stores
   responseText in a variable, checks status/nonempty content, then evals that
   same variable. The guard had prevented the canonical response-eval trait
   from matching; this is the main fetched-stage detection repair.
4. The next script assembles a PowerShell program from strings with an inserted
   marker, removes the marker, writes a temporary .ps1, and starts PowerShell
   through Win32_Process.Create with ShowWindow 0. The command requests hidden
   execution and execution-policy bypass, then deletes the temporary script.
5. Literal concatenation and marker substitution expose a PowerShell WebClient
   download from a Workers endpoint. It replaces `*` with `A`, reverses the
   response, Base64-decodes it, and calls Reflection.Assembly.Load. Reflection
   locates a method named Mesa and invokes it with 19 encrypted arguments.
6. ILSpy reveals a .NET Reactor protected assembly carrying task-scheduler
   interop types. The arguments decrypt with AES-256-CBC/PKCS7: the first 16
   decoded bytes are the IV; the rest are ciphertext. The key is the UTF-8
   password `006#5o6&qr1V` followed by bytes 0 through 19 to make 32 bytes.
   Configuration selects an easysend URL and a Caspol host name. Optional
   persistence flags are empty; merely containing task interfaces and enum
   definitions does not establish SYSTEM/boot persistence.
7. The managed downloader retrieves a JPEG, selects the text between the first
   INICIO and last FIM marker, replaces `###` with `A`, reverses the result,
   and decodes hex or Base64. The actual response uses Base64 and yields the
   native PE recorded below. Taking the last FIM matters: an earlier occurrence
   appears inside the encoded payload.
8. Managed injection code creates a suspended process (creation flag 4),
   allocates executable remote memory, writes PE headers/sections, applies
   relocations, adjusts thread context and the remote image base, and resumes
   the thread. These operations are visible in decompiled code. The trait
   added for the compiled assembly deliberately reports the narrower
   co-occurrence of downloader, decryptor, and image-replacement APIs as
   suspicious; it does not claim proven data flow from API names alone.

## Indicators and limits

Recovered network locations, defanged:

- `hxxp://38.247.161.228/18/wethinkingsureforme.js`
- `hxxp://38.247.161.228/8Xg122IK`
- `hxxps://rough-truth-e072.publicftpresend.workers.dev/dqqwvgcql`
- `hxxps://easysend.co/d/35579`

These identify the observed chain; no new rule requires these hosts, paths,
variable names, marker strings, or payload basenames.

The final extracted executable is an importless native x86 GUI PE with a
single high-entropy executable section, a reflective DOS-header stub, and
obfuscated dispatcher code. Disassembly confirms the packed loader structure.
Its ultimate application behavior and malware family remain unresolved; the
analysis does not claim a specific stealer or RAT identity.

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| Original HTA | 15447 | `be872654c1b956dca8eaf113f504c6ded6c5aeb6a769539a965488258da40a18` |
| Fetched WSH downloader | 1522292 | `f551753a0a2d93941263ac8bfdddbbcaf7fd7c7c8dee70ac1b2eb3ed790efb54` |
| Fetched WMI script stage | 783266 | `0b5c739dc3086f985ad260cfbbe56d469a04c5b69014e03ed7879acec9853e73` |
| Decoded managed loader | 145408 | `d97ee274c973756786f49f6709258d95feba3247bcd536178fb665a34ac93a92` |
| JPEG carrier | 2480482 | `38a9315c584b309366ab39b19de7b460cf6114350c7013cec5141b7b2c3915d8` |
| Extracted native PE | 285696 | `cb03fc78b378e6c9ead8b14c9acde56453d62e7ce5b4ae9cd0c5f399d770de84` |

## Regression coverage and taxonomy corrections

The `greatnesscoming-*` files in `../../hostile/` and `../../benign/` are inputs
for static analysis only. Exact assertions live in `../../expectations.toml`.
The HTA, stripped fetched JavaScript stages, and managed loader are retained
alongside small synthetic variants. The junk-padded downloads are not retained. The JPEG carrier is included
by the later x-improve review to exercise the trailer parser.

- Guarded response eval: var/let/const, renamed bindings, and UTF-16LE input.
  Controls cover unrelated variables, rebinding, mutation in guards, multiple
  declarators, mutation inside the guarded body, download-only use, and literal
  example text. The matcher requires adjacent binding and guarded evaluation,
  a single declarator/body statement, and a guard without calls or assignments.
- Hidden encoded HTA launch: require the encoded-command evidence, and extend
  the hidden-window downloader composite to encoded APPDATA fetch-and-run.
- Hex Chr expressions: rename the observation and consuming composite so they
  do not falsely require arithmetic when plain hexadecimal literals qualify.
- Task enum/API references: move neutral atoms out of persistence objectives
  and generic registration references out of the Zyra VPN identity. Retire the
  generic SYSTEM/boot verdicts that conflated interface definitions with use.
  Campaign identity composites retain their separate campaign evidence.
- Managed downloader/image-replacement profile: retain a suspicious finding
  grounded in the loader's API surface after removing false persistence and
  family findings.

`TaskApiReferences.cs` builds the harmless enum/interface control with:

```sh
mcs -target:library -out:testdata/benign/greatnesscoming-task-api-references.dll testdata/triage/greatnesscoming/TaskApiReferences.cs
```

Run the repository gate from its root: `make validate CLEAVE=<current-cleave>`.

## Completed verification

- All 20 focused fixtures passed; all 13 controls had zero suspicious or
  hostile findings.
- `make validate CLEAVE=/tmp/greatnesscoming-cleave-validator` passed all
  3,402 fixtures. The validator was a pinned copy of the current sibling
  Cleave build. An earlier run's sole failure was a rule-timeout diagnostic on
  the unchanged Tor control; isolated rescanning and the final full gate
  passed without changing its cap or suppressing the diagnostic.
- Updated atomscan reports for the original HTA, fetched UTF-16LE downloader,
  and decoded managed assembly were uploaded to Hopper.
- The final `hopper mv -target bad` request for the original HTA returned
  `noop`: 0 moved, 1 noop, 0 absent, 0 failed. It already had the requested
  bad verdict.

## x-improve follow-up

The follow-up reviewed all recovered layers with `atomscan --format=json`.
It adds 30 fixture cases, extending this chain's focused set to 50 inputs.
The new controls cover quoted and commented PowerShell examples, literal
(non-expanding) environment-variable text, local assembly loading, forward
indexing, normal PSHome paths, neutral thread-context API declarations,
ordinary markup, and restarted JPEG scans with no executable trailer.

Detection and readability changes:

- PowerShell AST rules recognize web downloads to APPDATA/LOCALAPPDATA and
  call-operator invocation, including smart quotes, renamed script files,
  case changes, and wget/iwr/Invoke-WebRequest spellings. The suspicious
  composite reports nearby operations; it does not claim identical paths.
- A descending-index slice observation combines with download, Base64 decode,
  assembly-load, and reflected-method calls. This suspicious profile names
  co-occurring operations rather than asserting byte provenance.
- A separate suspicious AST rule recognizes command invocation assembled
  from PSHome character indexes. It covers the still-obfuscated stage,
  without depending on its replacement markers or assuming the target is IEX.
- The Base64-decoder/GetMethod observation now describes proximity, replacing
  the unsupported claim that ordinary decoder syntax reconstructs a method.
  Task enum descriptions now use readable Task Scheduler terminology.
- A neutral markup observation reports repeated 128-column inline gaps.
- GetThreadContext name references are no longer suppressed for all .NET
  assemblies. A compile-only declaration control remains free of suspicious
  and hostile findings.
- Encoded executable-header atoms move out of the stego objective into the
  existing embedded-encoding leaf. The duplicate reversed-header observation
  is consolidated, and conventional and reflective MZER/CALL DOS headers are
  covered in both directions. Existing carrier and family consumers use
  those neutral observations; no new family attribution is made.

The JPEG extraction fix is in the sibling filefacts repository:
`src/formats/jpeg.rs`. Restart markers stay inside entropy-coded scan data,
so later stuffed bytes are not mistaken for segment headers. The extractor
now reports **406,253 bytes after the actual EOI**, and the existing hostile
JPEG carrier composite matches. Tests exercise all eight restart markers,
stuffing, truncated scans, and multiple scans; all 16 JPEG extractor tests pass.
The JPEG predicate also passes renamed delimiters and A-substitution markers,
plus forward/reversed conventional and reflective header variants.

JPEG integration was tested with a temporary Cleave source snapshot built
against the local filefacts fix via a Cargo path override. The installed
Atomscan was used to verify the trait-only PowerShell changes; its linked
extractor must be rebuilt against updated filefacts to acquire the JPEG fix.

Final follow-up verification:

- All 50 focused inputs passed, including 31 controls with zero suspicious
  or hostile findings.
- All 16 JPEG extractor tests passed.
- `make validate CLEAVE=/tmp/greatnesscoming-improve-cleave` passed all
  3,436 repository fixtures using the local filefacts parser fix.
- Atomscan verifies the smart-quoted downloader, decoded assembly profile,
  PSHome-index invocation, and updated encoded-header observation. The
  installed extractor still reports zero JPEG trailer bytes; the rebuilt
  integration reports 406,253 bytes and the hostile carrier composite.

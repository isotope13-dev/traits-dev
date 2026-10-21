# cxusage second review

Verdict: **MALICIOUS**. SHA256:
`db2d044bd12bf07aa3903607d6bd1ad152a2d9caee8d4817becea02696254fa6`.

This is a source distribution of the cxusage Codex usage CLI, repackaged with
two unrelated Windows LuaJIT loaders. The conviction rests on recovered code,
launch commands and misleading download instructions, without external threat
intelligence. No YAML change is justified by the firing findings reviewed here.

## Identification and execution paths

- `src/{cli,daily,pricing,utils}.ts` and corresponding `dist/*.js` implement
  a plausible usage-reporting CLI. They enumerate local Codex session JSONL,
  aggregate token counts, fetch public OpenRouter model prices, and print
  reports. The package bin entry is `dist/cli.js`; its prepublish hook builds
  TypeScript. This functionality does not explain the Windows bundles.
- The README repeatedly advertises `src/Software_v3.4.zip` as the application,
  documentation, prerequisites and release download. It even substitutes that
  URL into the purported session-log location. The ZIP contains
  `Launcher.cmd`, `luajit.exe`, and `uix.txt`; the batch file actually executes
  `start luajit.exe uix.txt`.
- `scrutiny/cxusage.zip` contains `Launch.cmd`, `luajit.exe`, `lua51.dll`, and
  `include.lib`. Its batch file executes `start luajit.exe include.lib`.
  The apparent library is obfuscated Lua source, not a native library.
- `uix.txt` uses decimal escapes, string-fragment permutations, encrypted
  constants, environment indirection, arithmetic and numeric state dispatch.
  Cleave recovers a script layer with resolved API names and command strings.
  I inspected assignments, call arguments and branch destinations in this
  layer, rather than using its strings or scan score as a verdict.
- For `include.lib`, I isolated the initial constant-table decoder before the
  VM entry, inspected its permutations and custom radix-64 arithmetic, and
  evaluated only that decoder with host I/O, modules and Python bindings
  unavailable. This recovered 1,057 constants. Substituting constant lookup
  calls and passing the resulting source through `cleave facts` recovered
  another readable layer. The payload VM and native code were not executed.

The two Lua scripts implement the same broad design with different constants
and state numbers:

1. They load FFI and bit operations, define Win32 types, resolve native APIs,
   and provide local PEB/export-table walkers. The small RWX allocation used
   for a PEB-reader stub is not proof of remote-process injection.
2. `loader.bypass_defender == 1` selects code constructing hidden PowerShell
   `Start-Process`, comment-separated `-Verb RunAs`, and
   `Add-MpPreference -ExclusionPath $env:SystemDrive -ExclusionExtension
   .exe, .dll -Force`. The assembled command goes to the resolved command
   wrapper with show flag zero. In `uix.txt`, the branch selects state
   12106172; `include.lib` selects state 927872. This is an elevation request
   to remove broad classes of files from scanning, not proof of a UAC bypass
   or successful elevation.
3. Configuration gates autorun behavior. A daily task template is formatted
   with random hours 10 through 14 and minutes 0 through 59, extended with a
   task name and executable action, and passed to the command wrapper.
   Other branches build one-shot PowerShell task registration and access
   Run/StartupApproved registry locations. These are executable paths, not
   merely declarations of task-related APIs.
4. Task handling reads `tasks`, `file_path`, `file_name`, `start` and loader
   options. It constructs local paths, writes returned data, and selects
   executable, DLL/rundll32, command/batch, PowerShell and Lua launch forms.
   The native-buffer path obtains `VirtualAlloc`, copies into its allocation,
   changes protection with `VirtualProtect`, casts that address to
   `LPTHREAD_START_ROUTINE`, and supplies it to resolved `CreateThread`.
   These implementations establish remote task/payload handling; no final
   downloaded payload or successful execution was observed.
5. HTTP helpers construct WinInet requests, send bodies with
   `HttpSendRequestW`, and read responses with `InternetReadFile`. Host-report
   construction includes computer/user identifiers, geographic fields and OS
   data. Task-report construction uses task IDs and `/task/` POST requests.
   Polygon `eth_call` and fallback endpoint handling are present.
6. GDI helpers call `GetDC`, obtain dimensions, create a DIB, use `BitBlt`
   with SRCCOPY, and serialize bitmap data. Multipart file/data construction
   also exists. Their presence alone is not used to claim a proven
   screenshot-to-network data flow. Hex conversion and byte-XOR operations
   are implemented, including an aliased `tonumber(..., 16)` call.

The configured HTTP endpoints differ (`213.176.73.151` in `uix.txt`,
`64.188.98.20` in the decoded `include.lib`). Addresses, exact task names,
contract addresses and random multipart boundaries are evidence locations,
not proposed signature gates. No endpoint, contract or next stage was fetched.

Rizin and PE header inspection identify LuaJIT/runtime carriers. The roughly
101 KiB after `lua51.dll`'s last section is its COFF symbol/string tables,
not evidence of an embedded malicious payload. Existing notable layout
measurements still accurately record bytes beyond sections; they do not
convict the DLL or establish concealment.

## Findings retained

The two hostile detections describe distinct supported behaviors: broad
Defender exclusions and daily-task persistence alongside those exclusions.
Neither was weakened. All suspicious findings were checked:

- Numeric conditional dispatch, escaped/reconstructed strings, nested return
  wrappers and proxy/environment indirection occur in the Lua source.
- Batch/data/runtime archive composites describe the actual carrier layout
  and packed Lua source. They remain suspicious rather than making LuaJIT
  or ordinary obfuscation inherently malicious.
- Executable-extension Defender exclusions are real generated command text.
- The source-package/README LuaJIT sidecar lure corresponds to the advertised
  nested archive and its launch instruction.
- `include.lib`'s custom radix-64 concealment finding is supported by the
  independently inspected decoder. It does not itself establish intent.

Neutral detections for HTTP, task configuration, memory protection, dynamic
API resolution, GDI, Run keys, process creation, elevation requests and
hex decoding remain accurate, including when those operations are dual use.
No shared rule was deleted, narrowed, demoted or relocated.

## Before/after verification and gaps

Ran `atomscan` and `cleave facts` on the supplied archive; also obtained facts
for both nested archives, both scripts and runtime files. Repeated the full
archive scan using `--no-update --follow none --mode slow -f json`.
All 23 reported files/layers retained identical trait IDs and criticalities.
There were **zero detection losses** and zero additions.

| Artifact | Verdict from review | Hostile | Suspicious | Notable |
| --- | --- | ---: | ---: | ---: |
| Supplied source ZIP | MALICIOUS | 2 | 11 | 281 |
| `src/Software_v3.4.zip` | MALICIOUS | 2 | 9 | 161 |
| `uix.txt` | MALICIOUS | 2 | 6 | 86 |
| `uix.txt##script@0` | MALICIOUS, same program | 2 | 5 | 85 |
| `scrutiny/cxusage.zip` | MALICIOUS | 0 | 1 | 66 |

The outer classifier probability remained 0.99. The recovered `uix.txt`
and script layer also receive 0.99. The reported member-level probability
for `Software_v3.4.zip` itself is 0.01124 despite its malicious child; the
outer decision still captures that child. More significantly,
`scrutiny/cxusage.zip` receives 0.000737 and its `include.lib` 0.000979,
both outside the classifier's flagged grid. The extra decoder layer hides
its attack behavior from automatic recovery, leaving one suspicious
concealment trait. This is a retained decoding/classifier coverage gap,
not a reason to relabel it benign, inflate severity, duplicate detections,
or add sample-specific encrypted constants to rules.

Model feature-version compatibility warnings and source-flow analysis gaps
were recorded by atomscan. The manually recovered behavior, rather than
absence of findings, determines the judgment.

Unknowns include whether anyone launched the bundles, their remote
configuration at deployment, whether exclusions/tasks succeeded, and what
payloads the server supplied. Those unknowns limit claims about observed
effects; they do not explain away the deceptive packaging and implemented
Defender-bypass/persistent-task code.

No YAML traits changed, so `make validate` was intentionally not run.

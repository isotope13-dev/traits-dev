Both requested samples are **MALICIOUS** after independent code review. No
external feed label or reputation score was used to establish their behavior.
The small native LuaJIT carrier and runtime inside the registry archive are
ordinary interpreter components; the script they are directed to execute is
malicious.

`c67697d95ec9…` is a LuaJIT FFI loader for an embedded .NET credential stealer.
Decimal string escapes and dozens of unused Lua-5.1 VM implementations obscure
the active statements. Following the actual top-level calls establishes:

- It hides the console. `pcall(u)` loads CLR, scans mapped memory for
  `AmsiScanBuffer`/`AmsiInitialize`, changes protection, zeroes matched names
  through `NtWriteVirtualMemory`, flushes the instruction cache and restores
  protection. Separate invoked helpers patch AMSI and ETW exports with
  `31 C0 C3` (zero return), and another patcher writes RET/NOP bytes.
- Its optional sidecar check writes a VBScript launching its own executable
  with a hidden window and registers a ten-minute recurring scheduled task.
  That branch requires an adjacent `.mui` file; its presence at deployment is
  unknown. The capability is not proof that the task was installed.
- `pcall(Mo)` invokes API-unhooking and tampering helpers, then applies a
  ten-character substitution, reversal, Base64 decoding and printable-byte
  rotation reversal to its embedded blob. Fresh data-only recovery produced
  271,435 shellcode bytes, SHA256
  `aa1b57e90a822bba295fd0369ea6729b50a13d13ef37f89a65fd7aba8ab8b187`.
  The loader copies these into native memory and uses a vectored access-fault
  handler and page transformations before calling the allocation as a function.
- Offline Chaskey-CTR decoding of the shellcode's Donut instance yielded a
  240,128-byte managed PE, SHA256
  `4180269c675c26e85d20a22f06587a5a45e6f4af5ee4a60fb73dc51317ce50e7`.
  This matches the retained decompilation in
  `../iexpress-lua-credential-stealer/payload-source/`, which was inspected
  again: the entry point invokes the collection orchestrator; Windows Vault
  items become username/host/password records; the reporting routine constructs
  mail and invokes `SmtpClient.Send`. Browser/application collectors,
  keylogging and screen collection are also implemented. The decode scripts in
  that existing review supply reproducible data transformations; no payload
  instructions or Windows API calls were executed during this review.

The active defense tampering and embedded credential-theft program tip the
standalone loader verdict. Its current launcher, user authorization and actual
runtime success are unknown; none is needed to establish these implemented
attack paths.

`571ca1fe6c61…` is a NetSim Pro browser-project lure carrying a Windows task
loader. The README repeatedly directs users to a ZIP under `Screenshots/`.
That ZIP contains `Application.cmd`, `loader.exe`, `lua51.dll`, and
`module.cso`. Its command is `start loader.exe module.cso`. The HTML implements
a browser network-learning simulator; it does not explain the hidden task
loader. Rizin inspection follows argv to `luaL_loadfile` at `0x1400027a3`,
then the protected execution path; the CLI initializes its Lua state at
`0x14000420e` and dispatches through `lua_cpcall` at `0x140004235`.

The source in `module.cso` has arithmetic numeric dispatch, permuted escaped
strings, encrypted constants and environment/proxy indirection. Extracted the
full recovered script with `cleave strings --format terminal` (JSON string
serialization truncates the recovered source), then parsed it and inspected
branch bodies and effects:

- `loader.bypass_defender == 1` selects state `11457996`. That branch builds a
  hidden PowerShell `Start-Process ... -Verb ... runAs` command containing
  `Add-MpPreference -ExclusionPath $env:SystemDrive -ExclusionExtension .exe,
  .dll -Force`. The complete assembled command is passed to its command
  wrapper with show flag zero. The wrapper calls resolved `WinExec` on its
  supplied arguments. This is an elevation request, not proof of a UAC bypass.
- The daily-task path formats `schtasks /create /sc daily /st %02d:%02d /f`,
  chooses hours 10–14 and minutes 0–59, adds `/tn` and `/tr`, and passes the
  completed command to the same wrapper. Alternate task actions include
  executable and DLL/rundll32 launches. One-shot task and Run-key branches
  also exist. Options gate these behaviors; no installed task was observed.
- Task/configuration handlers process `tasks`, `file_path`, `file_name` and
  `start`, open output files in `wb` mode, write data and select launch forms.
  The native-buffer path allocates memory, copies data, changes protection,
  casts the allocation to `LPTHREAD_START_ROUTINE`, and supplies it to
  `CreateThread`. This is local native execution; remote-process injection
  is not established by these APIs.
- WinInet helpers construct/send HTTP requests and read responses. Task
  reports use `/task/` paths. Polygon `eth_call` with fallback RPC hosts,
  host-report construction and GDI screen-copy helpers are present. No live
  endpoint or later payload was fetched. GDI plus networking alone is not
  claimed as a proven screenshot-exfiltration flow.

The advertised browser purpose, executable delivery, recovered defense
exclusions and durable task/payload handling jointly support MALICIOUS.
Deployment configuration, successful elevation/persistence and server-supplied
payloads remain unknown. The two hostile and all six suspicious findings were
checked against these paths and retained; the ordinary interpreter/runtime
capabilities remain notable.

Trait corrections preserve supported observations:

- The old low-bit regex matched `nG&1+` inside the standalone loader's encoded
  payload, not an arithmetic expression. Its non-Lua matcher and ID are
  unchanged except for explicit Lua exclusion. A parsed Lua `& 1` / `bit.band`
  rule replaces the Lua textual search, and existing attack consumers use the
  shared alternative group. Strings, comments, other masks and logical
  `(value) and 1` are tested as near misses. Every hostile/suspicious finding
  on four outside-batch Ruby/Python/TypeScript LSB and DNS-exfiltration corpus
  archives survived. Existing Ruby arithmetic and benign-prose controls pass.
- A line-length metric proves a file property. Moved the >1,000,000-byte
  observation to `metadata/file/line::source-line-over-1mb` at notable.
  Removed the redundant large-PE and protobuf aliases and their now-unused
  context helpers. Neither alias required the condition in its name; the
  large-PE wrapper even fired on this Lua script. There were no exact external YAML
  consumers of this retired leaf; its three obfuscation-ancestor consumers
  are JavaScript/TypeScript-only and cannot consume the old metric scope. A huge ordinary literal and a short control
  verify the new boundary. No supported attack relationship was removed.
- A Lua DLL name is runtime metadata, not interpreter execution. Moved its
  unchanged matcher and scope to `metadata/lang/runtime` and updated the
  sidecar consumer. The only broad interpreter-directory consumer is scoped
  to Python, outside this atom's scope.
- Audited the full 100-rule arithmetic leaf before adding the Lua alternative
  and grouping rule. Relocated two lexical observations: padding-alignment
  wording to natural-language phrasing, and hexadecimal/falsy call arguments
  to source-call syntax. Their matchers, scopes and severity are preserved;
  exact consumers were updated. No broad arithmetic-directory consumers
  were found. The destination call-directory selector feeds only PHP panel
  context, outside the moved JavaScript/VBS matcher scope. Positive, negative and an overflow-consumer control pass.

Verification: `check.py` here passes 13 focused controls. Twelve existing
Google-protos/source controls and all 13 existing Lua AMSI/ETW controls pass.
The older IExpress all-format harness has an unrelated failure:
its high-entropy PE fixture does not match the expected packing composite.
That composite and its dependencies were not changed by this review; the
Lua-specific checks were rerun separately and pass. The final repository gate
is `make validate`.

Repeated atomscan with explicit local traits, `--no-update --follow=none
--mode slow`, including all archive members/layers. Before/after summary:

| Artifact | Hostile | Suspicious | Notable before → after |
| --- | ---: | ---: | ---: |
| Standalone `loader.lua` | 3 | 0 | 28 → 26 |
| Registry ZIP | 2 | 6 | 171 → 171 |
| Nested ZIP | 2 | 6 | 140 → 140 |
| `module.cso` | 2 | 6 | 86 → 86 |
| `module.cso##script@0` | 2 | 5 | 83 → 83 |
| Native `loader.exe` | 0 | 0 | 24 → 24 |
| `lua51.dll` | 0 | 0 | 38 → 38 |

The standalone loader loses the false mask match and two overlapping
line-length findings, gaining the correctly placed line measurement. The
archive's only change is the DLL-name relocation, including propagated parent
findings. **No hostile or suspicious detection was lost.** Classifier
probabilities remain malicious: loader `0.9983795 → 0.99840814`, registry ZIP
`0.99 → 0.99`. The nested ZIP's own member probability is about `0.012` despite
its malicious script and inherited hostile findings; the root and script/layer
scores capture the attack. Automatic decoding also stops before the standalone
loader's embedded managed stealer, so its credential-theft behavior is known
from manual recovery rather than automatically surfaced payload traits.
These are retained classifier/decoder gaps, not reasons to restore inaccurate
rules. Atomscan also reports v18/v19 feature-schema compatibility warnings.

Raw scans, full recovered source, fresh payload bytes, facts and Rizin traces
are under the named scratch directory `acquit-c676-571ca1-review`.

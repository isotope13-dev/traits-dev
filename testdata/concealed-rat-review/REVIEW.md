# Concealed Windows payload and Scapy review

The original samples were read and disassembled, never launched on the host.
Scratch evidence, decoded stages, tool output and download provenance are in
`/usr/local/var/cyclotron/tmp.noindex/cyclotron-28a4cdc2/scratch/bad-analysis`.
The repository changes contain general operation/code patterns, not sample
hashes, chosen filenames, C2 addresses or encryption keys.

## Findings

| Original sample | Identification and verdict | Hostile before → after | Suspicious before → after |
|---|---|---:|---:|
| `8ae4130ad94c…` / `zapret-discord.exe` | **MALICIOUS**, concealed Salat loader | 0 → 3 | 0 → 2 |
| `6e7ffcc76962…` / `Free 9999+ Robox.exe` | **MALICIOUS**, obfuscated NjRAT 0.7d Horror Edition | 0 → 3 | 0 → 4 |
| `41e6daa8f455…` / `scapy` | **BENIGN**, upstream Scapy interactive launcher | 0 → 0 | 0 → 0 |

All three initial scans were classifier-benign. The revised Windows scans are
hostile; Scapy remains benign. No hostile/suspicious finding was removed.
The model bundle reports that its feature schema is older than the engine's
schema; this does not negate the static behavior evidence.

### Concealed Salat loader

The unsigned x86 GUI PE is Go 1.22 code with renamed runtime paths and bogus
Desktop Toolkit / Delta Systems / `pnlhost.exe` version metadata. It is not a
Discord DPI-bypass implementation. There is no Authenticode signature to verify.

Recovered Go pclntab entries establish this path:

* `main.m*in` at VA `0x4a27b0` sleeps approximately 57 seconds, invokes its
  unpacking closure, calls the installation routine, and maps the returned PE.
* The closure at `0x4a2900` decodes a first-byte-XOR password, derives a 32-byte
  PBKDF2-HMAC-SHA256 key with 100,000 iterations, concatenates 6,039,428 embedded
  bytes, removes interleaved padding, and reverses a six-part byte-operation
  recipe. ChaCha20 counter zero decrypts the resulting 3,592,168 bytes; raw
  DEFLATE produces a 3,593,216-byte UPX PE.
* Only the concatenation, unpadding and byte-transform helpers were emulated.
  Every other callable target was denied except bounded allocation/memmove
  stubs. KDF, ChaCha and inflation were reimplemented using standard libraries.
* The extracted PE SHA-256 is
  `9d78bfcf8af6b37dee34f88587d1f07de3fc887b2682b4c048bbc11df831ec0c`.
  `upx -d` recovers the 12,570,624-byte Go `salat` executable.
* Installation at `0x49cbb0` reads APPDATA/LOCALAPPDATA, builds a Windows cache
  location, writes a modified executable, sets file attributes, invokes hidden
  PowerShell `Add-MpPreference` with both path/process exclusions, and registers
  a Run value through `RegCreateKeyExW`/`RegSetValueExW`. These strings are
  first-byte XOR data and were decoded at their referenced addresses.
* The mapper at `0x4a07b0` checks MZ/PE headers, allocates/copies an image,
  resolves imports/relocations, applies protections, and calls image-base plus
  entry RVA through `syscall.Syscall` at `0x4a1a22`.

The unpacked payload's code confirms the Salat identity independently of the
external label. `getChromeLogins` at `0x8f2ce0` queries browser login records,
scans rows and calls `DecryptChrome`. The main task dispatcher at `0x8e27b0`
parses received tasks and invokes download, execution and collection handlers;
keyboard, screen, wallet and messaging-session collection routines are linked.
The browser collection, keylogging, tasking, Run-key and Salat detections already
fire accurately on this extracted stage and were preserved.

The packed stage and its automatic `!!upx@0` child each retain **8 hostile / 2
suspicious** findings. The explicitly unpacked stage retains **9 / 2**. The one
extra hostile finding there concerns LSASS token handling and was present before
these edits. No archive/decoded-stage attack coverage was lost. The outer
scanner still does not automatically reconstruct this custom encryption chain;
its three new hostile findings cover the visible wrapper. No runtime C2 success
or complete deployment context is claimed. Actual concealed Salat code and
unwanted installation/security exclusions explain the corpus provenance.

### Obfuscated NjRAT

The unsigned .NET/VB assembly has thousands of combining-character identifiers,
duplicate junk methods, arithmetic constant tables, and position-dependent XOR
string decoders. `dnfile`/`dncil` recovered CIL and tokens. A restricted evaluator
folded the table lookups/arithmetic/string decoders; it did not execute runtime
methods or native APIs.

The CLR entry token `0x0600008b` checks `Debugger.IsAttached`, calls FailFast if
attached, then calls the main routine. Decoded configuration identifies
`<- NjRAT 0.7d Horror Edition ->`, an install name `dllhost.exe`, a configured
host `mrbeast887.net.localtonet`, TCP port 7542 and a custom message delimiter.
Several installation/AV/VM switches are False or Disabled; capability presence
must not be reported as unconditional execution. The configured hostname is
not evidence that a connection succeeds.

* Method 89 connects TCP input to a length-framed buffer, writes received bytes
  into a MemoryStream, and starts a parameterized thread with `ToArray()`.
  Method 40 forwards that array to method 81, which decodes/splits commands and
  dispatches process launches, managed plugins, screenshots, registry operations
  and destructive commands. The new receive matcher binds the same buffer and
  stream field tokens across receive/write/thread dispatch.
* Method 137 repeatedly polls keys 0–255, tests the newly-pressed state 0x8001,
  translates characters, and appends foreground-window context and keys to the
  same field. It periodically stores records through method 93's RegistryKey
  SetValue routine. The new matcher binds the repeated field/Concat tokens;
  API declarations or polling alone do not convict.
* Method 99 reconstructs a 512-byte malicious boot sector, decodes
  `\\.\PhysicalDrive0`, opens it with GENERIC_ALL/OPEN_EXISTING, and calls
  WriteFile for 512 bytes. The embedded boot code prints the MBR overwrite
  taunt. The existing MBR rule now accepts that sector-write evidence even
  when the device path is encrypted. Taunt-only and writer-only controls fail.
* Method 88 exposes NtSetInformationProcess class 29 (BreakOnTermination).
  This and AV-disabling, scheduling and cleanup paths were inspected; their
  encrypted configuration strings are not promoted to automatic runtime claims.

The new hostile findings cover key recording, destructive boot-sector writing,
and TCP tasking in that destructive keylogger. Remaining coverage limits:
static rules do not generically decode this arbitrary managed string scheme,
so precise encrypted Run-key/Defender command findings and the configured C2
endpoint are still unavailable directly from the original scan. The code paths
were decoded and checked manually; no hostname-specific or duplicate rules
were added to raise the score.

### Scapy

The complete 1,474-byte file imports `scapy.main.interact` and calls it. It is
byte-identical to [the upstream v2.4.0 launcher](https://raw.githubusercontent.com/secdev/scapy/v2.4.0/bin/scapy).
The exact PyPI `scapy@2.4.0` source archive was fetched with forager, checked,
and compared; this launcher alone does not uniquely establish an installed
Scapy version. Upstream `main.py` initializes the interactive session, loads
normal user-selected startup files, and opens the configured Python/IPython
shell. There is no hidden downloader or implant in this launcher. It depends
on the installed module/startup configuration, which were not supplied.

The comment's legacy secdev.org documentation URL was also attempted with
forager. That site failed certificate verification; upstream GitHub and the
versioned PyPI archive supplied the source/dependency evidence instead.
Collection could reflect Scapy's dual-use packet crafting/sniffing role, an
associated toolkit, or a source mislabel. None proves malicious deployment of
this particular launcher. The benign marker records this evidence and does not
assert that missing host-side configuration is trustworthy.

## Corrections and coverage checks

* Boxed `##` comment padding no longer counts as Markdown headings. Ordinary
  four-heading Markdown controls still match; all identity/import findings stay.
* An extracted run beginning after a high-bit padding byte is not a real netcat
  command boundary. Native scans now use actual bytes, including legitimate NUL
  string boundaries; scripts retain the original matcher. Existing consumers
  keep the canonical `::nc` union. Similarly, Unicode identifier suffix 27017
  is excluded while real native/script MongoDB-port references remain.
* The engine omits simple any-union composites from displayed findings, while
  resolving them for consumers. The native/source primitives remain visible.
  No accurate attack signal was removed to change a classifier score.
* Go's repeated ChaCha sigma-state stores are excluded only from reconstructed
  string evidence; all ChaCha detections remain. A non-cipher native path built
  from immediate stores still matches. `format-n-writable` accurately reports
  literal markers in writable padding and makes no printf-execution claim.
* LSASS/atop and German findings now describe the matched name/word tokens;
  incidental tokens in padding do not establish process targeting, monitor use
  or actual German prose. Matchers/severities are retained.

Shared consumers were inspected before edits. A HEAD rules snapshot in scratch
was used to compare existing fixtures and new positive/near-miss controls.
No original hostile/suspicious trait or extracted-stage attack finding was lost.

Generate inert structural PE fixtures and check saved reports:

```sh
python3 testdata/concealed-rat-review/generate.py SCRATCH/controls
CLEAVE_VALIDATE=0 cleave --traits-dir . --format json SCRATCH/controls \
  testdata/concealed-rat-review/headings.md \
  testdata/concealed-rat-review/controls.sh \
  testdata/taxonomy/cc-audit-older-releases/hex-netcat-loop.sh > SCRATCH/controls.json
python3 testdata/concealed-rat-review/check.py SCRATCH/controls.json SCRATCH/controls.before.json
```

The generator contains small instruction excerpts and inert strings, not the
original payloads. Key recording without consistent field tokens, polling
without recording, mismatched XOR keys, taunts without writes, and writes
without a destructive payload are negative controls. Original samples and the
independently recovered Salat stage supply the non-synthetic positive evidence.

Validation refinement: the complete managed recording pattern is suspicious
on its own; its hostile composite additionally requires TCP and registry-write
references. The encoded Defender command is suspicious alone; its hostile
composite requires the PE mapper. Standalone commands/recorders are not
convicted without that additional context. The MBR alternative is a named
attack-context trait requiring the taunt plus managed sector-write pattern.

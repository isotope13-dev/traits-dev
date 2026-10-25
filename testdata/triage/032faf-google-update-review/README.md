# Google Update infected host and BusyBox shell tests

Reviewed originals:

| SHA-256 prefix | Identification | Verdict | Hostile before/after | Suspicious before/after |
|---|---|---|---|---|
| `032faf98349a` | GoogleUpdateSetup.exe carrying a native polymorphic PE infector | MALICIOUS | 0 / 1 | 1 / 2 |
| `dbbae63d8095` | BusyBox `star.tests` argument-expansion test | BENIGN | 0 / 0 | 0 / 0 |
| `c43664117dff` | BusyBox `glob_and_assign.tests` glob/assignment test | BENIGN | 0 / 0 | 0 / 0 |

`comparison.json` records the final atomscan comparisons, including separately
recovered stages and their UPX child. Do not add inherited parent findings to
child findings when counting distinct behaviors.

## Executable recovery and execution paths

The original is a 32-bit Windows GUI executable with Google Update Setup
1.3.36.152 resources and Omaha bootstrapper code. Its signature directory is
cleared, while old certificate material remains in the overlay. Those facts
alone do not establish an attack. Its actual entry path does:

1. Entry VA `0x404f0e` traverses arithmetic junk and overlapping opaque
   branches. At `0x405024`, a call/pop stub XORs 70 inline bytes with `0x5f`
   and returns into them. The recovered code preserves a code pointer through
   MMX and transfers to `0x559207` in the extended executable `.reloc` section.
2. At `0x55a8ec`, another call/pop obtains a code-relative parameter block.
   The decoder at `0x55a902` multiplies its state, adds 19, rotates left by
   three bits, XORs a byte, and adds the recovered plaintext byte back into
   its state. It increments the buffer pointer, decrements the byte count,
   and ultimately jumps into the decoded buffer. This specimen uses
   `TEST ECX,ECX`, where earlier supported specimens used `OR ECX,ECX`.
3. Bounded Unicorn CPU emulation, without Windows API execution, recovered
   the modified image and stopped on the first unmapped PEB access at
   `0x55c314`. The recovered mapper walks the PEB and the kernel export table
   to resolve GetProcAddress, then resolves VirtualAlloc, Beep and
   LoadLibraryA. It allocates executable memory and RC4-decrypts the embedded
   DLL. The trailer provides the eight-byte key `be1ea8e5cb9d0115`, payload
   RVA `0x15c650` and length `0x8c00`.
4. The mapper checks MZ, copies image headers and sections, applies HIGHLOW
   relocations, resolves imports and calls the mapped DLL with
   DLL_PROCESS_ATTACH. It then resumes the original host entry. No network
   traffic or successful Windows execution was needed to establish this path.

The extracted 35,840-byte UPX DLL has SHA-256
`ec55c4ba2ab0b530c4d613e9c0214611c734fc0d17e2fabec68ade33b980075c`.
UPX decompression produces a 76,800-byte DLL with SHA-256
`515fe2a9947e5f0d0df3bb67e4ec9cbdca55901249e5b8127704d9424a4766d2`.
These hashes independently agree with earlier recovered infections documented
in `testdata/triage/feedback-resource-20261024` and
`testdata/triage/good-pool-20261024/native-infector`.

Disassembly of the recovered DLL establishes the following reachable behavior:

- DLL entry `0x6240d1ed` initializes scanner state and starts download, cleanup,
  file-scan, drive-autorun and Run-key-scan threads. It then calls
  ExecuteTrampoline to restore the host's saved entry bytes.
- `InfectFile` at `0x624054fe` maps target executables, generates metamorphic
  and encrypted stages, patches entry code, extends image/section sizes,
  sets executable/write permissions, clears ASLR/NX and the security
  directory, flushes the mapping and restores timestamps and attributes.
  Header mutation is visible at `0x62406516`; SetFileTime at `0x62406750`.
- Recursive directory workers call InfectFile. `RegScanThread` at
  `0x624074b8` reads HKCU's Run values, extracts executable paths and infects
  them at `0x624076ce`. This is not evidence of a Run-key write.
- `CreateAutoRun` at `0x6240cbf2` packages the infector on fixed/removable
  drives and calls CreateProtectedAutorun. The latter writes autorun.inf
  with open/explore/autoplay commands, hides it with system attributes and
  locks it. The command targets are the replicated executable.
- `DownloadAndUpdate` at `0x624010c2` connects to `updatewin.ddns.net:8000`,
  sends DOWNLOAD and a requested filename, receives a bounded four-byte
  length, sends READY, and accumulates payload bytes. It writes that buffer
  to a randomly named temporary executable, checks the written length and
  launches the same pathname with CreateProcessW at `0x624015aa`.
  The endpoint was not contacted and the remote payload was not recovered.
- `CleanAllUsersTemp` at `0x624015f5` enumerates user profiles, constructs
  their AppData\\Local\\Temp paths and deletes enumerated `*.exe` and `*.rar`
  files at `0x62401872` and `0x62401933`. This targets other files, beyond its
  own temporary payload.

Unauthorized executable infection and drive propagation decisively support
MALICIOUS. No deployment context was supplied. The many family names in the
collector's filename do not establish family attribution.

## Shell test provenance and effects

Both samples match every byte and the SHA-256 of BusyBox 1.36.1 sources fetched
with forager, including retained `.forage.json` provenance:

- [star.tests](https://raw.githubusercontent.com/mirror/busybox/1_36_1/shell/ash_test/ash-vars/star.tests)
  re-execs the harness-provided shell with fixed arguments when invoked
  without arguments, then prints unquoted and quoted `$*` expansion. It has
  no hidden stage, network target or dependency to fetch. The notable variable
  command execution finding is accurate and remains unchanged.
- [glob_and_assign.tests](https://raw.githubusercontent.com/mirror/busybox/1_36_1/shell/hush_test/hush-glob/glob_and_assign.tests)
  creates two named local empty fixtures, compares globbing in assignments,
  arguments, built-in echo and `/bin/echo`, and removes precisely those two
  fixtures. The notable local-file deletion finding is accurate and retained.

After source review, the tests were run in an isolated scratch directory using
`/bin/sh` and a fixed THIS_SH. Both exited zero, printed the expected expansion
forms and left only their test scripts. The unknown external labeling pipeline
may have inherited an archive/package label or overreacted to shell syntax;
that is an explanation of a possible mislabel, not an asserted deployment fact.

## Trait changes and retained coverage

- Both decoder atoms now accept OR and TEST zero checks. Multiplication,
  rotation, plaintext feedback, inline return and final transfer requirements
  remain intact; keys, addresses, lengths and filenames are not fixed.
- A notable metadata observation records high-entropy RWX `.reloc` sections
  below 64 KiB. The prior large-section rule retains its exact scope and
  exclusions. The parasitic-entry composite accepts the smaller section
  while retaining both required execution-producing decoders.
- The original `brand`/`manufacturer` parameter match did not establish a
  device, reporting or even HTTP use: it matched the Omaha installer tag's
  `brand=ONGR`. Its supported syntax is preserved as
  `communications/url/query::brand-manufacturer-parameter`. Device-qualified
  model syntax is preserved separately as `device-model-parameter` in the
  same leaf. Only that qualified observation feeds the device-identity
  aggregate. The generic brand observation is not suppressed or demoted.
- A new hostile payload composite combines the existing native TCP buffer
  write/process-launch chain with the existing recursive PE-infector
  detection. This supplies attack admission without treating ordinary updater
  behavior as hostile. The recovered DLL gains a fifth hostile behavior;
  its four previous hostile and four suspicious findings remain intact.
- Review of the full 100-rule payload-file-execution catalog identified a
  misplaced context group: a quoted Run token or Run-method call established
  neither WSH, obfuscation nor payload execution. Its exact scope, predicate,
  confidence and component criticality move to
  `metadata/lang/source/shape::javascript-run-token-or-call`. Its sole exact
  consumer was updated; no ancestor directory selectors consume the old
  group. This preserves its source observation and the WSH payload rule's
  boolean condition, while keeping the payload catalog within its budget.

Consumers and earlier positive fixtures were inspected before changes. Forager
recovered two original infected hosts outside this batch, SHA-256 prefixes
`74ef3a48c097` and `c9799fd16c6b`, and both retained all prior detections in
before/after scans. Decoder controls cover renaming, both zero-test spellings,
missing inline return, missing plaintext feedback and non-executable relocation
data. The OR variant additionally exercises the engine's recognized native
recovery path. A recovered-DLL control changes the TCP buffer argument while
retaining infection evidence; the new TCP payload composite must not match it.
Telemetry fixtures verify retained device-qualified positive matches, preserved
generic brand/manufacturer observations and installer/AI-model near misses.

## Remaining detection and classifier gaps

The submitted executable has **one hostile finding**, below the requested
3–5 goal. Its actual drive worm, timestamp preservation, file infection and
TCP payload activation live behind feedback encryption, RC4 and UPX. The
separately recovered DLL has five hostile findings, but these must not be
fabricated on the original ciphertext.

The current native recovery implementation in Cleave's
`src/extractors/metamorphic_graft.rs` requires the OR-zero-test bytes in its
DECODER constant. This specimen uses TEST. The equivalent OR control exposes
the recovered DLL and its UPX child; the original exposes neither child.
YAML decoder coverage is fixed here; that extraction gap requires an engine
change. No shared rule was weakened to inflate the original's count.

The cross-user Temp purge still lacks a specific path-bound finding. Its
enumeration, path construction and DeleteFile calls were disassembled;
generic deletion and Temp strings do not bind the entire target set in a
YAML composite, and are insufficient for a hostile purge claim. The existing
native TCP receive/write/launch matcher was inspected and used to close the
separate recovered-stage download-execution gap.

The v18.18 atomscan classifier remains BENIGN for the original despite its
hostile finding (malicious probability approximately 0.89718 to 0.98526,
`lvl: -1`). It warns that feature version 18 predates version 21. This is a
classifier miss, not grounds to restore the inaccurate telemetry claim or
duplicate hostile findings. Both BusyBox samples remain classifier-benign.
Exact stage classifier results are in `comparison.json`.

All scans, facts, recovery scripts, disassembly, controls, fetched originals
and provenance are retained in:
`/usr/local/var/cyclotron/tmp.noindex/cyclotron-90084b2c/scratch/bad-032faf-review`.
The final required repository check is `make validate`.

# Reasoned review of the Fallout sample batch

All three supplied files were scanned with Atomscan and inspected with
`cleave facts` before editing traits. Specimens and their commands were never
executed. Original hashes are unchanged. Raw reports, facts, annotated native
disassembly, CIL, recovered images and Forager provenance are in the scratch
directory recorded in `review.json`.

## Judgments and execution evidence

* **frida-anti-analysis.py — BENIGN.** This 269-byte file matches the existing
  anti-analysis boundary fixture byte for byte. Its complete program lists
  `/proc`, reads process command lines, checks Frida/gdbserver names, prints a
  warning and raises SystemExit. It contains no payload, collection, network,
  persistence or destructive action. This minimal gate is insufficient to
  convict the artifact; the actual anti-analysis behavior remains suspicious.
  Deployment and authorship are unknown. It also lacks handling for non-process
  procfs entries and read failures, so successful execution is not assumed.
* **38b21e601cbd — MALICIOUS: Go file infector carrying GravityRAT GX.** The Go
  pclntab was decoded independently to associate call targets with names.
  `main.main` walks `C:\Program Files\` through `main.visit` (VA 0x62c450).
  That callback reads a visited file, obtains mutated self bytes, overwrites
  the path and writes an additional `.exe` image with generation marks and
  random padding. `plant_start_up` (0x62cba0) writes random executable names
  under System32; `add_startup` (0x62cae0) opens the HKLM Run key and sets its
  value. These are concrete unwanted modifications, independently of the
  embedded RAT. Success depends on permissions and the damaged instructions
  in this collected image; no privilege bypass is asserted.

  `get_self_mutated_bytes` (0x62cf80) decodes the embedded Base64 image and
  appends it to the supplied self-image buffer, followed by padding. Decoding
  its 0xd705c-byte constant at raw offset 0x2ca606 recovers a 660480-byte LSASS
  image plus a 69-byte footer. The image hashes to
  `1c0ea462f0bbd7acfdf4c6daf3cb8ce09e1375b766fbd3ff89f40c0aa3f4fc96`,
  the GX executable in [Talos's published analysis](https://blog.talosintelligence.com/gravityrat-two-year-evolution-of-apt/).
  This verifies the family independently of trait names and collection labels.
  Several raw images overlap later resource data; they are not independent
  malware families. The unit labeled Mono.Cecil by extraction contains the
  LSASS executable. The real Mono.Cecil resource was recovered separately.

  CIL tracing follows Program.Main -> Services.Start -> RootJob/TaskJobs.
  The report includes account/domain/host identifiers and is sent by
  UploadValues to the GX endpoint. A five-minute timer retrieves server tasks;
  task arguments reach hidden `cmd.exe /c` execution with redirected output,
  which UploadManager sends through UploadFileTaskAsync. Drive scanning selects
  documents; logical-disk arrival stages USB files and a ten-minute timer
  uploads them. Separately, ProcessManager enumerates running processes,
  formats a report, writes it and sends the same path through UploadManager.
  WMI BIOS/system/thermal probes feed VM detection. These paths justify the
  command, document, identity and new process-report detections. No execution
  handoff from the Go entrypoint into an appended RAT was established.
* **PXT 0.14.11 — BENIGN.** Forager recovered the versioned Go-proxy archive
  with the exact supplied SHA-256, preserving its provenance sidecar. Its
  package identity and code implement Microsoft MakeCode/PXT. WinRT file
  activation reads a selected firmware/project file; deployment writes compile
  output only to target-filtered removable drives. Serial/HID paths connect the
  editor to hardware. The local server checks its token for protected APIs and
  WebSocket routes. TouchDevelop's eval sites initialize generated scripts and
  precompiled plugins; the Electron updater downloads a configured release and
  launches its installer on quitAndInstall. Those execution capabilities fit
  the product's purpose. The included HTTP/HTTPS AppX rules really grant full
  WinRT access to local development and hosted editor origins. All four
  manifest findings remain suspicious; provenance does not erase that grant.
  Future hosted content and a particular machine's deployment are unknown.

## Changes and preservation checks

The Python detector previously inferred exit from a single warning string.
Its replacement requires executable membership-triggered SystemExit syntax,
near procfs enumeration/path evidence and the debugger names. Its description
explicitly states co-occurrence rather than unproven variable flow. The old
warning text remains a notable reference. A changed/missing warning still
matches a real gate; a warning alone, no exit, an unconditional exit, or absent
tool names does not. The old synthetic `analysis-gate.py` fixture only assigns
path strings and raises; it no longer supplies the unsupported hostile claims
that depended on the warning text. Its warning/path/tool observations remain.
The existing fixture expectations were updated to describe those facts.

Added the hostile infection-task process-report upload profile and a neutral
process report template observation. It requires admitted implant/task context,
process enumeration and process/machine report fields. Ordinary process lists
or ordinary HTTP clients alone do not qualify. The original GX image matches;
removing only the process report template removes the new profile while
retaining all five prior hostile findings. The real extracted Mono.Cecil DLL
has zero hostile/suspicious findings.

Six name-only Go observations moved out of infection/persistence into metadata,
retaining matchers, scopes and notable severity. Their descriptions now assert
routine-name references. Exact behavior and GoMiner consumers were updated.
Because the existing name leaf already contained 100 rules, every member was
reviewed and placed by required name qualification: `qualified` requires a
namespace/package/receiver; `token` makes no qualification requirement.
The 100 preexisting effective definitions are unchanged, including defaults
and dependencies. The complete inventory and map are in
`symbol-name-migration.json`; no old observation was discarded. Parent selectors
still reach both children. The timing downgrade consumer was inspected; the
real sample retains every prior suspicious finding. The synthetic qualified
name versus bare name controls, existing worker-name suite, Mirai symbol
positive and prose near miss verify placement and retained attack coverage.
Active exact-ID test manifests and consumers were updated; dated historical
scan records retain their original IDs.

## Scan comparison

Counts are distinct hostile/suspicious IDs across all analyzed units, including
embedded/archive members. `review.json` also records occurrences and member
deltas. The Windows sample's occurrences are 47 -> 56 hostile and 29 -> 29
suspicious: the added behavior matches nine LSASS analysis units.

| Sample | Verdict | H before -> after | S before -> after | ML alert level |
| --- | --- | ---: | ---: | ---: |
| Python gate | BENIGN | 0 -> 0 | 1 -> 1 | -1 -> -1 |
| Go infector / GravityRAT | MALICIOUS | 7 -> 8 | 3 -> 3 | 25 -> 25 |
| PXT 0.14.11 | BENIGN | 0 -> 0 | 1 -> 1 | 0 -> 0 |

There are no material detection losses in any supplied sample. All 482 units
and every finding in the PXT `--follow=none` comparison are identical before
and after. Default-follow scans expand current documentation/CDN assets and
are recorded separately; they do not indicate an archive modification or a
dependency exception. No hostile/suspicious finding originates in those fetched
assets. The remaining classifier disagreement is PXT's hostile alert
(probability 1.0). Python remains unalerted (0.743614 -> 0.802603); the Windows
file remains hostile (0.995). The installed model reports feature specification
v18 while the engine expects v21. No inaccurate rule was retained to influence
these scores.

`check.py` passes 19 assertions across eight static controls. The existing
worker-name suite passes four controls. Isolated GX, the process-template
negative, the real library, and both Mirai controls were scanned separately.
The required final full check is `make validate`; its log is retained in the
recorded scratch directory.

The three judgment markers were written beside the original samples, with
these exact lines also prepared verbatim in the scratch commit body:

```text
Python tool gate: only reports and exits; retain anti-analysis
Go infector + GravityRAT: file rewriting, Run key, command/file theft
PXT 0.14.11: verified upstream firmware tooling; retain WinRT grant
```

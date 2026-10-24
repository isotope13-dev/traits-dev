# Three-artifact review, 2026-10-24

The originals are identified by SHA-256 in `comparison.json`. Findings and
classifier outputs are separate from the reviewed verdicts. No specimen was
launched on Windows. CPU emulation stopped at the loader's first PEB access;
its purpose was recovery of self-modified bytes, with no Windows API emulation,
network connection, or host filesystem effects.

| Original | Identification | Verdict | Hostile before → after | Suspicious before → after |
|---|---|---|---:|---:|
| 74ef3a48c097… | Adobe bootstrapper infected with an encrypted native PE infector | MALICIOUS | 0 → 1 | 1 → 1 |
| 1f807f99a2e6… / Proteus.md5 | Checksum sidecar, 33 bytes | BENIGN | 0 → 0 | 0 → 0 |
| 36deb53571db… / local1.right | BusyBox ash test expected output, 26 bytes | BENIGN | 0 → 0 | 0 → 0 |

## Executable behavior and verdict

The outer image has Adobe Bootstrapper Small 20.6.20034.366983 resources and
substantial original installer/CRT/MFC code. That identity does not establish
benign intent, and unsigned status does not establish impersonation. Its
entry code actually takes an unrelated obfuscated execution path:

1. Entry VA `0x421c21` executes arithmetic junk and opaque branches, then reaches
   the call/pop XOR decoder at `0x421cf4`. It decodes 62 inline bytes with `0x5f`
   and returns into them. The decoded block preserves a code pointer through
   MMX and transfers to `0x477494` in the extended executable `.rsrc` section.
2. More junk precedes the feedback decoder at `0x4789b1`. Its state starts at
   `0x62384491`, multiplier is 1, increment is 19, rotation is left by 3 bits,
   and each recovered plaintext byte is added back to the state. It decodes
   `0xb00f` bytes and jumps into the decoded buffer. The increment instruction
   is `ADD EAX,imm8`, equivalent here to the existing rule's `LEA EAX,[EAX+imm8]`.
3. The recovered loader at `0x47a957` walks PEB loader structures and kernel
   exports to resolve GetProcAddress. It obtains VirtualAlloc and LoadLibraryA,
   RC4-decrypts an embedded PE at RVA `0x7aca0`, and manually maps it: headers
   and sections, HIGHLOW relocations, import resolution, and DLL_PROCESS_ATTACH.
   It then restores the original host entry bytes through the DLL's trampoline
   routine and resumes the host. Unreferenced Authenticode material remains in
   the overlay after the security directory was cleared.
4. RC4 recovery yields a 35,840-byte UPX DLL with SHA-256
   `ec55c4ba2ab0b530c4d613e9c0214611c734fc0d17e2fabec68ade33b980075c`.
   UPX decompression yields a 76,800-byte native DLL. Its entry `0x6240d1ed`
   starts the downloader, temp cleaner, infection scanner, drive autorun worker
   and Run-key scanner, then calls ExecuteTrampoline. These are reachable
   workers, not just exported names or diagnostic strings.

Relevant recovered DLL paths were independently disassembled:

- `InfectFile` at `0x624054fe` maps target executables, generates encrypted and
  metamorphic stages, patches entry code, extends a section and image, sets RWX
  permissions, clears ASLR/NX and the security directory, flushes the mapping,
  and restores timestamps and attributes. Header mutations are visible around
  `0x62406516`; SetFileTime is called at `0x62406750`.
- `CreateAutoRun` at `0x6240cbf2` creates executable packages on drives and calls
  `CreateProtectedAutorun` at `0x6240c91e`. The latter writes autorun.inf with
  open, explore and autoplay commands, sets hidden/system attributes, and locks
  the file. This is drive-navigation hijacking and propagation, not an ordinary
  autorun path reference.
- `RegScanThread` at `0x624074b8` opens HKCU's Run key with read access, enumerates
  value data, extracts executable paths, and calls InfectFile at `0x624076ce`.
  It does **not** establish a Run-key write. No registry-write persistence claim
  was added for it.
- `DownloadAndUpdate` at `0x624010c2` connects to updatewin.ddns.net on TCP 8000,
  exchanges DOWNLOAD/READY protocol messages, receives a bounded size and bytes,
  writes a random temporary executable, checks its written length, and launches
  that same path with CreateProcessW at `0x624015aa`. No server response or final
  downloaded executable was observed; neither is required to establish this
  static download-and-execute path.
- `CleanAllUsersTemp` at `0x624015f5` enumerates user profiles, constructs each
  `AppData\Local\Temp` directory, enumerates `*.exe` and `*.rar`, and calls
  DeleteFileW on the constructed results at `0x62401872` and `0x62401933`.
  This deletes other files in user Temp directories, not only this program's
  own staging file.

Executable infection, hidden drive reactivation and unsolicited payload
activation tip the verdict decisively to MALICIOUS. No deployment context was
provided, and attribution to the ransomware/RAT names in the collected filename
is unsupported. The sample is best identified as an infected Adobe host carrying
a native polymorphic file infector, without assigning a speculative family.

## Inert artifacts and provenance

Proteus.md5 consists solely of the line
`49fd4020bf4d7bd23956ea892e6860e9`. Exhaustive byte inspection establishes that
there is no executable stage, script, URL, dependency or additional content.
Forager resolved that MD5 to a separate 2,930,176-byte obfuscated .NET Windows
Forms executable, gchrome.bin, SHA-256
`d23b4a30f6b1f083ce86ef9d8ff434056865f6973f12cb075647d013906f51a2`.
Its MD5 was verified locally; the downloaded executable and its `.forage.json`
are retained in scratch. Its managed entry and metadata were also inspected.
The source's Proteus label pertains to that other executable, and collection
sidecar ingestion plausibly explains the checksum's hostile label. The actual
labeling pipeline is unknown. The checksum itself is BENIGN. Its three existing
checksum-format observations are accurate and unchanged.

local1.right exactly matches the SHA-256 and every byte of BusyBox 1.23.2's
[ash local-variable expected output](https://raw.githubusercontent.com/mirror/busybox/1_23_2/shell/ash_test/ash-misc/local1.right).
The adjacent [test script](https://raw.githubusercontent.com/mirror/busybox/1_23_2/shell/ash_test/ash-misc/local1.tests)
sets a variable, shadows/unsets it in a function, and prints its values. The
sample is the expected output, not that script. There are no references or
executable contents to follow. An inherited package/container malware label is
a plausible explanation; the actual source of the mislabel is unavailable.
Forager returned HTTP 200 but rejected the 26-byte response as an empty body;
a direct upstream retrieval verified the exact hash after that failed attempt.
Both upstream files and source records are retained in scratch.

## Rule corrections and coverage preservation

- The feedback decoder atom now accepts both ADD and LEA increment spellings.
  The remainder of its multiplication, rotation, plaintext feedback and final
  jump pattern is unchanged. Its sole composite consumer was inspected.
- The existing parasitic-entry composite retains its old high-entropy RWX
  `.reloc` alternative and now also accepts executable `.rsrc`. Both decoders
  and the writable entry section remain required. Nothing was weakened away
  from the retained relocation variant.
- A suspicious decoder composite records inline XOR execution together with
  the feedback decoder and writable executable code. It claims concealment,
  rather than inferring a C2 protocol or unobserved payload behavior.
- Adobe description, product and combined identity observations moved from
  masquerade objectives to `metadata/binary/provenance/version-info`. The
  combined identity is notable, rather than an incomplete component.
- The former suspicious unsigned-Adobe masquerade rule asserted deception
  solely from identity and a missing signature record. That unsupported claim
  is replaced by the notable `unsigned-adobe-bootstrapper-versioninfo` property,
  with its original predicates and platform-signature exclusion preserved.
  Its MPRESS attack consumers retain their packing and alteration evidence.
  These are semantic/taxonomy corrections, not score adjustments.
- Four raw resource-text observations previously filed under VERSIONINFO moved
  to `metadata/binary/resource/identity`: Updater.exe, Updater, Adobe Installation
  Helper, and host.exe. They did not require a version field. Exact consumers
  were updated, effective predicates/scope compared to HEAD, and ancestor
  resource/provenance consumers inspected. The version-info leaf remains at
  its 100-rule budget. The resource-identity leaf has 85 rules.

The original loses four old IDs, all replaced by correct metadata IDs. It loses
no supported capability or attack behavior. Every other original finding is
retained. The separately recovered infected host `c9799fd16c6b…` gains one hostile
and one suspicious finding, with no lost findings. Its original bytes came from
Hopper through forager, with provenance retained in scratch; it is outside this
batch and has the LEA-form decoder. The DLL has the same four hostile and four
suspicious findings before and after these YAML edits. Its accurate infection,
timestamp-preservation and drive-worm detections were left intact.

`controls.json` records scans of renamed, LEA-form, missing-feedback,
missing-inline-execution, non-executable-resource and plain unsigned-Adobe
metadata controls. These verify the distinguishing required evidence and that
ordinary unsigned Adobe metadata is no longer called impersonation. The two
cipher spellings and the external infected-host positive retain detection.
`scope-preservation.json` records the four exact effective-scope comparisons.

## Remaining engine and classifier gaps

The **original** has only one hostile trait, below the requested 3–5 goal.
The scanner reports one file and does not expose the feedback/RC4/UPX DLL as a
child, even though independent recovery validates it. The native loader's
later bytes are behind a stateful feedback transformation; YAML's existing
encoded-string matchers do not implement that transformation. Broader neutral
API/import combinations were inspected but do not bind those APIs to decrypted
payload paths. No inferred drive autorun, timestamp restoration, TCP update,
manual-map activation or temp-purge finding was fabricated on ciphertext.
The recovered DLL separately has four hostile findings across infection,
timestamp evasion and drive propagation, but its TCP update and cross-user
Temp purge still lack specific hostile detections; generic receive, launch and
delete capabilities do not establish their data flow. Further coverage requires
child recovery in the engine and suitably bound code/data-flow matchers.

The installed v18.18 classifier renders the original BENIGN before and after,
despite its new hostile static finding. Reported malicious probabilities are
0.9713183 → 0.99105364, with `lvl: -1`; calibrated classification remains benign.
The engine warns that feature version 18 predates version 21. Both inert text
files remain classifier-benign. No inaccurate trait was restored or duplicate
hostile trait added to influence those scores.

All scan/facts JSON, fetched artifacts and provenance, emulation output and
method disassembly are retained under
`/usr/local/var/cyclotron/tmp.noindex/cyclotron-90084b2c/scratch/trait-review`.

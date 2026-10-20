# First reasoned review of the supplied bytes

All three verdicts are **MALICIOUS**. They follow from code and recovered
payloads, not collector filenames, model scores, family rules, or prior
repository review records. No sample was run on Windows. Analysis used
`atomscan`, `cleave facts`, Rizin, pefile, Capstone and static UPX decompression.
Generated binaries, full disassembly and scan JSON remain in the task scratch
directory, `scratch/review-fallout`.

| SHA256 prefix | Identification | Deciding evidence |
| --- | --- | --- |
| `324f35bc4213` | StormAttack persistence/DLL-injection loader with erased DLL code | Active Setup self-copy/relaunch, alternate LanmanServer ServiceDLL replacement, remote LoadLibrary thread and shell self-deletion |
| `3d175318256b` | Floxif-infected Intel Installation Framework executable | Diverted entry, encoded saved host bytes, mapped Floxif DLL and return to the host |
| `7ba7fbe05438` | Damaged StormAttack wrapper with packet-tasked flood DLL | Received records select attack builders; raw UDP sendto bursts repeat until stopped |

## 324f35bc4213

The GUI PE's entry at VA `0x402674` reaches dispatcher `0x401cb0`.
The mode DWORD at `0x404120` is 3. The selected branch calls `0x401900`
and then `0x401390` at `0x401f8a`/`0x401f8f`.

`0x401900` constructs a GUID-named HKLM Active Setup Installed Components
subkey, writes a REG_EXPAND_SZ StubPath (`0x401a4b`), reads its own executable
using CRT file I/O, patches a copy, writes it with fwrite (`0x401b26`), and
relaunches the new path with CreateProcessA (`0x401b7e`). Cleanup obtains the
module path, converts it to a short path, reads COMSPEC, constructs `/c del`
with that path and `> nul`, creates the shell and resumes its thread
(`0x4014b8`/`0x4014d9`).

Alternative mode 1 extracts resource type DLL, ID 101 through `0x402460` and
the CreateFileA/WriteFile helper. `0x401260` replaces LanmanServer's ServiceDLL
registry value with a System32 DLL path. `0x401150` starts a calc/notepad/IE
child, allocates remote memory, writes a DLL pathname, resolves
Kernel32!LoadLibraryA, and passes that export and the remote pathname to
CreateRemoteThread (`0x40123d`). These are retained code paths, not evidence
that mode 1 was selected or installation succeeded. Mode 2 contains service
self-installation and a resource-injection service callback.

The DLL at file offset `0x5060`, length `0x9c00`, has SHA256
`0df2765cead245e3a89f9fafbbe5eb42ec7d41386a6c6dc235827539171335fd`.
37,736 of its 39,936 bytes are zero. Imports and entry code are erased; entry
RVA `0x741a` contains zero instructions. Its residual Storm/HTTP/API strings
do not establish a functioning downloader or flood payload. Existing loader
findings correctly describe code, and the damaged child has no hostile or
suspicious traits. No additional payload behavior is attributed to it.

The DLL damage, legacy resolved IAT contents and image-copy patch offsets
limit deployability. They do not explain the surviving attack paths as an
ordinary installer. Machine history, intended deployment and successful
execution are unknown.

## 3d175318256b

Resources identify an Intel(R) Installation Framework 1.4.3.0 / ICCS Setup.exe
host with a Visual Studio setup.pdb path. Those unverified declarations alone
would not prove vendor provenance. Its normal installation/service-management
purpose does not explain the additional parasitic loader.

At VA `0x42a8f8` the executable's entry is a JMP to `0x425faa`. That stub
saves registers and walks the PEB to resolve GetProcAddress. Calls to
`0x423df0` and `0x423e12` advance the saved return address by two or four
bytes, respectively, skipping deliberately invalid inline instructions.
The string routine at `0x423e22` decodes each byte as NOT(byte XOR key)
and marks the string record decoded.

The loader opens and reads its own image, copies five bytes from file-size
minus 29 (`0x4251ea`), decodes them, changes entry-page protection, and restores
them (`0x42532a`..`0x42536d`). The recovered original bytes are
`E8 67 AB 00 00`. The footer's last six DWORDs hold encoded recovery offsets.
Key updates before recovery yield `0x3a` for payloads and `0x29` for saved
entry bytes. Subtracting `0x3a` from the final DWORD yields `0x14f000`.
The DWORD there is a length of 69,337, followed by a bytewise XOR/complement
encoded PE at `0x14f004`; another length-prefixed 8,905-byte block follows.
The two actual payload-transform loops are at `0x425570` and `0x4255d8`.

Decoding the first block produces SHA256
`de055a89de246e629a8694bde18af2b1605e4b9b493c7e4aef669dd67acf5085`:
a UPX-packed x86 DLL exporting FloodFix, FloodFix2 and crc32. Static `upx -d`
recovers an lpk.dll-named PE with ordinary .text/.rdata sections. The outer
mapper calls the DLL entry for process attach and resolves FloodFix2 before
the `0x425f9f` handoff.

In the unpacked DLL, FloodFix/FloodFix2 (`0x1000d48b`/`0x1000d728`) restore
host header/code state, fix relocations and return to the host's entry.
Floxif's infection routine includes an E9 entry patch (`0x100055d2`), removal
of the certificate directory (`0x100056b2`), writes of the modified image and
length-prefixed payload/footer (`0x100058da`..`0x10005a6a`), followed by
SetFileTime (`0x10005a86`). Directory enumeration loops use FindFirstFileA /
FindNextFileA. Decoding .data string records yields executable extension
filters `.dll`, `.ocx`, `.exe` and configuration names such as `autorun.inf`.
This supports parasitic infection, independently of the export names.

Ordinary service imports belong to the installer host and establish no
unwanted service persistence. That incorrect suspicious objective is removed
by relocation, while both hostile infection findings remain. No ransom,
credential theft or successful live network transfer is established.

## 7ba7fbe05438

The wrapper shares the injector code layout, with mode 3, but many strings
including the Active Setup and LanmanServer paths have been replaced with
random text. The existing rules correctly refrain from claiming those
persistence surfaces. The resource DLL at `0x3060`, length `0x9c00`, has
SHA256 `902cd7f4ff9cf3445c9e3dc94e712e442d737f2bb981a8a6c86941d1a348a685`.

Its entry RVA `0x741a` reaches `0x10007176`, which initializes configuration,
creates a mutex and starts a worker at `0x10006922`. That worker repeatedly
calls `0x10006974`: address resolution, TCP socket connection, a host report,
then record receiver `0x10006ac9`. At `0x10006b45` recv reads up to `0x528`
bytes. A positive return gates copying that same buffer into a record, whose
first DWORD drives task dispatch. Task 1 selects attack builders with fields
from that record; task 2 sets the shared stop flag.

Raw flood routine `0x1000228e` creates
WSASocketA(AF_INET=2, SOCK_RAW=3, IPPROTO_UDP=17). `0x10002353`..`0x10002380`
sends twelve packets per burst, sleeps for a configured interval, and loops
back to the stop flag. The original flood and packet-tasked family detections
are justified; this is not merely the presence of socket imports.

The task-5 download helper still contains URLDownloadToFileA resolution and a
download call. However, bytes around `0x10006907` replace the CreateProcessA
argument setup with ASCII-like conditional branches and invalid data flow.
The existing bound download/launch rule correctly does not fire. Other task
branches also contain corruption; retained shutdown functions must not be
reported as successfully reachable control actions without a valid path.
The configured host bytes transform into non-hostname bytes, so no usable C2
endpoint is established. Instructions lie in a non-executable .data section,
another execution limitation. These defects do not make packet-controlled
attack code consistent with ordinary software.

## Trait changes and checks

- Move the generic service-admin/configuration composite into
  `micro-behaviors/os/service/configure`, rename it to
  `service-admin-configure-api-profile`, and report it as notable. Preserve
  its positive conditions and exclusions; remove context-dependent demotion
  and inherited persistence mappings. Remove its now-unused exception.
- Move ChangeServiceConfig2W/A observations from service/host to
  service/configure, retaining matchers, exclusions, platforms and PE scope.
  Their descriptions now state API evidence. Update both exact consumers.
- Add a notable, direction-neutral indexed XOR/complement byte-store
  observation under data/encoding/xor. Its matcher fixes neither keys,
  addresses, payload names nor sample identity.
- Exact ancestor-selector audit found no consumers of the affected service
  or data/encoding parent directories. Existing configure rules describe
  different observations: Config2's advanced-settings API is distinct from
  ChangeServiceConfig's main service configuration API.

`check.py` passes ten offline controls: benign import-only PE, omitted Config2,
text-only W API near miss, ANSI name, omitted CreateService, transform positive,
removed XOR, removed complement, changed key slot, and identical bytes outside
.text. The benign service fixture has no persistence findings. Retired IDs
are absent; new observations remain notable.

Final atomscan rescans confirm four hostile loader findings for `324f35bc4213`,
two hostile infection findings for `3d175318256b`, and three hostile wrapper
plus two hostile payload findings for `7ba7fbe05438`. Only the infected
installer gains the XOR observation and corrected service capability IDs;
it loses the unsupported suspicious persistence finding.

The engine-generated percent-decoding observation on printf formatting is
not a YAML trait and proves no concealed endpoint. No exception was added for
it. No Remcos or WannaCry behavior was established from these bytes.

The supplied tria.ge / VirusTotal pages were inaccessible through the web
tool. Microsoft's [Shtormec description](https://www.microsoft.com/en-us/wdsi/threats/malware-encyclopedia-description?Name=Backdoor%3AWin32%2FShtormec.A)
corroborates the StormServer.dll / LanmanServer lineage, and its
[Floxif description](https://www.microsoft.com/en-us/wdsi/threats/malware-encyclopedia-description?Name=Virus%3AWin32%2FFloxif)
corroborates PE/DLL infection. Claims about other variants' drivers, antivirus
interference or downloaded malware were not transferred to these samples.

# Native TEA/Tofsee and bitmap/MSI review

Both original artifacts are MALICIOUS. Original SHA-256 prefixes are 9538e96ed214
and 79d7036b030d. Only static disassembly, bounded decoder emulation, and archive
extraction were used; no specimen was launched on the host.

## 9538e96ed214: TEA wrapper around Tofsee

Entry 0x404d7b reaches WinMain 0x4045e8. Opaque predicates surround dead import
calls. The live path calls 0x403ef0, allocates a 0xcb50-byte global buffer,
computes PAGE_EXECUTE_READWRITE as 0x20+0x20 in 0x403eb9, copies encrypted bytes
from VA 0x412510, and decrypts eight-byte blocks through 0x403df3/0x4035b5.
The TEA helpers subtract delta 0x9e3779b9 and construct the initial sum
0xc6ef3720 from 0xc6ef34e1+0x23f. The key comes from VA 0x42c220. A 42,383,741
iteration null-argument SetLastError loop precedes the jump through the same
buffer slot at 0x403ee4. This is code unpacking and a useless API stall, not
ordinary application data decryption or a child-process launch.

The 52,048-byte decoded shellcode resolves exports through the PEB, synthesizes
API names, applies an MSVCRT-LCG XOR stream, and decompresses LZO data. Emulating
only the pure decompression function produces 76,368 bytes. Its embedded PE at
0xe50 is 72,704 bytes. Its SMTP dispatcher at 0x40a7c1 constructs HELO/EHLO,
AUTH LOGIN, MAIL FROM and RCPT TO commands and passes the resulting buffer to
Winsock send at 0x40a893. Bot-state configuration, recipient/message macros,
delivery counters and tasking support Tofsee identification rather than a
normal mail client. At 0x4083c0 it decodes the Defender Exclusions/Paths key,
opens it under HKLM, and writes a zero REG_DWORD using RegSetValueExA. Its
remote-image routines allocate/write another process, transplant the PEB
image base, change thread context, and resume the suspended thread. The
extracted PE already has six hostile and three suspicious findings, including
Tofsee identity, exclusions and hollowing; those accurate rules were retained.

Original-container hostile/suspicious counts: **0/1 -> 1/3**. The new hostile
finding covers evasive TEA unpacking/execution; the two new suspicious findings
cover the pointer-bound buffer handoff and large API stall. The existing PDB
finding remains. WriteProfileSectionA moved from header-malformation metadata
to filesystem configuration with its matcher, confidence and PE/DLL scope
unchanged. Both exact consumers were updated; there were no broad ancestor
selectors requiring additional rewrites.

## 79d7036b030d: signed OpenVPN host with substituted crypto DLL

The fixed VHD contains NTFS volume `document`, a signed OpenVPN GUI 11.29.0.0
renamed to a PDF/PIF lure, genuine Microsoft vcruntime140.dll, and a hidden
unsigned libcrypto-1_1-x64.dll. The GUI imports that exact library. All 4,397
exports of the substituted DLL alias VA 0x180001000; they do not implement
OpenSSL. Its process-attach routine 0x180013ff0 loads bitmap resource 100 and
reads the pixels through GetDIBits. Stack XOR strings decode to Base64 AES key
and IV. AES-256-CBC decryption of the 752x752 RGB pixel array produces a
length-prefixed 1,658,880-byte MSI. It is written under TEMP and launched by
CreateProcessW using `msiexec.exe /i "{}" /Qn` at 0x18000e6ba. The wrapper
terminates its host after staging. There is no desktop screenshot acquisition
on this path: GDI is the embedded-data carrier.

The MSI claims Google Chrome 126.0.6478.63 but is an MSI Wrapper package. Its
custom action extracts a cabinet containing an unsigned native setup.exe.
The executable has extensive flattened dispatch and opaque arithmetic
predicates, XOR-masked strings, and an embedded cpp-httplib HTTP client.
The final endpoint and full final-stage purpose remain unresolved; generic
HTTP APIs do not establish C2, credential theft, or exfiltration. The recovered
MSI and CAB were separately scanned; the CAB packaging finding is not used as
proof of intent or as original-container coverage.

Original VHD hostile/suspicious counts: **0/1 -> 2/1** (unique inherited traits).
Members: PDF/PIF host **0/1 -> 0/1**, malicious libcrypto **0/0 -> 1/0**,
vcruntime **0/0 -> 0/0**, NTFS UpCase **0/0 -> 0/0**. The second hostile finding
correlates the signed crypto-importing host with the bitmap/MSI export-stub
DLL. It does not require the attacker-chosen host filename. The false whole
OpenSSL-library identity was removed only for export tables whose entries
all share one RVA. Export-name observations and crypto API references remain.
No accurate attack finding was lost.

## Controls and classifier limits

Ten focused cases pass: both malicious specimens, genuine OpenSSL 3 from the
official OpenVPN 2.6.12-I001 AMD64 MSI, genuine OpenVPN GUI, genuine Microsoft
runtime, and five semantic near misses. Near misses change the TEA delta,
shorten the stall to 100 iterations, point the final jump at another slot,
change one aliased export, or remove the encrypted bitmap. The genuine library
retains OpenSSL identity; the relevant new objectives fail on the near misses.
The old OpenSSL consumers/exclusions were inspected before narrowing identity.
The fetched MSI and its .forage.json provenance remain in scratch.

Raw atomscan probabilities: 9538 **0.895575 -> 0.990000**; VHD **0.918769 ->
0.918769**. Live tiny output reports **suspicious (L85)** for 9538 and **benign**
for the VHD after editing, despite their hostile rule findings. These remain
classifier disagreements with the MALICIOUS analyst verdicts. The installed
v18 model reports an older feature specification (expected v21).

The three-to-five-hostile goal is not met on either original. For 9538, spam,
Defender exclusion and hollowing are demonstrable in the recovered PE, but
its custom TEA -> LCG-XOR -> LZO decoding is not propagated into the original
scan. For the VHD, AES bitmap decoding and subsequent MSI/CAB stages likewise
require manual extraction. The opaque final native executable supplies no
verified additional hostile outcome. Existing downstream detections were
checked rather than duplicated or projected through ciphertext. Additional
original-level coverage needs decoder/analysis-tree support, not extra copies
of the wrapper findings or invented final-stage behavior.

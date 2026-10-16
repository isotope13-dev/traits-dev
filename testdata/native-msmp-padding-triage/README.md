# StormAttack and Urelas review, 2026-10-16

All three specimens are **MALICIOUS**. Judgments use their bytes and Rizin
disassembly, independently of ML predictions and collector filenames. Nothing
was executed. These are local PE files, with no fetched package dependency.

| SHA-256 | Identification | Final unique hostile / suspicious findings |
| --- | --- | --- |
| `2bbf003ac0cee16e1fa88a9df9a1ef9d29c5e2ca5d23518d7c933f902b5d1cd9` | StormAttack service injector | 3 / 0 |
| `194064df59c3d9b43acacd598741242abdfa05c1d7f56071084e30ff00600a94` | Urelas MSMP configuration and network loader | 2 / 3 |
| `a2e595eccd5091ae051519c1a5d0f0ddd78f9a64c6aa3e69f283e5e1c2c4b860` | StormAttack injector with appended certificate material | 3 / 1 |

Counts include embedded children and deduplicate trait IDs. They are YAML
findings, rather than the historical ML explanation stored separately in
Atomscan's JSON. Final verification reads `raw.files[].traits`, not `ml`.

## StormAttack evidence

Both outer programs have identical executable code. Differences are in the DOS
and PE headers, resolved import data and the second specimen's appended
certificate material. The appended material does not establish a valid
Microsoft signature; the final scan reports a signature digest mismatch.

Rizin identifies these linked behaviors in both files:

- At `0x004011d1`, allocate memory in the newly created process; at
  `0x004011f5`, write the DLL path to that allocation. Resolve `LoadLibraryA`
  at `0x0040121a` and pass that function and the allocation to
  `CreateRemoteThread` at `0x0040123d`.
- At `0x00401306`, select LanmanServer's Parameters key. Replace its
  `ServiceDLL` value at `0x0040133e` with the constructed System32 payload path.
- The resource extraction path uses resource type `DLL`, identifier 101,
  and writes the payload before injection. Other paths install an automatic
  service, an Active Setup stub, and COMSPEC deletion of the original image.

The embedded PE starts at file offset `0x5060` in both specimens. Carving its
section-defined extent produces the same 39,936-byte artifact, SHA-256
`0df2765cead245e3a89f9fafbbe5eb42ec7d41386a6c6dc235827539171335fd`.
It carries the Storm DNS, welcome and `STORM:%d|%s|%s|%s|%s` protocol markers.
Its entry point is zero-filled and imports are absent, so its banners do not
demonstrate an executed DNS flood, reflection, or operational payload viability.
The concrete outer hijacking and injection establish malicious behavior.
Neither file provides evidence for Remcos or WannaCry.

Consolidate the duplicate .data DLL-name matchers into the existing
`storm-server-dll-name-data` observation, retaining their case-insensitive
text-matching union. The .rdata and UPX0 observations retain their scopes.
Keep the module identity but describe its DNS label accurately and use parent
technique T1498: the signature does not distinguish direct from reflected
network flooding. Existing LanmanServer and injector findings remain.

## Urelas evidence

The original PE contains usable loader code plus PECompact artifacts and
appended alphabetic filler. Rizin establishes:

- `0x0040a7d0` reads a 512-byte state block, complements every byte at
  `0x0040a835`, then validates `MSMP` (`0x504d534d`) at `0x0040a847`.
  The paired writer at `0x0040a880` validates the clear marker, complements
  the same-size buffer at `0x0040a8d5`, and writes it through `0x0040a4c0`.
  That writer constructs the temporary `golfinfo.ini` path.
- `0x004031f0` extracts resource 131, type `IDR_BINARY`. Its caller writes
  the extracted bytes at `0x00402c4c`, launches the constructed executable
  at `0x00402c71`, and updates the Windows NT CurrentVersion Windows key.
  Another installation branch launches its generated executable at
  `0x00402729` and writes that path to HKCU's `Run` value at `0x0040278a`.
- The loader profiles adapters and constructs controller targets from its
  MSMP state and embedded endpoints. The configured UTF-16 hosts include
  `218.54.31.165` and `218.54.31.226`; other code references
  `1.234.83.146` and `133.242.129.155`. Endpoints are observations, not the
  required basis of the family verdict.
- `0x00403bf0` constructs the retry-delete batch from its own module path,
  creates the batch, formats the deletion template and launches cleanup.
- The PhysicalDrive path reaches `CreateFileW` at `0x00403e78` or
  `0x00403e97`. The traced disk path obtains partition layout using IOCTL
  `0x70050`, reads 1024-byte blocks through `0x00403d90`, and looks for
  `_GBP` records. This establishes device access and record recovery;
  the previous comment about MBR patching was unsupported by this path.

Binwalk locates an encrypted ZIP at `0x264d0`, length 181,116. The loader's
embedded password `1234` extracts `HanAgent_pe.exe`, 228,352 bytes, SHA-256
`0742a171ff4693bb30cd153ca77039b1012b867ed7fa4aef30be00526ee55678`.
That child is PECompact2 compressed; it was extracted and inspected, not run.
Do not describe this member as the HGDraw capture DLL just because the parent
also names that helper. No sample-supplied endpoint was contacted.

[SonicWall's Urelas analysis](https://www.sonicwall.com/blog/urelas-spy-trojan-drops-multiple-malware-families-aug-22nd-2014)
corroborates the family-level NOT-transformed state, Run persistence and retry
cleanup. It describes surveillance in other Urelas specimens; this parent
loader's identity does not itself prove a screenshot-to-network data flow.
The supplied exact-sample Triage URLs were inaccessible to the browser.

Require the MSMP validation instruction and actual 512-byte complement loop
in both network-loader identities. Artifact filenames only corroborate the
first identity; renaming them leaves recognition intact. Rename the disk
variant to describe its required path reference. Update its two Elex consumers
without adding or removing any other alternatives. Keep generic resource,
launch, IP and retry-delete co-occurrence suspicious: it also fits legitimate
cleanup, and proves neither network payload acquisition nor a bound launch.

## Placement and inference corrections

No new directory leaf or exception was introduced.

| Previous definition | Disposition and preserved scope |
| --- | --- |
| `micro-behaviors/data/encode/payload::large-alpha-payload` | Move to `metadata/file/profile/string-population::native-long-alphabetic-strings`. Preserve the two-string count, letter-only regex, PE/DLL Windows scope and exclusions. Remove unsupported encoding/decoding mappings. Its two Canon-loader consumers reference the new fact. |
| `objectives/anti-static/obfuscation/encoding/custom::pe-low-alphabet-overlay-string` | Move to `metadata/binary/layout/overlay::adginpx-overlay-run`. Preserve pattern, overlay location and exclusions; make it a notable shape observation. A repeated G run contains no decoder evidence. |
| `...::tiny-dll-low-alphabet-overlay` | Move to `metadata/binary/layout/overlay::small-pe-adginpx-overlay-run`. Preserve the 65,536-byte ceiling and PE/DLL scope; describe both PE types accurately. |
| `...::tiny-dll-custom-encoded-payload` | Retire: low-alphabet data, overlay size and allocation/launcher references establish neither encoding nor execution of that data. No exact consumers. |
| `...::rundll32-custom-encoded-loader` | Retire its sole exact consumption of the small-overlay observation: export, allocation and loader API co-occurrence lacks a decoder or linked payload activation. Constituent API and shape observations remain. |
| `metadata/file/encoded::large-base64-like-string` | Preserve matcher and scope; describe alphabet membership without claiming that filler is encoded data. |

Ancestor selectors were reviewed as well as exact references. The removed
encoding observations do not qualify the scripted/image stego consumer's
file types. The broad `metadata/binary/layout/` selectors are suppression or downgrade
conditions, not positive attack evidence; the sample scans show no new hostile
claims from them. There are no broad arithmetic or string-population consumers
of these newly added IDs. The bitwise loop is placed under arithmetic, avoiding
the codec selector that would incorrectly call it compression evidence.

## Regression checks

Run:

```sh
python3 testdata/native-msmp-padding-triage/check.py --sample /path/to/Urelas
```

Seven generated inert PEs exercise the real loop and MSMP instruction, different
source/destination buffers, a different loop length, identical bytes in .data,
long alphabetic runs, short near misses, and Inno-style padding exclusions.
With the optional specimen, four further controls require both family profiles
on the original and renamed artifacts, and reject them after removing either
MSMP validation or the complement loop. Real specimens and extracted payloads
remain outside the traits repository.

Each original specimen was scanned with `atomscan` and inspected with
`cleave facts`. Final Atomscan JSON scans confirm the counts above. Finish
with `make validate`; no inline YARA source was added or changed.

Judgment marker contents (each at most 72 characters):

```text
StormAttack service injector: dedupe identity; narrow DDoS claim
Urelas MSMP loader: require config code; correct padding claims
StormAttack cert-overlay injector: narrow DDoS; dedupe identity
```

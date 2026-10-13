# Native PE triage, 2026-10-12

## Judgments from bytes

- `21a84f82887e` and `108ab3c18ffa`: malicious, closely related native
  Protected Storage stealers with autorun drive propagation. These are memory
  images retaining a UPX stub and resolved IAT pointers, not evidence of
  WannaCry encryption. Rizin identifies the XOR decoder at VA 0x428653,
  PStore factory resolution and COM enumeration at 0x42a4d4, form POST
  construction and transmission at 0x42964e, and linewise autorun construction
  around 0x42a394. Both expose the same credential-report and propagation code.
- `87b163ef79fb`: malicious multi-payload native dropper. The outer program
  reads its own image, searches delimiter-bounded payload regions, copies them
  into allocations and writes/launches extracted images. The embedded
  `wideshut.exe` at offset 0x1f630 unpacks with UPX 5.2.1. Its main routine
  copies itself into System32; VA 0x4021f0 writes a hiding-driver image,
  registers an auto-start kernel service, plants msfte.dll, manipulates WSearch
  and MSDTC, and launches `sc config msdtc obj= LocalSystem` with
  CREATE_NO_WINDOW. The driver has SSDT-hook and directory/process hiding rule
  handlers. No miner, ransomware, or feed-named stealer family is established.

The original carrier's automated evidence remains two suspicious findings:
opaque multi-PE overlay with hidden-launch APIs, and packed Microsoft resource
claims in an embedded image. UPX unpacking and driver recovery were manual;
YAML cannot make the analyzer expose those recovered code layers. We do not
upgrade generic overlay/API co-occurrence to hostile to satisfy a quota.
The two worm images retain three behavioral hostile traits, plus the engine's
UPX decompression-failed finding. That engine finding is outside YAML control
and does not itself establish malicious intent.

## Trait changes and placement

The logical-drive API composite moves from the autorun objective to
micro-behaviors/fs/traversal/drives; the CopyFile/module-path API composite
moves to micro-behaviors/fs/file/copy. Both are notable neutral API observations,
with matchers and PE/DLL scope preserved. All four local drive-set consumers
and the one copy-pair consumer now reference those capability IDs. Ancestor
selectors gain no new primitive capability: both composites require existing
members of the destination facility. No family identity or exemption is added.

The UPX HTTP atom now requires the complete POST request line, rather than a
printf prefix. The text request-line regex now uses a literal decimal point.
Bare POST method references are notable protocol evidence. The new overlay
composite lives in the existing pack/overlay leaf and explicitly describes
co-occurrence, not inferred payload data flow or a family attribution.

## Focused checks

- All three input SHA256 values verified; atomscan and cleave facts run on each.
- Final atomscan and JSON scans preserve both worms' three behavioral hostile
  findings and show the carrier's two suspicious findings across its layers.
- New overlay composite matches the original carrier; removing its overlay or
  replacing its CREATE_NO_WINDOW immediate prevents matching. Its extracted
  ordinary 64 KiB helper does not match.
- Replacing the worm's `POST %s HTTP/1.1` with `POST %s garbage` prevents both
  the revised UPX request-line atom and its form-POST composite from firing.
- Fixtures are byte mutations kept outside the trait repository; no live
  malware bytes or sample-specific executable names enter new YAML matchers.

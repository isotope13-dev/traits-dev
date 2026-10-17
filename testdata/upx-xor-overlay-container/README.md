# UPX/XOR/overlay container

`xor-decoder-in-upx-overlay-pe-carrier` (hostile) convicts a UPX image
combining an unrolled XOR decoder with an embedded-PE overlay. The size
leg used to demand half the image, which missed verified carriers
staging a 60KB-plus overlay PE beside the decoder at ~42% of the file;
it now requires thirty-five percent. The other four legs (UPX section
pair, embedded DOS header, XOR decoder bytes, VirtualProtect import)
carry the specificity either way.

## Controls

`verify.py` builds minimal PE32 fixtures (UPX0/UPX1 sections, decoder
bytes in .text, a VirtualProtect import, an embedded DOS header at the
overlay start) and scans them with `cleave --traits-dir`:

- `xor-overlay-40pct.exe`: 40% overlay. Must report the hostile.
- `xor-overlay-10pct.exe`: 10% overlay. Must not report it.

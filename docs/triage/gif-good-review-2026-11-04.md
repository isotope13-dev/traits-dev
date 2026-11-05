# GIF endpoint review — 2026-11-04

Thirty-five standalone GIFs were examined structurally: each has a valid
GIF87a/GIF89a header, a complete image block and trailer, and no trailing
data. They are small icons, flag images, and interface assets. Fresh local slow
scans reported no suspicious or hostile findings; validation passed and Hopper
confirmed good.

Four apparent GIFs are not valid images. They use a GIF89a prefix followed by
an eight-byte repeating-XOR encoded Windows PE beginning at offset 13. The
payloads were decoded offline for analysis and were not executed. The original
carrier scans independently report an invalid-GIF/XOR-PE masquerade hostile
trait plus a separate payload trait:

- `163eda7f8382`: decoded PE SHA-256
  `12a057ca7c92cda3cd0e09efc5bff2ebd3f7d2991e999038c7f31a6ac6a95c3d`;
  receives, decrypts, and executes code in memory.
- `684f863b5af6`, `79bc1595ad70`, and `f4698d9429b0`: decoded MiniDuke
  command backdoor variants, with matching command vocabulary, response
  strings, and custom wire alphabet. Their decoded SHA-256 values are
  `de8184c6850d17f90e861309828af1f7b7e3b1695ebe5d303d3d4b6ef4ba1218`,
  `29ad305cba186c07cedc1f633c09b9b0171289301e1d4319a1d76d0513a6ac50`,
  and `b1584a6f1059ad1c24bde2a9a8ae83ffc6679eb531d30f3f1c69f81e3a3819dc`.

All four were recorded bad after fresh carrier and decoded scans and passing
validation; original snapshots were hash-verified on relocation. The remaining input with contents, `1d2423a18210`, is a SonarLint VSIX. Its
manifest, bundled runtime and analyzer archives were reviewed; the fresh scan
examined 1,869 components and found no severe traits. Validation passed and
Hopper confirmed good. An additional directory `f9745bd5e08e__good` was already empty
when this review began and is not counted as an examined artifact.

GIF total: 36 good and 4 bad.

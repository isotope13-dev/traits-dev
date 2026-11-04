# JPEG mislabeled-good review, 2026-11-04

All 40 queue entries have been reviewed: 39 were confirmed good and the
hex-encoded Remcos loader was moved to bad.

The queue includes files whose actual formats are not JPEG. A slow local,
no-follow scan of the 33 files starting with a JPEG signature completed; this
is preliminary evidence for files not listed below.

Eighteen files (`e1f1ad9c11e0`, `f8f24578fcbd`, `962e7777ee53`,
`76b1f7804739`, `37cd2c0c86de`, `06d29dfdf796`, `39db6ce71c39`,
`b363a2b3b515`, `ee780248991e`, `48d690e4353d`, `2c4e349a6763`,
`7eacc90d952e`, `eb38feee200d`, `2b77d282870f`, `c8ec4fa03389`,
`fa5fcbf46f0e`, `49deed0eb08d`, and `d4e85e1ee5db`) are recognized JPEG
containers ending at the file boundary, without suspicious or hostile findings.
Their hashes were verified and Hopper confirmed each good label (18 no-ops).
Some originated in suspicious collections; the image contents themselves do
not inherit those collection labels.

Seven further JPEGs (`264e6104ac0a`, `06717dd3fdec`, `12ba9b7998a2`,
`9d3dcc82f3f0`, `14831c98f63b`, `d707ca091c59`, and `5d66376b4f5a`)
end at the file boundary and have no suspicious or hostile findings. The two
large-APP1 images contain XMP-encoded 256-pixel JPEG thumbnails. Two short
hex-decoding candidates come from repeated `2` bytes in JPEG quantization
tables, and another base64 candidate comes from repeated `E` bytes in image
data; these candidates do not establish hidden programs. Hashes were verified
and Hopper confirmed all seven good labels (no-ops).

Five files (`340875556e26`, `433f02f2e738`, `70f58bf59651`,
`954ac3e0637e`, and `0888cef2e588`) contain bytes after the first JPEG's
end marker, including a second JPEG. The intervening bytes and carved JPEGs
were inspected and scanned locally; neither the originals nor the carved data
had suspicious or hostile findings. The extra-data observations are retained.
Their hashes were verified and Hopper confirmed the five good labels (no-ops).
`f40a945b776d` similarly contains a second scanned JPEG, followed by 28,643
zero bytes. Its trailing data and carved image have no suspicious or hostile
findings; Hopper confirmed its good label (no-op).
`241e565921a5` has 209,539 trailing bytes after its first image. Those bytes
contain 3,512 JPEG-stuffed `FF 00` pairs and a single end-of-image marker at
EOF; every `FF` byte is part of one of those pairs or that marker. This is
consistent with residual JPEG scan data. The original and trailing region scan
without suspicious or hostile findings; Hopper confirmed the good label (no-op).

`2b60ee65948d` (`Attack.jpg`) is not an image: it is hyphen-separated hex
encoding of an obfuscated PowerShell loader. Static decoding reveals two gzip
stages, a reflected .NET assembly, and a call passing the second stage to a
Notepad-targeting loader. The second stage is a Windows PE whose own scan
reports a native Remcos RAT, keyboard and microphone collection, persistence,
and process-hollowing traits. No payload was executed. Two hostile observations
now match the original encoded bytes in separate directories: the loader call
with its decompression stage, and a fingerprint of the compressed Remcos stage
with that loader. The original scan reports both; controls missing the loader,
decompression call, or stage fingerprint reject the respective rules.
`make validate` passed. Hopper moved the sample from good to bad, and its
hash-verified snapshot was relocated to `/tmp/triage/misplaced-bad`.

Two other files in the JPEG queue are passive images with different formats:
`946cc3181f36` is a BMP, and `d9cf3620b077` is a GIF used as a ReportLab test
image. Local scans have no suspicious or hostile findings, and Hopper confirmed
both good labels (no-ops).

`e3bcebb8e08f` is a ZFPlayer source tarball, not an image. Its archive contains
Objective-C player and UI code, CocoaPods build scripts, images, and a stub test.
The local no-follow archive scan has no suspicious or hostile findings; source
and build-script review found no dedicated attack or exploit implementation.
Hopper confirmed the good label (no-op).

`02e0a98abb83` is an Inno Setup installer for Interior Design 3D. The scan
examined its application, rendering libraries, media libraries, and other
contents without suspicious or hostile findings. The application includes
product update references over HTTP. A prior rule described the co-occurrence
of registry API names as persistence; it has been relocated to a neutral
registry API-name observation. The actual executable matches the revised rule,
and a control without `RegReplaceKeyW` does not. The installer rescan reports
the corrected observation. `make validate` passed and Hopper confirmed good.

`53488c86f126` is the digiKam 8.6.0 source RPM. The no-follow scan inspected
its source tarball and thousands of members, including a bundled Mesa OpenGL
DLL, without suspicious or hostile findings. The package contains photo
management source and build files; its filenames do not expose exploit or
payload test fixtures. Hopper confirmed good (no-op).

`e4eef1b658ba` is the Astrometry.net 0.97 source tarball. Its C and Python
code implements astronomical image calibration; its setup hook runs make-based
build and install commands, already represented by the reported build traits.
The no-follow scan and a source search for attack and exploit patterns found no
suspicious or hostile content. Hopper confirmed the good label (no-op).

`8350c3561e04` is a JPEG with a genuine appended ZIP. The ZIP passes its
integrity test and contains only a JPEG, an MP4, and an XML content-type
manifest identifying those media types. Each member was separately scanned
locally without reference following and has no suspicious or hostile finding.
The outer file's single suspicious archive-in-media finding accurately describes
the unusual packaging; it does not alone establish malicious behavior. Endpoint
ruling: good. `make validate` passed and Hopper confirmed the existing label
(no-op).

# Font mislabeled-good review, 2026-11-04

`c1f33147c9b9` is hex-encoded JavaScript stored under a WOFF2 font name.
Static decoding reveals a loader that fetches JSON through Axios, takes the
`cookie` field from the response, constructs a function with that value, and
invokes it. It also constructs commands to install dependencies and run the
stage, including a hidden PowerShell path. Endpoint ruling: bad. Two new
hostile observations in separate execution and command-and-control
directories match the original encoded carrier. Removing the invocation
clears both; replacing the Axios fetch clears the command-and-control finding.
Validation passed, Hopper moved the sample to bad, and its hash-verified
snapshot was placed in `/tmp/triage/misplaced-bad`.

A preexisting rule declared any sufficiently long text under a font name
hostile. A filename/content mismatch alone does not establish malicious intent,
so that combination now has a neutral format observation; the loader's bad
ruling rests on the decoded behavior described above.

`034c3ed203cc`, `62dde529b296`, and `6885fcb5172d` are valid fonts that
Fontconfig identifies as Scheherazade Regular, Scheherazade Bold, and Noto Sans
Living Regular. Their scans report no suspicious or hostile traits. Endpoint
rulings: good; validation passed and Hopper confirmed all three labels
(no-ops).

`e6a925c8bf2e`, `cda1c17d5c99`, `a84e5d995836`, `fa3ff2fb8ee4`, and
`cd75796cdd97` are Brotli-compressed fonts. Bounded decompression and
Fontconfig identify all five, and scans of both the compressed and decoded
files report no suspicious or hostile traits. Endpoint rulings: good;
validation passed and Hopper confirmed all five labels. The old rule that
called an opaque font-named blob disguised was replaced by a neutral format
observation because compression alone does not establish malicious intent.

`454a3fc187e4` is an Access database that shares a TrueType prefix. Its
double-encoded fields include webshell-management data and strings for exploit
requests and webshell payloads. The database also contains a VBA project, but
the available analysis could not recover its implementation or establish how
the stored strings are used. The scanner identifies this database as unknown
and cannot attach a format-specific trait. Endpoint ruling: inconclusive,
pending inspection of the VBA project and the database consumer. Hopper moved
it to inconclusive and a hash-verified snapshot was retained.

`03866a69228f` is font-kit source, `5729921c1b22` is Aseprite source,
and `c510ed6ee2e0` is the KanFan manga-translation extension. The latter reads
cookies associated with an image's own URL to request that image, and its
header rule is scoped to the image host; the inspected code does not send
those cookies to a separate collection endpoint. Their scans report no
suspicious or hostile traits. Endpoint rulings: good; validation passed and
Hopper confirmed all three labels.

All 15 entries in the font pool have been reviewed: 13 good, one bad, and
one inconclusive.

`a58442e4e78f` is the Site Reviews WordPress package. A valid TrueType font
within it was incorrectly reported as having no font signature because the
scanner mistook its mostly UTF-16 name table for a BOM-less text file and
transcoded the binary. The input-normalization fix preserves sfnt bytes;
six focused encoding tests pass, including genuine BOM-less script controls.
The rebuilt scanner reports the exact original font hash and size, and the
package rescan reports no suspicious or hostile traits. A disguised hostile
font loader still triggers two hostile findings. Endpoint ruling: good;
validation passed and Hopper confirmed the label.

`bf7e950ce947` is a Signal desktop macOS installer. Its Electron framework
had file-write references and Apple-named cache paths, which were combined
into a claim of hidden payload staging without evidence of such a write.
That co-occurrence remains a neutral observation; a LaunchAgent-path positive
control still matches its suspicious path observation. The full rescan of
1,470 components has no suspicious or hostile traits. Endpoint ruling: good;
validation passed and Hopper confirmed the label.

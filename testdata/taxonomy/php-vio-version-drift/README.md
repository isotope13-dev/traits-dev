# php-vio 2.35.0 version-drift review

Verdict: **BENIGN**. The specimen is the source distribution of
`phpolygon/php-vio`, a PHP extension for GPU rendering, audio, video streaming,
and application input. SHA-256:
`0564348825b3ea974241c15194e19731aed153403f025689832d41dc704c2ecc`.

## Decisive release comparison

Fetched these upstream releases from GitHub codeload, without executing them:

| Release | Archive SHA-256 | Git archive commit |
| --- | --- | --- |
| [v2.34.1](https://github.com/phpolygon/php-vio/tree/v2.34.1) | `3779c076fc77a96972d059bbc6e55253a31ad73a459e3dbaae5e37937211f2e8` | `4216fc15a696a415725bac2305d33d697ed53d25` |
| [v2.34.0](https://github.com/phpolygon/php-vio/tree/v2.34.0) | `6ac683667cf1ca569d02948282a9ac6a6c022fa917b668310220a03befbb32b9` | `49ffe771dc1c9872e833a57f28c31732a2d8c02c` |

The specimen's Git archive comment is
`01f588f88758711feccaba932a6fb9426c65bc2a`. Compared with v2.34.1, only nine
files differ: release/version documentation, internal-enum comments, registration
of 17 keypad constants, the `vio_gpu_flush` stub declaration, a new parity test,
and a GPU-timestamp test averaging over frames. There are no removed files.
The workflow `.github/workflows/build.yml` is byte-identical in all three
releases (SHA-256
`0da5ca5fa89724ea1bea6c20eefdd65414f02169ea41cf42de7cd1ede400df8c`).
The additional v2.34.0 comparison isolates the ordinary miniaudio namespace fix:
public `ma_*` symbols become `vio_ma_*` to avoid linking incompatible copies;
the implementation moves into `src/`, with header/runtime version checks.

## Execution review

The flagged Windows step discovers the built extension and Windows SDK DXC DLL,
sets DLL search paths and required-feature environment variables, smoke-loads
php-vio, prints GPU capabilities, downloads the Microsoft Agility SDK from
NuGet for diagnostics, and runs explicitly listed PHPT tests. Its single
1,382-character line is a `php -r` diagnostic printing supported graphics
features. No reconstructed command, encoded payload, hidden interpreter, or
secret export occurs along this path. The other Windows test step downloads
pinned WARP, Agility SDK and DXC artifacts from their upstream repositories.
The release job's authenticated GitHub request triggers a declared downstream
rebuild with the release version and source-run link.

`cleave facts` on the extracted PowerShell step reports mean identifier entropy
3.9486 and mean identifier length 42.8162: long descriptive test filenames,
feature constants and environment names account for the measurement. Decoded
string inspection finds Windows path escapes interpreted as encoded bytes
(`\x64` path text becoming `d`), not another execution layer.

Module initialization registers backends, resources, classes and constants;
request initialization updates the PHP thread-local cache. Input messages go
through the extension's own window procedure, with clipboard APIs exposed as
application functionality. The Direct3D waits pace swapchain frames. The
OpenGL VMware string maps a graphics vendor to an adapter identifier. FFmpeg
opens the URL provided to the streaming API and writes encoded video output;
it is not an implicit module-load connection. The reviewed release changes add
no hostile activation or data transfer.

## Trait corrections and preservation

* Move PowerShell identifier/comment measurements to metadata. Replace the
  unsupported Invoke-Obfuscation attribution with a file-scoped measurement
  profile requiring both high mean identifier entropy and a long line. Preserve
  the atomic gates/exclusions. Retire `ps-encoded-downloader`: its comment and
  command-option evidence establishes neither download nor execution.
* Move the Win32 alertable-wait reference to process control. Reuse the canonical
  VMware vendor observation for native source and preserve the vendor-group
  consumer. Neither reference alone establishes analysis evasion.
* Move WSH command-line engine selection to runtime configuration, preserving
  matchers, scopes, exclusions and exact consumers. Selection of JScript does
  not require a misleading file extension or establish masquerading.
* Move current GitHub run-variable access and its alternative group to CI
  environment access. Preserve both hostile current-run deletion composites.
* Require ABI-specific encoding for an EVM calldata construction observation;
  plain `pack()` in a texture record is not EVM or C2. Add a separate notable
  PHP binary-packing call observation. Update the two calldata consumers.
* Require an indexed global value to be **returned**, rather than matching an
  anonymous function that appends warnings to `$GLOBALS`. The result belongs
  under control-flow return; the obfuscation composite supplies its other
  evidence separately.
* Retain fragmented NuGet path detection under string fragmentation, excluding
  the intact canonical `v3-flatconta` match. Plain upstream package URLs remain
  represented by existing URL/download traits.

Exact references and ancestor selectors were searched across the four tiers.
The changes to broad anti-static and indicator-removal selectors intentionally
remove these unsupported attack observations; neutral measurements and CI
variable access do not become objective evidence merely because a selector
previously included them. The native vendor group and explicit consumers of
moved observations retain references to their canonical neutral facts.

## Controls

Run from the repository root:

```sh
python3 testdata/taxonomy/php-vio-version-drift/check.py
```

The fixtures include the actual flagged test step, independent entropy and
line-length near misses, WSH engine options, graphics wait/vendor references,
PHP warning append versus returned global entry, binary texture packing versus
ABI calldata, intact versus fragmented NuGet paths, a CI run link versus two
current-run deletion mechanisms, and numerical string obfuscation. Scanning
never executes fixture contents. Existing leaves are used; no new taxonomy
partition or directory budget is introduced.

The post-edit local Cleave archive report and an independent Atomscan rerun
both contain zero suspicious or hostile traits. Remaining source-analysis gaps
reported by the engine were addressed for the relevant paths by direct source
and release-diff review; a clean scan is not the basis for the verdict.

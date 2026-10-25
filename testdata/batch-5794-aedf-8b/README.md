Reviewed samples: `5794c425710f`, `aedf0a99c37e`, `8b198f4f0a61`.
All three verdicts are **BENIGN**. Research artifacts, original fetched files,
`.forage.json` provenance, facts, and complete scans are in
`/usr/local/var/cyclotron/tmp.noindex/cyclotron-90084b2c/scratch/batch-5794-aedf-8b`.
The initial full scans and archive facts are in the sibling `fallout-review`
directory under their six-character SHA prefixes.

Chat with Work Desktop 0.5.0 is a Rust/Tauri desktop client and MCP file agent.
An independent download of its upstream v0.5.0 archive has the exact supplied
SHA-256, not merely matching package metadata. Traced the CLI pairing flow,
authenticated WebSocket session, tool dispatch, filesystem policy, command
planning and sandbox launch, and startup installation. Reads are confined to
configured shared roots and the deny policy excludes credential stores. Writes
and command execution require corresponding local root settings. The supervisor
reloads configuration and checks the requested working directory before starting
a command sandbox. Per-action approval for ordinary person requests trusts the
paired server; unattended bot commands additionally require an explicit local
folder loan. This is an intentional remote-access application, not an observed
backdoor or secret stealer. No installation authorization or server compromise
context was supplied.

The Windows MSI's WiX source installs its advertised binaries, scanner helper,
TWAIN DLL, documentation, shortcuts and per-user startup integration. The TWAIN
download checks both archive and DLL SHA-256 values before copying the DLL.
The downloaded DMG was examined independently before and after the YAML change,
then extracted with 7zz. Its bundled launch agent starts its own app in the
background. The native app carries the expected Developer ID identity and
SMAppService registration selectors. The source's startup preference calls the
autostart library to enable or disable this behavior. A bundle-directory string
does not establish unwanted persistence.

The two PXT archives are Microsoft MakeCode source trees. Compared every regular
archive member against independent GitHub tag downloads, normalizing only the
container prefix: all 1,090 v0.13.11 files and all 2,528 v5.37.66 files are byte
identical, with no extra or missing files. Traced CLI child-process wrappers
through build/npm/git operations, the local HTTP/WebSocket API and token checks,
simulator evaluation of compiled user programs, and resource Base64 handling.
The large `external/tdast.js` file is a TouchDevelop compiler/runtime bundle;
its evaluation paths initialize compiled scripts and its embedded Base64 data
includes image/audio resources. The newer WinRT backend opens and exchanges
reports with programmable HID boards. These behaviors fit development tooling;
the provenance comparison and execution paths support the verdict together.
No deployed-machine context or evidence of a substituted upstream release was
provided.

Both PXT classifier results remain HOSTILE, probability 1.0, level 0. The
probability-1 child records are AppX manifests declaring remote content with
WinRT access. Those declarations are real and retained; they are not themselves
proof of hostile execution. The manifests target MakeCode and its local debug
server and declare network/removable-storage/device access for the editor.
No package exception or score-targeting rule was added.

The YAML corrections are deliberately separate from verdicts:

* Moved `objectives/persistence/system/surface/paths::app-bundled-launchd-path`
  to `micro-behaviors/fs/path/config/autorun::app-bundled-launchd-path-reference`.
  Preserved its exact matcher and file/platform scope. The neutral reference is
  notable and has no ATT&CK persistence assertion or product exclusions. Removed
  the old path-only alternative from both persistence aggregators; neither a
  directory reference nor a non-Apple identity establishes the claimed abuse.
* Added `micro-behaviors/hardware/input/device::winrt-hid-output-report`, notable,
  for the previously uncovered WinRT HID output-report call in PXT v5.37.66.
  A Tree-sitter query requires the invoked member, so a reference, comment or
  quoted example passed to another function cannot satisfy it. API semantics
  are documented by [Microsoft](https://learn.microsoft.com/en-us/uwp/api/windows.devices.humaninterfacedevice.hiddevice.sendoutputreportasync).
* Audited exact and ancestor selectors for both the removed and new homes.
  The old atom had only its two local aggregators as consumers. New filesystem
  ancestor consumers are restricted to Windows PowerShell/PE observations;
  none gains an admitted attack from the macOS path. No hardware ancestor
  selector consumes the added HID rule. There were no pre-existing testdata
  fixtures or other extracted source samples matching the removed path atom.

One **engine-generated false positive remains**, outside YAML control:
`binary/embedded/base64-powershell` in `packaging/test-install.sh`. The shell
executes a package test in `sh -ec`; the reported offset 0xfd4 is the file-test
flag in `test ! -e /usr/share/applications/cww-app.desktop`. Decoding the
misidentified token `/usr/share/applications/cww` as padded Base64 then UTF-16LE
produces ten non-ASCII code points (30 UTF-8 bytes), whose SHA-256 is
`99423db1d2797a6ee829d703ba58d4e74a61ca363e61557553d796b82360f6e1`.
That exactly matches the scanner's synthetic PowerShell layer. There is no
PowerShell invocation or encoded command here. No YAML shadow or dependent-only
exception was introduced. Correcting this requires the engine/stng decoder to
distinguish shell `-e` file tests from PowerShell command arguments.

`python3 testdata/batch-5794-aedf-8b/check.py` checks five static focused
fixtures and two existing attack fixtures without executing sample code.
Both launchd directory variants retain the notable observation. An unrelated
directory and HID comments, strings, and uninvoked member references do not
match. Existing phishing/password/clipboard/LaunchAgent and trojanized Homebrew
fixtures retain all four hostile and three suspicious findings in total.
The actual PXT HID source and extracted DMG also match their new rules.

Counts, member-level differences, classifier results and scan limits are
recorded in `review.json`. Counts deduplicate IDs across members and decoded
layers; fetched dependencies are reported separately from the source archive.

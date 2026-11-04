# Tar filetype mislabeled-bad review — 2026-11-04

The 40-file snapshot contains 28 good, 4 bad and 8 inconclusive artifacts, including other tar-based package formats.

`fe8c03ed29d2` is an Arch recipe for a guitar application. It invokes `sudo pacman -U` during its build and skips the checksum, which is unusual and remains a suspicious finding, but the recipe itself is good; its remote dependency was not fetched. `7abade425911` is a game-streaming host package recipe with an informational install hook; it is good.

`5494d26d39cd`, `d61f96455908`, `639b7328b08c` and `5959754f0b0e` are Wolfi compatibility packages consisting of metadata, build records, SBOMs and symlinks to separately supplied binaries. The packages are good as standalone artifacts.

`1302aff98376` is a small Rust infrastructure library with a registered-function dispatcher and file-copy helper. Its dispatcher removes its own executable and reads requests from standard input, but the crate has no built-in network channel or credential-harvesting function. It is good as a general-purpose supporting library. `daf4879df749` is a Ruby OAuth integration and JWT-verification gem; its embedded source and metadata are good. Both scanners reported no hostile findings for these eight archives.

`ec20a84f7253` is a PHP lead-management library, and `6a68f3e26721` is a Rust OOXML derive-macro crate; their reviewed source has no hostile payload, so they are good. `b582126c3b6d` contains an nginx compatibility configuration and symlink; `9e47151f0a70` provides a compatibility symlink; and `631036e937cb` and `5a256994c996` contain nginx GeoIP and image-filter modules respectively. Their configurations, archive contents and module symbols match those roles, and they are good.

`0d007f3841c9` builds a traversal archive containing a root cron entry as part of an extraction-rejection test. The generated archive is an executable attack PoC, so the crate is bad even though the test expects rejection. Both scanners already report the hostile traversal/cron finding.

`852ef394a02c` is an Xcode project whose build phase invokes a hidden, twice-Base64-decoded command that posts a fixed marker to a remote endpoint and executes the response as shell code. `b75c1c078d88` is a 7z archive containing many architecture-specific ELF executables, including nested archives whose binaries match independent Ngioweb botnet and communication profiles. Both are bad; both scanners already report hostile findings. The Xcode payload's fixed marker is not a host-data finding.

`534a82056695` and `b46e5e8d8efb` contain Tamil and Telugu font files, font configuration, package metadata and SBOMs, with no embedded application code. They are good standalone font packages; both scanners reported no hostile findings.

`65b2ce41dd11` is an SSH implementation containing an executable SFTP regression test that starts a local server and attempts to open `/etc/passwd` through a traversal path. The test expects denial, but it constructs and submits the exploit attempt, so the crate is bad under the PoC policy. Both scanners match the new finding; replacing the traversal target clears the control. Atomscan reports the hostile trait but exits successfully. No successful file read or host-data transmission is asserted.

`a01144d5ef5d` is an ARM/WASM compiler backend; `65a87b1f96cd` is a CUDA backend; `b86ea45fd91e` is a language CLI; and `11ccc5eea805` is a local QQ chat export tool. Their inspected source and embedded helpers implement those roles, without the hostile host-data-transmission PoCs sought in this review. `5c7a9ebc62ce` and `692851578782` are browser map/UI packages without install hooks or executable attack payloads in the inspected contents. These six are good, and both scanners reported no suspicious or hostile traits.

`d636e57c016b` contains Grafana compatibility and service-management scripts. It is good; the one remaining suspicious observation is an archive security warning about its absolute symlinks to standard Grafana paths.

`56bdc849dd6f` and `5727ee8f38fa` contain Katib optimization service source and configuration; `b8c1a2e49ccc` contains Ruby Yajl bindings and their source/tests. Their reviewed code and package contents match those roles, and both scanners report no suspicious or hostile traits. All three are good.

`9e78a342e155` is a package containing a statically linked Zig hello-world executable, confirmed by its symbols and strings. It is good; both scanners reported no suspicious or hostile traits.

`8cb520a7ed4b` is an encrypted ZIP whose npm package contains a 77 MiB `.txt` file. The archive opens with the conventional malware-sample password; the file is actually an NSIS Windows installer containing compiler and debugger archives. The npm manifest has no install hook. Both whole-archive scans timed out, and the nested installer binaries could not be fully assessed, so the artifact is inconclusive rather than judged by the collector label or misleading extension. Hopper records it through purgatory.

`b754a83e49a1` is a Conda package containing a Pandoc cross-reference filter, its manual and license. The executable's identity strings and archive layout match that function; both scanners reported no suspicious or hostile traits. It is good.

`112a59159928` is a Bun source archive with more than 13,000 scanned entries. A protocol conformance test sends one conflicting-framing request and expects an HTTP 4xx response; separate test cases had been combined into a false smuggling finding. The conformance case now clears that finding in both scanners, while a modified control with a second pipelined request remains hostile. A full archive rescan reports no hostile traits, though Atomscan still exits 2 on its model score. The archive is inconclusive because the behavior of all embedded test packages and tools could not be independently resolved; Hopper records it through purgatory.

The following large artifacts are inconclusive; Hopper records them through purgatory. The scanners found no hostile traits in the portions reported, but the stated analysis limits prevent a confident endpoint ruling:

- `63748cab9de3` is a Homebrew package containing roughly 1,900 Ruby source files and install hooks. Cleave reported 2,654 files and Atomscan 2,436; the behavior of the remaining package-manager code and its dependencies could not all be independently resolved.
- `b4069dc9d095` is a Traefik container filesystem with a proxy executable and system files. The scanners reported different extracted-file counts, and the native executable and bundled scripts could not be fully verified.
- `69ce38e8db80` is an OpenCV Arch package containing many native libraries. Cleave timed out; Atomscan reported no hostile traits in 529 extracted entries. The native libraries could not be independently verified.
- `ff49d412deaf` is a Valgrind package containing native debugging tools and helper binaries. Cleave reported 145 entries and Atomscan 30; the native code and coverage gap remain unresolved.
- `7402d99637d5` is a Darwin developer-tools npm package containing a 96 MiB native executable and helper binaries. Both scanners reported no hostile traits across the eight entries, but their native code could not be independently verified.
- `e65fcf7dc0f1` is a Windows emulator distribution with many DLLs and a nested source archive. Cleave timed out; Atomscan reported no hostile traits but exited 1 on its model score. Separately extracted main executables had no suspicious or hostile cleave traits; the remaining bundled code was not independently verified.

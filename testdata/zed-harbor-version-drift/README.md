# Zed and Harbor release comparison

Both supplied samples are **BENIGN**. These are an editor and the Harbor
container-registry administration CLI. The findings confused ordinary file
exclusions and generated API operation names with attacker behavior.

## Fetched controls and provenance

* Zed 1.24.4 DMG: SHA-256
  `fda9ce886dbb4860fb366c647d4c6407bed95a288b45dd43cc59732ef21d8670`.
  GitHub's release asset digest matches the supplied DMG. `codesign --verify
  --deep --strict` verifies the extracted application and its bundled executables.
  The signature identifies Zed Industries, team `MQ55VZLNZQ`, and `dev.zed.Zed`.
* Fetched [Zed 1.24.3 ARM64 DMG](https://github.com/zed-industries/zed/releases/download/v1.24.3/Zed-aarch64.dmg):
  SHA-256 `fa4028fa85d1f1b7c9f9fd2ab43f272f6e7a634470f88b6b936fe4a557fcf34d`.
* Supplied Wolfi Harbor CLI 0.0.27-r0 APK: SHA-256
  `83c78df0f231c077227ec48bebd2fbb40257f347ea86e07037e91c5d43734003`.
  Its melange recipe pins upstream commit
  `1af93ace562d69b2293fa71733d4a4f5bb3c1503`. The executable's Go build information
  agrees with that revision, the Harbor module path, and the dependency-update
  build recipe. Its `+dirty` version is consistent with those recipe updates;
  that flag alone establishes neither compromise nor reproducibility.
* Fetched [Harbor CLI 0.0.26 Linux AMD64 release](https://github.com/goharbor/harbor-cli/releases/download/v0.0.26/harbor-cli_0.0.26_linux_amd64.tar.gz):
  archive SHA-256 `d05717300dbea2096ce601cfa43ba1f1b38a6dfa35fb977755b1dffcd93914df`;
  executable SHA-256 `d46ab12d6b6e822cb07b3564728c8cd13926977e5e9279fa699c200a56a33474`.
  This is the upstream release build, rather than an identical Wolfi build recipe.

The earlier releases also trigger the old broad rules when scanned with the
current engine and traits. The historical clean result in the queue is not
reproducible with this ruleset. The matching evidence predates these releases.

## Decisive behavior and diff evidence

[Zed 1.24.3 to 1.24.4](https://github.com/zed-industries/zed/compare/v1.24.3...v1.24.4)
changes only `crates/language_models/src/provider/opencode.rs`, the root Zed
version in `Cargo.lock`, and `crates/zed/Cargo.toml`. The functional change makes
model transport metadata optional and inherits a provider's transport when the
model does not specify it. It adds regression tests, not a filesystem collector.
The exact compared revisions are `2a857f5f2ec368745c1af5209d49836968fe75b8` and
`aed37547d8543000494fb69101c05daec5891068`.

The extracted binaries both contain the same `.DS_Store` exclusion material:
`crates/git/src/checkpoint.gitignore`, default `file_scan_exclusions`, and their
settings documentation. `HOME`, `~/Library/Application Support/Zed`, and the Rust
walkdir implementation are already present in 1.24.3. `BackgroundScanner` lists
children, applies `WorktreeSettings::is_path_excluded`, removes excluded entries
from its snapshot/watch set, and continues. The predicate checks path ancestors
against configured glob matchers. Rizin disassembly of the supplied binary's
predicate at `0x109643b08` confirms path component iteration and glob matching;
the compiler can inline it at callers. The matched path references do not bind
any data to collection or transmission.

Two additional notable findings were also misleading. The maintenance sentence
is a `Callout::preview` example in `crates/ui/src/components/callout.rs`:
“System maintenance scheduled for tonight”. `crates/workspace/src/persistence.rs`
implements SQLite workspace/session state, not service installation or autorun.
Both source files are unchanged across these releases.

[Harbor 0.0.26 to 0.0.27](https://github.com/goharbor/harbor-cli/compare/v0.0.26...v0.0.27)
changes error handling, registry commands, selection UI, CI, tests, and
dependencies (29 files). `pkg/api/info_handler.go`, `cmd/harbor/root/info.go`,
and the relevant go-client version (`v0.213.1`) are unchanged. Earlier revision:
`8c20d16b2f19adaa1c3b5fa7a6113c09938f65bd`.

The supplied executable's disassembly follows
`api.GetSystemInfo` at `0x9fb3c0` -> `utils.ContextWithClient` -> generated
`systeminfo.(*Client).GetSystemInfo` at `0x888040`. The generated operation builds
`getSystemInfo`, `GET`, `/systeminfo`, then submits it through the configured
Harbor transport. The configured registry URL and saved login credentials select
the server. The user-invoked `harbor info` command formats the response locally;
project-member creation also uses server configuration to choose authentication
handling. This is remote registry administration, not local host reconnaissance
or operator tasking. The earlier executable contains the same operation identifier,
request path, and API functions. Compiler changes (Go 1.26.3 to 1.27.3), dependency
updates, and differing upstream/Wolfi build settings explain substantial binary
layout and standard-library changes. No new first-party export names were added.

`cleave facts` was collected for both archives and extracted binaries, including
instruction-recovered and decoded text. Decoded candidates supplied no additional
executable payload or hidden command channel. Networking, crypto, credential
storage, file access, and subprocess capabilities remain visible at their ordinary
severities. Neither sample was executed. No machine-specific deployment context
was provided; the artifacts' behavior, purpose, provenance, and unchanged relevant
paths tip both judgments toward benign. This is not a claim about how an unknown
operator might use legitimate software.

## Trait corrections and controls

* Move macOS location references to `micro-behaviors/fs/path/location`, and
  `.localized` marker references to `micro-behaviors/fs/path/metadata-store`.
  Relabel the compound finding under `fs/directory/traverse` as file-scoped
  co-occurrence of traversal and metadata path references, at notable severity.
* Move system-info identifier vocabulary to
  `metadata/lang/source/naming/action`. Preserve the three lexical matchers and
  existing namespace filters. The Go-marker conjunction is notable metadata;
  it does not infer a RAT. Update `go-rat-full` to reference the relocated evidence
  and retain its former exclusions at that consumer.
* Move maintenance wording to `metadata/lang/natural/vocabulary/content-word`
  and the Rust module path to `metadata/lang/compiler/systems`. Remove unsupported
  attack mappings and update the AppleScript composite's direct reference.
* Direct and ancestor selectors were reviewed. Broad collection selectors do
  not inherit the relocated neutral paths: treating those references as collection
  would restore the original false inference. Other direct consumers resolve.

`cases.json` covers native positive controls, omitted recursion, omitted metadata,
insufficient location references, identifier suffix near misses, actual Go build
markers, neutral UI wording, and a non-Rust path near miss. C fixtures are inert
string-printing programs; the Go fixture prints an operation name. No fixture is
executed. Rebuild on macOS with `python3 testdata/zed-harbor-version-drift/build.py`,
then run `python3 testdata/zed-harbor-version-drift/check.py` from the repository root.

Both original sample archives were rescanned after the changes. The extracted
main executables have zero suspicious/hostile findings and no objective-tier
findings. The intended neutral observations still fire. Full `make validate` is
the final authoring gate.

Judgment marker lines:

```text
Zed 1.24.4: unchanged exclusion paths; neutral traversal traits
Harbor CLI 0.0.27: unchanged registry GET; neutral name traits
```

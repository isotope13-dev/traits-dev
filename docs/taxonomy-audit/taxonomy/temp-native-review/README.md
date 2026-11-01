# Temporary native staging review

Ten legacy `staging/temp` rules were reviewed and moved. Their matching
conditions, confidence and scopes are preserved. Their names and criticalities
now reflect the combination that is actually required, and inherited ATT&CK or
MBC labels that were not established by the matcher were removed.

The Go stage filename, function-name reference, hidden sysmon path and network
clues support a suspicious acquisition lead rather than a confirmed download.
A hidden numeric filename template, self path and shell reference are a notable
path profile. Base64, a temporary path and a driver suffix are partial evidence;
the combination with driver-service references remains a suspicious staging
lead. A richer unsigned-DLL combination retains hostile severity because it
combines a browser-target concealment pattern with temp, mapping, process,
wait and deletion APIs; the description does not assert a data binding.

The supposedly random-executable dropper required only a root EXE path and a
hash-shaped temporary EXE path, so it is now a notable path combination. Its
MPRESS variant remains suspicious for the packed sparse-loader combination.
The hash-shaped temporary path observation itself moved from file creation to
executable-path references; it did not require a create operation. NSIS temp
entry and high-entropy data remain a suspicious installer-layout profile.
Other rules in legacy `staging/temp` remain.

| Former ID | Destination ID | Criticality |
|---|---|---|
| `go-stage2-payload-path` | `micro-behaviors/fs/path/file::go-stage2-bin-text` | component |
| `go-c2-download-payload-func` | `metadata/lang/source/naming/function/communication::go-c2-download-payload-name` | component |
| `go-hidden-stage2-download` | `objectives/execution/staging/acquire::go-hidden-sysmon-stage2-network-profile` | suspicious |
| `native-hidden-shell-stager` | `micro-behaviors/fs/path/hidden::native-hidden-numeric-self-shell-references` | notable |
| `native-base64-temp-driver-drop` | `metadata/file/profile/encoding::native-base64-temp-driver-path-text` | component |
| `mapped-temp-payload-execute-cleanup` | `objectives/execution/payload/file-exec/spawn/native::unsigned-dll-temp-map-process-cleanup-profile` | hostile |
| `native-temp-driver-service-dropper` | `objectives/execution/staging/reconstruct::native-encoded-temp-driver-service-profile` | suspicious |
| `random-executable-dropper` | `micro-behaviors/fs/path/executable::root-exe-and-hash-temp-exe-paths` | notable |
| `mpress-random-executable-dropper` | `objectives/anti-static/pack/mpress::mpress-root-and-hash-temp-exe-paths` | suspicious |
| `installer-temp-high-entropy-data-stage` | `metadata/file/profile/installer-layout::nsis-temp-high-entropy-data-profile` | suspicious |

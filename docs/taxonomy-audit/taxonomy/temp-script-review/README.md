# Temporary script staging review

The Python and Zig files in legacy `staging/temp` were reviewed by matcher;
other rules in that directory remain. The 14 moved rules preserve their
matching conditions, scopes and confidence, including the external consumer
of the hidden shell-path rule. Unsupported staging and interpreter ATT&CK
labels were removed.

The Python composite's combination of a hidden temp prefix, symlink,
interpreter launch and staged-file references remains suspicious. Its exact
source fragments are components and do not independently establish payload
generation, writing or execution. The Zig command and decoder strings are
also components; the path and command profiles describe the source evidence
without claiming the decoder writes or launches the path. The beacon profile
requires POST beacon text and a hidden path, but does not bind them together.

| Former ID | Destination ID | Criticality |
|---|---|---|
| `python-hidden-temp-stager-dir` | `micro-behaviors/fs/temp/directory::python-hidden-svc-prefix-mkdtemp` | component |
| `python-stager-symlink-create` | `micro-behaviors/fs/link::python-source-link-symlink-call` | component |
| `python-symlink-subprocess-exec` | `micro-behaviors/process/create/argv-launch::python-executable-link-path-subprocess` | component |
| `python-decoded-stager-write` | `metadata/file/profile/operation-reference::python-generate-stager-call-text` | component |
| `python-stager-file-write` | `micro-behaviors/fs/write/file/mode::python-stager-path-open-write-mode` | component |
| `python-stager-exec-chmod` | `metadata/lang/source/syntax/call/member::python-stager-path-chmod-755-text` | component |
| `python-hidden-symlink-stager` | `objectives/execution/payload/file-exec/command/script-host-embedded::python-hidden-temp-symlink-launch-profile` | suspicious |
| `zig-hidden-temp-shell-path` | `micro-behaviors/fs/path/hidden::zig-hidden-temp-shell-path` | notable |
| `zig-shell-payload-commands` | `metadata/lang/source/literal/fragment/sequence::zig-id-uname-whoami-command-text` | component |
| `zig-hidden-tmp-lure` | `micro-behaviors/fs/path/hidden::zig-hidden-syshealthd-path` | component |
| `zig-b64-hidden-tmp-shell` | `metadata/file/profile/encoding::zig-base64-hidden-temp-shell-text` | component |
| `openwrt-zig-temp-shell-stage` | `metadata/file/profile/command-options::zig-hidden-shell-system-command-profile` | suspicious |
| `zig-hidden-b64-tmp-stage` | `metadata/file/profile/encoding::zig-base64-hidden-shell-path-profile` | notable |
| `zig-syshealth-lure-stage` | `metadata/file/profile/network::zig-hidden-syshealth-beacon-text` | suspicious |

Docker CLI v29.9.0-rc.2+incompatible and its pinned setup-buildx-action
594f3bf4285d9ea8dc53c9a0c9c4092420091003 are benign.

Fetched comparison artifacts:
- https://proxy.golang.org/github.com/docker/cli/@v/v29.9.0-rc.1+incompatible.zip
- https://codeload.github.com/docker/setup-buildx-action/tar.gz/e8235251b82e23c90e6fad50016f0a78b7f28f11
- https://codeload.github.com/docker/setup-buildx-action/tar.gz/594f3bf4285d9ea8dc53c9a0c9c4092420091003

The previous CLI release has identical container_run.md and build.yml.
Only 12 CLI files changed: cloud resolver terminal/context handling,
associated tests, CI updates, and go-runewidth dependency metadata.
The action diff adds pulling configured/default BuildKit images before
creating the builder. Its package.json and powershellCommand helper are
unchanged. The helper quotes local script paths and parameters, encodes
UTF-16LE as base64, and returns argv. There is only one powershellCommand
occurrence in the bundle: the definition, not a call.
The source map enumerates the same 839 source paths in both action versions.
No added credential export, payload execution, or attacker endpoint was found.

The Docker socket passage explains existing daemon access, followed by an
unrelated Windows path requirement. Generic give/full access/must wording
cannot establish coerced document access. Require the existing fixed-recipient
grant evidence with the mandatory language.

An EncodedCommand literal remains notable. Suspicious invocation now requires
launch evidence. The invocation composite moved from process/create/hidden to
process/interpreter/powershell/command, since it does not require a hidden window.
The bypass consumer references the new ID and the existing source/raw launch
legs directly. Source/raw observations retain their matchers without another
suspicious umbrella. The bare JavaScript option leg is replaced with a
child-process launch matcher. Positive launch control:
testdata/hostile/js-encodedcommand-static-payload.js (copied outside the testing
path for evaluation because testing-path exclusions otherwise suppress it).
The forced-recipient control still matches; socket-permission.md and the
extracted encoded-argv-builder.js helper do not establish either objective.

Additional placement corrections preserve the two filename matchers and their
exclusions: registry-metadata-json-basename and meta-json-sidecar move to
metadata/file/naming as metadata-json-basename and meta-json-basename.
All exact consumers were updated, including the wheel/sdist exe-link consumer.
These names do not identify npm/PyPI or supply-chain impersonation.
Repeated publication-field exclusions use a shared neutral publishing atom.

Atomscan's embedded engine is older than the installed Cleave validator: it
rejects the repository's existing for: [yaml] declarations. Cleave itself
supports YAML correctly. All six pre-existing YAML declaration files are
restored unchanged, and the engine source checkout is unchanged.

For the final Atomscan runs, a private copy supplies the missing YAML-to-Text
conversion entry in its older embedded engine. That is the same neutral bucket
used for passive structured text; both the YAML author scope and YAML input
route consistently to it. The single byte change is SHA-guarded and reproduced
by prepare-compat-tools.py; installed tools are untouched. This does not disable
validation, change criticality, or suppress any fixture. Final make validate
uses the UNMODIFIED installed Cleave executable.

Fixture expectations follow the relocated PowerShell ID. The WSL control
continues to require its hostile boundary-crossing trait; a standalone flag
no longer contributes a suspicious finding. The benign open-library cap allows
one additional valid notable observation. No hostile expectation was removed.

Verification: atomscan slow/no-follow scans of the full CLI ZIP and action
tarball, plus individual flagged members, contain zero suspicious/hostile
traits. Both forced-grant and actual encoded-launch positive controls match.
Cleave facts captured the archive, action bundle, source map and documentation.

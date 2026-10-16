# masscan-output-format anchor controls

The bare `--output-format` flag is shared by scanners, SBOM emitters, and
ordinary CLIs, so it is a neutral capability
(`micro-behaviors/process/argument/option::output-format-option`). The
masscan reading (`well-known/tool/offensive/frameworks::masscan-output-format`)
requires a masscan-specific anchor beside the flag.

Fixtures are compiled binaries (markers live in `.text`, as in real scanner
builds); sources and `build-controls.sh` document provenance. Fixtures are
scanned, never executed.

- `positive/flag-context`: flag plus tool name, distinctive options, and
  scan banner. Both the neutral atom and the composite fire.
- `near-miss/bare-flag`: the same flag with no masscan marker. Only the
  neutral atom fires.

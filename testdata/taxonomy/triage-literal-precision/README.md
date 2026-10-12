# Literal-precision triage controls

Four narrowed matchers, each with a positive that must still fire and a
near-miss drawn from real false-positive evidence that must stay silent:

- `arch-keyed-hex-blob-dict--rx-21`: was a bare `macos` substring with a
  placeholder description; now a sibling-shaped arch config-key marker.
- `finding-remediation-field`: bare `remediation:` matched narrative prose
  ("execute the remediation: 1. ..."); now assignment or quoted-key form.
- `agent-hook-input-read--tool-name`: bare word matched `{tool_name}`
  interpolation placeholders in log f-strings; now brace-guarded.
- `defensive-threat-signature-doc`: the `tool call details` alternative
  matched ordinary logging prose; now the built-in-signatures phrase only.

Cases checked with `cleave --traits-dir . --json` and assertions over
emitted IDs.

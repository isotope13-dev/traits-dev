These controls distinguish quoted prompt injection tests and defensive filter
examples from instructions carried by an agent skill. The existing passive-review
SKILL.md control must retain both hostile detections. The ungraded.md control
quotes the same phrase without a testing methodology heading and remains detected.

The reviewed wicked-garden 12.45.0 archive contains a safety-review input filter
that returns False for injection patterns and a feature-test playbook that probes
a configured system under test. Both are benign documentation. Existing same-file
exceptions now recognize safety-review headings, probe-method headings, and the
hyphenated spelling of prompt injection; no package identity exemption is used.

OpenCode Swarm 7.154.2 and 7.154.3 contain identical Windows sandbox tests. Both
encoded strings decode to `IEX (New-Object Ondows Nem)`, an invalid test payload
passed to detectPowerShellEscape and asserted true, never executed by the test.
The retained suspicious binary/embedded/base64-powershell finding is emitted by
the engine, rather than YAML. Each archive has one unique suspicious trait and
zero hostile traits. Graphifyy 0.9.82's wheel matches the supplied SHA-256 and
implements user-directed corpus extraction through configured LLM providers.
The fetched fastmcp and pydantic packages have no hostile or suspicious findings
in the supplied list. All dependencies were scanned independently before and
after editing the documentation traits.

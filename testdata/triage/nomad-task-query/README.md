# Nomad API task query false positive

Sample: `github.com/hashicorp/nomad/api@v0.0.0-20261007123744-e37365bc23fa`.
Archive SHA-256: `e2626b413d1f32f57159ecef9723a250e36e7fad92d575463aa804901ba5ba02`.
Judgment: BENIGN.

Fetched upstream releases from:
- https://codeload.github.com/hashicorp/nomad/zip/refs/tags/v1.7.7
- https://codeload.github.com/hashicorp/nomad/zip/refs/tags/v1.8.0
- https://codeload.github.com/hashicorp/nomad/zip/e37365bc23fa4e6ed24543c0392503f5b6a63ff2

Compared the API source trees. All 94 sample members are byte-identical to
upstream at the claimed commit. Compared with v1.7.7, allocations.go adds
SetPauseState/GetPauseState and request/response types for task schedules.
GetPauseState sends a caller-supplied task name to the configured Nomad client
allocation's /pause route. Its comment `?task=<task>` is an API placeholder,
not an AI prompt, exfiltration payload or remote execution instruction.
The same comment exists in v1.8.0; later code fixes the missing task query in
the request. Other changes include API fields, compatibility cleanup and
standard-library slices/maps iteration. The preceding commit's allocations.go
is identical; the release commit changes root-module dependencies, not API code:
https://github.com/hashicorp/nomad/commit/e37365bc23fa.patch

The original suspicious ai-prompt-url-angle-data composite combined a generic
task query key with angle-placeholder syntax. A bare task selector now stays
notable and needs AI chat endpoint context to join prompt composites. Plain
angle placeholders, including percent-encoded placeholders, are notable neutral
transport observations like existing dollar and brace templates. The higher
level image-template composites retain their suspicious classification.
No vendor, filename or exact placeholder allowlist suppresses the detection.

cases.json records positive and near-miss expectations. Scheduler, CMS and
OAuth examples must not be labeled AI prompt templates. AI task, camel-case
AI task, prompt and encoded prompt examples retain template findings. A task
query containing a templated remote image retains the suspicious image finding.

Further firing-trait corrections:
- Credential substring searches require a credential word in argument 1,
  rather than in the name of argument 0 (the auth separator false positive).
- The integer guard keeps its matcher but is named/described as a field
  comparison; its consumer supplies any activation claim.
- TaskName requires Windows -TaskName or /TN argument syntax; a Go field is
  neither Windows autorun nor a scheduled-task operation.
- HTTP request/client construction, response reads, certificate loading,
  stdio assignments and lifecycle hook references move to their supported
  operation homes. Exact consumers and fixture IDs follow the moves.
- A .pem suffix establishes a certificate/key path, not specifically a
  private SSH key. Its private-key/theft mapping is removed. Directory-only
  private-key and shell consumers intentionally no longer inherit generic
  PEM paths or ordinary stdio assignment as key/shell evidence.

Run `python3 testdata/triage/nomad-task-query/check.py` for the focused controls.

Verification: 46 focused trait assertions passed. The final atomscan archive
scan emitted zero suspicious/hostile traits and none of the AI prompt,
credential-keyword or Windows TaskName false positives. The v1.7.7
allocations.go control also emitted zero suspicious/hostile findings.

Judgment marker summary (63 characters):
`Nomad API: diff adds task scheduling; task= requires AI context`

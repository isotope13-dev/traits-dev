The JSON corpus traits describe grading expectations, not executed commands.
The exception requires both an expected answer rejecting untrusted commands
and an assertion forbidding embedded commands in the same file. Ordinary
instructions, unrelated prose, and incomplete grading records retain detection.
The controls use neutral archive paths to avoid existing test-directory
exclusions and verify that a neighboring fixture cannot suppress a live prompt.
The override-token rule explicitly includes JSON, so ungraded JSON instructions
retain detection without relying on embedded-text analysis.

Run `python3 testdata/taxonomy/command-injection-evaluation/check.py --cleave /path/to/cleave`.

Triage evidence: SHA-256
`1b8710000cdd988639dd33b55830cafc6d35bfa9394f0d9900a4ba4bd695ded8`
is the NVIDIA/skills archive at `80fd955e037bbd73cd1799fe0c6fd6612bedb8e0`;
all 5,977 regular files match that upstream Git tree byte for byte.
The pre-addition revision `6b053fab3c8b5075a99661456905d504bed786f7`
was fetched from upstream and archived for comparison; it emits no suspicious
or hostile traits. The alerting evals.json was introduced with the entire
Compute Sanitizer skill in `8a7430653e0d7c26e17642b03cc9297213fc16ac`.
The DeepStream SOP subtree has no changes between the compared revisions.

The two new adversarial cases quote a fake system override with an upload to
example.invalid and a fake developer message requesting privileged chmod.
Their expected answers and assertions forbid those actions. The accompanying
SKILL.md treats source and diagnostic output as untrusted data and restricts
commands to the requested CUDA diagnosis. evals/config.yml selects isolated,
GPU-free reasoning tasks and an LLM judge over expected_output and assertions;
these strings are test inputs, not shell execution paths. No obfuscated loader
or hidden command execution was found in this addition.
Decoded string inspection recovered ordinary Unicode escape punctuation in
three evaluation strings, with no encoded executable payload.

The DeepStream skill supplies application templates: its container entrypoint
launches a FastAPI server, Docker build steps install SDK/build dependencies,
and optional Kafka publishing serializes application inference results to the
configured broker. These capabilities fit its documented video inference
purpose. Deployment authorization and actual runtime configuration are absent;
the archive is judged BENIGN from its contents and the decisive source diff.

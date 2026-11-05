# ANI mislabeled-good review, 2026-11-04

The sole sample, `ce7f5c087a2a`, is an Alpine package containing an Airflow
installation and dependencies, not an animated cursor. Its first local slow
scan examined 41,831 reported components. It raised a webshell claim on
Airflow's AWS login handler because the matcher interpreted
`anyio.from_thread.run(request.form)` as a process launch. The matcher now
requires a bare process sink or an `os`/`subprocess` qualifier. The handler
no longer matches; a Flask request passed to `subprocess.run` still produces
the hostile webshell finding.

A Tornado test sends one HTTP request with conflicting framing headers to its
local test server and asserts a 400 response. A hostile desynchronization
finding had combined this request with unrelated request literals elsewhere
in the same test file. The revised rule requires request-assembly evidence;
the rejection test no longer reports a hostile finding, while an actual
pipelined request and existing separate-fragment Python and Go probe controls
retain theirs. The conflicting-header observation remains suspicious.

An archive-wide DNS/OOB rule had combined an installation hook, DNS API and
OOB host from separate package components and described that as a lookup by
the hook. It now reports only their co-occurrence. The bundled LiteLLM UI also
contains labeled prompt-injection test examples; a JavaScript source string
mentioning a system prompt is now recorded as a neutral phrase observation,
while a direct prompt text retains its suspicious observation.

The full archive rescan covered 41,831 reported components and found no
hostile traits. Its only suspicious trait is the conflicting-header test
described above, also propagated to the archive. Endpoint ruling: good;
validation passed and Hopper confirmed the label (no-op).

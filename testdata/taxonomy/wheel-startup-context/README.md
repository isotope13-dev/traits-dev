# LiteLLM 1.107.0 wheel review

All three requested provenance samples are **MALICIOUS** through their fetched
original wheels: musllinux x86-64 (`3e9014ef6a18` provenance), macOS x86-64
(`1745877fbb9a`), and manylinux x86-64 (`4fb7989a132f`). The hashes in the
request identify the provenance JSON, not the wheel bytes.

`forager fetch --all-wheels ... pkg:pypi/litellm@1.107.0` recovered seven
original wheels and their provenance in the task scratch directory. The three
wheel SHA-256 values match the provenance artifact digests:

| Platform | Original wheel SHA-256 |
| --- | --- |
| musllinux x86-64 | `1bbce8caa94f01c0aaa0b7ddae51553a8a32e1ce53d96d44fe583272aff7ad00` |
| macOS x86-64 | `7598727f209d717041db37f7dca271d3a7d328a279890e0e1d55375729aeb86d` |
| manylinux x86-64 | `462d0c9f67ca522d9e0e4acd245e90b36ce0d5353604a66bb7c43a1ec4a6fcf7` |

## Behavior and verdict

METADATA describes an LLM-provider API library. The wheels additionally install
`cook.pth`, `cook.py` and `sitecustomize.py` into site-packages through the wheel
`.data/purelib` mechanism. All three files appear in RECORD with their digests;
they are distributed contents. The three requested wheels have byte-identical
copies of these files. The other Unix wheels share them; Windows uses line-ending
variants with the same decoded collector bodies.

No sample was imported or executed. Python AST literal extraction, Base64
decoding and zlib decompression recovered both embedded source bodies. Their
final module-level `pc_entry()` calls were verified, not inferred from strings.

* `cook.pth` imports the compressed `cook.py` wrapper during site initialization.
  Its collector entry sets an environment guard and launches `pc_run_once` in a
  daemon thread. Successful transmission creates a one-time marker; preexisting
  guard/marker state can suppress a repeated collection.
* `sitecustomize.py` acquires a nonblocking file lock, forks, creates a session,
  redirects standard descriptors to the null device, changes directory, and
  runs an hourly loop. `requests.get` response text passes through executor
  helpers to `exec(compile(...))`. A GitHub-hosted domain list selects the HTTP
  server; the code path is `/codepy`. This is a reusable remote-command channel.
* Its second compressed collector runs after domain validation/resolution and
  before remote task execution. It uses the same environment guard, so ordinary
  startup ordering can suppress duplicate collection in the child. The .pth
  collector does not require that domain-list request to succeed.
* All sixteen collection modules are enabled by the supplied configuration.
  The code copies and queries Chromium login databases, unwraps Windows keys
  with DPAPI and decrypts AES-GCM passwords, and uses the Linux Chromium PBKDF2
  key and AES-CBC path. It also collects Firefox logins/key material and history,
  SSH files, shell histories, cloud/container/CI credentials, AI-tool tokens,
  process environments, GPG private keys, and TLS private keys. Cloud metadata
  queries retrieve IAM/service-account credentials and optionally verify AWS
  caller identity. A child interpreter uses Prisma queries to read LiteLLM
  provider credentials and model parameters.
* `pc_collect_all` results become a JSON document in `pc_run_once`. A random
  AES-256-CBC key encrypts that document; RSA-OAEP wraps the key. `pc_pack` creates
  an in-memory gzip tar with header, ciphertext and wrapped key. `pc_post` sends
  these bytes to the configured `http://www.litellm.dev/healthcheck` endpoint,
  with retry logic and a token header. This is a concrete collection-to-send
  chain, independent of the trait score.

The broad secret acquisition, concealed interpreter startup, and arbitrary
remote execution outweigh any benign diagnostic/tooling explanation. Installation
history, runtime transmission success and the final remote task body were not
provided. No actor attribution is asserted.

## Trait corrections and preservation

The old `pypi-wheel-pth-startup-host-recon-snapshot` rule did not require a
snapshot write, an upload, or a link between the .pth import and the surveyed
module. Two harmless diagnostic wheels reproduce its hostile match, including
one with the JSON/metadata code in an unrelated module. Their code performs no
file write, network request, secret targeting or concealed execution.

Its matcher, scope and type/platform coverage are retained under
`micro-behaviors/process/interpreter/python::wheel-pth-metadata-json-context`,
with a co-occurrence description and **notable** criticality. This preserves the
supported startup-context observation without claiming a hostile local snapshot
or supply-chain compromise. Unsupported ATT&CK/MBC objective mappings are removed.
The component facts remain unchanged. This correction is in the dependency's
rules; there is no exception for a dependent package.

The other corrections preserve matching and severity:

| Previous ID | Canonical ID and supported claim |
| --- | --- |
| `objectives/anti-static/obfuscation/multi-layer::python-medium-base64-decode-exec` | `objectives/anti-static/obfuscation/payload/encoded/exec::python-one-line-base64-exec-large-string`: one-line evaluation, Base64 decoding and a large string co-occur; only one encoding layer is required. |
| `metadata/file/data-blob::python-string-over-10k` | `metadata/file/profile/string-population::python-string-at-least-10k`: maximum extracted-string length is at least 10000; no opaque payload is inferred. |
| `objectives/anti-static/obfuscation/encoding/content::encoded-python-malware-pattern` | `objectives/anti-static/obfuscation/encoding/content::encoded-python-execution-primitives`: multiple encoded execution/decoding primitives, without a malware identity claim. |

Placement was checked by the matcher's standalone claim and by its nearest
alternative: interpreter startup context versus malicious persistence; one-layer
encoded execution versus multi-layer concealment; measured string population
versus executable payload. These are existing admitted leaves, with no new
partition or directory-budget change.

Exact and ancestor YAML consumers were inspected. The metric's only exact
consumer is rebased. No YAML rule consumes the retired snapshot ID or its
ancestor selectors. The obfuscation ancestor retains the moved execution rule;
its JS consumers cannot gain Python file-scoped evidence. The new encoded-parent
membership cannot satisfy the Ruby-only cookie backdoor. The broad Empire
interpreter alternative already selects the required .pth import constituent;
it has no threshold/proximity condition that could gain an independent role.
No consumer required expansion or an exception. Existing wheel fixtures were
inspected for startup members; none carries .pth/sitecustomize. The recovered
Windows wheel supplies an additional original positive outside this batch.

## Verification

For each requested provenance file, `atomscan --no-update --mode slow --format
json <path>` was run before and after, following its wheel dependency. `cleave
facts` was run on all three inputs, all three original wheels, and the two
representative injected Python files, including the decoded strings. The musl
wheel was additionally scanned directly in isolation before/after with
`--follow=none`; so was the out-of-batch Windows wheel. Final scans explicitly
select this checkout with `CLEAVE_TRAITS_DIR`.

| Input | Hostile before/after | Suspicious before/after | Risk before/after | Atomscan probability before/after |
| --- | --- | --- | --- | --- |
| musl provenance -> wheel | 6 / 5 | 8 / 8 | 807 / 690 | .99 / .99 |
| macOS provenance -> wheel | 6 / 5 | 8 / 8 | 804 / 687 | .99 / .99 |
| manylinux provenance -> wheel | 6 / 5 | 8 / 8 | 808 / 691 | .99 / .99 |
| isolated musl wheel | 6 / 5 | 8 / 8 | 807 / 690 | .99 / .99 |
| isolated Windows wheel | 6 / 5 | 8 / 8 | 806 / 690 | .99 / .99 |

These are measured local baseline scores, not the queue's older scores.
`compare.py` verifies every file hash and every finding/criticality against an
explicit mapping for the four corrections, across all archive and decoded
members. There are no other lost findings, severity changes or added findings.
Five hostile findings still cover remote control, browser credential theft,
developer-secret exfiltration and startup persistence. All verdicts remain
HOSTILE, agreeing with the reasoned MALICIOUS judgment. The only lost hostile
claim is the disproven snapshot inference, retained as notable context.

Four static diagnostic-wheel controls pass after correction, with no suspicious
or hostile findings; the two positive context controls formerly matched the
hostile snapshot rule. The existing fourteen Python startup/credential positive
and near-miss controls also pass. Reproduce:

```
python3 testdata/taxonomy/wheel-startup-context/check.py
python3 testdata/taxonomy/python-startup-credential-review/check.py
python3 testdata/taxonomy/wheel-startup-context/compare.py <reports-directory>
```

Artifacts, provenance, decoded bodies, full scans, facts, comparisons and logs
are retained under the task's `scratch/litellm-review/` directory. Each requested
full sample path has exactly one `.MALICIOUS` marker with an evidence-bearing
line under 72 characters. The required final gate is `make validate`, run after
all review files and markers are written, with output in `reports/validate.txt`.

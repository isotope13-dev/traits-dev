# gh-aw-actions v0.91.12 review

Verdict: **BENIGN**. The flagged constructor runs a locally compiled workflow
in an integration test with injected service doubles. The source and its caller
explain this behavior without an obfuscation or unauthorized execution claim.

Sample SHA-256:
`9e6ff333f274228a5e97ac4ef06b0042c7f6d8664ccf3bfa586864d6840a64bb`.
The archive is github/gh-aw-actions revision
`2f6729681c34eb94a2f94d533d4b6492de0d8a19`, tagged `v0.91.12`.

## Execution path and release evidence

`setup/js/work_queue_control_adapter_checks.cjs` exports
`verifyCompiledDispatchIdentity`. Its caller in upstream gh-aw v0.91.12,
`pkg/workflow/work_queue_dispatch_identity_integration_test.go:127`, puts the
local compiler's `step.With["script"]` into the helper's JSON stdin. The helper
constructs an AsyncFunction with injected `require`, `core`, `github`,
`context`, `exec`, `io`, and `getOctokit` arguments. It supplies fake tokens,
in-memory queue clients, assertions and temporary state. Its require shim
returns Node builtins and two selected local adapters; this is test dependency
injection, not a security sandbox. Mock dispatch/run responses exercise valid
and invalid publisher, credential, worker, tag and revision identities.
Temporary files and environment changes are cleaned up in `finally`.

The flagged file is byte-identical to the same file in upstream gh-aw v0.91.12
(member SHA-256
`603c083687330af93f22d8bc399fbdbb634f1a8f0da270d649518eb06be81050`).
Forager recovered original GitHub source archives for these comparisons, with
their `.forage.json` provenance kept in scratch:

- `v0.91.11`, revision `c0d661a2925687358c937720c5c7d3c338299f55`,
  is the immediate predecessor. Both archives contain 879 regular files;
  16 differ. The AsyncFunction invocation is unchanged. The helper's diff
  adds `wrong-dispatch-tag`, tag-read assertions and immutable tag refs.
  Other changes cover OIDC endpoint validation, merge-aware PR patch policy,
  queue reconciliation, model-usage accounting, and safer redaction errors.
  This predecessor also fires the old trait with the current rules; the queue's
  clean-earlier premise does not hold for the immediate predecessor.
- `v0.91.0`, revision `aeaf7fe417d183340479027223c9a1c16464bdbc`,
  has no suspicious/hostile findings and lacks this AsyncFunction helper.
  The later release added compiler/work-queue testing functionality.

`cleave facts` and the decoded-string view were inspected, along with the
source, mocked sinks and upstream caller. No concealed payload is involved in
this execution path. Network operations, process execution, token use and
filesystem operations elsewhere in these CI actions remain useful capabilities;
the benign verdict does not suppress them. The review establishes the shipped
code's purpose, not the trustworthiness of an unknown deployed workflow or of
arbitrary inputs someone might supply to the exported helper.

## Rule changes and consumers

The old `objectives/anti-static/obfuscation/eval/require::async-function-require-arg`
matched a plain constructor argument, which establishes no concealment. It also
matched a quoted example and a one-argument constructor whose body is `require`.
Replace it with the notable capability
`micro-behaviors/metaprogramming/generation::js-async-function-require-parameter`.
The parsed-call matcher requires a first string argument `require` and a second
argument, so it actually observes a parameter rather than the function body.
Keep the existing general AsyncFunction compilation detection unchanged.

The exact consumer, `server-response-async-code-execution`, now uses the neutral
ID. Its remaining HTTP-response/request-context requirements are unchanged.
Three ancestor consumers select `objectives/anti-static/obfuscation`: concealed
credential exfiltration, long-tail build configuration, and hidden listener.
They correctly stop treating ordinary loader injection as concealment; no neutral
generation reference was added to those selectors. No source generation ancestor
selectors were found. A search of the other supplied sample artifacts found no
additional matching constructor; archives over 60 MiB were excluded from that
focused search. The upstream original provides an additional real benign case;
the remote-hotfix fixture tests the retained attack mechanism, not an asserted
malware-family attribution.

The old `allowlisted-require-shim` exception had this rule as its only consumer.
Remove that now-unused suppressor; its two underlying observations remain.
The new neutral capability needs no test-name or shim exclusions. This also
avoids silently disabling the response-execution composite under test paths.

The generation leaf had 100 rules. Reviewing its contents found two quoted-loop
matchers and their union incorrectly classified as code generation. Move their
unchanged definitions to `metadata/lang/source/literal/target-loop-template.yaml`,
updating all three scanner consumers. Parsed YAML equality and exact consumer
replacement checks confirm unchanged matchers, scope, severity and logic.
There are no source or destination ancestor selectors. The `id: metadata` in
wheel/sdist packaging is a local definition, not a directory reference.
This leaves 98 rules in generation without changing a directory budget.

## Verification

Run `python3 testdata/triage/gh-aw-actions-version-drift/check.py` for seven
controls: local compiler code, hostile HTTP hotfix, quoted documentation, other
parameter names, a body-only constructor, quoted loops and an executable loop.
The hostile response-execution finding survives the change. The quoted-loop
positive and negative controls preserve the relocation's boundary.

Before/after atomscan reports cover the same 924 entries, including members.
The only lost finding is the incorrect suspicious obfuscation claim on the
helper and its inherited archive finding; the notable require-parameter
capability replaces it at both levels. No other detection is lost. The helper's
trait risk changes from 56 to 17. No suspicious or hostile findings remain.
The classifier remains BENIGN: its generic route probability changes from
0.53701013 to 0.7082891, the tar route from 0.05635941 to 0.017967612, and
the helper probability from 0.0008800526 to 0.0000920693. No classifier verdict
disagreement was exposed. Probability movement is recorded, not optimized.

Full scans, facts, decoded strings, commit/tag records, provenance, corpus-search
limits and focused results are in
`/usr/local/var/cyclotron/tmp.noindex/cyclotron-d11fe31e/scratch/version-drift-*`.
The required final repository check is `make validate`.

# SimpliRoot 3.6.1 version-drift review

Verdict: **BENIGN**. Identity: SimpliRoot WordPress live-chat, CRM lead-capture,
call-tracking and measurement-gateway plugin, version 3.6.1. Original SHA-256:
`fd1e861a9d2620aaedaf1e706d0cb3a2ee1fbfc1aeb6a1ee41ed6b8592d355ed`.

## Decisive release comparison

Fetched the original 3.6.0 ZIP with:

```
forager fetch -o <scratch>/simpliroot-3.6.0 https://downloads.wordpress.org/plugin/simpliroot-lead-capture.3.6.0.zip
```

Recovered identity/version agree with its PHP plugin header and readme. SHA-256:
`2d4440b784ca1fbd6ad43152357bb04edcdcad23814e84607b1ec29e002581b7`.
The original ZIP and `.forage.json` provenance remain in the task scratch tree.
The complete recursive diff changes only the main plugin PHP, readme and
`tests/cmp-strip-test.php`. Includes, all other tests and license are identical.

Production code adds `simpliroot_cmp_to_top`, which finds the plugin's existing
consent-script tag inside `<head>`, moves it ahead of other scripts while keeping
an early charset declaration ahead of it, and otherwise returns the input
unchanged. The existing output-buffer hook now calls the stripping and ordering
functions in sequence. Its existing guards require a project token, enabled CMP
configuration, and a frontend non-AJAX request. There is no new endpoint or
server-side remote-code execution path in this release.

The flagged test previously had two `eval($m[0])` sites. The new ordering test
adds a third, crossing the unchanged three-match density rule. Every site
extracts a fixed named function definition with `preg_match` from the adjacent
local plugin source read by `file_get_contents`; the result is evaluated so
assertions can invoke those functions outside WordPress. This is visible,
unencoded test code. It is not an encoded payload or analysis concealment.
`cmp-strip-test.php` here is a byte-for-byte copy of that original member.

## Execution and effects reviewed

* Form-builder hooks and the frontend submit listener collect contact fields,
  attribution, consent-checkbox states, page URL, IP and user agent. They store
  leads in a local WordPress table, POST JSON to the configured project at the
  documented CRM service, and retry with WordPress cron. The frontend skips
  password forms and hidden/token fields. These features predate 3.6.1.
* The measurement gateway is off unless enabled in validated configuration. It
  accepts fixed measurement paths and host suffixes, limits body/query sizes,
  disables redirects, verifies upstream TLS, filters outgoing headers/cookies,
  and excludes WordPress login/session cookies. Response analytics cookies
  require the explicit consent signal. No arbitrary upstream URL is accepted.
* Consent takeover removes listed CMP assets from page output and, under both
  `cmp` and `cmp_takeover`, deactivates matching installed consent plugins.
  It records which plugins it disabled and restores those when takeover ends.
  This consequential dual-use behavior is explicit, reversible, documented,
  and unchanged from 3.6.0; its neutral deactivation capability needed coverage.
* Cache handling invokes installed cache-plugin APIs and issues loopback probes
  and PURGE requests. TLS verification is disabled on these loopback requests;
  the accurate notable finding remains. The invalidation REST route uses a
  permissive framework callback but its actual handler verifies a timestamp
  and HMAC before clearing caches. The framework callback cannot establish
  absence of authentication in the handler.
* Test shell execution removes the fixed temporary plugin directory made by the
  takeover test. PHP callbacks, JSON/URL encoding, HMAC, HTTP, cookie handling,
  scheduling, execution and filesystem findings are retained. No concealed
  stage, malicious persistence, credential theft, or attacker command channel
  was established by the archive's execution paths.

Deployment settings, whether the site owner authorized its configuration, and
contents of remotely served scripts are unavailable. This verdict concerns the
provided archive; the release diff and coherent implementation favor ordinary
plugin maintenance over compromise, without assuming a deployment history.

## Rule changes and consumer preservation

* Relocate `dense-eval-calls` to the notable source-syntax observation
  `metadata/lang/source/syntax/call/arguments::php-dense-variable-eval-syntax`.
  Its text regex, counts, density, PHP/platform scope and exclusions are
  unchanged. A lexical population is not an obfuscation technique. The
  multilayer-obfuscation composite references the new ID and retains its
  original matching population. Old ancestor consumers confined to JavaScript
  or ELF cannot consume this PHP atom.
* Rename the lowercase `id`-entry observation and update both consumers. The
  cache-handler registry is a concrete benign match: those entries establish
  lowercase ID syntax, not a scanner signature table. Matcher and severity stay
  unchanged.
* Rename the REST-route composite to describe file-level co-occurrence with a
  permissive callback. Preserve all predicates and update all four exact
  consumers; authentication in the handler is not ruled out by those facts.
* Add a notable structured-call detection of `deactivate_plugins`. Declarations,
  comments and string references alone do not satisfy it. Activation detections
  remain intact. This behavior is also present in the earlier release.
* Relocate the short-function population profile and three related metrics to
  `metadata/file/profile/function-population`, preserving their predicates,
  criticalities and exclusions. Update its two exact objective consumers and
  retain membership in the complexity rule's former directory exclusion by an
  explicit reference. This neutral profile fires on the unchanged cache test's
  mock functions and establishes no obfuscation. Correct the `code_ratio`
  description: a probe with one empty one-line function and 100 top-level echo
  statements reports 0.01; ten empty functions in twelve lines report 0.83.
  It measures function-span line coverage, not executable body content.

## Verification and remaining limits

`python3 testdata/taxonomy/simpliroot-version-drift/check.py` covers nine controls:
the two original test members, dense eval syntax, multilayer decoding/evaluation,
ordinary lowercase IDs, real plugin state calls, non-call references, a signed
REST handler, and generated empty function declarations. These copies are static
scanner fixtures; they are not standalone runnable copies of the plugin.

`python3 testdata/encrypted-request-webshell/check.py` passes its ten existing
positive/negative controls. Before/after scans of that directory and five
existing hostile PHP fixtures produced 17 reports with identical detections
after intentional ID mappings. They cover encrypted request webshells, header
evaluation/error masking, socket-to-eval, remote callbacks, and the OptinMonster
supply-chain loader. No hostile finding was lost. The multilayer control retains
its suspicious finding; dense eval syntax itself is intentionally notable.
No other existing PHP fixture in testdata met the old three-call density gate.

The synthetic `request-eval.php` control exposes a remaining limitation: direct
HTTP input assigned to variables and later evaluated has only neutral findings
here. The old density heuristic supplied an obfuscation label without proving
obfuscation. Its removal does not supply a correct request-provenance detection.
`cleave facts flow` retains the assignments and eval inputs but represents the
PHP superglobal source as unknown/merge rather than a member-read origin, so a
source-to-sink matcher on those facts cannot establish that relationship. This
separate detection gap is recorded rather than restoring the inaccurate label.
It is not behavior found in the sample's test-eval path.

Original/final archive scans: hostile **0 -> 0**, suspicious **1 -> 0**, notable
**127 -> 129**. The flagged member changes **0/1/9 -> 0/0/10** (hostile/suspicious/
notable); main plugin notable **86 -> 87**; cache test notable remains **13**.
Every other member remains at zero hostile/suspicious. Every original observation
is retained under its corrected ID/criticality; plugin deactivation is the only
new operation. Atomscan's calibrated classifier is BENIGN before and after; its
v18 feature-model age warning remains an engine/model limitation, not a sample
behavior or a reason to inflate traits.

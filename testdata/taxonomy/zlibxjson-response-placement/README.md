# zlibxjson 8.2 stranded-member review

The original wheel is confirmed MALICIOUS and was not re-judged. The extracted
`zlibxjson/main.py` is independently MALICIOUS. Both supplied SHA-256 values
were verified. The program was inspected statically; no specimen was executed.

The console-script declaration invokes `zlibxjson.main:init`; importing the
module only exports that function. With APPDATA set, init passes its hardcoded
Discord attachment EXE URL and APPDATA to the download helper. That helper
creates the directory if necessary, derives a basename after removing the URL
query, streams a checked HTTP response to that binary file, and returns its
path. The caller passes the returned path to the launch helper, which calls
Popen with shell=True and CREATE_NO_WINDOW. With no APPDATA, init only prints a
diagnostic. Launch exceptions are printed; transfer exceptions are not caught.
There is no obfuscation, persistence, credential access, exfiltration,
privilege escalation, or cleanup in this member.

The sole command is a hidden external Windows executable loader, with no
substantive library functionality or documented installer purpose. Placeholder
package provenance and the absence of an explanation for this command support
the individual malicious judgment. Deployment authorization, payload contents,
and runtime success remain unknown. Forager returned 404 for the payload URL.
The mandatory exact-version all-wheels attempt found unavailable PyPI metadata
and failed its browser fallback because Chromium ICU data was unavailable.
The supplied original wheel remained available throughout.

## Trait corrections and coverage

Moved `raise-for-status` from `http/lib/requests` to `http/response`: this API
validates a response, independent of the client backend. The matcher, confidence,
notable severity, platform scope, and Python scope are unchanged. Updated its
explicit consumer and all ancestor-directory consumers by adding the relocated
atom as an alternative. Each affected selector was an `any:` alternative;
cardinality and proximity still select the same underlying observations.

During the response-leaf review, the existing `native-status-field-pair`
matcher proved misplaced: it only recognizes `status=active` beside
`service_target=`. Those key/value strings alone establish neither HTTP nor a
service operation. Moved and renamed it to
`metadata/lang/source/syntax/key-value::native-status-service-target-fields`,
with an accurate description and unchanged matcher, scope, confidence, and
notable severity. Its beacon consumer still requires its independent HTTP POST
pattern. No broad destination-ancestor consumers acquire the new field fact.
The response and key-value leaves each contain 100 rules after these moves.

All firing sample traits were checked against source, call, literal, flow, and
decoded-string facts. Accurate existing coverage includes streamed HTTP-file
staging, APPDATA destination flow, query-stripped basename construction,
returned-path-to-hidden-shell activation, environment access, shell parsing,
console suppression, and package entrypoint declarations. No additional
supported distinct behavior needs a detector. No matcher was weakened and no
severity was reduced. The existing CDN composite correctly describes endpoint
co-occurrence rather than claiming URL-to-chain data flow.

The 3–5-hostile-trait goal remains unmet: the only implemented action is the
covered download/stage/hidden-launch chain. Its reusable mechanics also fit
legitimate updaters, so they remain suspicious. Reviewed the entire call chain,
package entrypoint and missing-payload recovery; found no additional persistence,
theft, evasion mechanism, destructive effect, or escalation. The unrecovered EXE
prevents downstream analysis. Splitting this one flow into several hostile
traits would duplicate or invent behavior. The package-context judgment is
stronger than any supported generalizable hostile predicate here.

## Verification and remaining classifier gap

`python3 testdata/taxonomy/zlibxjson-response-placement/check.py --baseline <HEAD-traits>`
passes placement controls and all 18 before/after fixture comparisons, including
existing specimens outside this batch. The controls distinguish an actual
raise_for_status call from a name/docstring reference, ordinary local status
fields from HTTP beacon context, and a lone service-target field from the pair.
All 10 existing stranded-review controls also pass. Every finding and severity
is preserved after normalizing the two relocated IDs.

Full Atomscan scans before/after have the following distinct H/S/N counts.
Archive parents inherit member findings.

| Analysis unit | Before H/S/N | After H/S/N |
| --- | --- | --- |
| main.py standalone | 0/2/25 | 0/2/25 |
| wheel | 0/2/31 | 0/2/31 |
| wheel member main.py | 0/2/25 | 0/2/25 |
| METADATA | 0/0/3 | 0/0/3 |
| entry_points.txt | 0/0/3 | 0/0/3 |

There are no material detection losses. The member and wheel both retain model
probability 0.99525124 at calibrated FP level 5000; the default classifier is
BENIGN, disagreeing with the member judgment and the archive's confirmed
conviction. The source analysis reports `flow-query-incomplete`; manual tracing
establishes the supplied helper relationships. The scanner also warns that
feature specification v18 predates expected v21. No rule was inflated to change
that classifier result.

Raw before/after scans, full facts (including decoded strings), normalized
comparisons, baseline traits, and Forager logs are under
`/usr/local/var/cyclotron/tmp.noindex/cyclotron-90084b2c/scratch/zlibxjson-analysis`.
Final repository validation is run after all edits and judgment markers.

The marker lines are:

```text
zlibxjson loader: hidden Discord EXE launch; fix response placement
zlibxjson 8.2 wheel: confirmed malware; hidden EXE loader verified
```

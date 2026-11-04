# Probable-hostile review — 2026-11-04

Source: `/var/tmp/gauntlet-triage/probable-hostile`, 161 SHA-256-verified artifacts (781,447,542 bytes). The manifest is bookkeeping, not a sample. All 161 artifacts have completed static review. After official-registry and preserved-payload follow-up: 89 good, 68 bad, 4 dual-use, zero inconclusive. See the latest reassessment below; earlier provisional rulings are retained as history. Final validation passed and all Hopper classifications are recorded.

Working inventory and safely extracted members: `/tmp/probable-hostile-review/`. Initial local atomscan reports: `/tmp/probable-hostile-initial.jsonl`. All inspection is static; package scripts and payloads are not executed.

## Detection corrections

- Fontus 0.0.1 and 0.0.2 implement an explicitly invoked font census, local cache, and JSON collector upload. Three hostile composites incorrectly combined ordinary inventory/tunnel behavior with tiny 0.0.x package metadata. Sparse metadata supplies no attack evidence. Removed those redundant hostile claims, retaining the existing suspicious shell-inventory-to-quick-tunnel finding and neutral operations. A call in a separate `__main__.py` is CLI activation, not covert import execution.
- Split API names, reflected environment access, and `getBuiltinModule` establish concealment, not a hostile payload. Corrected that composite's severity. A second composite claimed remote tasking from split fetch plus an unrelated local spawn. It now requires the independently detected remote zsh prompt-command channel. Version 0.0.16 only stores received JSON; versions 0.0.21/0.0.22 interpolate remote text into a command-substituting zsh prompt.

## Scanner discrepancy

Installed atomscan omits extensionless `Rakefile`/`Gemfile` archive members as unknown even with `CLEAVE_SKIP_CACHE=1 --show=all`. Current sibling cleave recognizes them as Ruby and detects three hostile traits in each of the `xmastree` and `et_phone_home` gems. The local filefacts path recognizer already includes these filenames. A temporary build of atomscan against the current sibling cleave/filefacts corrected the Ruby filename recognition without adding an engine feature. Installed scanner dependencies were stale. The final scan uses that temporary build.

## Checklist

- [x] Verify all 161 sample hashes and inventory formats.
- [x] Initial local atomscan pass over the entire input.
- [x] Review each artifact and its meaningful component findings.
- [x] Repair and verify the reviewed missing/misleading detections; limitations below.
- [x] Complete `make validate`.
- [x] Stage and hash-check all good copies.
- [x] Apply all final Hopper classifications after validation.

## Reassessment of inconclusive rulings

The initial seven provisional inconclusive decisions were reviewed again against the endpoint standard after the user challenged the threshold. Three were revised to good: both Luckee wheels implement a compiled Cython CLI with OAuth/query/attachment/session interfaces, and the model ZIP contains inert model data with no loader or exploit. Standard native compilation, unavailable original source, or an unfamiliar data envelope alone do not establish a material security ambiguity.

Four remain inconclusive, all because decisive dependency code is unavailable:

| Artifact | Present implementation | Specific unresolved evidence |
| --- | --- | --- |
| `dependencykfeg-25.1.3.tgz` (`34503e3c7329`) | Empty module; direct GitHub tarball dependency | Referenced `node-acct-utils-1.0.0.tgz` returns HTTP 404; cannot inspect dependency install hooks or runtime code. |
| `atlassian-wallboard-plugin-10.0.0.tgz` (`bb2ca45dc5d9`) | Manifest-only dependency wrapper | GitHub `node-ac2.tgz` returns 404; `claims-ac1` release cannot be resolved. |
| `hijuko_pilara-1.0.0.tar.gz` (`8f9e45a7a26c`) | Version module plus ordinary setuptools dependency declaration | Workers-hosted `plugin_atomic_string_memo` archive returns 404; dependency behavior is unavailable. |
| `tw-motion-css-2.0.2.tgz` (`382d0736f88f`) | Reviewed Tailwind plugin invoking a scoped PostCSS helper | `@codentra/postcss-kinetix` implementation cannot be resolved; resemblance to malicious plugin templates is insufficient to convict this artifact. |

These are unresolved installation/runtime chains, not confirmed malicious wrappers. On an endpoint, inspect the actual installed dependency, package cache/lockfile, process ancestry and resulting file/network activity. A wrapper manifest, off-registry URL, sparse metadata or another package's reputation alone cannot establish a malicious payload. For binary training, retain exclusion until the missing implementation is reviewed. A reviewer judging the wrapper bytes alone could reasonably call them inert; the unresolved label explicitly refers to their executable dependency chain.

## Additional corrections and verification

Browser campaign/tab-query and own-provider Yahoo referral observations moved to neutral subjects; wildcard-host search interception remains hostile. Removed hostile claims from generic PEP 508 URL dependencies, ordinary scoped PostCSS plugin composition and the explicit coding-agent credential broker; retained sensitive-operation warnings and actual attack-specific rules. Split API-name observations no longer duplicate the internal-binding concealment warning. Added the raw-JSON-to-command-substituting-zsh-prompt exploit composite and the AES-wrapped image-transplant carrier composite. Restricted the FNV API-resolution claim to manual PE export lookup; the sentence-segmentation addon now has no suspicious finding.

Static positive/negative fixture checks passed (eight cases), including a remote prompt whose unsafe interpolation is removed in the negative control. The 3KMK3 PowerShell carrier now has three hostile findings from distinct payload behaviors.

A sibling cleave bug fix adds credential, memory-JAR and raw TLS API salience to the existing bounded JAR class sampler. Previously it selected ordinary updater/library classes and skipped the malicious initializer. The focused Rust unit test passed, and a full JAR rescan now finds four hostile traits across credential access, TLS egress, session handoff and mod activation. Source change: `../cleave/src/analyzers/archive/analyzers.rs`; no decoding feature was added.

Full validation passed earlier in this review (`/tmp/probable-hostile-validate-final.log`). Subsequent concurrent taxonomy migration in the shared checkout introduced unrelated validation failures: unrecognized metadata directories, missing well-known size/section constraints, an oversized preexisting loader directory, and a media-PHP regex limit. The latest current-tree validation is `/tmp/probable-hostile-validate-final3.log`. No Hopper mutations were applied after that failure. Current Hopper client was built temporarily from sibling source because installed CLI lacks canonical inconclusive/dual-use labels; API dry runs supported both canonical pools and reported no absent or failed samples.

All 89 good artifacts were copied into `/tmp/triage/misplaced-good/<sha256>/<original-name>` and rehashed. Detailed artifact rulings are saved in `probable-hostile-review-2026-11-04.json`. Temporary extraction, static-disassembly evidence and scanner outputs remain under `/tmp/probable-hostile-*`.

## Explicit limits

- The mail-client bootstrap exports `JSON.stringify(account.imap)` through its external HTTP logger, exposing a password-bearing configuration. Manual source inspection establishes bad; the generic co-occurrence rule remains suspicious because it does not bind arbitrary logger definitions across functions. No inflated hostile count was added.
- The UDP-flood ELF has one justified hostile technique. Main disassembly directly shows the repeated fixed-size sendto bursts; no artificial three-way detection was added.
- Sweat Tweaker is a local administrative utility with two accurate independent suspicious warnings for disabling ELAM and process mitigations. It was judged good after complete script review; both warnings remain as an explicit exception to the preferred good-sample count.

Final full atomscan output contains all 161 artifacts plus the bookkeeping manifest (`/tmp/probable-hostile-final.jsonl`). Two Fontus and one direct-URL sdist report were refreshed after correcting reintroduced generic composites. All 89 good samples have zero hostile traits. One good administrative script retains two accurate suspicious warnings, as documented above. Final prompt-injection packages retain one hostile exploit finding each after redundant warnings were removed; their bad rulings are based on the implemented injection, not finding counts. Per-artifact unique finding counts are included in the JSON ledger.

## Official registry and preserved-payload reassessment

The four dependency-chain inconclusive rulings above are superseded. The earlier review stopped too soon at unavailable URLs and failed to consult registry security-hold records, exact-version reports and preserved dependency samples. All four are now bad, with different evidence strength and explicit limits.

### dependencykfeg 25.1.3 — confirmed install beacon

Direct official npm checks on 2026-11-04 show `latest: 0.0.1-security`, description `security holding package`, maintainer `npm`, and security replacement timestamp 2026-10-30T18:04:59.241Z. The former version survives in publication history but is absent from the versions map; both version metadata and original tarball now return 404. This is a confirmed security hold, not merely a missing arbitrary URL. Sources: [official registry](https://registry.npmjs.org/dependencykfeg), [MAL-2026-18416](https://osv.dev/vulnerability/MAL-2026-18416).

The complete local wrapper exports an empty object and declares one GitHub `main` tarball dependency under the unusual name `node-acct-utilssss21`. It supplies no account utility. The mutable branch allows changes to executed installation code without a new wrapper release. The [merged original report](https://github.com/ossf/malicious-packages/pull/1689) explicitly records the reviewed outer SHA256 `34503e3c732923719e8bc65beacccba9a90b89e9ead6efbe8c656f2be9efa2ab`.

Recovered the preserved second-stage v2 tarball from Hopper by its published SHA256 `2707f1c7c853cd703495678ade5e3819a98620f5f6b6ca247b962d727b3ff84a`; its extracted index.js independently hashes to the report's `10718a307135d20b94153375c1fdf473a437d2cf98673bc09be86a81c51bd25d`. Static source review confirms:

- `preinstall: node index.js` activates without importing the supposed library.
- `execSync(curl .../burp_collaborator.txt)` selects the collector from a remotely mutable text file; an empty value disables the beacon.
- Collects `whoami`, hostname, home and working directories, platform, architecture and Node version. Calls `ipinfo.io/json` for public IP, operator and ASN.
- Sends the JSON report over HTTPS with `rejectUnauthorized: false`; errors are swallowed and the response is ignored.
- Payload labels itself `claims-acct-unl`, corroborating reuse across the account-themed package cluster.

The historical first-stage variant is reported to use a fixed Burp Collaborator subdomain over HTTP; that older tarball was not recovered. The current recovered variant is sufficient for the bad ruling. No credential-file theft or remote command tasking is claimed from this code. The repo's current 404 does not weaken the already recovered behavior.

### atlassian-wallboard-plugin 10.0.0 — confirmed chained install beacon

[npm's official record](https://registry.npmjs.org/atlassian-wallboard-plugin) shows the original release removed and replaced under security hold at 2026-11-02T13:35:49.045Z. Its `claims-ac1@1.0.0` dependency also has a security-holding replacement. The package has no wallboard implementation; it points to the same GitHub repository through `node-ac2`, which in turn depends on `node-ac3`. Both preserved tarballs were recovered and hash-verified against [MAL-2026-18437](https://api.osv.dev/v1/vulns/MAL-2026-18437): `254e322d…` and `ff368653…`.

`node-ac3` runs its index.js in preinstall and at load. Static base64 decoding yields the collector-resolution curl command, `/health`, and `node-acct-utils`. Its body reports home/cwd and runtime/platform/architecture, POSTs to the fetched hostname with certificate checks disabled, and suppresses errors. This is concrete dependency-triggered collection, supported by the [exact-version advisory](https://github.com/advisories/GHSA-vj43-6r45-847h), rather than inference from an Atlassian-like name alone.

### hijuko-pilara 1.0.0 — dedicated dependency-confusion probe

The 416-byte original sdist contains only setup.py, a name/version module and sparse PKG-INFO. All were inspected; there is no encoded Python stage or custom setup class. Setup declares one PEP 508 URL dependency at the campaign receiver. Resolving that dependency causes an outbound request to the receiver even when the server returns no usable archive; this establishes the contact mechanism, not arbitrary execution or secret export.

[GHSA-h764-w9gv-g9fr](https://github.com/advisories/GHSA-h764-w9gv-g9fr) and [MAL-2026-18581](https://api.osv.dev/v1/vulns/MAL-2026-18581) identify this exact version as a download-tracking dependency-confusion probe in campaign `2026-10-vacsdk`. The original analyst labels it probably pentest/low harm; dedicated attack probes remain bad under the endpoint classification policy. The receiver hostname in the report exactly matches setup.py.

Official PyPI project and JSON endpoints currently return 404, while its simple index has no release links. Hopper's prior provenance records the original files.pythonhosted.org URL, version, size and matching sample hash. Therefore release unavailability is established; PyPI does not expose a security-removal reason here, and one is not asserted. The missing archive does not erase the implemented tracking request or the exact-version campaign evidence.

### tw-motion-css 2.0.2 — campaign carrier, still live

The official npm registry still serves 2.0.2. Downloading its official tarball reproduces the exact reviewed SHA256 `382d0736f88f18e88a0e168f76d7efa1c3fd784b9404472f74277c2a0681c52d`. `@codentra/postcss-kinetix` returns 404, which can represent private visibility; no takedown is claimed for either coordinate from that alone.

The [original OpenSSF submission](https://github.com/ossf/malicious-packages/pull/1694) and [Corgea campaign investigation](https://corgea.com/research/tailwind-animatecss-fake-interview-private-scope-npm-october-2026) identify the exact package/version/helper pair among replacements introduced after related security takedowns. Local code traces `plugin.js` → `styles.js` → `motion.js`; top-level require loads the private helper, and style generation executes it in PostCSS. The exact target and activation match the reported fake-interview carrier, supporting bad classification of this distribution. Private final-stage bytes remain unavailable; specific downstream credential theft, RAT functions or payload decryption are not claimed as independently observed.

### Detection and recording

Generic direct-URL declarations and ordinary PostCSS composition remain neutral; a 404 is not substituted for attack evidence. Existing official-registry rules correctly flag the removed npm coordinates under security hold. Added one behavior-based rule for a load-time host census POST whose collector comes from shell output and whose request disables certificate verification; the plaintext resolver had escaped the existing encoded-resolver rule. Positive and two near-miss controls verify the body and certificate-verification boundaries. Eleven static regression cases passed. No sample or recovered payload was executed.

Evidence is retained in `/tmp/probable-registry-evidence`, including raw official responses, response headers, exact package-coordinate scanner reports, recovered tarballs, extracted source and cryptographic digests. Registry requests were read-only; private package tokens were not acquired or used.

## Completed disposition

Current full validation passed (`/tmp/probable-hostile-validate-withdrawal-final2.log`): hostile 3318/3318, suspicious 2094/2094, notable 9623/9623, baseline 1418/1418. Eleven static regression cases passed. A final full atomscan pass contains all 161 artifacts plus the manifest; all 89 good artifacts have zero hostile findings, with the documented two-warning administrative-script exception. The newly added rule was checked against the full set and the recovered malicious dependency.

Hopper preflight and application completed for all 161 reviewed artifacts: 89 good (17 moved, 72 already matching), 68 bad (8 moved, 60 already matching), 4 dual-use (3 moved, 1 already matching), zero inconclusive. No absent or failed samples. Logs: `/tmp/probable-registry-evidence/hopper-{dry,apply}-{good,bad,dual-use}.log`. All 89 good copies remain hash-verified in `/tmp/triage/misplaced-good`. The earlier validation-block and inconclusive statements above describe superseded intermediate states.

The additional corpus search found no preserved `plugin-atomic-string-memo@1.0.0` or `@codentra/postcss-kinetix@1.0.1` implementation. This limits payload detail, not the dedicated-probe and reported-carrier rulings. npm second stages were independently recovered, hash-verified and read statically; no endpoint sample was executed.

## x-improve follow-up: readability and evidence boundaries

Re-ran local `atomscan --format=json --mode=slow --follow=none` over all 161 original artifacts and all three recovered dependency archives. Before/after reports: `/tmp/probable-improve-{before,after}.jsonl` and `/tmp/probable-improve-stages-{before,after}.jsonl`. No sample classifications or pool locations were changed by this follow-up.

Corrections:

- Security-hold messages now state the registry observation instead of saying every held dependency is hostile. Removed the hostile finding on npm's inert `0.0.1-security` manifest; its placeholder identity remains notable. The corresponding registry record is also neutral when it describes the replacement version. An older release demonstrably removed under security hold still matches the hostile withdrawal rule; an ordinary unavailable/unpublished release does not.
- Retired six generic empty-entry/dependency-carrier composites. Empty exports, an absent entrypoint, or a direct URL alone do not establish a hidden payload. Their independent manifest, URL and archive-member facts remain visible. The sole PhantomRaven consumer now references the same underlying observations and preserves its existing exclusions. The parent packages' bad rulings still rely on the independently recovered attack stages, official withdrawal evidence and exact-version reports.
- The new collector observation follows the curl result through string conversion into the hostname of the same POST request. This replaces co-occurrence of any curl call with any shell-derived hostname in the startup-census rule. The HTTP client is identified through its `require('http'/'https'/'node:https')` origin, so renaming its local variable does not hide the channel and a custom object named `https` is not mistaken for the Node client. Local-path JSON must reach a request stream created from that imported module.
- Shortened the Node concealed-spawn and cgo wrapper descriptions. Archive-level cgo findings now say the wrapper sits beside shell-tasking/result-reporting code; they do not pretend archive co-occurrence proves the wrapper's callee. The encoded-URL findings similarly describe the evidence without asserting an unproven decoder-to-resolver binding.

The full before/after comparison preserves every hostile finding on the original artifacts and recovered stages. Only the retired speculative wrapper warnings disappear from dependencykfeg, wallboard and the inert node-ac2 helper. All 89 good artifacts retain zero hostile findings. The earlier corpus classifications are unchanged; this skill does not add a moving workflow.

New focused cases cover renamed HTTP imports and collector URLs, an encoded collector, unrelated curl/POST statements, a custom request object, both npm placeholder-manifest repository forms, a placeholder registry record, an original security-withdrawn release, ordinary unpublication, and two inert URL-dependency wrappers. The existing eleven triage regressions are retained. Detailed assertion script: `scripts/review/test-probable-hostile-improve.py`.

Follow-up verification complete: all 23 focused/original static regressions passed; final `make validate` passed (hostile 3319/3319, suspicious 2096/2096, notable 9641/9641, baseline 1420/1420). `git diff --check` passed. The JSON ledger's finding counts now reflect the final improvement scan. Classification and Hopper-recorded fields were preserved.

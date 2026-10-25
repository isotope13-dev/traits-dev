All three samples remain **MALICIOUS** after a second source-level review.
The public-registry queue labels and scanner scores were not used as evidence
of intent. All supplied hashes match. The CRX3 archive's JavaScript members
were compared byte for byte with the supplied extraction.

| Sample | Identification and decisive behavior | Hostile before → after | Suspicious before → after |
|---|---|---|---|
| `3ee81750d98b` | Hidden `InternalCache` HTA remote JScript loader | 2 → 2 | 0 → 0 |
| `884c21918880` | AiPrice Amazon.ae Price Tracker 4.0.1, identified cross-site browsing reports | 1 → 1 | 2 → 1 |
| `8e137530d390` | SCKit-labelled CI credential bridge | 2 → 2 | 0 → 0 |

The HTA runs `RunPayload` from `window.onload`. It removes window chrome,
suppresses the taskbar entry, requests minimization, resizes to zero, and moves
to negative coordinates. It synchronously fetches an HTTPS response with
`MSXML2.ServerXMLHTTP.6.0`, assigns `responseText` to a local variable, and
passes that same variable to `eval`. The empty catch suppresses errors and
the window closes afterward. The unresolved `%codigo_js%` template text does
not disable this script. There is no encoded executable stage in the supplied
HTA. The hidden remote execution chain tips the verdict; sanctioned testing
context and the remote response are unavailable. No success or downstream
payload behavior is assumed. The two existing hostile findings cover hidden
execution and fetched-source evaluation. The added notable load-handler
observation covers the trigger. Fetching, COM use, evaluation, window control,
and empty exception handling were already covered. A third hostile finding
would duplicate these effects or invent the absent response's behavior.

The extension actually implements price history, shopping overlays, image
search, translation, screenshot search, and related site requests. Its manifest
loads the common and content bundles on HTTP and HTTPS sites, grants all URL
host access, and declares cookie, scripting, storage, and request-rule authority.
Those declarations alone are not evidence of theft. Runtime handlers for
cookies, script injection, and request rules were traced; no separate cookie
stealer, remote-command channel, or arbitrary downloaded payload was established.

The decisive extension path is the general browsing telemetry in common module
32575. Module 57455's `Cf` export calls the usage-report routine, which calls
the event routine and appends a page-view event. The content application calls
that routine with a 1-in-50 sampling gate on top-level pages. The `v4Q` helper
resolves to `globalThis === globalThis.top`; it is not a shopping-domain gate.
The application supplies a fuzzy platform fallback for unmatched top-level
sites. A separate competitor-extension survey can also produce events.
Common module 43347 initializes the queue's three-second and before-unload
flushes. The beacon carries the persistent extension user ID as `cid`, session
ID as `sid`, and the current full URL, referrer, and title as `dl`, `dr`, and
`dt` to Google Analytics `/g/collect`. Direct usage reporting does not pass
through the separate privacy-gated `sendAnalysis` wrapper. Defaults set
`privacyConsentRequired` false and `privacyStatus` true; initialization also
marks the install privacy prompt as already shown. There are exclusions for
some login/admin-like pages; this is not proof of transmission on every page.

Identified browsing export beyond the storefront task, enabled by default and
reachable without a shopping action, tips the extension verdict. Actual user
consent, installation history, and server-side retention are unavailable. The
Google Analytics destination alone does not establish maliciousness. The one
hostile finding describes the supported browser-data transfer. The remaining
computed-constructor finding accurately reflects obfuscated lookups; ordinary
bundling and dual-use extension APIs are preserved. No additional independent
hostile effect is supported, so the 3–5 goal cannot responsibly be met here.

The extension's suspicious numeric-array XOR finding was false. The matched
`fromCharCode((s ^ i) - a)` loop is in the Bing image-search adapter: it decodes
the middle component of an image signature using `atob`, a repeating string
key, and an offset, then sends it as `X-Image-Knowledge-Signature`. A nearby
numeric array belongs to a different obfuscated Baidu signature library.
The array is not the XOR loop's input. The Baidu closure's character-substitution
table and rotated lookup pool were decoded without executing the specimen.
They resolve to CryptoJS-style AES/CBC, padding, and signature-generation code
that incorporates BAIDUID, URL, user-agent, platform, and timestamp fields.
Computed `new` expressions resolve to constructors such as WordArray `init`;
they are not concealed Function constructors. This is obfuscation, not evidence
of another malicious executable stage.

The coarse XOR conjunction was moved to `micro-behaviors/data/decode/xor` and
renamed to describe proximity. Its matcher, window, types, exclusions, and
explicit consumers are preserved. The unsupported array-input and concealment
claims were removed, and its severity is now notable. Ancestor consumers were
reviewed: the ELF debugger composite is outside this JavaScript rule's scope;
other generic concealment consumers must not infer concealment from unrelated
numeric data. The actual extension's computed-lookup obfuscation remains
suspicious. Existing genuine XOR/eval and CI-relay controls retain their attack
findings, including the renamed relay fixture. The numeric-array/eval control
still activates the explicit XOR-array evaluator consumer.

The shell script writes a quoted heredoc to a dotfile in `RUNNER_TEMP` or
`/tmp`. That staged shell checks for live PyPI/npm secrets, uses `printenv` to
select `PYPI_API_TOKEN` and `NPM_TOKEN`, and pipes their values into curl's raw
HTTP request body to an unrelated HTTPS endpoint. The wrapper appends
`BASH_ENV=<bridge path>` to `GITHUB_ENV` and exits 1. Later Bash steps can source
the bridge while their publishing credentials are live. The body was extracted
and its own facts inspected. Its execution depends on later steps actually
running despite the failure; successful theft is not assumed. No global host
persistence, worm propagation, or further executable payload was found.
Testing markers and the SCKit label do not corroborate a malware family. Raw
credential export and shell-startup poisoning tip the malicious verdict;
authorization for a security exercise is unavailable.

The old token-upload rule required only a token name near an unrelated stdin
upload and incorrectly filed that combination as build-pipeline trojanization.
Its replacement lives in environment exfiltration and joins the secret source
and raw-body pipeline at the same source-command offset. It covers `printenv`,
`echo`, and `printf`, while requiring registry-token source names before that same
pipe. Generic service-token authentication, single-quoted literal token text,
and unrelated uploads do not supply a hostile result. Validation exposed a
real benign keychain-to-service authentication fixture; its general token
upload observations remain notable, and only the overbroad hostile inference
was narrowed. The CI composite additionally requires an actual
`BASH_ENV` append to `GITHUB_ENV`; comments and variable references cannot
supply the write. The previously missed quoted heredoc write is now detected.
Credential theft and CI startup poisoning remain the two supported hostile
results. Job abortion is documented but is insufficient as a standalone hostile
impact rule; adding another finding for the same startup hook would duplicate
the poisoning.

Adding the complete stdin-body pipeline observation required an upload-leaf
budget review. The original 100-rule catalog is recorded in
`upload-leaf-review.json`. The protocol-unspecified authentication-upload helper
call was moved, with its matcher, scope, severity, and exact consumer retained,
to `micro-behaviors/communications/transfer`. A helper named `uploadToken`
does not establish HTTP. Generic HTTP selectors appropriately cease treating
that name as HTTP evidence. Both leaves remain within existing budgets.

`summary.json` records exact before/after counts, ID moves, differences,
classifier outputs, and the requested archive-member comparisons. The only
changed CRX member is `content-script.js`: 0 hostile/2 suspicious becomes
0 hostile/1 suspicious, with the corrected observation retained as notable.
`background.js`, `chunk-common.js`, and `chunk-vendors-24b3e646.js` retain
0 hostile/0 suspicious each. No unmapped sample finding disappears.

The calibrated ML result remains unflagged (`cls=0`, `L=-1`) for all three
samples before and after, including the requested archive members. Root
probabilities change from 0.9930771 to 0.99309 (HTA), 0.8319694 to 0.8170047
(CRX), and 0.9851859 to 0.98824245 (shell). These are classifier misses against
the inspected behavior. The installed model warns that feature schema v18
predates the engine's expected v21. No inaccurate finding was restored to
increase the score.

`check.py` passed 30 focused and existing controls under neutral scratch paths
so test-harness exclusions could not hide failures. The existing 16-case HTA
response/evaluation suite also passed. Samples were not executed and no live
payload endpoint was contacted. Full facts, formatted bundles, decoded strings,
the extracted bridge, rule traces, and reproducible atomscan JSON reports are
in the named scratch directory `scratch/acquit-review`. Judgement marker
contents are recorded verbatim below; the final required command is
`make validate`.

```text
HTA loader: hidden remote eval; add load-handler trait
AiPrice 4.0.1: exports browsing URLs; fix XOR false positive
SCKit CI bridge: steals publish tokens; bind upload and env hook
```

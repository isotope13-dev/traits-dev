Registry sample second review (2026-10-24)
=========================================

The three exact supplied artifacts are preserved in fixtures/; identification
is based on their contents, not a feed conviction or a package-family guess.
Run `python3 testdata/taxonomy/registry-loader-review/check.py --scratch <dir>`.
Use an empty scratch directory outside the rules tree for generated controls.
The checker parses all controls, retains two pre-existing malicious extension
archives, and exercises the Python helper chain with mocked HTTP and DNS.
It never imports the sample under its main or startup-hook identity.

Identifications and judgments
-----------------------------

* hostname_loader.js (5d640b7352aa6cfb6372c5e56e3933609a3fa40662c0bddc03fb19d1634c1298):
  MALICIOUS periodic response-host JavaScript loader. check() reads a GitHub
  raw-content response, substitutes its complete text into the authority of
  another HTTP URL, reads that response and directly evaluates it. check() is
  called at module scope and registered at a one-hour interval. No signature,
  version, origin constraint or payload verification intervenes. The fetched
  stage is not supplied, so no child payload effects are attributed. Repeated
  unrestricted execution through a mutable rendezvous, with no other product
  function or deployment authorization, tips the judgment. Ordinary remote
  configuration alone is a near miss and now has a neutral capability home.

* renamed_daemon.py (844eae64fdf2a08542df9a1284249222b677fcc4e83ffa588c98f759815b0d5b):
  MALICIOUS Python remote-code daemon. _retrieve returns HTTP response text;
  read_stage submits it through a thread-pool executor with retries. run reads
  the locator text, selects the first domain-shaped line, resolves that host,
  formats it into an HTTP authority, fetches code through the same helper,
  and activates that exact code via exec(compile(...), {'__name__':'__main__'}).
  The domain validator admits localhost too; it validates syntax, not trust.
  main takes a nonblocking exclusive lock, forks, calls setsid, redirects
  descriptors 0/1/2 to os.devnull and changes directory to /. The child invokes
  run forever, suppressing exceptions and sleeping 719 seconds between attempts.
  Both __main__ and the explicit sitecustomize branch activate main. A startup
  import requires installation under the interpreter's hook name/search path;
  these standalone bytes prove that activation support, not that installation
  has happened. No hook write, reboot setup, credential theft or cleanup exists.
  Hidden, repeated arbitrary code execution and startup-hook activation support
  tip the judgment without needing to identify the final payload. The HTTPX dependency version and successful remote retrieval are unknown.
  The mocked helper test confirms the successful-response compile/exec path;
  it does not establish the behavior of an installed HTTPX error path.

* inert-wallet.xpi is the exact wallet-export.xpi
  (a315a80f53769ece1eeda1fbf8aa51d0d9602310ae8b6f21d520ab92f1177ba3):
  BENIGN inert Fixture Wallet 1.0 extension fixture, retaining suspicious code
  capabilities. All four ZIP members were compared byte for byte with the
  supplied extraction. The manifest declares clipboardRead and no collection,
  but no background scripts, content scripts, popup/action or options entry.
  form.html contains an unbound password field labeled for a seed phrase and
  loads no scripts. entry.js only defines onInput(field); no caller or listener
  binds it to that field. It passes field.value to collectMetrics in a timer
  if called. sender.js only defines kml and collectMetrics; its POST sends
  caller-supplied object properties, with static wallet metadata, if invoked.
  kml builds http://193.148.56.48/app.php from [91+102,91+57,91-35,91-43],
  decimal scheme character codes, dot separators and a PHP path. Obfuscation
  and the input-object POST are accurate suspicious observations. Nothing
  reads clipboard data. The complete archive supplies explicit fixture naming
  and disconnected, unreferenced components rather than a deployed collection
  chain; external wiring or a different package could change the judgment.
  The former hostile claim was unsupported: a generic parameter's .value and
  timer are not evidence of DOM input, nor do separate archive members prove
  seed-to-network flow. This conclusion does not rely on a clean scan.

Rule corrections and consumer audit
----------------------------------

* dom-value-report-channel no longer accepts the two generic value/timer
  shapes without browser-input evidence. Their atomic detections and the
  broader value-property-reporting-call remain unchanged. Its only exact
  attack consumer is wallet-input-telemetry-http-exfiltration. Real DOM edit
  listeners, password-input aggregation and seed-field selectors still qualify;
  both pre-existing wallet/clipboard attack fixtures must retain wallet theft.
* The JavaScript fetched-host atom moves to http/url/build, notable, because
  response-directed service discovery alone is neither C2 nor concealment.
  Its exact tree queries and file/platform scopes are preserved. The bound
  response-to-eval atom and hostile stager move to execution/payload/script-eval;
  the periodic execution findings stay in the beacon directory. Exact beacon
  consumers and active fixture contracts follow the moves. No directory-level
  source selector selected these moved IDs. Broad command-and-control/channel
  consumers lose the standalone JS stager intentionally: a one-shot activation
  is no longer misrepresented as a control channel. The repeated beacon and
  interpreter primitives still describe the original attack.
* github-raw-browser-fetch moves from artifact download to HTTP client/service
  with its matcher unchanged. Its description now claims only the bound request
  target. github-raw-fetch explicitly follows the move, preserving all existing
  attack consumers. HTTP-client directory consumers gain only an actual fetch
  call with a bound GitHub URL; their existing target/type conditions remain.
* requests-response-body-access is renamed to
  python-client-response-body-cooccurrence, preserving its entire matcher and
  all exact consumers. It accepted library-neutral raise_for_status beside a
  response-body member, including this HTTPX sample, so the old library-specific
  name and body-flow claim overstated its evidence. The new name/description
  state precisely the co-occurrence it detects. Relevant executable fixture
  contracts follow the rename; historical reports remain historical records.
* New python-response-host-threadpool-poll binds the returned text, selected
  stripped line, URL authority, fetch/execute helper names, code variable and
  polling function. Its detached-tasking composite additionally requires the
  existing daemon finding. URLs, helper names, timing and archive names do not
  gate either rule. It adds the previously missed response-selected control
  destination while preserving polling and startup coverage. Overwritten hosts,
  routing text and code, local sources, unrelated polling and non-executing
  compilation are negative controls.

Placement was checked first by supported claim, then against nearest alternatives:
URL construction versus C2, request target versus stored download, one-shot
payload evaluation versus periodic control, and generic value properties versus
browser-input acquisition. No new directory or global budget exception is used.

After narrowing the wallet source group, report deduplication also omits two
unchanged OR wrappers: gecko-no-data-collection-claim and
wallet-phrase-entry-surface. Their atomic no-collection sentinel and seed-entry
label still fire. This is presentation deduplication, not lost fact coverage;
the rules themselves still match in test-rules.

Coverage limits
---------------

The JavaScript has two distinct hostile findings: response-selected payload
activation and recurring execution. No supported third independent hostile
behavior exists: there is no obfuscation, durable autorun registration, credential
source, exfiltration, process injection, staging on disk or cleanup. Checks of
module activation, URL flow and callback identity preserve those observations
without creating another hostile rule for the same execution sink. The Python
has three hostile findings after adding the destination handoff. The fixture
extension retains its endpoint-concealment and JSON-POST capabilities.

Before/after counts and classifier results are recorded in results.json.

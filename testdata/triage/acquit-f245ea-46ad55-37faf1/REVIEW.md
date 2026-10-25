Review of f245ea / 46ad55 / 37faf1 (2026-10-25)

All three original samples are MALICIOUS. Judgments come from source execution
paths and mocked effects, rather than rule names, registry labels or scores.

| Original sample | Hostile before → after | Suspicious before → after | Local model before → after |
| --- | --- | --- | --- |
| neloura 0.1.54 wheel | 2 → 2 | 0 → 0 | benign → benign |
| verify-uasputnik.html | 1 → 2 | 8 → 0 | hostile → benign |
| multichain-table-clipper.py | 2 → 1 | 0 → 0 | hostile → benign |

`comparison.json` records the original SHA-256 values, all archive members,
per-member counts, normalized ID changes and model probabilities. There are no
lost observations after accounting for renamed/moved IDs. Severity changes are
intentional and do not erase the capabilities. Scans use local analysis, slow
mode, no rule updates, and `--follow=none`; dependency fetching is excluded from
the reproducible comparison. The queue's wheel scan included four additional
notable findings from fetched astronomy data; the hostile/suspicious counts are
unchanged. The model is v18.18 and logs an older feature specification (v18 vs
v21); all final model levels are -1. These are classifier misses, not reasons to
restore misleading traits.

Neloura

The original wheel was recovered using `forager fetch --all-wheels` for
`pkg:pypi/neloura@0.1.54`. The registry copy has the exact supplied SHA-256;
every hashed RECORD entry verifies. Original artifacts and .forage.json
provenance remain in scratch/acquit-review/forager.

The application is a FITS astronomy viewer. The launcher prepares ~/.neloura,
links packaged assets, starts uvicorn on 127.0.0.1 by default and opens a browser
or notebook iframe. main.py mounts the static directory, and static/index.html
line 66 directly loads the vendored SweetAlert2 11.22.2 bundle. Its top-level
code is reached when that script loads, independently of using a dialog.

The exact extracted routine in regional-payload.js checks /^ru\b/ on the
browser language and a .ru/.su/.by/.xn--p1ai suffix on location.host. It records
a first-visit time in localStorage. After more than three days, it sets body
pointerEvents to none, creates an audio element with a remote MP3 URL, sets
loop=true, appends it, and attempts playback after a further timeout.
regional-trace.json contains eight executions with mocked browser objects,
including first visit, exactly three days, four days, another language,
localhost, an explicit port and a matching remote host. No media was fetched.

Localhost does not activate this host gate, nor does a host ending in :8000.
The launcher also explicitly supports remote notebook proxy URLs and a host
parameter. No actual affected deployment is assumed. Packaging and the local
science application are legitimate context, but the undisclosed, unrelated,
deliberate input/audio sabotage inside a loaded dependency tips the artifact
judgment to malicious. Ordinary science features do not explain it.

Other reviewed paths are consistent with the advertised app: local coding
runs submitted Python in a subprocess with plot capture and termination;
coding.py uses a user-provided PEM certificate to manage CANFAR Skaha sessions;
main.py downloads astronomy data, has explicit TLS-verification disabling,
launches df and its own peak_finder.py with argv, and manages application files.
The encodings concern image/plot data and application assets. These capabilities
remain notable, including dangerous or dual-use ones. They are not counted as
additional attacks. The existing single-member sabotage finding remains
1 hostile / 0 suspicious; main.py, static/main.js and static/files.js remain
0 hostile / 0 suspicious. No wheel attack finding was weakened or removed.

The goal of three distinct hostile traits is not reached: the two wheel
findings describe one sabotage routine and its bundled identity. Its input and
audio effects, locale/host gate, persistent timestamp and delay already have
supported detections. Adding a third hostile alias would duplicate that routine;
no separate theft, persistence or payload-execution objective was established.

ClickFix HTML

The page poses as Cloudflare human verification. report('open') requests a
server payload; a nonempty response replaces the fallback command. Clicking
the checkbox reports another event, copies the current command, reveals Run /
paste / Enter instructions, and leaves Done disabled for 35 seconds. The
fallback is msiexec /i with a remote HTTPS MSI and /passive. The click report is
asynchronous, so the copy uses the already available value; an open-response
update can already have changed it. html-trace.json executes the original
inline script with mocked DOM, clipboard, fetch and timers, showing both the
fallback and server-updated paths. No command was executed on the host.

The instructions solicit unrelated software installation as a human check;
that deception, rather than the Cloudflare text alone, tips the judgment.
No deployment origin, server-side handler implementation or final MSI behavior
is available. Forager was used for the MSI URL; repeated connection refusals
prevented recovery, and the retrying fetch was stopped. No payload family,
credential theft, PowerShell execution or successful native installation is
claimed. Network observations cover requests for the page's payload and click
telemetry; they do not claim credential exfiltration.

Added general observations for fetch payload/action queries, fetch text
callbacks and command-variable assignment, plus a hostile composite requiring
human verification, Run and paste instructions, clipboard writing and the
payload-fetch callbacks. The existing remote-MSI lure finding stays hostile.
There are two supported attack aspects: remote command refresh and the
clipboard MSI execution lure. The unavailable MSI prevents adding any supported
traits for its subsequent behavior. A third hostile label for the same page
sequence would add no distinct coverage.

Neutral verification and instruction evidence was moved out of credential
access / execution objectives, with names that describe the actual match:
copyright text does not prove fraud, vfclick/spinner identifiers do not prove
Turnstile identity, and verification wording does not prove phishing. Ordinary
Run/paste help and command copying are retained as neutral observations.
"Verification Code" alone does not prove a copy button, MFA or OTP collection.
The one-address Tron matcher likewise does not establish multiple addresses or
a table. ID mappings and explicit consumer updates are in moves.json.

Python clipper

run() polls pyperclip.paste every 0.3 seconds. It passes new values to hijack(),
which fullmatches ETH/EVM, Bitcoin-style and Tron regexes and returns a fixed
entry from SWAP. Only changed results are copied back; a cache avoids rewriting
its own last value. clipper-trace.json records the original functions under a
bounded, mocked clipboard: all three address families are replaced, ordinary
text is preserved, and whitespace around an EVM address is stripped before
matching. There are no network calls, startup hooks, encodings used to execute
code, credential reads or hidden stages.

The replacement strings contain obvious placeholders; BTC/Tron validity and
attacker control are not established. The supported hostile result is silent
address corruption/substitution, not successful financial theft. There is no
user-selected transformation or consent interface. A disclosed lab exercise
could change deployment context, but none is provided; the executable behavior
tips the security-engineer judgment to malicious.

The former broad hostile rule required only clipboard read/write and several
address recognizers. That cannot distinguish a clipper from a normalizer or
clipboard utility. Its evidence survives as a neutral clipboard observation.
The other old composite also lacked a bound replacement path: a hardcoded table
and address regexes can remain unused while unrelated text is copied. Its ID
is retained with a structural rule binding the address-bearing replacement
table, matching helper, copied value, helper result and clipboard write, plus
polling and multi-chain recognition. Names are arbitrary. Renamed variants
still match; normalization, unrelated writes and unused recognizers do not.

One hostile finding covers the only independent attack behavior. No supported
additional objective is uncovered; three hostile traits here would inflate a
single clipboard substitution loop.

Shared-rule retention and checks

Before changing shared rules, their direct consumers, ancestor directory
selectors and existing positive fixtures were inspected. The broad write
selector's original members are enumerated explicitly in the relocated neutral
composite to avoid self-reference or adding itself as new evidence. Directory
consumers are recorded in directory-consumers.json. Existing named consumers
retain the moved evidence and original scopes. No product/filename allowlist
was added to suppress an attack.

Existing Python table clippers and Python/TypeScript polled clippers retain
hostile detections. The JavaScript table_clipper.js fixture exposed a coverage
loss when the broad co-occurrence rule was corrected; a bound regex-table
clipboard rewrite detector now preserves that real attack coverage. Its
replacement rule requires the same read value to be checked and rewritten,
the same regex and table entry in test/replacement, plus clipboard polling and
multi-chain patterns. Benign near misses independently remove the replacement
or change the checked source.

25 focused positive/negative cases pass with check_review.py: original and
renamed table clippers, existing external positive fixtures, MSI lures, an
ordinary MFA page, honest Run help, CAPTCHA copy controls, omitted source/sink
legs, no server update, and comments-only request syntax. The marker lines are
recorded verbatim in marker-lines.txt. Full make validate is the final action.

Full validation initially found two stale fixture expectations. The JavaScript
clipper now requires the structural rewrite atom and its new hostile composite
instead of the retired co-occurrence hostile ID, retaining min_hostile=1. The
benign admin HTA gains the accurate WScript-name observation: its exact score
expectation moves from 7 to 8 and requires that new trait. Its max_hostile=0,
max_suspicious=0 and forbidden dropper traits remain enforced. No matcher was
weakened to meet a score cap.

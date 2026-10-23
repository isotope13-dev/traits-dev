# Android fixture, libsignal archive, and ScreenConnect session review

This is a second review based on the supplied bytes, source control flow,
extracted stages, and isolated API mocks. No external malware attribution was
used. All three supplied SHA-256 values were checked. Original specimens and
full scan/fact reports remain in the task's `samples` and
`scratch/second-review` directories; `scan-summary.json` records the observations.

| Sample | Identification and judgment | Hostile before → after | Suspicious before → after |
| --- | --- | --- | --- |
| `dfcd8827a570` | Synthetic Android accessibility fixture: **BENIGN** | 4 → 0 | 5 → 0 |
| `fd4e7a6b9c9f` | Source archive of `@RILLYZY/libsignal-node` 2.0.1 with a Baileys patcher: **MALICIOUS** | 2 → 3 | 0 → 1 |
| `124a9dcf3677` | ScreenConnect automatic script-transfer fragment: **MALICIOUS** | 2 → 2 | 0 → 0 |

Counts refer to the outer report's unique findings, including inherited archive
member findings. The archive's `install.js` changes from 2H/0S to 3H/0S;
`src/curve.js` changes from 0H/0S to 0H/1S. No other archive member acquires a
hostile or suspicious finding. No supported attack detection was removed.

## Android: a fixture, with useful API observations

The file declares itself a synthetic, non-buildable behavior fixture. Inspection
confirms that characterization rather than relying on the comment:

* Both accessibility callbacks are empty. Nothing invokes `lockInRecents`,
  `blockRemoval`, or `startRemoteSurveillance` from an event or entry point.
* `serializeUiXml` returns the constant `<UI/>`; `postJson` returns `{}` without
  opening a connection. `getString("status")` therefore fails before the
  model-action dispatch even if `lockInRecents` were manually invoked.
* `startVNC` returns a plain object; `takeScreenshot`, `sendVncInventory`, and
  `retry` are empty. AES cipher construction and installed-application
  enumeration are real API expressions, but no encrypted VNC connection,
  screenshot, or inventory transmission is implemented.
* The removal method searches labels and creates touch-consuming overlays.
  Its `button` variable is never used to obtain bounds or position the overlay
  over the selected controls. It is uncalled and does not implement the
  asserted target-specific removal interception.
* Gesture dispatch, scrolling, Recents navigation, node access/search, overlay
  attachment, touch-listener registration, AES construction, endpoint literals,
  and application inventory remain useful neutral observations.

A compiled app, manifest, callback wiring, and working transport/capture helpers
would materially change the assessment. They are absent here; deployment of a
working implant is not inferred from method names.

## Archive: ordinary protocol code plus an unrelated account-action graft

The gzip container is a tar source tree, not a Git HEAD reference. Its manifest
identifies the fork and version above. `index.js` exports Signal protocol
helpers; the library implements session setup, ratchet/key derivation, AES-CBC,
MAC checking, key handling, and caller-provided session storage. The generated
protobuf module handles Whisper message encoding. Those crypto operations are
preserved as capabilities.

`install.js` contains a complete newsletter module in a template literal.
Tracing its executable path shows:

1. Locate an installed Baileys tree through `require.resolve` or three local
   search paths; require an existing `lib/Socket/newsletter.js`.
2. Use a hidden `.cache` marker under that dependency's `node_modules` directory
   to skip later replacement attempts.
3. Hash the existing module and replacement text, overwrite the module, verify
   the written hash, and create the marker.
4. The replacement's `makeNewsletterSocket` schedules an unsolicited WMex FOLLOW
   query for a fixed newsletter JID after two seconds. Errors are swallowed;
   the application caller supplies neither the target nor an opt-in.

The helper is exported and runs when the script is explicitly invoked as main.
The manifest has no install lifecycle script, and `index.js` does not load the
patcher. Merely installing or requiring this archive is **not** claimed to run
it. In the main path, the immediate `process.exit` also prevents the helper's
later 20-second exit timer from running. Activation and target deployment remain
unknown, but the implemented silent dependency modification has no role in the
advertised Signal crypto interface and tips the verdict to malicious.

A second missed behavior is in `src/curve.js`: `verifySignature` returns `true`
when its initialization flag is set, without invoking `curveJs.verify`.
`SessionBuilder.initOutgoing` supplies that flag and ignores the returned value.
Key-format and length checks still run; this finding does not claim all
identity checks are disabled. A compatibility or testing shortcut is possible,
so the new signature-verification finding is **suspicious**, not hostile.

The template stage is plaintext source, not concealed Base64 execution. Base64
and hexadecimal elsewhere serve protocol serialization, keys, and hashes.

## ScreenConnect: automatic remote execution requests, with explicit limits

`handle` reads endpoint connection status, selects Host connections, and checks
an in-memory delivered-ID set. Each new ID invokes the helper, which reads every
local `*.vbs` file under a Public-profile library directory, registers the bytes
as virtual files, assigns them to a transfer message with `FileAction.Run`, and
queues that message. Removing disconnected IDs permits delivery on reconnect.
Guest connections do not trigger this path.

There is no consent/configuration branch around per-Host script delivery. This
is an automatic script injector rather than the ordinary caller-selected RMM
transfer API. Its directory sweep and rearming on reconnection tip the verdict
to malicious. The class name is not needed for that judgment.

The supplied file does not import/bind `ScreenConnect`, instantiate the class,
register its handler, provide a client, or contain the VBS payloads. The queued
message carries no explicit destination connection ID: routing depends on the
external client. The code establishes queued transfer-and-run requests, not
successful remote execution or a complete self-replicating worm.

Two hostile findings cover automatic Host delivery and reconnect redelivery.
The 3–5 goal is unmet because the absent scripts and runtime supply no evidence
for additional payload behavior, persistence, exfiltration, evasion, or privilege
escalation. A new bound comprehension-to-registration rule covers file-byte
staging at notable severity. Its initial value-flow matcher could not resolve
the list comprehension; the tested AST matcher binds the comprehension variable
to the registration argument instead. No extra hostile rule duplicates this
staging behavior to increase the count or score.

## Rule corrections and retained coverage

* Model/UI text, JSON-helper names, overlay names, and quoted control labels
  were incorrectly treated as attacker objectives or asserted data flows.
  They now have source-property or neutral capability homes and descriptions
  limited to their actual evidence. Model endpoint, UI, and parser
  co-occurrence is notable; neither that co-occurrence nor task locking alone
  establishes an attack or durable persistence.
* The removal guard now requires the same accessibility search-result variable
  to receive the Uninstall-control bounds query, plus touch consumption and
  overlay evidence. A bound removal variant still fires; an unrelated bounds
  query and the supplied fixture do not. The second guard reports model/Recents
  context with removal obstruction, not invented persistence.
* The accessibility/VNC/AES/inventory profile is retained as neutral protocol
  context. Remote support can have that feature set. A no-argument empty
  screenshot helper no longer proves capture; the screenshot rule requires a
  parsed call with a third argument, preserving the platform callback form and
  rejecting declarations. Existing MediaProjection detections remain intact.
* ScreenConnect transfer operations moved from product identity to neutral
  transfer capabilities. Generic registration/enqueue method names no longer
  claim ScreenConnect identity; the generic FileAction.Run reference is source
  member metadata. Endpoint field clusters and cache-maintenance syntax moved
  out of worm objectives. Host delivery/reconnect findings remain hostile, with
  unchanged evidence selection, in `delivery/remote-admin`: no self-propagation
  is established. The added taxonomy contract distinguishes OS service creation
  and self-copying worms.
* Python glob is filename search, not proof of recursive traversal. It is
  consolidated with the existing PHP glob observation, consumers are updated,
  and rglob remains recursive traversal. Existing PHP path-search and directory
  fixtures outside this batch retain their expected distinction.
* Node crypto import matchers and consumers moved intact to import metadata
  with notable severity. Literal Buffer.from source syntax moved out of package
  completeness. A Gemini URL literal now describes an endpoint reference,
  not an observed REST call. No generic network/crypto primitive was demoted.
* The archive gains a write-source/path binding for its persisted newsletter
  graft and the signature-success shortcut. An ordinary newsletter patch and
  an unlinked output path do not satisfy the replacement finding.

Exact consumers and relevant ancestor selectors were inspected before moves.
The original Android screenshot and VNC consumers were reviewed, including the
WebSocket RAT and screen-tree composites. The crypto-import consumers, PHP
search consumers, existing remote-session rules, and existing newsletter timer
rules were also reviewed. Original matchers are preserved where their claim is
accurate; narrowing is limited to the unsupported claims described above.
`id-moves.json` records the principal adaptive-UI relocation set.

## Checks and classifier result

`cleave facts` and slow local `atomscan` scans were run for each original sample;
member source and the template stage were separately inspected. The regression
checker exercises 18 positive and negative cases, including retained removal
and C# automatic-session patterns, real screenshot call shape, remote support,
unrelated bounds, caller-driven transfer, file-byte data binding, the signature
shortcut, and existing PHP fixtures outside this batch. `trace.py` executes the
reviewed JS in QuickJS with in-memory filesystem/protocol mocks and the reviewed
Python against fake paths, a fake client, and fake messages. It verifies the
module replacement, two-second follow, cache behavior, both signature branches,
and reconnect delivery. It performs no real remote actions.

The model reports are recorded separately from the engineering judgments:

* Android: calibrated alert level 0 → no calibrated alert (`lvl=-1`), agreeing
  with the benign second review.
* Archive: no calibrated alert → level 0, agreeing with the malicious review.
* Python: no calibrated alert → level 5000; every model route still returns
  `cls=0`. This remains a classifier gap at stricter thresholds despite
  two supported hostile rules. Accurate taxonomy is retained; no rule is
  duplicated or inflated to change the score.

The installed bundle is v18.18 and warns that its feature schema is v18 while
the engine expects v21. Raw probabilities and per-member results are preserved
in `scan-summary.json`; probabilities alone are not used as verdicts.

Run the focused checks from the repository root:

```
python3 testdata/triage/android-newsletter-session-review/check.py
python3 testdata/triage/android-newsletter-session-review/trace.py <task-samples> <extracted-install.js>
```

Final repository validation is `make validate` after markers and this record are
written. There are no inline YARA edits and no precompile operation is needed.

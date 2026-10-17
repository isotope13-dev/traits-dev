# First reasoned review, 2026-10-17

All three submitted specimens are judged BENIGN under the concrete-harm standard.
This is a review of the supplied bytes, not an endorsement of remote content.

* `3cdcf9…` is @rikipurpur/9router 2.8.3, an explicitly disclosed fork of
  an AI API router. Postinstall installs SQLite/tray runtime dependencies.
  The compiled Tailscale installation path downloads the official MSI and
  invokes msiexec with UAC. Optional Firebase backup requires a user-supplied
  RTDB URL; it has no built-in recipient. No hidden theft was identified.
* The fetched Tailscale 1.104.1 MSI has a successfully verified Tailscale Inc.
  Authenticode signature. Its Binary.TSCA stream is the installer custom-action
  DLL, with Tailscale installer function names and a Go runtime. The two TLS
  callbacks at 0x26da9bee0 and 0x26da9beb0 perform CRT initialization/cleanup;
  GetThreadContext/SetThreadContext participate in Go thread preemption.
  A renamed MSI stream is not vendor impersonation. The removed conjunction
  never required an unauthorized thread target or execution transfer.
* `e189de…` is an obfuscated browser traffic-distribution loader. Decoding its
  hex escapes reveals SHA-256 over date/time/seed input, remapped to an
  alphanumeric domain label; random suffixes do not determine response type.
  It inserts a script and fetches/evaluates the response on load failure.
  Win/Mac platforms are excluded; a misspelled flag leaves Linux eligible.
  A persisted pageshow plus a localStorage gate requests a navigation URL;
  selected mobile browsers also submit an empty hidden form to that URL.
  A QuickJS browser mock confirmed these effects with inert HTTP responses
  and no network or host bindings. No credential collection, exploit, mining,
  or malicious second stage is present in the supplied file. Keep the
  encoded-source evaluator suspicious; ordinary eval/navigation stay notable.
  The array join and fromCharCode calls format the digest, not decoded code.
* `bf2c71…` unpacks with stock UPX to Eupdate Helper 4.0.1, an ESET update
  relay. At 0x412c6e it calls MessageBoxW; the comparison against IDYES (6)
  at 0x412c77 gates the replacement download. The other branch logs refusal.
  It checks the downloaded MZ header, swaps its own image and launches it.
  The relay returns 404 for .signed suffixes (0x4146c7–0x41473b) and removes
  SERVERS/LINKS/HOSTS routing sections (0x417c40–0x417d1d). These operations
  do not patch the ESET client's verification or prove malicious updates.
  It invokes ecmd.exe /update, registers HKLM Run with an elevation prompt,
  takes port 8000 by terminating a listener owner, and periodically appends
  random padding through a standby executable. Retain the suspicious hash
  rotation and the notable termination, registry, TLS, and download facts.
  Reputation is adverse, but it does not establish an additional hostile
  payload or theft in these bytes. The provided sandbox page was unavailable.

Removed composites inferred harm from ordinary capabilities, unsupported
cross-path co-occurrence, or a filename disagreement. Exact moved references
were updated; the two consumers of the dynamic-evaluator directory retain
both evaluator mechanisms. Global-eval/response-text now explicitly records
co-occurrence. Existing remote-response and XHR controls were updated to those
neutral claims. The consolidation of overlapping createHash SHA-256 rules
frees one digest slot for the missed embedded round-constant observation.

Run `python3 testdata/taxonomy/first-reasoned-review-2026-10-17/check.py`.
The runner copies fixtures outside the test tree, so fixture-name suppressors
cannot decide whether the behavior is present. It checks positive and nearby
negative cases, severity, and the absence of hostile conclusions.

Hex escape density now describes source representation under metadata/lang/encoding,
with notable severity and Windows/Unix scope, rather than a runtime hex encoder.

The expanded package scan also fetched GitHub's codespaces asset. Its for-of
loop iterates FormData while updating a different URLSearchParams object. The
old browser-UAF primitive did not bind receivers and inferred exploit intent
from ordinary state management. The exploit primitive is retired: neither in-place collection mutation nor
nearby mutations of another object constitute a browser UAF.

The pageshow listener no longer masquerades as a click listener; click matching
now requires the click event argument. A location member on an assignment's
left side is described as a reference, not a read. Whole-source whitespace
ratios move from padding to the documented text-shape profile home.

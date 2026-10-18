# Second review: Android overlay and CI secret theft

All three supplied samples remain MALICIOUS. Judgments follow source behavior;
scanner labels, scores, family comments, and endpoint reputation are not evidence
used to establish intent. No malware feed, scanner, or advisory corroboration was
sought or assumed.

## Source findings

* `GhostOverlayService.java` (`1a9c1c520d89…`): an incomplete Android PIN-theft
  implementation. An accessibility callback checks foreground package names
  against payment apps. It installs an overlay with a listener that maps touch
  coordinates into digits, appends those digits to a PIN buffer, and invokes a
  gesture replay helper. At six buffer characters it serializes the buffer into
  an HTTP POST body and writes it to the URLConnection output stream. The base
  URL comes from an unavailable `RemoteConfig` implementation. The hostname in
  a comment does not establish its effective destination or family identity.
  There is no obfuscation or encoded payload in the recovered literals.
* This implementation is defective: `FLAG_NOT_TOUCHABLE` prevents this window
  from receiving touch events, so the installed listener cannot implement its
  intended interception path as written. The fixed keypad geometry does not
  implement a standard PIN keypad mapping, no touch-action filter exists, and
  networking is attempted synchronously from a UI callback. No working APK,
  permission configuration, successful capture, or successful send is proven.
  The judgment describes credential-stealing source intent, not demonstrated
  operational success. Android documents the non-touchable flag at
  https://developer.android.com/reference/android/view/WindowManager.LayoutParams#FLAG_NOT_TOUCHABLE.
* `security-audit.yml` (`b2f729e6c4b2…`): on push/manual dispatch, checks out
  complete repository history, interpolates PAT and npm secrets, extracts AWS,
  GitHub, GitLab, API-key and private-key markers from files/history, gathers
  surrounding AWS-key lines, and sends the aggregate in a raw HTTP POST to a
  public IP. The job does not perform an audit result check. Its nonempty
  delimiter strings make the send condition true even without credential hits.
* `github_actions_security.yml` (`5a7105e468bf…`): on push/manual dispatch,
  writes an unused cache-bust environment variable, then sends six CI secrets
  (PyPI, npm, DockerHub, AWS ID/secret, SSH key) in one HTTP body to a public IP.
  The secrets are payload fields, not authentication for their issuing services.
  Neither workflow contains an encoded payload or additional obfuscation.
* Both workflow shell bodies were also traced in a synthetic local Git
  repository with fake credentials and `curl` replaced by a local argument
  recorder. Recorded bodies contained the fake CI secrets; the audit body also
  contained a credential removed from the current tree and its history context.
  No sample destination was contacted. Workflow scan reports flag incomplete
  embedded-source analysis; manual review and the controlled trace covered the
  complete supplied scripts, rather than inferring behavior from that scan gap.

## Detection changes

* Move token-assignment text from test-fixture metadata to source syntax;
  preserve the two real demo/regression-suite consumers explicitly. Broad
  testing selectors must no longer treat ordinary token text as benign context.
* Move coordinate-mapping helper calls to neutral input behavior, preserve the
  raw-touch reconstruction consumer, and describe a helper name as evidence
  rather than proof of credential recovery.
* Replace overlay/gesture/HTTP co-occurrence convictions with a class-scoped
  payment-target and listener-buffer relationship, plus a separate serialized
  bytes-to-stream-write relationship. The capture rule requires the same
  mapped digit variable to be appended; the stream rule requires the same
  byte-array variable to be sent. They remain bounded source patterns, not
  interprocedural flow analysis or proof of runtime reachability.
* Consolidate duplicate touch-listener and overlay-type observations at their
  neutral homes. Remove unused neutral wrappers from credential objectives and
  remove the generic touch-plus-POST exfiltration rule. Suppress the claimed
  touch-capturing overlay when the source contains the non-touchable flag.
* Require UI context for a PIN-field label, a call for UI action behavior, a
  statement-like assignment for credential environment writes, and a typed
  Java file stream for Java file output. Generic Java stream writes remain
  notable under their canonical stream traits.
* Move PyPI credential-name references out of CI behavior and preserve all
  explicit bridge consumers. Describe getPackageName as an API call without
  claiming that its receiver is the current application.

The six cases in `cases.json` passed after scanning with `cleave --traits-dir .
--json testdata/taxonomy/credential-overlay-review`. Check the output with
`python3 testdata/taxonomy/credential-overlay-review/check.py <report.jsonl>`.
The capture fixture deliberately retains the non-touchable flag: its positive
findings describe installed malicious handlers, while the working-touch-capture
claim must remain absent. Near misses cover ordinary buffers, a different
stored value, unrelated upload bytes, actual file output, and token text in a
request body. Final atomscan scans retain two hostile traits per supplied
sample (capture and input export; developer/cloud export; CI-secret export).

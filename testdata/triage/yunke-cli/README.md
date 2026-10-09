Yunke CLI 2.0.6 triage

Artifact SHA-256: bf70041b78cb94eeb6defb1ddd617ae44274513ef314ccf17a9d1dba79c65ca9
Judgement: BENIGN for the supplied archive bytes.

The four archive members implement an AI CLI, CRM and phone API clients,
OAuth with a loopback callback, skill ZIP installation and optional diagnostic
report submission. Postinstall removes the older omni-cli package and its
skills/state, then installs eight vendor skills into detected agent directories.
Deletion runs Node with inherited preload flags cleared to bypass a deletion
shim. This is aggressive migration behavior; the targets are the old package,
old state, skill directories and caches, rather than unrelated user data.
Diagnostic upload requires an explicit report.submit command, input paths and
CRM login; the install path does not invoke it. Registry checks display update
notifications; npm builds ask the user to update through npm. No secret theft,
concealed executable payload or unauthorized command channel was found.
The externally blocked version's firewall page was inaccessible during review.
Remote skill contents are not included in this judgement.

Corrections preserve notable signals rather than introducing a package allowlist:
- Move the /sdcard reference from wiping to filesystem storage paths.
- Move registry requests from persistence to HTTP client behavior; rename for
  metadata requests since the concatenated URL alternative need not be latest.
- Move generic NODE_OPTIONS comparison/override atoms from Pino identity to
  runtime environment observations; retain Pino composite references.
- Reuse the canonical loopback binding observation instead of a duplicate
  Electron-fixture atom; the fixture composite retains its other required legs.
- Move an OpenClaw name reference from identity to application target references.
  Remove its malware exclusion: a name mention remains true in malicious code.
- Match Base64 helper calls through symbols, excluding method definitions;
  restrict to seven scripting types supported by these call projections.
- Group tree-sitter predicates with the callback query so entry/mkdir handlers
  cannot satisfy a finish/post claim.
- Remove a pure Net::HTTP.post alias and use its canonical consumer reference,
  freeing the HTTP client leaf's rule budget without a taxonomy split.

Atomic moves preserve effective scope and matchers except the separately noted
Base64 correction and OpenClaw exclusion removal. Exact consumers are updated;
directory selectors now receive neutral facts in their correct capability homes.
The concrete archive rescan has zero hostile and zero suspicious findings.
Run `python3 testdata/triage/yunke-cli/check.py` for positive/near-miss controls.

# Datadog IDE extension review

Scope: all 122 VSIX artifacts under
`/data/malicious-software-packages-dataset/samples/ide_extensions`.
The corpus review remains incomplete. No LLM interpretation or Hopper verdict
writes are requested. Scanner output verifies coverage; it does not establish
an artifact's disposition without code review.

## 2026-11-15: local validation and chat rendering

### Labfile 0.0.5

SHA-256: `70742de0edc0df14dfa0ad301b633b792a96566d6cb34139b4c55f5021e9f4c4`.

Reviewed the manifest, all executable JavaScript members, grammar/schema and
archive inventory. Activation registers document validation callbacks and file
decorations. The validator parses document YAML, reads its bundled JSON schema,
runs Ajv and reports diagnostics. Its reviewed JavaScript contains no outbound request, subprocess,
payload decode or dynamic execution path. The archive omits the required `yaml`
and `ajv` modules, so its normal activation is broken.

The preliminary benign disposition is superseded: Microsoft's removal history
explicitly lists `labfile.labfile` as **Malware**, removed 2025-10-20. The exact
publisher/name pair now has a hostile distribution-identity finding. This
reports the provider's classification without inventing executable payload
behavior in the reviewed source. The reason for Microsoft's malware ruling is
not disclosed in the removal entry.

The only suspicious finding was the generic `fs.readFileSync` observation filed
under exfiltration. Removed that duplicate atom and updated its consuming
composites to use the existing neutral file-read call observation. The schema
read remains visible at notable severity.

### Axion AI 1.0.0

SHA-256: `1c79151398bc48e9c2afa19822f1968595d5147c5ef227045a0c1f5475780e82`.

Reviewed activation/command registration, the webview message dispatcher, AI
request construction, model destinations, file access/change tracking, local
conversation persistence and the predictive/swarm helper services. User chat
requests include project filenames and up to 10,000 characters of the active
file, sent to the selected model provider with its configured key. Suggested
changes are tracked before the webview's apply action writes them. API keys are
stored in global editor configuration; conversations are saved in globalState.
The webview loads third-party rendering scripts from a CDN and renders model
Markdown. These are security-relevant implementation choices, but the reviewed
application code does not establish covert host collection or a payload loader.
Microsoft explicitly lists `StefanYosif.axion-ai` as **Malware**, removed
2025-12-23. Its exact publisher/name pair now receives a hostile identity
finding. Complete third-party dependency review is still pending; the reviewed
application functionality does not override that provider classification.

Its script-execution finding matched ordinary `div.textContent` followed by
`appendChild`. Replaced that matcher with a neutral AST observation requiring
creation of a script element, body assignment and insertion of the same
identifier. XOR loader objectives now consume this observation and supply the
decoding/execution context. Its other suspicious finding was the generic local
file read described above (the conversation import reads a user-selected file).

### Verification

- Initial behavior checks: cleave and atomscan both reported zero suspicious/hostile
  findings after the false-positive corrections. This result is superseded by
  the Microsoft-listed identity findings above. Atomscan ran locally in slow mode with updates
  and reference following disabled; no original code was executed.
- Existing fetch/XHR XOR script-loader fixtures retain their hostile findings.
- Existing Node home-tree flag exfiltration and current-directory content upload
  fixtures retain their hostile findings after the file-read reference change.
- New controls: `javascript-chat-dom-text.js` and `node-local-schema-reader.js`
  have no suspicious/hostile findings.
- Full `make validate CLEAVE=/home/t/bin/cleave` failed on existing worktree
  issues, including non-leaf files, broken references and oversized regexes.
  Output: `/tmp/vsix-continue-validate.log`. This gate remains open.
- Reports: `/tmp/axion-and-labfile-final.json`,
  `/tmp/axion-labfile-atomscan.json`, and
  `/tmp/vsix-ui-read-regressions-final.json`.

## 2026-11-15: CodeLLDB clone and removal-history correction

CodeLLDB clone: `codevsce.codelddb-vscode` 1.11.9, SHA-256
`8902b7107014573826ea32f45325d958ad692298234e5efb4401b24836e7dcb0`.

Reviewed the manifest, activation modification, debugger registration, platform
acquisition and command/launch paths in the bundled entry point. The injected
activationState block records first/last activation and updates the latter
after two days; it does not execute a payload. Existing CodeLLDB code still
looks up `vadimcn.vscode-lldb` for its version/platform configuration, so startup
can fail without that original extension installed. Platform acquisition reads
the original extension's configuration, downloads its platform VSIX, invokes
`workbench.extensions.command.installFromVSIX` with a Uri array and removes the
temporary file. Do not claim the clone's version necessarily becomes the
downloaded platform version: that lookup uses the original extension's manifest.

All 85 shipped files in its three external npm dependencies exactly match their
published tarballs: jsonc-parser 3.3.1 (19), string-argv 0.3.2 (8), yaml 1.10.2
(58). No extra or changed dependency file was found in this comparison.

Microsoft lists this exact identity as **Impersonation**, removed 2025-12-18.
Keep its republish/activation-clock warning suspicious. This is distinct from
the **Malware** entries for Labfile and Axion, whose distribution identity
findings are hostile.

Installer coverage now recognizes the array-based installFromVSIX command as
well as installExtension. HTTP GET can supply the remote-fetch clue alongside
fetch(). Added a minimal remote-platform installer fixture and a local-only
Uri-array control. Added positive fixtures for both malware-listed identities
and controls independently changing publisher and extension name.

Provider evidence: [Microsoft removal history](https://github.com/microsoft/vsmarketplace/blob/main/RemovedPackages.md).
Saved response: `/tmp/vsix-removed-current.md`.
Final checks: `/tmp/ide-listed-originals.json`,
`/tmp/ide-listed-fixtures-final.json`, `/tmp/codelldb-final.json`, and
`/tmp/ide-listed-atomscan-final.json`.

Both original malware-listed distributions and their positive fixtures match
the hostile identity rule. All four publisher/name controls remain clear.
The remote-platform installer fixture is suspicious, while the local-only
Uri-array fixture has no suspicious/hostile finding. The original CodeLLDB
clone has suspicious static installer and activation-clock findings; atomscan's
overall model decision is hostile. The provider entry still says Impersonation,
so the static findings do not claim a proved malware payload.

Repeated full validation failed on pre-existing worktree errors. Current
output: `/tmp/vsix-identity-installer-validate.log`. No validation diagnostics
name the new identity definitions or the installer changes. The full validation
gate and overall corpus review remain open.

## 2026-11-15: SecureCodee 0.0.2

Identity: `AhmedSlem.secure-codee`, SHA-256
`7f6b5422eba24760a05a200a1789e084d3b65213a285ce9485dea85d60a3c472`.

Reviewed activation, authentication/token storage, scan dispatch, diagnostic
mapping, decoration handling and webview messages. Activation restores saved
results and registers commands; it does not automatically send documents.
The manual scan command gets the active document's full text and language,
then sends them with a bearer token to a hard-coded ngrok API `/scan` route.
The README mentions an API URL setting, but the implementation uses a literal
`API_URL` and does not read that setting.

Login posts the supplied email to `/auth/check-email` and `/auth/send-otp`,
then posts email/OTP to `/auth/verify-otp`. The returned token and plan are
stored in editor globalState. Account creation opens
`https://securecode.contentkit.studio`. The results webview displays findings,
opens file locations, dispatches the same commands and persists diagnostic
state. Its additional remote resource is a public icon repository. No unrelated
secret sweep, hidden subprocess or downloaded executable stage was found in
these application paths. The source-code transfer is observed, user-triggered
service behavior; the finding does not assert that this login is phishing.

All 319 shipped files in its 23 npm dependencies match the published versions
byte for byte: Axios 1.13.2 and its flattened dependency tree. Comparison
included package manifests and JavaScript, not merely package names. The
tarballs are saved as `/tmp/vsix-secure-<name>-<version>.tgz`.

[Microsoft's removal history](https://github.com/microsoft/vsmarketplace/blob/main/RemovedPackages.md)
lists **AhmedSlem.secure-codee** as **Malware**, removed 2026-01-31. The similarly
named `AhmedSleem.secure-code` entry is a separate coordinate. Added a hostile
finding for this exact publisher/name pair and a suspicious behavior composite
for source-code/language fields posted through an ngrok API. The underlying
POST-body observation is neutral and supports shorthand or explicit field
syntax in either order.

The original had no suspicious/hostile finding before these changes. Both
cleave and atomscan now report its hostile identity and suspicious transfer
behavior. The minimal identity fixture matches; independently changing the
publisher or name clears it. The source-transfer fixture matches; changing the
destination to an ordinary API or changing the body to health/status fields
clears the transfer finding.

Reports: `/tmp/secure-code-before.json`, `/tmp/secure-code-final.json`,
`/tmp/secure-code-fixtures.json`, `/tmp/secure-code-atomscan-final.json`.
Full validation still fails on existing worktree errors; no diagnostics name
the new SecureCodee or source-code transfer definitions. Output:
`/tmp/secure-code-validate.log`.

## 2026-11-15: Claude autocomplete 0.1.0

Identity: `siffat-ahmed.ai-autocomplete-siffat-ahmed`, SHA-256
`174faa457023acb69b8f8ebfb69015f2aad596d712f2e4eeb053d9767fdb4344`.

Reviewed all six executable modules: extension activation, completion provider,
API client, context extraction, configuration and cache. No external dependency
code is bundled. Language activation registers inline completions and explicit
commands. Requests require an API key and enabled configuration, include the
configured number of lines before/after the cursor plus filename, language and
cursor position, and go to `https://api.anthropic.com/v1/messages`. Authentication
uses the supplied key as `x-api-key`. The response is converted into completion
text; the explicit completion command inserts it through WorkspaceEdit. Neither
path evaluates a downloaded script or launches a subprocess. The cache is an
in-memory Map keyed with SHA-256 and a five-minute expiry. The key is saved in
global editor configuration. No other request destination or unrelated secret
collection was found in the shipped executable modules.

The manifest claims the repository `anthropics/claude-autocomplete`.
[Microsoft's removal history](https://github.com/microsoft/vsmarketplace/blob/main/RemovedPackages.md)
lists this exact publisher/name as **Impersonation**, removed 2025-12-15.
Added a suspicious identity finding that reports that removal reason without
claiming an executable malware payload or a credential-stealing destination.

The original previously had no suspicious/hostile finding. Cleave now shows the
impersonation warning; atomscan retains the same warning while its overall model
verdict remains benign. A minimal identity fixture matches, and independently
changing publisher or extension name clears it. Reports: `/tmp/siffat-before.json`,
`/tmp/siffat-final.json`, `/tmp/siffat-atomscan-final.json`.

Full validation still fails on existing worktree errors; the new definitions
receive no validation diagnostic. Output: `/tmp/siffat-validate.log`.

## Corpus inventory

`ide-extensions-datadog-inventory.json` records all 122 original VSIX files,
SHA-256 hashes, package identities, versions, sizes and exact case-insensitive
matches against Microsoft's removal history. There are 113 matches and nine
unmatched identities. Removal reasons remain separate from review status.
Only reviews substantiated in this ledger are marked complete; pending entries
do not erase previous thread work and must be reconciled with that evidence.

Initial investigation: `IconKief.icon-theme-material` 5.29.0. Its desktop
entry point has an inserted activationState block that refers to `context`
inside an activation function whose parameter is named `e`. The exception is
caught and logged before the remainder of activation. The existing suspicious
republish/activation-clock finding describes this incomplete preparation;
the comparison below resolves dependency and browser-entry review. No matching Microsoft
removal entry was found for this exact coordinate. Do not substitute the
different `Iconkieftwo.icon-theme-materiall` entry.

## 2026-11-15: IconKief comparison completed

Original SHA-256:
`1d61d7eecdd955ae24ac747b664ecd6aba692b6c9d6354afbae29ac6ffb246a6`.
Compared with the same-version `PKief.material-icon-theme` VSIX from its
[Marketplace artifact URL](https://pkief.gallery.vsassets.io/_apis/public/gallery/publisher/pkief/extension/material-icon-theme/5.29.0/assetbyname/Microsoft.VisualStudio.Services.VSIXPackage),
SHA-256 `70cdb2653fc6307b6a3c916511065a0d697b618e39ea62e7c3c84d5308324343`.

All 209 shipped dependency files across 12 dependency installations (11 unique
packages) match their published npm tarballs. Nested eventemitter3 copies are
compared separately rather than incorrectly counted as extra files in their
parent packages. The browser entry point is an empty activate/deactivate shim
and exactly matches upstream. No archive file was added relative to upstream.
Excluding dependencies, 1,211 files match byte for byte; the only changed files
are the VSIX manifest, content-type declaration, README, package.json and desktop
entry point. Manifest changes rename the publisher/name/display name, remove
the prepublish build script and broaden activation from onStartupFinished to
`*`. README changes rewrite the upstream promotional prose.

Removing just the inserted activation-clock block from a temporary copy makes
the desktop bundle match upstream's parsed JavaScript structure, operators,
identifiers and leaf values. Comparison normalizes formatting-only parentheses,
single-argument arrow parameter wrappers, optional new-expression parentheses,
delimiter punctuation and equivalent numeric spellings; array holes are
preserved. Neither bundle was executed. Helper and output:
`/tmp/vsix-ast-compare/`, `/tmp/iconkief-ast-comparison.txt`.

The inserted block references `context.globalState` while activate receives
`e`, with no `context` binding in the bundle. Normal activation therefore
throws and logs before the remaining activation setup. Existing top-level
command registrations still occur. The injected block has no attached payload,
network receiver or dynamic execution. Retain a suspicious disposition for the
republished extension and unexplained activation-clock insertion; do not assert
a proved malware stage or successful clock update. Changed the warning's
description to state that the extension *contains* a clock. A minimal broken
clock fixture matches; an otherwise identical first-party control stays clear.

Also corrected an independent false positive: the old suspicious `/root`
substring matched the `</root>` XML wrapper in the genuine svgson parser.
Replaced it with a neutral JavaScript root-home path literal observation and
updated its two exfiltration consumers. Both existing hostile home/root flag
search fixtures retain hostile findings; the new XML-wrapper control is clear.

Final reports: `/tmp/iconkief-cleaned-final.json`,
`/tmp/iconkief-atomscan-cleaned-final.json`, `/tmp/iconkief-clock-fixtures.json`,
`/tmp/iconkief-root-regressions.json`. Full worktree validation remains open;
the prior run's output is `/tmp/iconkief-validate.log`.

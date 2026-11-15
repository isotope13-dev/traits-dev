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

### Compact JSON reporting gap

The installed atomscan's compact decision omitted the activation-clock finding,
although its full report retained the suspicious composite and named it among
the verdict's top findings. `scan/src/lookup.rs::collect_hits` discarded every
finding with `from` contributors. That removes both ordinary inherited copies
and genuine container composites whose members hold only the component traits.

Changed hit selection to discard a container copy only if a referenced
contributor actually has the same finding ID and dependency coordinate at
reportable criticality. Cross-file composites now retain the enclosing artifact
path without inventing a source offset. Inherited matches continue to report
their member's path and evidence location. The regression verifies both cases
in one report; it passes. `cargo fmt --check` and both repositories' diff checks
also pass. The scanner model verdict is separate and is not forced to hostile.

Full original output: `/tmp/iconkief-atomscan-full.json`. Rebuilt compact output
check: `/tmp/iconkief-fixed-json.json`; build/run log:
`/tmp/iconkief-fixed-json.log`. Final trait validation still fails on existing
worktree issues: `/tmp/iconkief-final-validate.log`.

The rebuilt scanner's original-artifact compact JSON check passed: its model
severity remains benign, and `findings` now includes the suspicious
`republished-extension-activation-age-clock` composite on the VSIX path. The
installed binary has not been replaced; the verified build is
`../scan/target/debug/atomscan`.

## 2026-11-15: Amazon Q VS Code 1.84.0

Sample: `compromised_lib/amazonwebservices.amazon-q-vscode/1.84.0.vsix`,
SHA-256 `47f7840ecab6312d2733e1274c513050405886c70f2037fb2f1e9099872b0464`.
No exact Microsoft removal record was found. Its manifest declares no
`extensionDependencies` or extension pack; the only package dependency is the
repository-local `aws-core-vscode` (`file:../core/`), bundled into the shipped
build.

The main Node entry point exports `Sr` as `activate`. On activation, `Sr`
awaits `hr`, which invokes `q --trust-all-tools --no-interactive` with a task
to erase files under the user's home directory, clear configuration, enumerate
AWS profiles and terminate EC2 instances, remove S3 objects and delete IAM
users. This is direct destructive tasking with the agent's permission checks
disabled, not a merely theoretical agent capability. Existing hostile
agent-directed destruction traits match the sample; the `json-full` scan also
reports the sample hostile. An initial report also produced a network-profile
upload composite by combining common AWS SDK facts from distant parts of the
large bundle. Tightened that composite to require evidence within 4 KiB and
demoted generic `serverUrl`/`packageInfo` field-name markers to notable. The
network-profile hostile fixture still matches, while the final full scan no
longer reports that unrelated composite on Amazon Q.

The bundle also contains a beta updater that downloads a VSIX, validates the
publisher and extension name against the AWS product identity, and offers the
artifact for installation after a user confirmation. The updater runs only for
non-release builds, so this code is not expected to activate in the packaged
1.84.0 release. Still, code that installs a second VSIX merits a suspicious
review finding. Added `vscode-source-installs-vsix-artifact`, which reports the
install command near a `.vsix` package literal without asserting malicious
payload contents. A minimal installer fixture matches; an ordinary
marketplace-ID install control clears it. The existing missing-gallery
dependency composite remains hostile when the follow result says the required
extension has no release.

Fixture scans and full artifact scan:
`/tmp/vsix-installer-positive.json-full.json`,
`/tmp/vsix-installer-control.json-full.json`,
`/tmp/amazon-q-vsix-final.json-full.json`. The hostile agent fixture matches four
existing hostile findings; its safe-task control clears them. Reports:
`/tmp/amazon-q-hostile-fixture.json-full.json`,
`/tmp/amazon-q-control-fixture.json-full.json`,
`/tmp/amazon-q-host-command-positive.json-full.json`,
`/tmp/amazon-q-host-command-control.json-full.json`,
`/tmp/amazon-q-network-profile-positive.json-full.json`.

## 2026-11-15: ChatGPT-B0T 0.0.1

Sample: `malicious_intent/0xS1rx58D3V.ChatGPT-B0T/0.0.1.vsix`, SHA-256
`16a3169d5b75fe7df05488e7627380af9ea9a0c34d78ac413dde1e79e47dc021`.
Microsoft lists this exact publisher and extension as malware (3/18/2025).
The extension's chatbot command activation has a `help` input branch that
decodes an obfuscated payload, creates a PID-named lock file under the user's
home directory, opens a TCP connection to `6.tcp.eu.ngrok.io:16587`, accepts
commands, executes them with `child_process`, and returns output or errors.
The original full scan already reported the backdoor and JavaScript-obfuscator
runtime as hostile/suspicious. Added an exact listed-identity hostile composite
as a separate detection path, with positive and publisher/name near-miss VSIX
fixtures.

`--follow=all --format=json-full` identifies six declared npm dependencies,
all physically bundled under `extension/node_modules`: `node-fetch` 3.3.2,
`data-uri-to-buffer` 4.0.1, `fetch-blob` 3.2.0, `formdata-polyfill` 4.0.10,
`node-domexception` 1.0.0, and `web-streams-polyfill` 3.3.3. The included
dependency manifests and files scan benign, and the extension source does not
use `node-fetch`. The first sandboxed run could not resolve the declared
semver ranges against npm because registry DNS/network access was unavailable.
The escalated retry completed without registry warnings. The full report
contains the bundled package manifests and versions, each with benign
package-level results; no Fletch-specific finding ID is emitted in the report.
The VSIX's own backdoor is independently confirmed.

The identity positive, both near-miss controls, and original full scan are
`/tmp/chatgpt-b0t-listed.json-full.json`,
`/tmp/chatgpt-b0t-other-publisher.json-full.json`,
`/tmp/chatgpt-b0t-other-name.json-full.json`, and
`/tmp/chatgpt-b0t-sample.json-full.json`. The dependency-follow scan is
`/tmp/chatgpt-b0t-final-follow.json-full.json` (204 file/report records).

## 2026-11-15: HTTP Format 1.1.2

Sample: `malicious_intent/498-00.httpformat/1.1.2.vsix`, SHA-256
`435308cde3bf1420d399b5cdc1bfe7c654b15ee53fae93d6bfae331e1a41a33b`. No
Microsoft removal record was found. Its extension registers HTTP file
formatting commands and reformats request text; the activation bundle contains
the formatter/parser and bundled Axios code. The `json-full` scan is benign
across the VSIX, extension bundle, and manifest, with no suspicious or hostile
traits. The manifest declares `axios` at `^1.7.7`; `--follow=all` retained that
dependency reference but returned no resolved Axios package record or
Fletch-specific finding. The sandboxed registry lookup logged DNS failure; an
escalated retry emitted no registry warning but still returned only the six
files in the VSIX. Treat the dependency's Fletch state as unknown from this
report, not benign.

Reports: `/tmp/httpformat-1.1.2.json-full.json` and
`/tmp/httpformat-1.1.2-follow.json-full.json`.

## 2026-11-15: ETHcode 0.5.0

Sample: `malicious_intent/7finney.ETHCode/1.0.0.vsix`, SHA-256
`48aaa3827bc40c65e029b242d853faf4b2965605592f12c03f08c58d511a71a3`.
Microsoft lists this version as malware (6/26/2025). Its activation bundle
contains an obfuscated, platform-gated child-process launch that hides a
PowerShell download-and-run command. Existing hostile traits detect the
dropper and launcher, so the sample was already hostile before the dependency
rule changes.

The extension manifest hard-depends on `ibm.output-colorizer`. A required VSIX
is installed and activated by the editor, so raised
`vscode-extension-dependency-declared` from notable to suspicious. Added a
hostile composite for a hard extension dependency whose Fletch result says the
gallery has no release. A minimal hard-dependency package manifest matches the
suspicious trait; an `extensionPack` recommendation control does not. ETHcode's
network-enabled `--follow=all --format=json-full` report records
`references.unresolved_extension_count: 0`, so its IBM dependency is not
classified as missing. The earlier sandboxed attempt logged DNS failures and
is not used to infer the Marketplace state.

Reports: `/tmp/ethcode-0.5.0-follow-escalated.json-full.json`,
`/tmp/ethcode-0.5.0-final.json-full.json`,
`/tmp/vscode-dependency-positive.json-full.json`, and
`/tmp/vscode-dependency-control.json-full.json`. Fixtures:
`testdata/suspicious/generated/vscode-hard-extension-dependency/package.json`
and `testdata/notable/controls/vscode-extension-pack-recommendation/package.json`.

## 2026-11-15: AutoMindX 1.0.1

Sample: `malicious_intent/AutoMind.automindX/1.0.1.vsix`, SHA-256
`ea1ba4ae4aecef8ebfa9d5c9b6ea26cbd0187b4abad654c71a9c265a3ece5365`.
Microsoft lists this exact extension as malware (12/22/2025). Its manifest
description says it downloads and installs the AutoMind extension, and the
bundle contains code that downloads and installs a remote VSIX. The full scan
reports the exact listed-identity composite as hostile and both the archive and
source download/install composites as suspicious. The listed-identity fixture
coverage is recorded with the VSIX malware identity rules.

The `--follow=all --format=json-full` report sees the bundled Axios dependency
tree as benign package-level results. Its sandboxed registry lookups could not
resolve some semver ranges; the extension installer itself is independently
suspicious. No separate VS Code dependency PURL was emitted for its runtime
download target, so this run does not establish whether that target currently
exists in the gallery.

Full report: `/tmp/automindx-1.0.1-follow.json-full.json`.

## 2026-11-15: Lexica Image Fix 0.0.1

Sample: `malicious_intent/BenjaminFriedl.lexica-img-fix/0.0.1.vsix`, SHA-256
`796f1ff15b97bfcc0e0c7e148e7814d5001acfa28ee4f6a47a89db4b6661f69b`.
Microsoft lists this exact release as malware (10/20/2025), but its complete
activation bundle contains only a user-invoked image move: it copies the
selected image into the configured workspace folder, deletes the original,
rewrites Markdown references, and reports success. The package has no network
or process-execution references, and the original `json-full` scan was benign.
Added an exact publisher/name/version composite so the listed release is
hostile without claiming that the observed file operation is itself malware.

A minimal VSIX with the exact identity is hostile; a same-publisher/name
version 0.0.2 control does not trigger the composite. The original artifact,
positive fixture, and control scans are `/tmp/lexica-img-fix-final.json-full.json`,
`/tmp/lexica-img-fix-identity-positive.json-full.json`, and
`/tmp/lexica-img-fix-identity-control.json-full.json`. The sample was copied to
`elrond:/tmp/hostile/796f1ff15b97bfcc0e0c7e148e7814d5001acfa28ee4f6a47a89db4b6661f69b/0.0.1.vsix`;
the remote SHA-256 matches the inventory.

## 2026-11-15: BlockchainIndustries toolkits 0.0.1

The Datadog set contains three VSIXs, all listed by Microsoft as malware on
9/12/2025: `bitcoin-toolkit` (`f33a48f3c53a8f4ea7226a3f0bdc3ae0ee162fe3c686461d87dcbd4adacef009`),
`hardhat-toolkit` (`4765411edba7e601766b4cb01124d47d71f1684f15d046cb2f677f60a8881d39`),
and `solana-toolkit` (`a537fa7daa0aa23e7cd0480bcec93652b29763be91d32a4489f808493a4bd1df`).
The three archives share the same short extension source: activation registers
a `helloWorld` command that displays a greeting. No network, process, or
credential behavior was found, and the original scans were benign. Added
version-specific hostile identity composites for each publisher/name/release
tuple from Microsoft's malware listing; this records the provider's exact
disposition without attributing unseen behavior to the boilerplate payload.

Each positive identity fixture matches hostile, and a control from the same
publisher with a different extension name remains benign. Full reports:
`/tmp/bitcoin.json-full.json`, `/tmp/hardhat.json-full.json`,
`/tmp/solana.json-full.json`, `/tmp/bitcoin-fixture.json-full.json`,
`/tmp/hardhat-fixture.json-full.json`, `/tmp/solana-fixture.json-full.json`,
and `/tmp/control-fixture.json-full.json`.
The three original VSIXs were copied to their SHA-named directories under
`elrond:/tmp/hostile/`; each remote SHA-256 matches the inventory.

## 2026-11-15: Darcula Theme from PyCharm 0.9.0

Sample: `malicious_intent/Bobronium.darcula-from-pycharm/0.9.0.vsix`, SHA-256
`2f9d82fb8b4b1ad0ed9aa66f8d8430b6b1b65e6d8abdb09027d93e6b727b79d5`. No
Microsoft removal record was found. The six-file VSIX contains a theme JSON,
documentation, examples, and a manifest, but no executable extension entry
point or dependencies. Its README openly describes it as a fork of the
PyCharm Darcula theme; the Marketplace listing describes the same fork and
theme features. The `json-full` scan is benign with no suspicious or hostile
findings. I found no behavior-based trait to add and have left the verdict
benign despite its placement under `malicious_intent`.

Report: `/tmp/darcula-from-pycharm-0.9.0-follow.json-full.json`.

## 2026-11-15: CSF-RED 0.0.1

Sample: `malicious_intent/CSF-RED.CSF-RED/0.0.1.vsix`, SHA-256
`2a675259db7b80bb346b67940433145bff2e495ea6bbf7f0000711df433db65f`.
Microsoft lists it as malware (6/05/2025). The description calls it a proof of
concept for opening shells from an extension. The current full scan already
reports hostile TCP shell-bridge and auto-activated reverse-shell composites;
no additional trait was needed. Report:
`/tmp/csf-red-follow.json-full.json`.

## 2026-11-15: AI Docs & Comments 0.0.8

Sample: `malicious_intent/CodamaSoftware.ai-docs-and-comments/0.0.8.vsix`,
SHA-256 `074e4482ec84f347c2ed8ea875e92863efc115d20610a6b33e3aa7f4486f812b`.
No Microsoft removal record was found. Its two explicit commands send the
selected function text to `api.openai.com` using a user-configured OpenAI API
key and replace or annotate the selection with the response. The code contains
no process execution or other network destination; this is the advertised
functionality, not an independent exfiltration path. The full scan is benign
with no suspicious or hostile findings. No trait change was warranted.

Report: `/tmp/ai-docs-follow.json-full.json`.

## 2026-11-15: CSV Rainbow 3.3.1

Sample: `malicious_intent/csvmech.csvrainbow/3.3.1.vsix`, SHA-256
`c5894b4143846f6c77e9dd01a10aab9bea49c907c487051e87b0e6267a86f81f`.
Microsoft lists this exact publisher/name as malware (12/2/2025). The archive
contains the CSV editor feature set and no external package dependencies. It
reads and streams workspace files for CSV operations. Its newer activation
code also stores `firstActivated` and `lastActivated` timestamps, updating the
latter every two days; those values are not used elsewhere in the shipped
code. The timestamp composite is suspicious, but the scan provides no evidence
of an active payload or external exfiltration. The hostile verdict is grounded
in the exact Microsoft-listed identity.

Added a minimal hostile VSIX identity fixture. The package.json-only near-miss
control does not trigger the VSIX identity rule. Reports:
`/tmp/csvrainbow-3.3.1-follow.json-full.json`,
`/tmp/csv-rainbow-identity-positive.json-full.json`, and
`/tmp/csv-rainbow-identity-control.json-full.json`. The original sample was
included in the earlier SHA-verified `elrond:/tmp/hostile/` copy set.

## 2026-11-15: Sync Settings VS Code 0.18.2

Sample: `malicious_intent/cweijamysq.sync-settings-vscode/0.18.2.vsix`, SHA-256
`b05858ee95a168e278cf8a6d91ec6568b2f7adc0f0096aa1254952bd28bdb4ec`.
Microsoft lists it as malware (12/2/2025). The extension implements settings
synchronization and declares `zokugun.cron-tasks`, which resolves in Fletch.
Its activation code also stores first/last activation timestamps and updates the
last timestamp only after two days; the values are not used elsewhere. The
GlassWorm identity composite already gives a hostile verdict, and the activation
clock is suspicious. No missing-dependency hostile finding applies. Report:
`/tmp/sync-settings-vscode-0.18.2-follow-network.json-full.json`. The sample
was included in the earlier SHA-verified copy set under `elrond:/tmp/hostile/`.

## 2026-11-15: Echelon Solidity Language Support 1.0.1

Sample: `malicious_intent/EchelonStudios.blockchain-language-support/1.0.1.vsix`, SHA-256
`20261ca4eadf646c87d33aa4d0c1ac7d62e26616a7e808840e96e5903de2d6f8`.
Microsoft lists it as malware (9/03/2025), but the archive has no runtime
entry point: it contributes Solidity grammar, snippets, and language metadata.
Its 1.4 MB icon is a valid PNG with a C2PA record naming GPT-4o as the media
creator; no appended data was present. Added an exact publisher/name/version
composite based on Microsoft's malware disposition. The positive VSIX fixture
matches hostile and a version 1.0.2 near-miss remains benign. The original is
copied to `elrond:/tmp/hostile/20261ca4eadf646c87d33aa4d0c1ac7d62e26616a7e808840e96e5903de2d6f8/1.0.1.vsix`;
remote SHA-256 matches. Reports: `/tmp/echelon-ethcompiler-follow.json-full.json`
and `/tmp/echelon-identity-fixtures.json-full.json`.

## 2026-11-15: EthCompiler among-eth 1.0.2

Sample: `malicious_intent/EthCompiler.among-eth/1.0.2.vsix`, SHA-256
`ce72b79e324371134db762fe70b8b1789af899d7217461bc3658a6bd84743eb6`. The
package bundles a webpack loader that decodes hex data and executes shell
commands from buffered responses; a zero-width display name also masquerades
as a Solidity language extension. Existing hostile and suspicious traits cover
these behaviors. Report: `/tmp/echelon-ethcompiler-follow.json-full.json`.

## 2026-11-15: Solidity compiler extensions

`EtherFoundation.vs-ranket` 1.1.1 (`8a1372719cbf27a7122bab13ce753516f34bc5e21780e9260a64e63cdcababf9`)
and `Ethereum.SoliditySupport` 1.0.0
(`906ed264dedcb881928926d33118162791764ddbd9cf463d8d2393c6e1470ee7`) are
already detected hostile. The first bundles heavily obfuscated startup code
with platform-gated child-process behavior; the second has a JavaScript
obfuscator string-array runtime and computed child-process execution. Existing
traits cover both; no new trait gap was found. Report:
`/tmp/etherfoundation-ethereum-follow.json-full.json`.

## 2026-11-15: Expressjs session 1.24.0

Sample: `malicious_intent/Expressjs.expressjs-session/1.24.0.vsix`, SHA-256
`42cc6a8d60d8ac757ab3b1d901126ec2780927114471280281f2c9f9c97d7c10`.
Activation immediately collects the username, home directory, current working
directory, and platform, then POSTs them as JSON to
`xn--expessjs-00d.com` (a punycode lookalike of expressjs.com). The manifest
activates on `*`; session-library naming and bundled dependencies mask the
credential-free host-profile upload. Existing payload-carving, host-profile
exfiltration, and package-name typosquat traits detect it. Report:
`/tmp/expressjs-session-1.24.0-follow.json-full.json`.

## 2026-11-15: GavinLamWood Solidity Compiler 0.0.8

Sample SHA-256: `5b82fe2e0fd132273af1518a787d072db89452f3cac55619259c95d902159e93`.
The archive reuses the same heavily obfuscated `src/extension.js` payload as
the EtherFoundation Solidity compiler sample, activated at startup. Existing
JavaScript obfuscator and platform-gated child-process traits detect it.
Report: `/tmp/vs-blanket-0.0.8-follow.json-full.json`.

## 2026-11-15: GitlensPro repackaged extensions

Reviewed six releases from the `GitlensPro` publisher: `aicode-companion`
(2.0.0, `7783dc65d9e6d4bf459c2c1b9236f91f17c80bac73e4b81f9348e97525a06698`),
`codebeauty-formatter` (2.0.0,
`e5ec921e5ac0ff112f305857440075ae7227aadb4895b6d51b6cdc15e85c821a`),
`error-lens-ultra-pro` (2.0.0,
`fcaecc1c2eaee3bd1a5f2c5b478f99df9b128506ff44d1e5db4df6eb5922c74a`),
`gitlens-monocharged` (1.0.0,
`ee873b427a188f711509dcded3b739e7f46db0c02a6462414ab105c89684a4a8`),
`gitpro-ai-tools` (1.0.0,
`b9889b6102523a414b940fdd80ddf67c83b56cc161a6a9277f215d2c1fc09fce`),
and `peacock-workspace-colorizer` (2.0.0,
`6255390dea9e90474b5d61488f9e58b2ceb007f5b4cd483a553bc53dd07f3c45`). All
are already detected hostile: activation downloads and launches a hidden
executable, and bundles host-profile communication to a raw IP address.
Existing detached-executable and raw-IP traits cover the family. Report:
`/tmp/gitlenspro-family-follow.json-full.json`.

## 2026-11-15: Solidity extension payloads

`JacobETH.solidi` 1.0.7 (`7b545a61c45e7e9957b2a3b6af1c3a50bf2972c6431c047d592f0ecca55466f8`)
and `JohnGaffney.blankebesxstnion` 1.0.2
(`e19d5d8f941b9a98fbb3b65e1e6077fa00d97529e351e455297b0204ec07e9ed`) are
already hostile. JacobETH includes a hidden temporary batch and obfuscated
computed child-process launch; JohnGaffney reuses the hex-decoded shell loader
and zero-width Solidity display-name masquerade seen in other samples.
Existing traits cover all findings. Reports:
`/tmp/jacob-john-follow.json-full.json`.

## 2026-11-15: Email Grabber and AWSWHH

`JosephDembele95.email-grabber` 1.0.6 (`cd655274687202a1e286240341f4e81b863f69af6914e0d7d23f1cf36ecd55e8`)
contains a DNS TXT callback that receives and executes code, already covered by
DNS command-channel and bundled-extension traits. `JuanFBlanco.awswhh` 0.0.7
(`319de2fee235b1e198a873b9ee61fc6aabffba2ce2087eaad19218ad7b7f3514`) is an
obfuscated Solidity extension with a PowerShell download-and-execute cradle,
also already detected. Report: `/tmp/joseph-juan-follow.json-full.json`.

## 2026-11-15: Juan Solidity extensions

`JuanFranBlanco.solidit-vscode` 0.0.1
(`31c6e939b1ecaf8fb68d00cc21cbd6087c8e87a5c093294d252ac2ad88ab996d`) hides
zero-width characters in its Solidity identity and contains a startup temporary
batch payload with self-defending obfuscated JavaScript. `JuanRiseETH.solidit`
1.0.2 (`025191786cccb6d23ad3ea0dd577893db699672f1ab7a7f4ab559fec467d9f91`)
contains the platform-gated computed process loader also found in other fake
Solidity extensions. Existing traits detect both. Report:
`/tmp/juanfran-juanrise-follow.json-full.json`.

## 2026-11-15: NotToTest and OPENEDAI

`NotToTest.NotToTest` 0.0.1 (`d513b9032182828f8ee62270ce4fe141cd4ec871675ca516cc5c12e8d5632283`)
is a proof-of-concept TCP reverse shell with RFC1918 stream bridge and socket
callback shell behavior, already detected by existing traits. `OPENEDAI.OPENEDAI`
0.4.51 (`70f33f51433f4b5d3e994553aa26a87c308b9c5f5472d9f4d6f64354ddf9631e`)
repackages a Codex-like VS Code extension and carries a zero-width concealed
eval payload; existing Unicode decoding and extension-eval traits detect it.
Report: `/tmp/nototest-openedai-follow.json-full.json`.

## 2026-11-15: OzzyDev777 fake extensions

Reviewed `csharp-editor-pro` 2.0.0 (`df6279df009ac699d31731edfd0eb8f6337f8bcaa448e6d5fa504de0b29abf73`),
`dark-ai-professional` 2.0.0 (`1c2da414ca657ccd7c86b9a1b28f3b39d0fc21658d77cd4ae70e53445b8e02a3`),
`gitlens-turbo-pro` 2.0.0 (`d455c88e647e993b7cb81b6954957f28eab438defe2d422e251c5639c992ef1c`),
and `peacock-professional-edition` 2.0.0
(`ce7dac459438c6754c2e7dfde07a5babff96bc19043acfd16dd9713d2ce79c53`).
All are detected hostile: startup downloads and launches a hidden executable,
with raw-IP host-profile communication; the C# editor also recursively reads
directories. Existing traits cover these behaviors. Report:
`/tmp/ozzydev777-family-follow.json-full.json`.

## 2026-11-15: Clipboard History Manager 0.1.0

Sample SHA-256: `acb115d3986d901ba2db951e9f6bdcb8bdba308bb60b8a3397becdc2a6ddbe98`.
The VSIX implements a clipboard history provider and local storage, with
commands to inspect, paste, delete, and clear entries. Full scan is benign; no
network, process, or credential access behavior was found. No trait change.
Report: `/tmp/clipboard-history-manager-follow.json-full.json`.

## 2026-11-15: Puglight extensions

`discoverito` 0.0.1 (`87ae7f03436591c6dfd8bd44494f90d896122c4beb5b268f8f76eabd8a0ad8bf`)
collects account/process inventory at startup; `persistorito` 0.0.1
(`137e0ec991415629b46d4aae2b58f39611b8c729f96159a32652f3c7803f46fd`) adds
daily scheduled-task persistence and remote command/file access; `sysmotivate`
0.0.3 (`f6c65dacc626917fca4ad1cc75f5b2f32ff7d85079a1f51d6a007b0d6efe2d8c`)
implements event-driven HTTP command polling. Existing traits detect all
three. `inspiredaily` 0.0.1
(`37256430e47e7f949ef0621762ed4583ef8bee5a0839e929cab432cb0c93a660`) declares
a hard dependency on known-malicious `puglight.elevatio`; network-enabled
Fletch confirms the required extension has no Marketplace release, activating
the hostile unavailable-dependency composite. This sample was previously only
suspicious for hard extension dependency. It was copied to
`elrond:/tmp/hostile/37256430e47e7f949ef0621762ed4583ef8bee5a0839e929cab432cb0c93a660/0.0.1.vsix`;
remote SHA-256 matches. Reports: `/tmp/puglight-family-follow.json-full.json` and
`/tmp/puglight-inspiredaily-network.json-full.json`.

## 2026-11-15: ab-498 formatter and playground releases

Microsoft lists all four exact releases as malware (6/24/2025): `cppformat`
1.0.8 (`6d035a976f67a35ff7adb5dc1c87957b3bd81fa4b0c1fa3b28636bee3ec9c12b`),
`cppplayground` 1.0.42
(`2a5e329d44403e27c7bb5e2713d364d020319ca89bf099f4ee933f97e8da8518`),
`httpformat` 1.1.0 (`72c0a96b9bddba3b730342b9b40f04c7ac2fb6c0b7c8d0d9d988109f4ef7aecc`),
and `pythonformat` 1.0.50
(`0200806b14f835f559d32c2d1c07429a227b1e79a2e749a3096a10aad6f053cf`).
Behavior scans were otherwise benign except `cppformat`, which also has a
suspicious recursive directory-read finding. Added precise publisher/name/version
identity composites, four minimal hostile VSIX fixtures, and a same-publisher
unlisted-name control. All positives match hostile; the control remains benign.
The four originals were copied into their SHA-named `elrond:/tmp/hostile/`
directories and all remote hashes match. Reports:
`/tmp/ab498-family-follow.json-full.json` and
`/tmp/ab498-identity-recheck.json-full.json`.

## 2026-11-15: Shiba, Iconesvscode, dontdownloadthis, Shiny

All four samples already scan hostile. `ahbanC.shiba` 0.1.4
(`58ac09a29d42281d45c2373d58da14e6d8d38509a3f9df66a374132a8ab879d0`) uses a
remote PowerShell command path with Telegram shell output and a raw-IP callback.
`dontdownloadthis.dontdownloadthis` 0.0.2
(`e3e7ece591884b5ca541b39c052a22f42d793ddfdaaa01f0a1b10b3106436606`) starts a
temporary batch payload and removes its artifacts. `bphpburnsus.Iconesvscode`
12.15.0 (`179c25d69c34f332d0f2b408d30c47356c9da679ecf404ab8f16a1e29dc62c69`)
and `eamodas.shiny-vscode` 1.3.2
(`111596481d07cf6f360ee77b615cd6dde4ee1dd6880f1dcb4a4c09b03c18fbec`) both
match GlassWorm identity and activation-age-clock traits. No additional traits
were needed. Report: `/tmp/ahban-icones-dontdownload-shiny-follow.json-full.json`.

## 2026-11-15: EmbedDTeam impersonation releases

Microsoft lists `embedded-build-analyzer` 1.1.3
(`e07d2f8c8dcfb5d225b5107d6752aee9d2e29680055c8dc978d000db3a5d430e`),
`embedded-cortex-debug` 1.14.0 (`dddd509326ceb2973254e07d63c84c1ac79e828a9334db8261f43dbc90e26a6d`)
and 1.14.1
(`faf06f760024dbf1b8eaf3a29355544e73e337d03a07bc048cc5fa53da67788c`), and
`embeddedprojectmanager` 0.0.1
(`b84987ab0a14b8fa6fcb9af787794f4e62c6b6b909372667aae7f4107fa14343`) as
impersonation. Added exact suspicious identity composites for these release
tuples. The analyzer enumerates build inputs and invokes its expected toolchain;
Cortex-Debug's debugger process and directory operations match its advertised
functionality. Their identities and declared hard dependencies remain visible
for review. Fletch resolved the Cortex-Debug 1.14.x mcu-debug dependencies and
the 0.0.1 project-manager dependencies.

`embeddedprojectmanager` 0.0.2
(`a981a897b95df87869dc5caceca2c1ef1c4aed147f79300654eb9ebb13d5ac05`) instead
hard-depends on the removed EmbedDTeam Cortex-Debug and Build Analyzer VSIXs.
The network-enabled scan fires `vscode-requires-unavailable-extension`; a
minimal VSIX fixture matches hostile and an available mcu-debug dependency
control stays benign. The original 0.0.2 VSIX was copied to
`elrond:/tmp/hostile/a981a897b95df87869dc5caceca2c1ef1c4aed147f79300654eb9ebb13d5ac05/0.0.2.vsix`;
remote SHA-256 matches. Reports: `/tmp/embeddteam-family-network.json-full.json`,
`/tmp/embeddteam-vsix-dependency-fixtures.json-full.json`, and
`/tmp/embeddteam-impersonation-recheck.json-full.json`.

## 2026-11-15: Flutter, Darcula, and poisoned assistant

`flutcode.flutter-extension` 3.122.0
(`09bfe7d81794d8ab15a6cfb9d75e7e13feb0ce8ba5624bfb65afdb8252909dc2`) matches
the existing hostile GlassWorm identity and activation-age clock traits.
`hajoo.poisoned-extension` 1.0.3
(`cfab4f708b46f3057c48829960a2e325b577a49f48e9122a4d22ca5d17781f2a`) includes
a coding-assistant prompt that explicitly asks for vulnerable code, already
covered by hostile traits. `garytyler.darcula-pycharm` 1.0.0
(`437ab29c8f442b450f2ce8bea64097a9e97b5779b3ea7b1d26618f175522fd2b`) is a
data-only theme. Its hard dependency on MagicPython resolves in the networked
Fletch scan; no hostile behavior was found. The hard dependency remains
suspicious for review. Reports: `/tmp/flutter-darcula-hajoo-follow.json-full.json`
and `/tmp/garytyler-darcula-network.json-full.json`.

## 2026-11-15: Juan Blanco Solidity trojans

`juanbIanco.soli989` 0.0.189
(`556aa6a359fbfa1c83658c4d06ad08c68d978b46a0bc713ad10f376564d4486d`)
profiles the host and executes the HTTP response in a Node VM; existing
response-eval and exfiltration traits detect it. `juanblan281.solid281`
0.0.189 (`ac4af25b0c46e2dc3ba9c66fae3ff83afeee4e2053d0816fab3406d41aee5915`)
contains a Python PTY shell channel and zero-width Solidity masquerade, already
detected by existing traits. Report:
`/tmp/juanblanco-soli-family-follow.json-full.json`.

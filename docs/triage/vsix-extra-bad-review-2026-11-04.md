# Additional VSIX bad-label review, 2026-11-04

This tracks the 100-file snapshot under
`/var/tmp/triage-vsix-20261104/mislabeled-bad/`. The snapshot paths do not
necessarily reflect current Hopper labels. Unlisted files remain unreviewed.

`89bd0d3933d6` (Sinch Conversation API 0.1.8) is hostile under the
user's policy. Its archive matches the Open VSX published checksum. The
registered `sinch.skills.generate` command submits `npx skills add
sinch/skills --skill '*' ...` to a workspace terminal: `skills` has no
version pin, and the repository reference does not specify a revision. The
terminal or npx may still prompt, so the archive does not establish that an
installation took place. Independently, the RCS webview uses a nonce-bearing
script tag with a remote `prd-latest/remoteEntry.js` URL, allowing that code
to change independently of the VSIX. The webview route and skills command are
separate execution paths; their combination meets the user's rule. No claim
is made that the repository or remote script actually served malicious
content. Added observations for the terminal dispatch and latest remote
webview script, two suspicious archive findings and a hostile composite.
Controls pinning the npx package or replacing the latest webview path clear
the corresponding observations; pinning the CLI alone would not pin the
skills repository. The archive matches, a reduced VSIX fixture contains the
shipped code, full validation passed, and Hopper confirmed the bad label.

`0e2bcbd60d11` (DotShare 3.2.0) is recorded good with one suspicious
finding. Its SHA-256 matches the Open VSX published checksum. In the
user-invoked LinkedIn or Telegram sharing fallback when credentials are
missing, the extension URL-encodes the first workspace's local filesystem
path into the social service's share URL and opens it externally. This
exposes the path to the selected service; the fallback does not upload
workspace contents. The bundled sharp library contains unpinned npm commands
in diagnostic or package metadata, but those strings were not shown to be
executed. A generic suspicious rule captures the social URL, workspace-path
encoding and external-open sequence; controls replacing the path, both
destinations, or the open call clear it. Archive scan matched, full validation
passed, and Hopper moved the sample from pending to good.

`14298de07b25` (Voltai Staging 0.0.1780268057) is hostile under the
user's policy. After activation,
version enforcement can fetch a mutable `install.sh` from the configured
release base, chmod it, and run it through Bash. A specific CLI version is
passed as an argument, but the installer script itself is not version-pinned
or verified in the reviewed path. Independently, when no server URL is
configured the extension falls back to `http://166.117.3.52`; a structural
information request can attach the locally stored Voltai bearer token to
that plaintext HTTP endpoint. An HTTPS configuration overrides the fallback,
and an available token and the relevant request are prerequisites; neither a
real transmission nor malicious server content has been established. The
separate script execution and plaintext credential exposure meet the user's
rule. The surfaced `curl ... | sh` failure message is only a suggestion and
is not the evidence of execution. Added observations for the linked
download/chmod/Bash call and the conditional HTTP bearer path, and a hostile
archive composite requiring both. Controls altering the script path or shell
call and switching the fallback to HTTPS or removing the bearer header clear
the respective findings. The archive matches; a compressed fixture contains
the manifest and shipped entry point. Full validation passed and Hopper confirmed the existing bad label.

`be0868053d8a` (wlnxingdev.free-senltig 17.6.0) is hostile under the
user's policy. It republishes GitLens
marketing text and repository under a foreign publisher, and Microsoft lists
the identity for impersonation. Compared with the official Open VSX GitLens
17.6.0, it changes entitlement logic to return a paid Pro plan expiring in
2099 and adds a ZIP extraction module. Both official and republished builds
have an MCP setup path that queries the GitKraken `gkcli-proxy` production
`active` release, downloads the returned ZIP, extracts the CLI, and executes
its install command. The code does not pin a release or verify an archive
hash in this path. Actual downloaded bytes and any execution on a particular
machine are not established. The active installer plus independent
impersonation meets the user's hostile policy. Added a source observation
covering the linked active metadata, ZIP download and CLI execution; a
suspicious archive rule covers the floating installer and a hostile rule also
requires the foreign-publisher finding. The official 17.6.0 archive matches
only the suspicious installer rule, while controls pinning the channel or
removing its download or install call clear the observation. A reduced VSIX
fixture contains matching identity metadata and the shipped entry point. Full
validation passed and Hopper confirmed the existing bad label.

`6aec1a6e6a27` (AIBC Ads 0.1.16) is reviewed as good with one
suspicious finding. It advertises
spinner ads and periodically obtains ad records from the configured AIBC
portfolio service. When an ad is available it appends generated ad code to
the installed Anthropic Claude Code extension's webview JavaScript, after
creating a backup. The injected script inserts the remote ad text into
`innerHTML` without HTML escaping; malicious markup in a response could
affect the webview, subject to its content security policy. The reviewed
archive does not establish that the service actually returned hostile markup
or that injected code executed. It also installs a bundled CLI status-line
script and replaces the corresponding Claude settings entry; restoring the
stored settings backup can discard unrelated settings changes made since the
backup. The bundled heartbeat sends the product's device ID and, if present,
its own AIBC bearer token; it does not read prompts or source from stdin. The
ad service supplies data, not an identified unpinned package version. Added
a suspicious source signature combining the remote portfolio, rewrite of the
Claude webview, and unescaped HTML insertion. Controls changing the target,
write, HTML sink, or portfolio route clear it. The signature is tailored to
this implementation and does not prove that any payload was served. Archive
scan matches; full validation passed and Hopper recorded good.

`faf06f760024` (Embedded Cortex-Debug 1.14.1) is reviewed as good with
one suspicious identity finding. The
manifest describes a fork of marus25/cortex-debug, and Microsoft lists the
`embeddteam.embedded-cortex-debug` identity for impersonation without a
version-specific explanation. The extension and debug-adapter bundles show
debugger and telemetry functionality; no floating runtime installer was
established. Package-build scripts containing npm commands are not executed
by normal VSIX installation. All 12 bundled USB native modules exactly match
the published `usb` 2.14.0 tarball, and all 10 serialport native modules
match `@serialport/bindings-cpp` 10.7.0. Added a suspicious identity-level
observation with an inert positive fixture and separate changed-publisher and
changed-name controls; this does not claim the identity listing establishes a
malicious payload. Archive scan matches the observation. Full validation passed and Hopper recorded good.

`6fa510cee20d` and `734a5add9f3e` (KuaiJS 0.9.15 and 0.9.13)
meet the user's hostile policy. Their
5,262 members differ only in the VSIX manifest, package manifest, and main
JavaScript. Each main file conceals over 12,000 strings with an RC4 table and
decodes module names at runtime. Static offline decoding and call tracing show
that the `runInstallDependencies` method resolves the command
`npm install ms-types@latest ms-vite-plugin@latest -D` and passes it to
`child_process.exec`, using the project path as its working directory. The
method is also invoked from `checkAndInstallDependencies` in the newer
release; the exact trigger and whether a particular installation ran have not
been established. The command specifies floating latest versions and this is
independent of the strong string obfuscation, satisfying the user's policy.
No claim is made that the packages fetched from npm were themselves malicious.
The ID includes `ms-vscode` but the publisher, display name and icon identify
KuaiJS; that ID alone is not treated as Microsoft impersonation. Added generic
suspicious coverage for a dense encoded-looking string sequence, RC4 decoder
and computed module imports; a second rule matches both releases' specific
encoded command-to-exec paths as hostile. The latter is tied to the two
encodings and is not a general-purpose decoder. Controls removing the
computed import or changing the alphabet clear the generic rule; controls
altering the ciphertext or execution argument in either release clear the
hostile rule. Both original entry points have been added as compressed
hostile fixtures. Full validation passed and Hopper confirmed the existing bad labels.

`52c75a5b1b37` (Antigravity Ask Bridge 0.3.2) is recorded good with one
suspicious finding for a serious exposure. Its archive SHA-256 matches the
Open VSX published checksum. The disclosed bridge activates by default and
provides HTTP endpoints for retrieving conversations and artifacts, submitting
prompts, and invoking agent UI actions including acceptance and terminal-run
actions. The server installs permissive default CORS and has no authentication
middleware in the reviewed route setup. Although the README describes loopback
addresses, the bundled Hono adaptor passes an omitted hostname to Node's
`listen`; this normally binds the unspecified address, subject to host network
configuration and firewall. The artifact route checks a string prefix rather
than a path-component boundary or resolved symlinks, a separate traversal
weakness. Reachability, exploitation, actual conversation access, and commands
executed by any particular client are not established. This is an openly
described automation bridge with unsafe implementation rather than evidence of
a covert-control payload. The README recommends `npx antigravity-ask`, but
the extension itself has not been shown to execute that command; it is not
counted as an unpinned runtime installer. Added a suspicious observation for
the combination of a Hono conversation route, default CORS, and `serve` without
a hostname option. Controls adding a loopback hostname, restricting CORS, or
changing the conversation route each clear it. The matching is syntax-based
and does not by itself prove remote reachability or absence of authentication.
Full validation passed and Hopper recorded good.

`a04bacbc3dd6` (NGC CommitGuard 1.2.0) is recorded good. The archive
SHA-256 matches the Open VSX published checksum. Its activation installs the
bundled pre-commit hook for each workspace Git directory using a truncating
write, without first preserving an existing hook; this can disable previous
checks. Its pre-commit scanner lists staged paths but reads their working-tree
contents rather than staged blobs, so partial staging can evade its checks.
These are security and reliability defects, not evidence of a theft payload.
The dashboard includes a Chart.js script with version 4.4.1 explicitly named;
it has no integrity attribute, but is not an unpinned version under the
user's policy. The reviewed scanner emits detections locally; no transmission
of scanned contents was established. Its bundled js-beautify unpacker has
Packer examples embedded as test strings; the prior obfuscation rule falsely
classified these strings as an executable payload. Added a JavaScript AST
check for an eval call with the Packer-shaped function while preserving text
matching for HTML and shell. The standalone packed example matches, the
unpacker module no longer receives that suspicious trait, and permanent
fixtures cover both. Added a neutral observation for the truncating
pre-commit write; different-hook and exclusive-write controls clear it. The
post-change archive scan has no suspicious or hostile traits; full validation
passed and Hopper recorded good.

`3903262426bc` (Smarty Formatter 2.1.2) is recorded good with one
suspicious finding. Microsoft lists this publisher and extension identity for
impersonation. The package replicates the description and presentation of
aswinkumar863's Smarty Template Support, while using a different publisher and
repository. Its shipped Node and browser language-server bundles are exact
byte matches to upstream 2.1.0 from Open VSX; a tokenized comparison of the
client bundles shows formatter changes and publisher metadata. The manifest's
postinstall commands are development scripts, not evidence that the VSIX
installer executes npm. No floating runtime installation or second suspicious
behavior was established. Added a suspicious identity-level signal with a
minimal fixture; controls changing the publisher or extension name and
omitting the VSIX ExecutesCode property clear it. Validation passed; Hopper
recorded the good ruling. This is not a claim of upstream authorship or that
the client bundles are byte-identical.

`87ae7f034365` (Puglight Discoverito 0.0.1) is retained bad. On every
activation the extension notifies the user that it is collecting system data,
then writes the full Node process environment, host and network inventory, and
process list to a predictable Desktop JSON file, and writes local account and
privilege information to a second Desktop file. This captures all environment
values without filtering; those values may contain credentials, but the
artifact does not establish that any particular secret was present. The
reviewed entry point does not send the reports over the network. Microsoft
identifies this exact extension identity as malware; the combination of that
context and the implemented automatic, unfiltered environment collection is
the basis for the hostile ruling. The Microsoft VS Code repository URL in the
manifest is consistent with a starter template and is not separately treated
as proof of impersonation. A behavior-linked generic rule detects full
environment serialization to the Desktop without depending on the product
name. Redacted environment, different serialized object, and non-Desktop
destination controls do not match. The existing unattributed collector fixture
is suspicious on this behavior rather than hostile by identity. Full
validation passed and Hopper confirmed the existing bad label.

`0aaebf73e917` (AI Box 1.1.7) is hostile under the user's policy. Like 2.0.2,
archive, it reads Cursor access and refresh tokens and installs editor hooks.
Opening its panel fetches an Apollo configuration and syncs enabled hook
script bodies into Cursor or Qoder's executable hooks. The response can
change independently of the installed archive and the reviewed code has no
content pin or signature verification. This is an unpinned remote-code path;
combined with the independent Cursor token access it meets the user's hostile
policy. There is no evidence here about what the remote service actually
returned or whether a particular hook executed. Its bundled guide also has
user-clicked terminal commands including `npm install` and
`pip install -r requirements.txt`; these can depend on project lockfiles or
requirements and are not treated as proof of a floating package version.
The floating npm execution found in 2.0.2 has not been established in 1.1.7.
Added a source observation that links the fetched Cursor hook configuration
to the sync call and a hostile composite requiring that link, the Apollo
endpoint and hook key, script-content writes, and the Cursor token query.
Controls breaking the fetch, callback data flow, or token query each clear the
hostile composite. Atomscan matches the original archive, `make validate`
passed, and Hopper confirmed the existing bad label.

`5809bda98294` (BkCode 0.89.0) is hostile under the user's policy. Microsoft lists this
identity as malware without version details. The 705 KB entry point uses an
encoded, rotated string table; its strings were decoded offline without
executing the extension. The decoded code includes an AI coding agent, an
Ollama model pull, optional user-controlled PowerShell, and an activation
event to Google Analytics using VS Code's machine ID, respecting the editor's
telemetry setting. The bundled README discloses the analytics and machine ID.
A floating npm command occurs in an example prompt, while a floating PyTorch
install occurs in generated documentation; neither has been shown to execute
automatically. The decoded installer flow does submit unpinned `winget install`
and `winget upgrade` commands to an editor terminal after the user chooses the
corresponding Ollama action. Its extensive string-table obfuscation is an
independent suspicious characteristic. No claim is made that an installer
actually ran on a particular machine or that its downloaded content was hostile.
The bundled sql.js JavaScript and WASM match the published 1.14.1 package.

Added a general suspicious rule for a terminal-submitted floating winget
install or upgrade, and a narrowly scoped hostile rule for this encoded
installer dispatch and rotation. Plain floating commands match while a pinned
control does not; controls altering the encoded command, dispatch index, or
rotation checksum clear the hostile finding. Atomscan matches the archive,
`make validate` passed, and Hopper confirmed the existing bad label. The
encoded rule depends on this particular table and checksum; it does not decode
arbitrary obfuscator variants.

`a1b14da8f83e` (SFRA Toolkit 0.0.2) is hostile under the user's policy. Its optional dependency
installer asks the user before submitting `npm install sgmf-scripts --save-dev`
to a terminal, then its other commands can invoke that tool. The command itself
does not specify a version; an existing workspace manifest or lockfile may
constrain what npm resolves. A separate active-file view interpolates an
unquoted workspace filename into `execSync` Git commands, making crafted
filenames a shell-injection risk; this is a vulnerability, not evidence that
the extension contains an exploit. Microsoft records the extension identity as
malware without version-specific behavioral evidence. An older rule treated
that identity alone as hostile, and its hostile fixture contained only an inert
activation function. Changed the identity finding to suspicious, moved that
identity-only fixture to the suspicious pool, and added linked observations
for the unversioned installer. Under the user's policy the installer plus the
independent removal signal yields a hostile archive finding. Controls pinning
the installer or changing the publisher clear that composite. A linked source
observation records the shell interpolation without treating all matching
implementations as exploitable; a control replacing the interpolation clears
it. Atomscan matches the archive, full validation passed, and Hopper confirmed
the existing bad label.

`bc17d3a4fede` and `8e5c125987b5` (Dev Session Canvas 0.19.0 and 0.24.2)
are recorded good with one suspicious finding each. Both let the user choose a terminal installation of
Claude Code or Codex using a global npm command without a version pin. The
bundled command property reaches the terminal dispatch helper; added a
suspicious finding for that linked configuration and call. The extensions
also offer commands to open local Codex or Claude configuration files; the
reviewed creation path uses exclusive file creation and does not overwrite an
existing auth file. The newer archive adds a template marketplace and both
bundle a terminal supervisor, webview and native PTY code. The PTY JavaScript
and native binaries match the published node-pty 1.2.0-beta.12 tarball. The
reviewed supervisor uses a local socket for managed terminal sessions. In the
newer archive, installing a marketplace template saves it for a separate
user-initiated apply action; applying it checks workspace trust for agent and
terminal nodes. No independent second suspicious trait was established.
Atomscan reports the installer finding on both archives, and controls pinning
both commands or breaking the field-to-helper call clear it. Full validation
passed and Hopper moved both archives to good; the unpinned installation risk
remains visible in the scans.

`0e0dbc15868d` (Embedd Project Manager 0.0.5) is hostile under the user's
policy: Microsoft records its extension identity for impersonation, and its
code checks the latest GitHub release and offers to download and install the
newer VSIX. The check runs after a delay when enabled; the VSIX download and
installation require the user to choose Install. The updater follows the
release asset URL without an extension-level version or content pin. This
does not establish that any particular downloaded release is malicious or that
the user installed one. Added separate suspicious observations for the
identity and updater plus a hostile archive composite. Controls changing the
publisher, selecting a versioned release URL, or removing the local extension
installation call clear the composite. Atomscan matches, full validation passed,
and Hopper confirmed the existing bad label.

`234a2d8dbe40` (TuyaOpen IDE 0.1.3) is hostile under the user's policy.
Microsoft records the extension identity for impersonation. When starting its
LAN debugger, the extension generates a dependency manifest with floating npm
ranges, installs it, and loads the resulting packages. A fresh installation
has no extension-supplied lockfile for that generated manifest. The separate
`npx ... --no-install` build path does not itself download a package. Added
source observations for the generated manifest and installer, a suspicious
identity signal, and a hostile archive composite. Controls pinning all ranges,
changing the manifest argument or installer command, or changing the
publisher clear the corresponding finding.

The original scan also falsely claimed that a postinstall hook sent
environment names over HTTP: its hook, environment enumeration and HTTP body
came from different bundled components. Restricted that heuristic to a
single source file within a package and downgraded the remaining unlinked
co-occurrence to suspicious. A second remote-script finding came from a
web-preview bundle that matched unrelated script and HTTP URL fragments;
requiring the fragments to occur close together cleared that match. The final
scan retains the actual floating-dependency and identity findings. Full
validation passed and Hopper confirmed the existing bad label.

`0ca8837146f2` (Multi 0.0.88) is hostile under the user's policy. Its
activated VS Code platform initializes a browser manager whose default
Chromium resolver selects the latest revision. On a cache miss, the resolver
downloads that revision and performs an unsandboxed launch check; the web
fetch tool also launches the resolved executable with `--no-sandbox` and
`--disable-setuid-sandbox`. A configured revision, environment override or
existing cache can alter the download path. The combination of a floating
executable and the separate sandbox bypass meets the user's rule; no claim is
made that the downloaded browser itself is malicious or that any particular
install occurred. Added linked source observations and an archive hostile
composite. Pinning the resolver default, restoring the launch sandbox, or
breaking the resolver-to-launch binding clears the corresponding control.
Atomscan matches, full validation passed, and Hopper reported the bad label
was already recorded.

`5a251527afb4` and `fd46de73c673` are SWEObeyMe 5.0.2 and 5.0.26.
Each has hundreds of bundled files. The older entry point
removes older directories bearing its own extension prefix at startup. The
newer entry point registers its bundled MCP server in a Windsurf config;
the README describes automatic MCP configuration. If the existing config
cannot be parsed, the implementation resets the in-memory object and writes
it back, risking loss of other entries. The newer release sends extension-host
error messages and stack traces to a default webhook; that error path does
not consult the `errorReporting.enabled` setting even though the setting says
false disables all automatic reporting. Another MCP tool explicitly reports a
false positive and can send the tool-provided code context and file path to
the webhook. No actual report, source content, credential, or malicious
destination has been observed. Both initial archive scans have no suspicious
or hostile traits. Added linked source observations for posting an error
stack and for posting supplied code context, with suspicious findings for the
missing opt-out reference and the context report. Removing the context or
changing the POST body clears the latter; adding an opt-out reference clears
the former. The new scan reports both findings on 5.0.26, and full validation
passed. The supplied webhook server is designed to create GitHub issues from
received diagnostics, but the deployed service's actual operation and any
particular report are not established. Subsequent analysis found the floating MCP checks described below; the newer
release is retained bad under the user's policy.

In 5.0.2, the bundled MCP server prepends an orientation prompt with mandatory
tool-use instructions to the first tool result of a session. The extension
advertises AI governance, but the automatic instruction insertion is a
suspicious characteristic and now has a dedicated finding. Removing the
directive or replacing the prepend clears it. Its old-version cleanup is
limited by the extension's own directory prefix; its reviewed issue-report
path uses a user-configured webhook or GitHub integration. The final scan has
one suspicious and no hostile findings; no unpinned installer or independent
second suspicious trait was established. Full validation passed and Hopper
moved this exact release to good, retaining the prompt finding.

The latest rescan also identifies the startup-prompt behavior in 5.0.26, in
addition to its two reporting findings. The report handler's input explicitly
allows a code snippet and constructs a POST containing that snippet and file
path; the handler does not itself establish that the user supplied or approved
a specific report. The extension settings state that automatic governance
failure reports contain no file contents and that disabling reporting stops
all automatic reporting. The extension-host error path nevertheless sends
stack traces on its catch paths without reading that opt-out. Those facts are
recorded separately because the snippet-report tool and automatic host-error
handler are different paths; no actual report or specific contents have been
observed.

Later tracing corrected the earlier conclusion about 5.0.26: its registered
`comprehensive_error_detection` and `comprehensive_error_detection_file` MCP
tools call a detector that invokes `npx eslint --version` and `npx prettier
--version` through a promisified `child_process.exec`. Other checks also
execute floating npx commands. Existing local packages, npm configuration and
interaction can affect resolution or execution; no installation on a machine
is established. These floating checks plus the independent reporting and
startup-directive findings meet the user's hostile policy. Added an observation
linking the registered handler to the promisified exec and npx checks, plus a
hostile archive composite requiring an independent suspicious finding.
Controls pinning the npx command or breaking the handler dispatch or exec
binding clear the observation. A compressed fixture contains the shipped MCP
and extension code; the final scan matches, full validation passed, and
Hopper confirmed the existing bad label. The 5.0.2 MCP bundle does not contain
this error-detector path.

## Reviewed and recorded good

- `9faa1af91e46`: Tooltitude for Go 1.50.1. The extension starts its bundled
  native language server and reports product telemetry to its configured
  Tooltitude endpoint. The macOS binary's identity identifies a Go language
  server; its inspected imports contain local process and filesystem operations
  but no ordinary socket-connect import, and the scan found no suspicious or
  hostile traits. The exact older upstream binary was unavailable at the
  checked Open VSX endpoint, so no byte-for-byte provenance claim is made.
  Full validation passed and Hopper moved this exact archive to good.
- `64ee935d8c6f`: Rstest 0.10.6. The extension uses workspace test
  configuration and a bundled worker for test integration. Its bundled
  macOS native SWC module matches the published `@swc/core-darwin-arm64`
  1.15.41 tarball byte for byte. No floating installer or hostile payload was
  identified. The current scan has no suspicious or hostile findings, full
  validation passed, and Hopper moved the archive to good.
- `b40ec13e47f5`: Infracost 0.4.1, recorded good with one suspicious
  finding. Its bundled macOS language server matches the official Infracost
  LSP v0.3.13 release binary byte for byte. The extension offers to update it;
  after the user selects Update, the server checks GitHub's latest release,
  downloads an asset and replaces the current executable without a version
  pin. Added native updater observations and an archive finding; altered binary
  controls that remove the latest-release or download/replace indicators clear
  the observation. The final scan reports that single suspicious finding,
  full validation passed, and Hopper moved the archive to good. The updater
  risk remains visible and no particular later release is asserted malicious.
- `eeeb8334f88f`: MES Reference Library 3.19.7, recorded good with one
  suspicious finding. On first activation it can sync wiki Markdown from the
  mutable `main` branch, render raw HTML, and display the resulting page in a
  script-enabled webview. A changed upstream page could therefore execute
  scripts when viewed; no script tags or event handlers were found in the
  bundled HTML and Markdown reviewed. This is an implemented trust-boundary
  weakness, not evidence that the remote source served malicious code. The
  identity is listed by Microsoft as untrustworthy without a version-specific
  rationale. Added a suspicious archive observation for the combined source,
  renderer and webview characteristics; pinning the branch or disabling raw
  HTML or webview scripts clears it. Atomscan matches, full validation passed,
  and Hopper moved the exact archive to good while retaining the finding.
- `bd0b6cf18bcf`: IronPLC 0.205.0. Its language and editor support finds a
  separately installed compiler through configuration, environment or known
  local paths, then communicates with it for analysis and execution. The
  reviewed archive does not install a floating dependency or contain a
  hardcoded external payload endpoint. Microsoft lists the identity as
  untrustworthy without a version-specific explanation. The current scan has
  no suspicious or hostile findings, full validation passed, and Hopper moved
  this exact archive to good.
- `88f441a7af6c`: 4D Call Chain Explorer 0.3.12. The extension and its
  stdio MCP server implement 4D call-graph, editor and test workflows. The
  test runner uses a configured command; no floating installer was found.
  The bundled tree-sitter modules import parser/runtime functions and WASI
  descriptor operations, with no network import. Microsoft lists the identity
  as malware without version-specific evidence; the inspected entry points do
  not establish a payload. The current scan has no suspicious or hostile
  findings, full validation passed, and Hopper moved this exact archive to good.
- `f65066186abd`: ShipStatic 0.2.10. The command asks the user to select a
  deployment directory and uploads its eligible files to the configured
  ShipStatic service; its bundled MCP server exposes the corresponding deploy
  action. It excludes dotfiles and disallowed extensions, but its recursive
  walk uses `statSync`, follows symbolic links, and does not check that their
  resolved targets remain in the selected directory. A link inside the chosen
  directory can therefore bring eligible files from elsewhere into a deploy.
  This is an exposure risk, not evidence of an attacker-selected destination
  or of a real upload. Added a neutral source observation for the recursive
  `statSync` walk; both bundles match and an `lstatSync` control does not.
  The current scan has no suspicious or hostile findings, full validation
  passed, and Hopper moved this archive to good.
- `8068c23bd16b`, `8e8c5609ee46`, and `8a5f81c7c32b`:
  EveryAPI 0.25.0, 0.23.0, and 1.1.0. These implement an AI chat and coding
  agent using the configured EveryAPI endpoint and a user-supplied key. The
  0.23.0 and 0.25.0 JavaScript files are byte-identical; 1.1.0 has a newer
  bundle and UI. Reviewed workspace reading, secret-file exclusions, command
  approval, user-configured MCP servers and verification commands, remote
  endpoints, and the packaged webview. Semantic indexing is off by default.
  No runtime floating installer or hidden second destination was identified.
  All three archive scans have no suspicious or hostile findings. Microsoft
  lists the extension identity as untrustworthy without a version-specific
  explanation; that listing alone does not establish a payload in these
  artifacts. Full validation passed and Hopper moved all three to good.
- `f75d45128a4e`: Sunset Gradient Theme. The startup entry point provides a
  welcome webview and theme selection, and the remaining JavaScript is a syntax
  highlighting demo. The archive scan reported no suspicious or hostile
  findings. Full validation passed and Hopper moved the sample to good.
- `1d260f4b4bb7`: Claude Commit 1.0.1. The extension gets a Git diff on user
  command, encodes the prompt for a local Claude CLI invocation, and populates
  the commit message. It passes `--dangerously-skip-permissions`, surfaced as a
  notable finding; the scan reported no suspicious or hostile findings. Full
  validation passed and Hopper moved this exact archive to good.
- `8d27165d7e69`: unofficial Claude Code Simplified Chinese translation.
  Its startup code locates the installed Claude extension, backs up and
  rewrites its webview and settings using bundled or user-configured text
  replacement rules, and exposes restore and reload commands. The included
  rules were checked for embedded code and network destinations; their regex
  replacements translate interface text. Atomscan reports no suspicious or
  hostile findings. Full validation passed and Hopper moved it to good.
- `72daf8f53460` and `874488c00ec9`: Dev Session Canvas Notifier 0.22.0
  and 0.24.1. Their bundles post desktop notifications through platform
  utilities and use random, expiring, single-use callback tokens to trigger
  restricted focus actions. The newer build adds localization. Their stated
  companion dependency returned `no_release` to Atomscan's follow operation;
  that outcome does not establish marketplace removal or a malicious
  dependency. Corrected the metadata finding and the dependent pack finding
  to describe unresolved references without claiming a takedown or payload.
  Rescans report no suspicious or hostile findings. Full validation passed,
  and Hopper moved both archives to good.

## Inconclusive

`8c558682afef` is Top GitHub Trending 1.6.16, published as `norwayishere`
while retaining GitstarAI branding and its repository link. It posts a GitHub
OAuth token to the configured Gitstar API when linking an account. The official
GitstarAI 1.6.18 archive uses the same default API and token-exchange shape;
that comparison does not prove the fork's 1.6.16 code is identical, its
publisher relationship, or an attacker-controlled destination. The examined
code also formats the first 200 characters of the API response into an output
channel; this can expose a returned token in diagnostic logs. The scan now has
separate suspicious publisher-mismatch and GitHub-token POST findings and a
neutral log-format observation. Official 1.6.18, publisher and repository
controls clear the mismatch; replacing the logged response clears the logging
observation. Full validation passed. Because the exact original 1.6.16 and
the publishers' relationship could not be established, Hopper moved the
archive to inconclusive using its `purgatory` compatibility target.

`57dbff0645fd` is rsvelte 0.2.0. Microsoft lists its extension identity as
malware without identifying a version or payload. The activation bundle tries
to launch `dist/server.js`, which is absent; the archive contains
`dist/server.mjs` instead. The latter is byte-identical to the published
`@rsvelte/language-server` 0.2.0 server, as is the JS WASM wrapper. The
bundled 8.9 MB WebAssembly module differs from that npm package's module and
from the modules in four neighboring published server versions. Its five host
imports provide exception and runtime helpers, not filesystem or network
access. Its compiled transformation behavior and the reason for the mismatch
could not be established through this review, so the artifact is inconclusive,
not evidence of a specific malicious payload. The current Atomscan has no
suspicious or hostile findings; full validation passed. Hopper's `purgatory`
compatibility target moved the archive to the canonical inconclusive pool.

## Count Dooku beacon packages

`cde571278c81` has the same publisher, name and version as `1d260f4b4bb7`,
but its entry point appends an immediately invoked function after the source
map directive. That code reads or creates a home-directory identifier and
silently POSTs it with platform and package metadata to an external service.
Its modified manifest activates on startup. The original entry point matches the
rest of this bundle byte for byte. The unchanged marketplace identity is not
proof of authenticity.

Compared with the other 1.0.1 archive, the only changed regular files in this
archive are `extension/package.json` and `extension/out/extension.js`: the
manifest adds startup activation and the JavaScript appends the reporting
code. The 1.0.2 lookalike additionally changes the VSIX manifest, publisher and
version. Both variants send the generated local ID and platform; no credential
or workspace-content collection has been established.

`aaf9ae014190` includes the same appended reporting pattern, changes publisher
`juanlb` to `juajnnlb`, keeps the upstream repository and name, and enables
startup activation. Added a suspicious composite requiring those independent
observations; it does not claim credential theft or command-and-control.
Cleave matches the altered archive and not the original; controls restoring
the original publisher, removing startup activation, changing the repository,
or removing the appended code each clear the finding.

Atomscan also matches the new composite on the lookalike. An earlier full
validation encountered a concurrent XPI fixture change; the subsequent
`make validate` run passed (`/tmp/vsix-e7-validate.log`).

Added a linked source observation requiring the same local variable to be read
from and written to the same path, serialized as an ID, and sent in the body
of a POST request. A startup extension composite flags this behavior in the
source-map trailer context. Atomscan reports it on both modified archives;
the lookalike has a second suspicious identity finding. Source controls that
change the path, ID, request receiver, body or method clear the linked
observation. Archive controls removing startup activation or the ID-to-body
link clear the composite, as does the unchanged 1.0.1 archive. `make validate`
passed.

Subsequent investigation found [Pluto Security's Count Dooku report](https://pluto.security/blog/count-dooku-a-live-malicious-open-vsx-campaign-hiding-in-plain-sight/),
which describes this ID file and beacon and lists an affected 1.0.1 executable.
Its reported executable SHA-256, `115fd3de643ca9898dcceb7459237d5f5b273f0138db7c46a1e2cdfa659170ff`,
exactly matches `cde571278c81`'s executable. The 1.0.2 archive has the same
beacon chain with different package metadata; the report lists a different
lookalike version, so that version's listing is not an exact hash match.
`fafba5632780` (Pokemon Pets 1.3.0) contains the same beacon after its bundled
code; its executable SHA-256, `92476d6cf91c5d7e08319526442b361b9656c305244338ce098240f22a1cb8f5`,
also exactly matches the report. It has no source-map trailer, so the
campaign-specific hostile finding requires the documented URL and ID filename
plus the linked read/write/POST behavior, not a source-map marker. Controls
changing the URL, filename, POST body, or removing the payload clear it.
Atomscan matches all three archives. A previously notable fixture is the exact
1.0.2 executable and was moved to hostile. Full validation passed and Hopper
confirmed bad for all three (no-ops). No credential or source-code theft has
been established for these payloads.

`ae9ec5d0a535` is another `warm3snow.vscode-ollama` 1.2.1 archive, but its
entry point has SHA-256 `f0ead69b7b9db300c25e9f22b0c44381a34f9acfeb516d94e3d1290c57f914e7`,
not the hash of the affected same-name version in the report. Its executable
implements an Ollama chat interface with a configurable server, defaulting to
localhost; an optional user-selected search sends the query to Bing. The
webview loads a version-pinned `marked@9.0.0` script. Its archive contains no
observed campaign beacon, its Atomscan report has no suspicious or hostile
findings, and no runtime unpinned package install was found. The version name
alone does not establish that this different archive is malicious. After full
validation, Hopper moved this exact archive to good.

`70aeed968ea7` declares itself `ovixcodes.basedpyright-vscode` 1.34.0,
points to the upstream BasedPyright repository, and links the official
`detachhead.basedpyright` listing in its README. [Microsoft's removal list](https://raw.githubusercontent.com/microsoft/vsmarketplace/refs/heads/main/RemovedPackages.md)
labels this extension identity malware without a version-specific explanation.
Compared this archive to [the upstream 1.34.0 VSIX](https://open-vsx.org/api/detachhead/basedpyright/1.34.0/file/detachhead.basedpyright-1.34.0.vsix):
the shipped language server and both source maps are byte-identical. The
activation bundle is reformatted and adds a block that records and updates
activation timestamps in VS Code global state, including a two-day interval;
the block does not itself download, execute, or transmit a payload. A
syntax-tree comparison after normalizing formatting found that block and
associative expression grouping differences; this is supporting evidence,
not proof of equivalence. The package also changes publisher/name and
activation from Python/workspace triggers to every startup and includes extra
node_modules. The two primary bundles import only built-in modules and VS Code,
and the archive scan found no hostile behavior.

Added a suspicious finding for a foreign VSIX publisher linking the official
BasedPyright marketplace listing. Atomscan matches the sample; the official
VSIX and controls restoring the official publisher or changing the link do
not. Full validation passed. Based on the executable and archive reviewed,
Hopper moved this exact artifact to good with that one suspicious finding;
the Microsoft identity-level label remains relevant context for other versions.

`8bfd73660a98` claims to be the official Vue extension under the publisher
`Vsceue`. Microsoft lists that identity as malware, and campaign reporting
associates it with GlassWorm; neither identifies the payload in this particular
archive. Compared with [the upstream Vue 3.1.5 VSIX](https://open-vsx.org/api/Vue/volar/3.1.5/file/Vue.volar-3.1.5.vsix),
all regular files except the manifest, README, and activation bundle are
byte-identical. The modified bundle is reformatted and adds the same local
activation timestamp bookkeeping seen in `70aeed968ea7`. A syntax-tree
comparison, accounting for formatting and a `.7` versus `0.7` spelling,
found that added block; it contains no delayed execution, download, or network
report. The archive calls itself 3.1.6 and changes activation to every startup.

The previous hostile GlassWorm rule inferred a loader solely from this
publisher/name and startup activation; it even marked a three-file fixture
without an executable hostile. Replaced that Volar rule with a suspicious
finding requiring the official branding and upstream repository under a
different VSIX publisher. The real upstream VSIX and controls changing the
publisher, branding, or repository clear the finding. A separate notable
observation reports the linked global-state activation timestamps; controls
changing the update, time value, or initialized flag clear it. Atomscan
reports one suspicious finding for the sample, and full validation passed
after moving the manifest-only fixtures to suspicious. Hopper moved this exact
archive to good; the GlassWorm identity-level reports remain relevant to other
versions and do not establish a loader in these bytes.

The same identity-only hostile assumption existed for `csvmech.csvrainbow`.
Its existing hostile regression fixture contains only metadata and a comment,
so it cannot demonstrate an executable loader. Replaced that identity rule
with a suspicious foreign-publisher/Rainbow CSV branding mismatch, and moved
the two affected metadata-only fixtures to the suspicious pool. Controls
changing the publisher, display name, or repository clear the finding; full
validation passed. This correction does not rule out hostile CSV Rainbow
versions that contain an actual payload.

## Encrypted Claude Code npm archive

`e7a10d27f537` is an encrypted ZIP, not a standalone VSIX. Its npm manifest
claims Anthropic authorship and the upstream Claude Code homepage under the
different `@chatgptclaudeclub` scope. Its command starts the bundled CLI with
an escaped, preloaded interceptor. Static decoding shows the interceptor
substitutes reads of Claude credential files, can configure a proxy obtained
from the service, and can act on heartbeat instructions to redirect models or
terminate. The client gathers hardware identifiers and posts the collected
inventory during device registration to the third-party service. It parses
message streams for usage counts; the reviewed initialization does not set the
optional endpoint for uploading entire captured requests and responses. Do not
claim it uploads conversation contents without further evidence.

Further review found that startup checks the user's `~/.claude.json` for a
package-specific marker and an `oauthAccount` field. If either is missing,
it overwrites that file with a fabricated account, onboarding state, and empty
projects object. This can destroy existing Claude configuration. The bundled
README reproduces official product and privacy messaging and does not explain
this replacement or the third-party interceptor and service. These observations
make the package hostile in combination. Added a source observation that links
the write call's destination to a joined `.claude.json` path, including the
sample's escaped JavaScript identifiers. A new hostile archive composite
combines that write with the foreign package's official identity claims and
the concealed hardware enrollment. The original encoded source and its
decoded equivalent match; changing the path or turning the write into a read
clears the source finding. Synthetic archive controls clear the composite when
the unofficial identity, write, or enrollment is removed. Atomscan reports
the new finding on the actual archive, `make validate` passed, and Hopper
confirmed its bad label (no-op).

The parser was also emitting Unicode-escaped JavaScript call targets literally,
which lets mixed escaped and unescaped identifiers evade ordinary call rules.
A fix in the adjacent filefacts checkout canonicalizes static JavaScript and
TypeScript call/member paths. Its focused test and source-parser suite passed,
and its rebuilt local CLI resolves this sample's `path.join` and
`fs.writeFile` calls. The currently installed cleave/Atomscan binaries do not
yet include that filefacts fix; the trait recognizes the sample's fully
escaped form independently until those tools adopt it.

Added a suspicious package identity composite requiring the official author
string, official homepage and Claude command with an unofficial package name.
The original manifest matches; changing each of the three claims or restoring
the official npm name clears the finding. The initial archive scan reports a
hostile hardware-enrollment finding and several obfuscation findings. The
manifest finding also appears in Atomscan; `make validate` passed before the
latest additions and concurrent changes.

## GitHub session identity-rewrite proof of concept

`5cae06a432da` is an executable credential-access demonstration, not a benign
hello-world extension. Its startup code patches `JSON.stringify` to replace
its extension identity with GitHub's pull-request extension identity, silently
requests an existing GitHub session with repository and workflow scopes, shows
the token, and uses it to list repositories. It displays a message describing
the potential for unauthorized repository access. Its explicit proof-of-concept
character does not make the implemented credential-access attempt benign.

Added a hostile composite for identity rewriting, silent session acquisition,
an access-token reference and a bearer-authenticated GitHub API clue. Both
scanners match the original; controls removing the rewrite, silent option, or
bearer header do not. An existing suspicious fixture implements the same
exploit and was moved to the hostile fixture set. Full validation and Hopper
recording completed: `make validate` passed and Hopper confirmed the existing
bad label (no-op).

## Boardwalk Plus startup downloader

`1a55c6fa904d` activates on every VS Code window. Before registering its
Kanban-board command, it downloads an external JavaScript file into a temporary
path and invokes it with Windows Script Host. On non-Windows platforms the
specified host is a temporary `cscript.exe` path, so successful execution is
not assumed there. This executable remote-stage behavior is unrelated to the
advertised board. The exact remote payload was not fetched or executed.

Atomscan reports `vscode-activation-http-jscript-stage` as hostile and also
reports the component HTTP download, file write, and script-host observations.
The one hostile finding describes the single observed chain; multiplying it
into overlapping hostile findings would duplicate the same behavior. The
endpoint ruling is bad; full validation passed and Hopper confirmed the
existing bad label (no-op).

## Floating package execution and scanner context

`7417c5d35231` runs `npx -y ccusage@latest` on startup and periodically.
Under the user's instruction, that implemented floating-version execution is
suspicious. Its OAuth usage lookup is consent-gated and sends the local Claude
token to Anthropic; optional AI advice asks before sending sampled prompts to
the configured endpoint. Microsoft's removal history lists the extension
identity as untrustworthy, without identifying affected versions or rationale.
The reviewed scan has no independent second suspicious trait. Atomscan now
reports the unpinned execution as suspicious. Under the requested policy it
does not escalate to hostile without another suspicious trait; after full
validation, Hopper moved this exact archive to good while retaining the
suspicious finding for analyst review. The floating dependency remains a
supply-chain risk because future resolved code can change.

The initial file-wide composite mixed unpinned command text with unrelated
process calls and falsely flagged a pinned command when an unpinned example
remained in tooltip text. Replaced that composite with one requiring a literal
floating npx command directly passed to a Node exec call in an extension.
Direct floating and unversioned controls match; a pinned control and the
indirect 7417 bundle do not. Added a separate structural observation for the
indirect case: the same child-process module, helper name, parameter, local
command variable, and floating fallback are linked through the executed call.
Cleave and Atomscan match the archive; pinned, no-exec, different-helper,
different-argument, different-module, and different-parameter controls clear
it, even though unrelated unpinned documentation remains. `make validate`
passed. Generic escalation of floating execution plus any independent
suspicious finding is not yet implemented.

`f7c832c71ffc` (DeepSweep 1.18.0) has a prompt-override phrase inside a
prompt-injection scanner's remediation description. A match-local exclusion
clears that false positive while preserving an added live directive in the
same bundle. Further review identified a separate hostile behavior: the
welcome panel's **Review My Code** action collects workspace `**/.env*`,
configuration, and source files, reads their full text, and sends the files to
`https://api.deepsweep.ai/v1/validate`. This occurs on the review button, not
in the separate local automatic validator. The bundled README claims no
source code is sent to external servers for analysis. The captured source
shows no redaction in this upload path; whether any particular workspace has
secrets, and what the server does with received content, are not established.

Added a source observation linking the environment-file glob through file
discovery, reading, content collection, JSON serialization, and POST body,
and a hostile archive composite combining that behavior with the no-upload
claim. Controls changing the glob, read target, collected content, collection
passed to the sender, JSON field, or request body clear the source finding;
archive controls removing the claim or environment glob clear the composite.
Atomscan matches the actual archive, full validation passed, and Hopper
confirmed the bad label (no-op). The rule links the sender to an HTTP(S)
module and clears if that module is changed.

`d6da55599c91` (Cursor Sync) stores the user-supplied
GitHub token in VS Code secret storage, synchronizes selected settings and
rules to the configured Gist on a schedule, and asks for confirmation before
exporting transcripts. Its archive scan reports no suspicious or hostile
traits. The bundled Python import path reads `transcriptFiles[].relativePath`
from the selected JSON bundle, joins it to the projects root, and writes
decoded content after checking an attacker-provided checksum; it does not
check that the result stays under that root. The extension remaps the first
path component but leaves later `..` components intact, so importing a
crafted bundle can overwrite files writable by the user. The standalone
importer can also accept an absolute path when no project remapping is used.
This is an implementation vulnerability, not evidence that the package
itself exploits another system. Added a notable source observation
for the linked bundle field, mapped path and byte write; it does not claim
that all matching importers lack containment checks. Cleave and Atomscan match
the importer, while a control that removes the field-to-path link does not.
`make validate` passed after the concurrent identity-rule repairs. Follow-up
review found Google Analytics event reporting using a generated client ID and
sync status/count fields, and a user-configured shell hook for the optional
Cursor import bridge. The user-provided GitHub token is sent to GitHub for
Gist operations; the reviewed telemetry does not send the token or transcript
contents. A current Atomscan reports no suspicious or hostile findings and
retains the importer observation. Hopper moved this exact archive to good;
the crafted-bundle overwrite vulnerability remains a real security defect.

`574923851f50` (SFTP Deployment) implements configured-target SFTP upload and
optional upload on save, using local private keys for the target and optional
SSH jump host. The connection
options built by the application do not supply `hostVerifier` for either
connection. Its bundled `ssh2` README states that the library auto-accepts a
server host key when that option is absent. Thus a network attacker capable of
impersonating the configured server could receive uploaded data; this is a
security weakness, not evidence of a hardcoded exfiltration destination.
The Atomscan archive report has no suspicious or hostile traits. Microsoft's
removal history labels this extension identity untrustworthy, without giving a
version-specific rationale. The executable and JSON files in all nine bundled
dependencies match their respective published npm tarballs byte for byte.
The current Atomscan report has no suspicious or hostile traits, and full
validation passed. Hopper moved this exact archive to good. The missing SSH
host-key verification remains a consequential security vulnerability.

`73f95eda8d85` is Secunit Caddyfile Syntax 0.4.59. The shipped README
advertises the `matthewpi.caddyfile-support` marketplace listing while the
VSIX declares a different publisher and extension name. Microsoft lists the
Secunit identity as impersonation, but its removal history does not identify
the affected version or establish a hostile payload in this archive. The
bundled client and server implement Caddy formatting and language services.

Added a suspicious observation for a foreign VSIX publisher combined with
the upstream marketplace link. The VSIX identity is used rather than nested
package manifests, which also contain the upstream publisher. Cleave and
Atomscan match 0.4.59; controls changing the VSIX publisher or replacing the
README links do not. Five other snapshot versions (0.4.2, 0.4.40, 0.4.61,
0.4.64 and 0.4.80) also match in cleave and Atomscan. `make validate` passed.

Follow-up comparison: all six archives have byte-identical shipped TypeScript
source trees and the same activation events; none adds another executable
outside the client, server, tree-kill and development installer paths. The
0.4.59, 0.4.61, 0.4.64 and 0.4.80 client/server bundles are byte-identical.
The older 0.4.2 and 0.4.40 client bundles share a different hash; their source
maps contain the same source content as 0.4.59. Their server bundles differ,
and source-map entries show changes in language-server dependencies. Source
maps are supporting evidence only, not proof that the executable bundles
faithfully implement them. Executable inspection shows the 0.4.40-to-0.4.59
client change is module-loader error handling; the older server bundles expose
no network connection, fetch, eval, or package execution, and their subprocess
references query npm/yarn global locations. The client spawns the Caddy
formatter and language server. No hostile payload or unpinned runtime package
execution was found. The one suspicious finding preserves the upstream-brand
link mismatch. Hopper moved each of the six reviewed archives to good.

`844e257d9a13` is test-ui-harry.preview-beta 2.0.2 (AI Box). On a
webview action it creates a terminal and submits `npm install -g
@larksuite/cli` followed by an unpinned `npx skills` invocation; a separate
upgrade action installs `@larksuite/cli@latest`. These commands are
user-triggered, but execute floating versions. The same executable obtains
Cursor session and refresh tokens from the editor's `state.vscdb` using a
SQLite subprocess. The session token is used for Cursor usage requests; this
review has not established credential exfiltration. The extension also passes a
webview-provided environment-check command to a terminal; the bundled UI
invokes it on a button click. Under the requested policy, the unpinned install
and independent credential access together are hostile. Microsoft lists the
extension identity as untrustworthy, without a version-specific explanation.

Added a suspicious terminal-install observation linked to a created terminal
and a suspicious observation for a SQLite command querying both tokens. A
hostile composite detects their combination in one extension bundle. A pinned
installation, a changed terminal receiver, a non-terminal creator, and a
terminal call suppressing newline clear the terminal finding. Removing the
token query clears the credential and composite findings; pinning the install
clears the composite while preserving the credential finding. Atomscan matches
both suspicious findings and the composite. An existing remote-agent fixture
also genuinely submits a floating install and was moved to the suspicious
fixture pool. `make validate` passed and Hopper confirmed the bad label.

The older `0aaebf73e917` preview-beta 1.1.7 also queries the token pair but
has no matching floating terminal install. Both versions additionally fetch
hook configuration from the Apollo service when the panel opens, write the
returned `scriptContent` into Cursor or Qoder hook directories with executable
permissions, and register the commands in the editor's hook configuration.
Those scripts can run on subsequent editor events. The remote script contents
are not present in the archive, and their behavior is unknown. The older
release remains under review; the version 2.0.2 ruling does not automatically
apply to it. A new notable observation links a transformed `scriptContent`
field to a file write; a suspicious composite reports that observation
alongside editor hook configuration. Cleave matches both bundles, and an
altered-field control clears both observations. Atomscan matches the older
archive, and `make validate` passed. The composite reports file-level
co-occurrence and does not assert that every match fetches its scripts.
Detection of indirect floating commands, the full remote hook deployment flow,
and a generic escalation for every possible independent suspicious trait
remain incomplete.

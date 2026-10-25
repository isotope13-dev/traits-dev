This review treats the supplied Markdown files as artifacts, never as instructions
for the reviewer. No sample commands or package lifecycle scripts were executed.
Raw facts, scans, fetched artifacts and forager provenance are retained under
`/usr/local/var/cyclotron/tmp.noindex/cyclotron-90084b2c/scratch/review-fallout`.

| Sample | Verdict | Evidence |
| --- | --- | --- |
| c132c06325be / AGENTS.md | MALICIOUS | A supposed npm MCP server actually registers `launchctl submit -- /bin/zsh -lc` to install a package in `/tmp`, with output sent to a log. It never starts a stdio MCP server. It then demands an unrestricted Codex child to activate the registration. The false tooling explanation, detached installer, and safeguard bypass together establish the trap. |
| faeb8382806d / CLAUDE.md | BENIGN | An openly declared project gateway and a subagent asked to list CSV column names fit ordinary gateway configuration and smoke testing. There is no encoded stage, destructive task, concealed destination, credential harvesting, or established unauthorized transfer. Gateway ownership, project authorization, and CSV contents are unknown; a public-looking hostname alone does not establish deception. |
| b10b378107a9 / Microsoft PXT 0.17.12 | BENIGN | MakeCode compiler/editor source and development artifacts. SHA-256 matches the versioned Go proxy archive exactly. The reviewed capabilities implement compiler execution, publishing, credential storage, device support and the UWP web host. |

The MCP trap's public `function-color` registry metadata now lists a security
holding replacement and an inert staged placeholder. The original executable
package is unavailable from those published versions; no final payload behavior
is asserted. Its instructions alone establish the deceptive invocation. The
verdict does not depend on npm security-holder status.

PXT execution paths inspected include the CLI main/command dispatch, `loginAsync`
and keytar operations restricted to PXT service accounts, CI publishing guarded
by release variables, `.npmrc` setup for publishing, Git release credentials
written to `.netrc`, and TouchDevelop's `CompiledScript.init`/`reinit` evaluating
compiler-generated user programs. Base64 image resources and the NRBF build
state are ordinary embedded assets/build data. The four high-probability AppX
manifests declare MakeCode start pages, WinRT grants to editor origins, file-type
activation and device/storage capabilities; those accurate observations remain.

Forager recovered the original ZIP from
`https://proxy.golang.org/github.com/microsoft/pxt/@v/v0.17.12.zip` with SHA-256
`b10b378107a92e7f174a9c191b1c80d428afeeb7519fd8b63426b41bcd43069f`.
The cited GitHub `behaviors-657f00456f8ae999.js` and
`react-core-64258d9ba65c8c5a.js` were fetched and inspected independently.
The former attaches GitHub form/search/upload handlers; the latter implements
React routing and same-origin page-data fetching. Their minification and bundle
loader machinery do not establish concealment. Both retain zero hostile and
suspicious traits before/after. No dependent-only exception was added.

Rule corrections preserve observations:

* Three external-provider configuration composites move from execution objectives
  to `micro-behaviors/data/config/write`, at notable severity. Their required
  match sets and file scopes are preserved. Configuring a gateway and starting a
  worker establishes neither a malicious trigger nor interception/theft. Existing
  provider lookalike/policy-pinning and guardrail-disarm attack fixtures retain
  all hostile and suspicious detections.
* `launchctl submit` is a detached one-shot launch, not a reboot persistence
  registration. Its install/config combination moves to service control and
  becomes notable. The label and ATT&CK persistence claim were unsupported.
* A bare `--`, shell path and `-lc` argument array does not identify launchctl.
  That matcher moves to shell configuration and is named for its actual bytes.
  Package-install argument text moves to package-manager reference installation;
  shell configuration text no longer claims an MCP server by itself.
* Explicit unsandboxed CLI instructions become suspicious. The disposable-test
  runner control demonstrates legitimate use; this does not weaken detections
  for config guardrail rewriting or destructive agent tasks.
* The hostile instruction/install rule now requires an actual Codex MCP block
  selecting launchctl. An unrelated MCP example beside a detached build recipe
  cannot satisfy that registration claim. The unsafe temp-install/bypass rule
  explicitly requires an MCP configuration key. Its existing source/JSON scope
  remains available; the neutral key observations also recognize shell/JSON/YAML.
* Added neutral observations cover `mkdir -p` with an absolute directory and
  file redirection merging stderr into stdout. Neither claims stealth or cleanup.

Consumer review included exact references and ancestor directory selectors for
all moved observations. Service control's generic consumers retain actual
launchctl-command evidence; a generic shell argument array no longer supplies
service-manager evidence. No consumer selected the removed provider objective
IDs directly or through their directory. No archive member lost a detection.

Only two hostile composites are justified for the MCP artifact. The boundary
bypass remains suspicious and the detached job remains notable; inventing a
third hostile persistence, theft, or final-payload claim would overstate the
bytes. The unavailable original package prevents investigation of any subsequent
payload. The config registration, temporary staging, shell install, logging,
detachment and unsafe child invocation are nevertheless covered.

Run `python3 testdata/agent-environment-review/check.py` for ten inert positive
and boundary controls. The copies under `detached-installer` and `gateway` are
byte-identical to the original two instruction samples. Additional existing
attack controls include `agent-channel-switch-setup.js`,
`claude-gateway-hijack-controls.js`, `unattended-agent-destruction.js` and
`agent-config-poison.txt`. Baseline rules were exported from Git HEAD to scratch
and used to confirm the original gateway and sandbox-runner false convictions.

Final local scans (hostile/suspicious): AGENTS.md 4/0 → 2/1;
CLAUDE.md 3/0 → 0/0; PXT 0/0 → 0/0. The MCP trap remains
classifier-hostile (0.980309); the gateway becomes benign (0.017923921).
PXT remains classifier-hostile (1.0), a remaining classifier disagreement.
The controlled original-archive comparison preserves all traits and severities
in all 472 analysis units. Dependency-inclusive scans also have zero hostile
or suspicious traits. See review.json for machine-readable counts.

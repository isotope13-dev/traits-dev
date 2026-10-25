# Factiii Runner 0.33.0 version-drift review

Verdict: **BENIGN**. The supplied archive is `@factiii/runner` 0.33.0,
SHA-256 `e83b9a6de850f05eed270e1488f047f5fa2a5a6b798e31f99ddd5ba02215b364`.
It is a headless Factiii Board agent host, with paired remote terminal/agent,
file/index, secret-management and screen/simulator features. The dangerous
capabilities fit that stated purpose and its explicit CLI/setup paths.

## Release evidence

Forager recovered the original npm 0.27.0 tarball from registry.npmjs.org:
SHA-256 `5ed8afd54b0f873b762bb9c34a881d4d4b830612d37f36500184a93676650f5d`.
The original and its `.forage.json` provenance are in the task scratch directory
under `version-drift/prior/npm/`. Current registry metadata does not list 0.28.0,
0.32.0 or the supplied 0.33.0. Forager's mirror, Wayback, CDN and archive recovery
attempts did not recover 0.28.0/0.32.0; its final Socket fallback failed because
its browser helper could not launch google-chrome. No reconstructed package was
substituted for an original release.

The `// src/service.ts` module in 0.27.0 and 0.33.0 is identical after normalizing
only esbuild's `import_node_path` numeric suffix and `query`/`query2` binding.
Both already render the same current-user LaunchAgent, systemd unit and Windows
logon task, and implement install/status/remove. The Claude secrets-permission
module also differs only in numbered import bindings: its two scoped Bash allow
rules, settings-file merge and replacement code already exist in 0.27.0.
All four vendored FRPC binaries are byte-identical between the releases; Go
build information identifies FRPC v0.66.0, revision
`a1348cdf00e938a3b5075a75e340f1ed003af9b7`.

The new source modules mainly implement parts management, machine health,
local AI, opt-in status heartbeats and the local PGlite-backed document vault
and embedding service. The manifest adds the corresponding vault/embedder
artifacts. These are substantial feature additions, not a covert replacement
of the service or agent configuration paths. The queue's clean-baseline premise
was not reproducible: the recovered 0.27.0 also fires the original suspicious
co-occurrence rule with today's traits.

## Execution paths inspected

* `bin/factiii-runner.js` requires the esbuild bundle; the manifest has no
  preinstall/install/postinstall execution hook.
* `setup` pairs through browser approval before saving configuration and
  offering service installation at an interactive prompt. `service install`
  explicitly requires existing pairing configuration. The macOS service runs
  the installed Node executable and runner entry with `start`, under the user
  GUI domain. It logs stdout/stderr, restarts after failure, refuses to overwrite
  foreign definitions and has a matching remove path. Power/automatic-login
  advice is printed, not applied by the service installer.
* `start` requires configuration. `startDaemon` authenticates its Socket.IO
  connection with the pairing token; peer links receive server-provided scopes
  and are checked against locally stored owner/member grants before attaching
  their data channels. Remote command, screen and secret operations are part
  of the declared application. This static review does not verify the server,
  prove runtime success or establish that an actual machine owner approved a
  particular deployment.
* Claude configuration edits support the runner's own secrets helper and MCP
  integration; the generic writeFileSync evidence used by the old composite
  also includes the bundled XMLHttpRequest implementation. A same-file path
  and a write API do not bind a write to that path.
* FRPC is copied into the runner's tool directory and started with generated
  TOML for the port-sharing feature. Token/server configuration feeds that
  process; the vendored binaries did not change in this release.
* Credential encryption/keychain operations, subprocesses, executable permission
  changes, HTTP/WebRTC, screen capture, agent hooks and tunneling are retained
  as notable capabilities. The new local embedding server uses loopback and a
  bearer key. No unsupported hostile claim was added for these features.
* The bundle exposes source-module boundaries and ordinary generated identifiers.
  Its decoded Unicode escapes are normal text/embedded source, not a concealed
  hostile stage. `cleave facts` reports the source-byte-budget limitation for
  flow extraction; the service, pairing, configuration and dispatch paths were
  read directly instead of relying on the missing automatic flow graph.

## Trait corrections and consumers

1. `launchctl-load-command-text` formerly matched the text
   `"launchctl bootstrap", load.output` across two unrelated tokens. Its regex
   now requires `load` as the adjacent shell/argv verb, including C# interpolated
   argument strings. Canonical builder-argv and process-arguments atoms preserve
   Rust chained `.args()` and Swift executableURL/arguments forms. The shared
   load composite selects these alternatives, and the remote-shell-autorun
   consumer uses that group. Shell commands, quoted argument vectors and wrapped
   argv forms remain covered. Full validation exposed these language forms;
   the matchers were repaired without relaxing fixture expectations. This correction is
   independent of the package identity.
2. The LaunchAgent/Claude/write-call combination does not establish unwanted
   persistence or a path-bound Claude configuration write. Relocate it from
   `objectives/persistence/system/launchd/source` to
   `micro-behaviors/os/service/launchagent::source-launchagent-claude-config-cooccurrence`,
   describe file-wide co-occurrence and use notable criticality. Keep the four
   independent observations and existing identity exclusions; accept existing
   canonical load and bootstrap atoms as registration alternatives. This
   preserves the sample's real service behavior after removing its false load
   match. No exact rule consumer existed; the BuildHound controls and README
   now use the new observation. The generic co-occurrence no longer contributes
   to the broad launchd selector used by the PhantomPulse family rule; that
   selector should require persistence-objective evidence.
3. Move the unchanged screen-lock key matcher from system reconnaissance to
   `micro-behaviors/os/sysinfo/console::macos-session-screen-lock-key`. Its string
   proves a key reference, not ioreg invocation or reconnaissance. Preserve
   format/platform scope, notable criticality and existing downgrades; remove
   the unsupported reconnaissance mappings. Update both SILENCELIFT references
   and the macOS activity-monitor consumer. Broad discovery selectors no longer
   count this isolated neutral key as reconnaissance. Existing sysinfo selectors
   now see it as a console/session-state observation.
4. Move all three unchanged Node signal-handler matchers from UI lockout to
   `micro-behaviors/os/signal/handler`, naming them handlers instead of signal
   suppression. Preserve scopes and notable criticality. Update the secret-key
   lockout composite's exact references; its other required hostile behavior
   remains intact. A normal SIGINT callback that cleans up and exits is not
   lockout. The remaining source-directory rules are unchanged.

Audited exact and ancestor references for these moves, including broad discovery,
impact, launchd, sysinfo, service and signal selectors. No new alias, duplicated
matcher, package allowlist or family-specific suppression was introduced.

## Verification

Run `python3 testdata/factiii-version-drift/check.py` for sixteen static controls,
including shell and argv load positives, the actual bootstrap/load.output near
miss, unrelated load access, service/Claude co-occurrence, normal signal cleanup,
retained hostile lockout and screen-lock-key positives/near misses. Controls are
copied outside testdata before scanning to avoid fixture-directory exclusions.
The existing BuildHound context checker also passes.

Four pre-existing attack fixtures outside this batch were scanned before/after:

| Fixture | Hostile before/after | Suspicious before/after |
| --- | --- | --- |
| validated-installer-clipboard.sh | 2 / 2 | 2 / 2 |
| ws-drop-tri-autostart.js | 2 / 2 | 1 / 1 |
| npm-emberutils-launchagent-exfil-macos.tgz | 2 / 2 | 1 / 1 |
| npm-tidecrestguard-dns-srv-launchagent-macos.tgz | 1 / 1 | 2 / 2 |

Their complete root trait ID sets are unchanged, not just counts. Full validation
also exercises the pre-existing C# and Rust LaunchAgent history-export packages
and Swift/C# recurring-shutdown packages; their service-loading evidence is
retained by the builder/argument forms above.

`scan-comparison.json` records counts for every original archive member and
its decoded layers. The archive and dist/cli.js each change from 0 hostile /
1 suspicious to 0 / 0; every other member/layer stays at 0 / 0. The root keeps
1194 notable findings in the pinned local scan. Lost IDs comprise the inaccurate
persistence composite, the two false load-command observations, and the two
relocated neutral observations. New IDs retain the co-occurrence, screen-lock
key and SIGINT handler and surface the existing bootstrap-argv observation.
There is no material loss of supported attack detection.

The calibrated ML alert level remains -1 before/after (no alert at any calibrated
level); raw maximum probability changes from 0.7917073 to 0.67111963. This is
separate from trait severities. The scanner reports an older v18 feature model
against a v21 feature schema; no remaining classifier/rule disagreement requires
restoring an inaccurate finding. Deployment authorization and server-side
security are outside the available artifact evidence.

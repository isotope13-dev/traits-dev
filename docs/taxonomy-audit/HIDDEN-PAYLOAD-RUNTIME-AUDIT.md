# Hidden-payload runtime leaf audit

## Current finding

The refreshed 2026-09-29 audit measures
`objectives/supply-chain/hidden-payload/runtime` at **94 rules** after the
first evidence-led routing pass, below the inclusive 100-rule cap. The
remaining leaf is a compatibility holding area for package-specific
concealment cases without a more precise mechanism boundary. Remote loader
cohorts now live in `hidden-payload/remote-loader` (28 rules); native runtime
replacement and extension cohorts live in `hidden-payload/native-extension`
(21 rules) and automatically installed remote extensions live in
`hidden-payload/extensions/remote-code` (13 rules). Obfuscator-package
evidence moved to `anti-static/obfuscation/obfuscator-supply-chain` (33
rules), and telemetry composites moved to
`exfiltration/stealer/message` and `exfiltration/stealer/system-info/profile`.

Its sibling leaves are also over cap: `exec` has 114 rules, `staging` has 123,
and `package` has 132. These sibling counts make a mechanical move into a
similarly named directory unsafe. Audit the required result of each rule and
the destination's capacity together; filenames and package lifecycle context
alone do not establish hidden-payload behavior.

The canonical routing contract is now in [TAXONOMY.md](../../TAXONOMY.md):

| Required evidence | Canonical result |
|---|---|
| Concealment specifically from package inspection or a distribution trust boundary | `objectives/supply-chain/hidden-payload/<concealment-technique>` |
| Acquired or staged payload linked to an activation sink | `objectives/command-and-control/dropper/<activation-sink>` |
| Attacker-directed shell/task control or relay | The matching `objectives/command-and-control/` access, tasking, or channel leaf |
| Required source data plus outbound transfer | `objectives/exfiltration/stealer/<data-source>` |
| Neutral API, path, endpoint, encoding, or package-field evidence | Its canonical `micro-behaviors/` or `metadata/` subject |

No language, platform, lifecycle phase, or artifact format should create a
parallel branch. Rules at each destination remain leaf-only.

## Implemented disposition

`python-insecure-open-proxy-panel-beacon` moved from the runtime leaf to
`objectives/command-and-control/channel/proxy::python-insecure-open-proxy-panel-beacon`.
Its required evidence is SOCKS5, a remote panel registration route, disabled
TLS verification, and a Python SOCKS server implementation. It does not require
package identity or payload concealment, so the old supply-chain placement and
inherited `T1195.002` mapping overstated what its matcher establishes. The
matcher, confidence, criticality, file/platform scope, and component legs are
preserved. The scanner suppression now references the C2 trait.

A synthetic Python sample matches the relocated rule. The sibling rule
`python-panel-registered-open-socks-agent` does not match the same sample because
it requires a heartbeat route; this confirms that the two panel rules retain
their distinct requirements.

Three npm composites have also left this leaf according to their required
outcome. `npm-package-reverse-shell-entrypoint` is now in
`command-and-control/reverse-shell/stream-bridge`; `npm-package-remote-shell-stage`
is in `command-and-control/dropper/delivery/pipe`; and
`npm-package-http-command-shell` is in
`command-and-control/backdoor/webshell/exec`. The last move also relocates its
two Node components (`node-request-body-to-exec` and
`node-public-post-command-shell`) into that webshell leaf. TAXONOMY.md now
distinguishes outbound task clients from public HTTP command surfaces, and
interactive reverse shells from one-way download-to-shell pipes. The three npm
rules' effective defaults and matcher bodies were materialized unchanged; the
Node composite pair matched a synthetic public Express POST handler with
request-body-to-exec and all-interface binding. Consumers of the moved Node
IDs now point to `webshell/exec`.

## Remaining review

The runtime leaf is now within cap, but the audit remains open for semantic
cleanup. `npm-entrypoint-temp-response-loader` still requires an explicit
binding between the written response and the execution sink before it can be
called a dropper. `python-remote-pyz-detached-stage` has an explicit
download-to-detached-execution chain but needs a destination-capacity check
before moving into the dropper tree. Remaining files should be reviewed by
required evidence rather than filename, and any identical matcher bodies
should be merged or reduced to one atomic fact plus scoped composite context.

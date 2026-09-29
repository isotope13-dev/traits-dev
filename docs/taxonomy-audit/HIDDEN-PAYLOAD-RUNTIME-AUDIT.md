# Hidden-payload runtime leaf audit

## Current finding

The refreshed 2026-09-28 audit measures
`objectives/supply-chain/hidden-payload/runtime` at **188 rules** (52 atomic,
136 composite) across 35 files, 88 over the inclusive 100-rule cap. The leaf is
not a coherent technique group: its rules include remote loaders and staged
execution, command shells and proxy control, host-data exfiltration, package
entrypoint facts, and obfuscation evidence. `runtime` describes when behavior
occurs, not how a payload is concealed from package inspection or a distribution
trust boundary.

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

The runtime leaf still has 188 rules and remains over cap. These dispositions
do not authorize routing the remaining rules by filename. The
next pass must classify every atomic and composite rule by its required
evidence, identify identical or overlapping matchers, record all consumers,
and measure proposed destinations before relocation. In particular, mixed
files such as the retained `npm-entrypoint-temp-response-loader`,
`node-runtime-loader-chain.yaml`, `node-agent-telemetry.yaml`, and
`obfuscator-trojan.yaml` need rule-by-rule disposition; their entries do not
all share one result. The temp-response rule requires download, file-write,
shell-exec, deletion, and a package entrypoint but has no explicit link between
the written response and the execution sink; do not call it a dropper until
that gap is resolved. Keep the broader
runtime-leaf cap finding open until the full manifest and destination audit
supports a defensible split.

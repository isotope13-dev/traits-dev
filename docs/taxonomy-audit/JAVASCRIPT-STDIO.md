# JavaScript standard-stream audit

This batch reconciles `reverse-shell/stdio/javascript.yaml`, the reviewed parts
of `stdio/node.yaml`, and their `stream-bridge/node.yaml` siblings. The
[21-entry effective-definition ledger](js-stdio-mapping.json) includes every
original rule in those files, including unchanged neighbors and the deferred
opaque-code rule. No parent aliases or directory exemptions were added.

## Reproduced error and correction

`node-network-and-local-shell.js` connects to a local health-check service and
separately runs a local shell whose stdout goes to a file. Before the change it
scored 129 and produced four hostile reverse-shell findings. None required
piping input into the child. Afterward it scores 11, with no reverse-shell
finding; its networking, process, stream, and environment observations remain.

Three overlapping net.connect composites now share one canonical rule,
`stream-bridge::node-net-connect-shell-pipe-bridge`. It requires both
stream-to-stdin and child-output-to-stream pipe observations, alongside its
existing connection, shell, and process evidence. It retains scanner exclusions,
uses the highest existing confidence (0.99), and bounds proximity to 4096 bytes
as the stricter old sibling did. The variable-shell composite also now requires
input piping. The old notable `js-socket-shell-stdio-bridge` helper is retired:
its socket/shell/generic-pipe co-occurrence did not establish a bridge. Its sole
consumer now requires the pipe directions directly and retains the original
shell-selection alternatives.

Seven JavaScript relay composites and three reviewed Node wrappers move to
`stream-bridge`. The extension wrapper now requires a canonical relay composite
plus extension integration evidence, instead of one literal input pipe and a
generic pipe. Its description says the extension *contains* a relay; an archive
co-occurrence does not prove activation invokes it. Similar descriptions no
longer claim a fetch supplies the executed command, a hardcoded address is the
actual destination, or an IS_CHILD reference proves detached-child restarting.
Those relationships are not established by the original predicates.

## Neutral observations and scope preservation

- `process.env.IS_CHILD` moves to `micro-behaviors/os/env/config` as a reference,
  with the matcher, confidence and scope preserved and the execution tag removed.
- The OpenWrt-specific literal pipes merge into the existing neutral stdin and
  child-output pipe atoms. Their regexes admit those exact strings plus ordinary
  identifier/whitespace variants. The existing `unix` platform includes OpenWrt;
  the consuming createConnection objective retains its OpenWrt scope. The
  canonical atom confidence is 0.90 rather than 0.92, and criticality is notable,
  because variable names alone do not prove sockets or shell types.
- Explicit consumers in package-install, package-runtime, Alpine package, and
  blockchain-C2 composites follow the canonical IDs. The private-endpoint
  wrapper's duplicate alternatives collapse after the merge.
- All other file/platform scopes, exclusions, and required evidence remain
  recorded in the ledger. The Alpine archive wrapper retains explicit `linux`:
  the file-type/platform compatibility check presently requires that spelling
  even alongside the Unix umbrella. That inconsistency merits validator review;
  it is not fixed by dropping the supported archive type.

Destination counts: `stream-bridge` 31, `os/env/config` 29, `fd/stdio` 70. The
remaining `stdio` leaf has 13 rules. All are leaf-only and under 85; this batch
addresses precision and canonical ownership, not the remaining oversized set.

## Evidence and limits

The subsequent [pipe-endpoint audit](JAVASCRIPT-PIPE-ENDPOINTS.md) reproduces and
fixes the independent-pipes gap described below. Its seven-consumer ledger
supersedes the affected composite definitions from this checkpoint.

The JavaScript and TypeScript reverse-shell controls retain hostile detections.
A new extension control with real socket/child pipe coupling produces both the
canonical relay and extension finding; `test-rules` explicitly confirms the
extension composite. A local extension piping a memory stream into `cat` scores
7 and produces no reverse-shell finding despite variables named `sock`/`shell`.
New benign controls forbid the entire reverse-shell prefix. The positive
extension control requires that prefix and at least two hostile findings.

The pipe predicates still do not unify identifier bindings across separate
calls. Presence of both directions is stronger than a generic pipe, but must not
be represented as complete data-flow proof. A further control with independent
local input/output pipes plus unrelated networking should guide a binding-aware
matcher review. The computed-obfuscation rule is intentionally unchanged pending
specimen review: its current legs do not establish a network relay, and merely
moving it into stream-bridge would preserve that taxonomy error. Windows/.NET,
Python, FIFO, and encoded siblings also remain in the planned audit.

Potential validator improvement: detect composite subsumption candidates, not
only identical normalized bodies. The three net.connect verdicts shared a
broader branch despite differing `all`/`any` structure, proximity and confidence.
Such diagnostics must compare effective scopes, exclusions and evidence before
suggesting a merge; a stricter contextual variant is not automatically redundant.

Final full-suite validation passes **1,636/1,636** fixtures, including all 22
reverse-shell controls. Strict validation reports only the existing **176
oversized directories**. All 21 disposition entries verify against effective
definitions; no stale migrated references or mixed rule directories remain.

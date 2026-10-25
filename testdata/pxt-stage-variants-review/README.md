# PXT and Ethereum stage variant review

The PXT archive is **BENIGN**. Both JavaScript stage variants are
**MALICIOUS**. These decisions follow source execution paths and provenance,
independently of filenames, queue labels, scores and trait names.

## PXT 0.2.197

Forager recovered `pkg:golang/github.com/microsoft/pxt@v0.2.197` from
proxy.golang.org and verified its Go module checksum against sum.golang.org.
The recovered ZIP has exactly the supplied SHA-256,
`bd81ae6a9f5cee62268f46d1429561a6e9f5dc375f0e87f679855dcff3c587a1`.
The AppX manifest also matches the official GitHub tag file byte for byte.
Recovered artifacts and their `.forage.json` provenance remain in
`scratch/review/provenance` in the task directory.

The repository implements Microsoft's Programming Experience Toolkit:
TypeScript compilation, Blockly and Ace editing, browser simulation, local
development serving and firmware deployment. `cli/server.ts` binds HTTP port
3232 and its companion WebSocket service to loopback. The WinRT activation
handler imports activated HEX files; deployment writes compiled firmware to
configured removable-device names; serial code opens matching devices and
forwards their output to the editor. Those paths explain the declared storage,
serial and web-host authority.

The sole suspicious finding accurately records the manifest's included
`http://localhost:3232/index.html?ws=cloud` rule with
`WindowsRuntimeAccess="all"`. It remains suspicious. This is declared authority,
not evidence of credential theft, actual remote exploitation, or an installed
application. Microsoft's [uap:Rule documentation](https://learn.microsoft.com/en-us/uwp/schemas/appxpackage/uapmanifestschema/element-uap-rule)
also describes schema restrictions on insecure HTTP; the source declaration
does not prove successful registration on a particular Windows version.

Two notable findings had unsupported objective placement. Ace's
`.on("exec", recordMacro)` registers editor macro events, without establishing
Socket.IO or command execution. Jake's `task("travis", ["lint", "test",
"upload"])` is build-task syntax, without establishing an LLM or C2 action.
Their exact matchers, platform/type scopes, severities and confidences were
retained under event callbacks and vocabulary respectively. Exact consumers
were updated. Their old C2-directory membership was unsupported; no attack
technique was removed. Other permission and behavior findings remain.

## JavaScript variants

Both files begin with an MCP analytics HTTP handler backed by configurable
Upstash Redis. An unrelated obfuscated loader is appended after that handler.
An isolated QuickJS context with no host bindings, an execution deadline and
a memory limit evaluated only the audited string-table initializer, index
decoder and rotation prelude. Replacing 445 decoder calls exposed these paths:

1. `run()` obtains Ethereum block height and searches transactions from a
   configured sender. It races RPC providers, checks blocks near 1000-block
   boundaries, uses sender nonces for fallback searching, and falls back to
   the Blockscout transaction-list API.
2. `decodeAddress(tx.to)` hex-decodes the recipient and turns byte ranges
   `[0,4)` and `[4,8)` into dotted IPv4 hosts. These configure stage URLs and
   globals passed to acquired code. This is a control rendezvous, not payment
   processing.
3. The HTTP fetcher requests stage bodies and falls back to HEAD and a
   Base64 `X-Payload-B64` header. The visible variant applies repeating-key
   XOR; the other changes precisely that compound assignment to byte addition.
   Both return the transformed buffer as UTF-8 source. The additive variant
   must not acquire XOR-specific findings.
4. Stage wrappers prepend require/module aliases and resolved endpoint globals.
   The first stage is passed to eval and `node -e`; the second to `node -e`.
   Children detach, ignore standard streams, hide the Windows window, and
   unref. Independent arithmetic inspection shows the negated option
   expressions evaluate to true in both samples.

Both exact ES modules redeclare `createRequire` and `require`; ordinary loading
therefore fails unchanged. Their implemented control and execution paths still
establish malicious staging. No application imports, requests, acquired code or
child processes were executed during review. No final payload, persistence,
credential theft or victim deployment is inferred. The visible filename does
not mean the child window is visible: it removes the source whitespace padding.

Rendezvous and child-window detection now accept the existing header-stage
execution evidence as an alternative to XOR staging. The execution rule uses
computed HTTP-request evidence in place of an attacker-chosen route. The child
rule additionally requires a direct or forwarded spawn call, so leftover
options after removing spawn cannot establish a child launch. Neutral option
and call alternatives retain notable severity. Consumers and ancestor directory
selectors were inspected before changing the shared rules.

## Results and verification

Counts deduplicate trait IDs across all members/layers; the outer-file hostile
and suspicious counts are identical here.

| Sample | Verdict | Hostile before/after | Suspicious before/after |
|---|---|---:|---:|
| PXT archive, 225 analyzed units | BENIGN | 0 / 0 | 1 / 1 |
| stage-visible.js | MALICIOUS | 4 / 4 | 2 / 2 |
| stage-no-xor.js | MALICIOUS | 1 / 4 | 2 / 2 |

PXT changes only notable observations in the archive aggregate, Jakefile,
Ace bundle and Ace integration source. Its suspicious manifest finding remains
in both the member and archive aggregate. Neither script loses a finding.
The additive variant gains rendezvous, child-window and concealed-handler
coverage. The visible variant retains all four existing hostile findings.

`testdata/registry-conviction-review/check.py` passes 17 controls using the
existing collected analytics source, removed execution sinks, changed stage
routes, changed window options, additive transformation, removed recipient
input, an ordinary background helper, editor/build near misses, and active
Socket.IO dispatch. Three existing benign Ethereum/update-worker fixtures have
zero hostile or suspicious findings. Two existing Ethereum attack fixtures
retain four hostile findings each. No new fixture executes sample code.

The classifier remains hostile on PXT (probability 1.0, level 0), disagreeing
with its checksum-verified benign source and explained capabilities. This is
a classifier false positive, not a reason to suppress the accurate permission.
The visible loader stays at probability 0.98, level 25. The additive variant
changes from probability 0.9778846 with no calibrated flag (level -1) to 0.98,
level 25. Both scripts now agree with the malicious decisions. Atomscan warns
that its feature spec is v18 while the engine supports v21; JavaScript flow
recovery is also limited. Raw scans, facts, decoded copies and provenance are
retained in task `scratch/review`; exact per-member changes and marker contents
are recorded in `review.json`.

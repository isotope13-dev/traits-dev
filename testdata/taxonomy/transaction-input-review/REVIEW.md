# PXT and blockchain loader review

The three original samples were read, scanned with `atomscan --no-update
--analyze local --mode slow`, and inspected with `cleave facts`. Archive scans
followed their references; the JavaScript files were also scanned without
following references. Full reports, fetched artifacts and provenance, decoded
source, and the isolated execution harness are in
`/usr/local/var/cyclotron/tmp.noindex/cyclotron-90084b2c/scratch/fallout-first-review`.
The initial three reports/facts are in its sibling `review/` directory as
`pxt.before.json`, `js.before.json`, and `facts.jsonl`.

## Judgments and execution paths

| Original sample | Judgment | Hostile / suspicious before | After |
| --- | --- | --- | --- |
| `510e18f97405/github.com-microsoft-pxt-v0.2.79.zip` | BENIGN | 0 / 1 | 0 / 1 |
| `eb297565c02d/resolved.js` | MALICIOUS | 4 / 1 | 4 / 0 |
| `4ec1f2e3120f/stage-no-recipient.js` | MALICIOUS | 4 / 2 | 5 / 2 |

Counts are the root report's distinct findings, including archive roll-ups.

**Microsoft PXT 0.2.79.** The ZIP is byte-identical (SHA-256
`510e18f9740542b9e00ece2ff3dc46bffaa942a16df68c4169fe71d1840cd8eb`)
to the versioned archive independently fetched with forager from
`https://proxy.golang.org/github.com/microsoft/pxt/@v/v0.2.79.zip`.
This is an educational TypeScript/Blockly compiler, editor, simulator and device
deployment toolkit. Its build/process execution, generated-code evaluation,
cloud/project I/O and serial-device access agree with that purpose. The CLI
server binds `127.0.0.1:3232`; the AppX manifest loads
`http://localhost:3232/index.html?ws=cloud`, calls itself a local test app, and
grants that HTTP page WinRT access. Its companion WinRT code enumerates serial
devices, reads serial data, accesses removable storage and deploys compiled
programs. Those are real permissions/capabilities, without evidence of an
unwanted loader or data theft.

The manifest member has 0 hostile / 1 suspicious before and after. `tdast.js`
is the large TouchDevelop runtime/compiler; Blockly is its generated block
editing library. The Virtual Earth reference leads to Bing Maps code, whose
resource initialization, map geometry, rendering, events and networking serve
mapping. The supplied Bing URL was fetched with forager and inspected and
scanned independently: 0 hostile / 0 suspicious before and after; its isolated
classifier probability remains 0.13496776. No dependent-package exception was
added. The original archive still aggregates to classifier probability 1.0,
despite its benign purpose and verified distribution bytes; this disagreement
is retained rather than suppressing the accurate WinRT grant. Its ZIP-model
route probability changes only from 0.3211409 to 0.31602746.

**resolved.js.** This is a decoded Node loader fragment. It obtains a pointer
from a Tron account's newest outgoing confirmed transaction (`raw_data.data`,
hex decoded and reversed), with Aptos transaction arguments as fallback. It
uses that pointer for BSC `eth_getTransactionByHash` calls, tries two RPC
providers, hex-decodes `result.input`, selects a delimited field and applies a
repeating-key character XOR. Two independent keys/accounts supply two stages:
one goes to direct eval; the other to detached `node -e`, ignored stdio and a
hidden Windows window. Child creation failure falls back to eval. A timestamp
guard suppresses another invocation within 30 seconds.

The fragment needs a wrapper-provided `global.r` require alias and the truthy
`_$_2ee9` string-table variable. It is not a functioning standalone CLI.
`trace_resolved.py` ran the unchanged fragment in QuickJS with stubbed HTTPS
and child-process APIs and inert, known test payloads: it confirmed both sinks,
child options and the repeat guard. Without the table global, no stage executes.
No attacker payload was executed, and no final-stage theft or persistence is
claimed. Its concealed, mutable transaction-to-code chain tips the judgment;
its original wrapper/deployment is unavailable. Classifier probability changes
from 0.99798083 to 0.99869674.

**stage-no-recipient.js.** The visible portion implements an Animotion MCP
analytics endpoint using Upstash Redis. After extensive padding it appends a
string-table-obfuscated Node loader unrelated to analytics. Only the audited,
self-contained table rotation/decoder was executed in isolated QuickJS; 445
lookup calls through 46 aliases were replaced for inspection. The decoded
source queries Ethereum blocks/nonces and an explorer fallback for transactions
from a chosen sender. It hex-decodes the selected transaction's **value**, not
its recipient, into two four-byte dotted endpoint strings. It then requests
HTTP stages, XOR-decodes response bytes, or Base64-decodes an `X-Payload-B64`
header and XOR-decodes that. GET failures fall back to HEAD/header retrieval.
One stage is evaluated inline and also launched in a child; the second is
child-only. Children are detached, hidden, ignore streams and are unreferenced.
These hidden stage paths, plus their unrelated analytics carrier, support
MALICIOUS. No secret theft by the visible Redis authentication code is inferred.

The exact supplied module has duplicate `createRequire` imports and duplicate
`require` bindings. QuickJS module parsing reports `SyntaxError: duplicate
import binding`. This prevents execution as supplied. The verdict describes
its concrete implant content, not successful compromise or a running implant.
The deployment, wrapper and final payload are unavailable. Classifier
probability changes from 0.98 to 0.99642366; low ML confidence relative to these
static hostile findings remains a classifier limitation.

## Rule corrections and coverage

* AppX HTTP-origin WinRT authority moves from `permission/extension-api` to
  `permission/runtime`; `remote-content` becomes `http-content`. A loopback URL
  is not a remote host. Matching and suspicious severity are preserved, and
  the token-forwarding consumer follows the new ID.
* Public/encoded provider observations and provider clusters move out of C2
  objectives to their neutral HTTP RPC/blockchain homes. Encoded-provider
  matchers and scopes are retained. Four endpoint encodings formerly marked
  baseline become notable. The old Polygon directory selector is expanded to
  its exact five former members so its threshold counts remain intact.
* Transaction-context hex decoding moves to `data/decode/hex`; generic
  `input`/`raw_data` variable names no longer claim blockchain provenance.
  Three broad text atoms exclude unrelated Clojure/mIRC/ircii file types to
  respect destination matcher scope limits. No reviewed artifact loses a match
  through those scope exclusions.
* The old hostile `blockchain-tx-input-dead-drop` only required public RPC
  references and nearby hex decoding. Its observation survives as notable
  `transaction-hex-public-provider-context`; hostile XOR-code concealment now
  also requires repeating-key character reconstruction and evaluator/child
  context. Ordinary wallet decoding does not establish payload staging.
* The transaction interpreter and child loaders move to their execution homes.
  `blockchain-remote-payload-eval` moves out of supply-chain inspection abuse:
  its matcher established no package boundary. Its transaction subset is
  represented by the more specific interpreter rule; other branches remain.
* `blockchain-transaction-hidden-child` adds the distinct ignored-stream and
  hidden-window behavior of the resolved transaction loader. The generic C2
  fetch umbrella no longer surfaces alongside the canonical transaction loader;
  this accounts for the original fragment's suspicious-count reduction.
* `nested-transaction-value-field` and
  `obfuscated-ethereum-value-stage-rendezvous` cover the larger sample's value
  field rather than inventing a recipient read. The composite description
  explicitly states co-occurrence, not proven interprocedural data flow.
* Explorer/provider name references move out of dropper objectives and are
  named for the actual matched hosts/API names. Aptos Labs is not necessarily
  an explorer. The `node -e` text followed by eval in an error callback is a
  source-text relationship, not an eval inside the child: it moves to source
  syntax metadata. The related text-only HTTP/eval roll-up becomes notable.
* A separate bound RPC-response → transaction input → hex decoder → eval
  matcher retains direct, non-XOR code-delivery coverage as a notable
  `process/deploy/script-eval` capability. Dynamic delivery alone does not
  establish hostile intent. The source, transaction and code bindings must be
  immutable and agree; an unrelated eval cannot complete the chain.

The resolved sample retains four distinct hostile observations: XOR code
concealment, inline interpreter activation, detached interpreter activation,
and window/stream concealment. The larger sample retains its original four
hostile observations and gains the transaction-value rendezvous. There is no
demonstrated attack-coverage loss. No final payload, credential theft,
persistence, or cleanup is invented to increase counts.

## Checks

Focused reports compare the original tracked ruleset with the edited rules:

* `wallet-display.js`: former hostile transaction dead-drop finding removed;
  decoder, RPC and evaluator primitives retained. It displays input bytes and
  separately evaluates a fixed calculator expression.
* `hex-eval.js`: complete remote hex-to-eval flow remains detected as notable
  delivery; its former generic hostile assertions lack independent attack
  context. This is a technique control, not an attributed malware specimen.
* Included/excluded AppX rules distinguish actual declared grants. The existing
  AppX token-forwarding consumer retains both hostile findings on
  `appx-token-forwarding.ps1` before and after the move.
* Transaction-value reading plus octet formatting alone produces no hostile
  rendezvous. Mutating only the original sample's value field to `fee` removes
  the new rendezvous and retains its original four hostile findings.
* Changing only `windowsHide:true` to false in the original resolved fragment
  removes its new window-concealment finding and retains three hostile findings.
* Existing `ghappier-ethereum-deaddrop-resolver.js` and
  `obf-xor-eval-spawn-stage.js` fixtures retain all hostile/suspicious findings.
  Existing benign Ethereum contract/recipient controls remain clear of H/S.
* The collected loader-utils contract and its encoded inner stage outside this
  batch retain their existing findings. The independently fetched
  `pkg:npm/web3@1.10.4` published bundle has no hostile/suspicious findings
  before or after; it was inspected as a real SDK control, not an exception.
* Exact and ancestor consumers were audited; broad process-creation/C2
  selectors intentionally no longer inherit metadata-only command-text or
  provider observations. The focused positive fixtures retain coverage.

`git diff --check` is clean. The required final repository check is
`make validate`; its result is reported with the completed review.

Judgment marker contents (one line each, verbatim):

```text
Microsoft PXT: authentic toolkit; retain localhost WinRT grant
Blockchain loader: XOR stages feed eval and hidden detached Node
Animotion implant: blockchain HTTP loader; duplicate imports block run
```

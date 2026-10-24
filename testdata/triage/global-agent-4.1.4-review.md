# global-agent 4.1.4 release review

Verdict: **BENIGN**. The artifact is the Node.js global HTTP/HTTPS proxy
library, SHA-256
`2e1bf274a4f719ee2100c908171f8884a0f95743c22a3742362e9d09d39ddb74`.

## Decisive release comparison

Fetched `pkg:npm/global-agent@4.1.3` with forager from the npm registry. Its
original tarball SHA-256 is
`478ca4fff13292091adabb7f8ef985bf952f809cbf53ee5f9828ebd49b47a0a8`.
The tarball and `.forage.json` provenance are retained in the task scratch
directory under `global-agent-previous/npm/`.

Both archives contain 47 regular files. No members were added or removed;
40 files are byte-identical. The seven changed files show:

* `Agent.js` now forwards HTTPS options when `this.protocol === 'https:'`,
  replacing a check of `configuration.secureEndpoint` that Node does not set.
* `HttpsProxyAgent.js` supplies the destination `host` to `tls.connect`,
  enabling identity checking when SNI is omitted for an IP address.
* `createGlobalProxyAgent.test.js` adds DNS/IP certificate subject alternative
  names, verifies SNI and IP certificate success, and asserts rejection with
  `ERR_TLS_CERT_ALTNAME_INVALID` for a mismatched host.
* `parseProxyUrl.js` unwraps bracketed IPv6 addresses after `net.isIPv6`;
  its test file adds an IPv6 documentation-address case.
* `Agent.d.ts` simplifies the HTTPS request-option type; `package.json`
  corrects the typings entry point and changes the version. Dependencies and
  package scripts are unchanged.

The TLS-disable assignment at test line 267 is identical in both releases.
The queue's earlier-clean premise is not reproducible with the current rules:
4.1.3 also reports this same suspicious finding.

## Execution and effects

The public entry point exports `bootstrap` and `createGlobalProxyAgent`.
Bootstrap initializes a global controller on an explicit call. The factory
reads configured proxy environment variables, honors NO_PROXY, and wraps
Node HTTP/HTTPS agents and request functions. Requests use a configured proxy
or fall back to the original agent. HTTP proxy credentials are Base64 encoded
for Basic authorization. HTTPS opens a TCP socket to the configured proxy,
writes an HTTP CONNECT request, checks the response, then wraps that socket
with TLS using the destination and caller's certificate/options configuration.
TLS verification defaults to enabled; callers can supply a different policy.

Tests are not imported by the library's entry-point dependency graph. The
flagged Vitest callback sets `NODE_TLS_REJECT_UNAUTHORIZED = 0` while testing
the library's policy reader against local proxy/HTTPS fixtures. The suite
backs up the variable and restores it in `afterEach`, and closes its servers.
That is a real security-boundary weakening in test code, so the existing
suspicious trait remains intact; the benign verdict does not suppress it.

The source is readable TypeScript-generated CommonJS. Import helpers and
nullish-coalescing expansions are compiler output, with no concealed stage
identified. Reviewed the runtime modules, test setup/cleanup, imports,
certificate generation, connection destinations, and package scripts.
`cleave facts` was collected for the archive and relevant members, including
literal/text/flow views; no encoded executable stage was identified. The
logger defaults to no-op and delegates to a caller-provided logger.

The coherent certificate-verification fixes and their regression tests tip
the judgment toward benign. No deployment configuration or independent
publisher attestation was supplied; this review does not determine who
configured a proxy on a particular machine. Static call tracing establishes
the described capabilities, without claiming runtime network success.

## Trait changes and checks

Extended the existing notable `socket/connect::net-connect` and
`socket/connect::node-tls-connect` matchers to cover TypeScript's numbered
default-import aliases (`net_1.default`, `tls_1.default`). No traits were
removed, demoted, relocated, or excluded. Shared consumers were reviewed,
including reverse-shell relays, framed remote-command agents, and MySQL TLS.

Added a compiled-client positive fixture and reference-only/unrelated-client
negative fixtures to `testdata/expectations.toml`. Focused engine scans pass
these controls. Existing TLS and two executable reverse-shell fixtures retain
all findings. A namespace/method/whitespace matrix preserves all 36 exercised
previous net matcher forms.

Re-scanned the original archive with atomscan, local analysis, slow mode,
updates disabled, and reference following disabled. Counts below are unique
traits per archive/member (archive totals inherit member detections):

| Unit | Hostile before/after | Suspicious before/after | Notable before/after |
| --- | --- | --- | --- |
| Archive | 0 / 0 | 1 / 1 | 88 / 90 |
| createGlobalProxyAgent.test.js | 0 / 0 | 1 / 1 | 39 / 40 |
| HttpProxyAgent.js | 0 / 0 | 0 / 0 | 6 / 7 |
| HttpsProxyAgent.js | 0 / 0 | 0 / 0 | 14 / 16 |

Every original archive-member trait remains present. Added net connection
coverage in the test and both proxy classes, plus TLS connection coverage in
the HTTPS class. There are no material detection losses. The 4.1.3 comparison
also gains both connection traits (87 to 89 notable; still 0 hostile and 1
suspicious).

The archive's rule score remains 66. ML classification remains BENIGN
(`cls: 0`, calibrated level -1), and its recorded archive probability is
unchanged at 0.8820435; the npm route probability is 0.18534708. Terminal
output confirms BENIGN while displaying the retained suspicious TLS finding.
There is no verdict disagreement. Analysis reports contain bounded-flow gaps;
the connection paths were checked directly in source. The installed model
also reports an older v18 feature schema against the engine's v21 schema.

Full validation is the final task action; its outcome is reported in the
task's final response.

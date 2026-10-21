Bencher main source archive — BENIGN

Sample: `023e3cf78567e372603aad230913809e500583cf2c983b3817a214199e9ad8b0`.
This is Bencher, a continuous benchmarking platform, with Rust services and a
TypeScript web console. Static source review found an ordinary Playwright
performance test, not wallet-secret acquisition or export. No sample code was
executed. No obfuscation was present on the implicated path.

The decisive change

Fetched the upstream v0.6.12 and v0.6.13 release archives. Neither includes
`services/console/e2e/speed.e2e.ts`; v0.6.13 also lacks the console end-to-end
runner and workflow. The current archive adds the Playwright dependencies,
runner, fixtures and performance assertions together. The current flagged file
is byte-identical to upstream main.

The narrower upstream change is commit
[c0387143b0b6460e5a84ff302d66c70feebae547](https://github.com/bencherdev/bencher/commit/c0387143b0b6460e5a84ff302d66c70feebae547),
“Add the account's Keys and legacy tokens to the new console (#1283)”. Its
parent is `c3a27d1dfdb5d57f822443d4f210406091617f8b`. The diff adds the
legacy-token speed test and this response mock:

```typescript
const response = await route.fetch();
const { "content-length": _, ...headers } = response.headers();
await route.fulfill({
  response,
  headers: { ...headers, "x-total-count": "1" },
  json: [{ user: seed.member.user.uuid, token: "legacy", /* fixed dates */ }],
});
```

The original regex starts at `route.fetch()`, crosses completed statements and
response-header handling, then matches `user: seed` in the response JSON. It
establishes neither an outbound header value nor a wallet source.
`fixtures.ts` loads `seed.json` through `BENCHER_E2E_SEED`. The Rust runner in
`tasks/test_console/src/task/e2e/mod.rs` starts API and console servers at
`http://127.0.0.1:<free port>`, creates test users/projects, writes that JSON,
and launches Playwright. The mock is restricted to the expected token-list
URL and GET method. It displays a fabricated legacy token because the API no
longer creates that token type. These execution paths and the upstream diff
support the benign verdict; absent detections are not its justification.
Runtime deployment was not observed, and this review does not authenticate
an unrelated installed instance.

Rule correction and coverage

The seed and mnemonic atoms now require a header-map value inside the second
argument of a fetch call. Source strings, comments, neighboring response
objects and sibling JSON bodies cannot supply that value. The names explicitly
say “seed-named”/“mnemonic-named”; arbitrary variable names do not establish
wallet secrets. These neutral network operations are notable under
`micro-behaviors/communications/http/header/custom`, with no inherited
exfiltration ATT&CK/MBC mappings. The three existing wallet composites reference
the relocated observations and retain their hostile classifications.

Before editing, reviewed every exact atom consumer, wallet-directory/ancestor
consumers and the existing hostile fixture
`testdata/hostile/xrpl-wallet-header-exfil.js`. That fixture exports generated
seed and recovery-mnemonic values in fetch headers alongside wallet factory
operations; both hostile detections remain. A validator-export control also
retains `js-seed-validation-header-exfiltration`. The fixture's score remains
122. Its two generic variable-name observations are now notable, so the fixture
requires the new IDs and no longer requires those observations to be suspicious.
No hostile rule was removed or weakened. Attempts to fetch the withdrawn
xrpl@4.2.1 registry artifact returned HTTP 404; published attack-version coverage
was not independently verified from that artifact.

The custom-header leaf was already at its 100-rule budget. Two existing facts
specifically about Content-Type and Content-Length were moved to those header
homes, with their consumers updated. Effective matchers, defaults, platforms,
file types, severity, confidence, section gates and mappings are identical
(`string_literal` is the documented alias of `literal`). No directory-specific
selectors of those three leaves were found. Parent protocol/header scopes still
include them. Positive and negative JSON-charset and ELF .rodata controls verify
these moves; no budget was raised and no new taxonomy leaf was created.

Run `python3 testdata/triage/bencher-header-values/check.py` from the repository
root. Eleven controls passed, covering the original response mock, sibling JSON,
quoted/commented code, ordinary numerical seed transport, property/call-derived
header values, wallet/validator exports and the two placement-only moves.

Scan comparison

Ran `atomscan` and `cleave facts` on the listed archive, and dumped full facts
for the flagged source member, including its symbols, literals and flow graph.
The archive contains 8,145 analyzed units in both before/after JSON reports.
Only the false `fetch-header-seed-value` finding disappeared from the source
member and archive parent. Every other emitted trait and criticality remained
identical. Source score: 52 → 13. Archive score: 175 → 137. The earlier v0.6.13
archive has score 126 and no suspicious/hostile findings.

The final terminal archive rescan reports “1 files scanned, all clean”.
The calibrated ML results are unflagged before and after (`lvl=-1`, model
classes 0). Its generic raw probability remains high, 0.819793 → 0.8505431,
while the TAR model probability falls 0.015318751 → 0.0034666162. These values
are recorded separately from the evidence-based benign judgment; no traits
were added to manipulate the classifier. The engine warns that its v18 model
uses a newer feature extractor. The source also has recorded static flow
analysis gaps; the readable source and harness supply the execution-path
evidence. AST matching cannot recover an unparseable source layer, and unknown
alias/obfuscation variants remain outside this signature's claim.

Full validation is the final action after the judgment marker is written;
its result is reported in the task's final response.

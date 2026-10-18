# Supply Chain Guard reference-data precision

Verdict: **BENIGN**, Supply Chain Guard v6.0.15, an open-source supply-chain
security scanner. The submitted Go module ZIP has SHA-256
`d6a5855cf4c90aa672d4aab75e80fa92d69127b6088e8773c94b9a26a0435d5e`.

Compared with the preceding release fetched from
`https://codeload.github.com/homeofe/supply-chain-guard/tar.gz/refs/tags/v6.0.14`
(SHA-256 `303677d215f006fb2b5081295181670b9f3c6a6adbf9d2953e0cad15d5d991ca`):

- Every source change outside `threat-intel.ts` is a version-string update.
  `threat-intel.ts` adds 23 package advisory records, advances the feed date,
  and updates its bundled version. The dependency graph and lifecycle scripts
  are unchanged; `prepare` invokes the TypeScript compiler.
- `src/ioc-blocklist.ts`, `src/__tests__/campaigns.test.ts`,
  `src/__tests__/core-broad-gap-matchers.test.ts`, and `src/patterns.ts` are
  byte-identical across the two releases. The workflow example changes only
  its self-reference from v6.0.14 to v6.0.15.
- The v6.0.15 GitHub tarball has SHA-256
  `1b9ebf5264b658fa3373f89c32b62a3220f65409df55bf305b47402b5485d5f7`.
  All 319 regular files in that tarball match the submitted ZIP members.

Execution-path review: the CLI calls the scanner, which reads candidate files
and passes their content to `checkIOCBlocklist`. That function iterates the
domain, IP, hash, wallet, and account catalogs, compares them with input text,
and returns findings. It does not contact those indicators. `checkFileDigest`
hashes candidate bytes for lookup. Campaign tests write quoted strings into
temporary fixtures, call `scan`, inspect returned findings, and remove the
temporary directory. The eval and hijacking strings flagged in the other
tests are quoted matcher inputs and assertion messages, respectively.
No obfuscated payload or new execution path occurs in the release diff.

The original rules also reproduced the reported false positives on v6.0.14.
Corrected scans of both releases and both archive formats retain ordinary
capabilities and report zero hostile and zero suspicious traits.

The changes recognize TypeScript IOC table declarations alongside CommonJS
exports, exclude IOC strings in structurally recognized scanner fixture
callbacks, and require parsed calls for promise-eval and hijacking-log claims.
An imported runner or a lone table declaration cannot silence IOC signatures.
The fixture context only suppresses IOC signatures; live eval remains visible.

Placement changes preserve existing matcher scopes unless explicitly described
above:

| Old ID | Canonical replacement |
| --- | --- |
| `well-known/tool/detection/supply-chain-guard/ioc::c2-blocklist-declaration` | `metadata/file/catalog/identity::c2-blocklist-declaration` |
| `well-known/tool/detection/supply-chain-guard/ioc::package-blocklist-declaration` | `metadata/file/catalog/identity::package-blocklist-declaration` |
| `well-known/tool/detection/supply-chain-guard/ioc::exported-ioc-blocklists` | `metadata/file/catalog/identity::exported-ioc-blocklists` |
| `well-known/tool/detection/pattern-catalog::ioc-blocklist-check-function` | `metadata/file/function::ioc-blocklist-check-function` |
| `well-known/tool/detection/pattern-catalog::ioc-domain-table-member` | `metadata/lang/source/syntax::ioc-domain-export-member` |
| `objectives/command-and-control/dropper/script-eval/remote-code::then-eval-pointfree` | `micro-behaviors/process/interpreter/eval/indirect::js-promise-eval-callback` |

The last row also changes text matching to a parsed call with `eval` as the
first argument, and levels the neutral callback capability as notable.
All active YAML consumers reference the canonical IDs.

Run `python3 testdata/taxonomy/scanner-ioc-reference-precision/check.py`.
Ten controls cover TS/CommonJS catalogs, a declaration without a matcher,
scanner fixture callbacks, a runner import with live endpoints, quoted versus
live eval, eval beside fixture code, and quoted versus logged hijacking text.
The runner analyzes the fixture sources without executing them.

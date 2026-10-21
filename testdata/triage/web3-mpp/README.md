# Swagger UI, Web3.js and Solana MPP review

All three submitted artifacts are **BENIGN** on the available evidence. These
judgments apply to the submitted bytes, not to every site or application that
might embed them. No deployment origin, page HTML, installed dependency lockfile,
or operator configuration was supplied.

## Swagger UI initializer

SHA-256: `b23fd10df07f63bf377df9d99d7c91a266cdae06b2d37c2e4049f0e3d49079ac`

The complete 383-byte program assigns an onload callback. That callback calls
`SwaggerUIBundle` with a relative `./docs.json` specification, a DOM target,
standard API/standalone presets and the standard DownloadUrl plugin. It stores
the returned UI on `window.ui`. It neither intercepts requests nor collects
secrets, evaluates fetched source, executes programs, or supplies an external
callback destination. `validatorUrl: null` is ordinary Swagger configuration.

The referenced `docs.json` and the implementations supplied through the page's
globals were not provided. There is no origin against which the relative URL
can be fetched. The official [initializer](https://github.com/swagger-api/swagger-ui/blob/master/dist/swagger-initializer.js)
and [configuration documentation](https://github.com/swagger-api/swagger-ui/blob/master/docs/usage/configuration.md)
were fetched and reviewed as implementation context. A malicious embedding page
could use this ordinary initializer; that possibility does not make these bytes
malicious. Collateral collection from a flagged site is a plausible source-label
explanation, but the labeling source's rationale is unknown.

The former library-identity matcher also matched an initializer and an isolated
configuration property. Its reference observation now lives in source naming;
a separate call matcher records actual Swagger UI initialization.

## Web3.js 1.2.11 browser bundle

SHA-256: `57260df9b7b8c98913555b9221c91668e94b69f180335b5cd956be0884f772c3`

The 1,163,746-byte artifact is byte-for-byte identical to the published
[Web3.js 1.2.11 distribution](https://cdn.jsdelivr.net/npm/web3@1.2.11/dist/web3.min.js).
The version is also present in the embedded package metadata. This comparison
corroborates the code analysis rather than replacing it.

The UMD wrapper exports the Web3 constructor through CommonJS, AMD or the browser
global. Its Webpack entry constructs the Ethereum, Whisper and Swarm interfaces
when called by a consumer. Provider requests and transaction submission are
caller driven. Accounts APIs sign with caller-supplied keys or explicitly
managed wallet entries; there is no added recipient substitution or unsolicited
key export. The default HTTP provider points at localhost:8545. HTTP and
WebSocket clients, ENS operations, signing, AES, RSA, hashes and KDFs fit this
library's advertised purpose. Swarm support includes launcher/file interfaces
for its Node-facing implementation; browser shims limit their availability.

Beautification and execution-path review resolved the conspicuous constructs:
`new Function("return this")` obtains the global object, Underscore compiles
user templates, and vm-browserify's `eval(this.code)` implements its documented
VM compatibility interface. XOR/modulo loops occur in ordinary cryptography.
The Unicode normalization tables, hash/curve constants and encoded literals
are data, not a recovered second-stage program. The cookie collection call is
an HTTP cookie jar's `getCookies`, not Selenium. ENS uses `setApprovalForAll`
for operators as well; the API cannot establish an NFT-only operation.

A flagged hosting page, minified dynamic-code helpers or broad crypto/wallet
heuristics could explain the external label. No page or application calling
this bundle was supplied. There is no artifact modification relative to the
published distribution to support a tampering claim.

## @solana/mpp 0.6.0

SHA-256: `d8eac27bb859b13f4d3fd3eba4bbb0acfe439b14dc8cea94b67da3d324c4408c`

The archive exactly matches the tarball linked by the
[npm version record](https://registry.npmjs.org/@solana%2fmpp/0.6.0).
The [npm provenance statement](https://registry.npmjs.org/-/npm/v1/attestations/@solana%2fmpp@0.6.0)
records the Solana Foundation build at commit
[`a1c04503d089c794afb6ec0b9d4a6659d2c6435a`](https://github.com/solana-foundation/mpp-sdk/tree/a1c04503d089c794afb6ec0b9d4a6659d2c6435a).
All 19 shipped source files match that commit. This is a comparison with the
registry's recorded attestation, not an independent Sigstore signature audit.
The manifest exports library modules and has build/typecheck scripts; there is
no installation hook.

Client charge handling constructs SOL or SPL transfers using the challenge's
amount, currency and recipient, signs through a caller-provided signer, and
returns a payment credential or broadcasts through the configured Solana RPC.
The server decodes and verifies transfer amounts, recipients, token programs,
allowed instructions and bounded fees before co-signing. It simulates,
broadcasts and checks confirmation. Session helpers sign cumulative vouchers
and pay for HTTP 402 retries; they do not enumerate local credential stores.
The optional global fetch patch is caller invoked and restored in `finally`.

The generated UI was unescaped and beautified separately. Its mainnet/devnet
path connects through Wallet Standard and calls the wallet's transaction-signing
feature after the payment button is clicked. Private keys remain with the
wallet. A separate localnet branch generates an ephemeral Ed25519 keypair and
funds it through Surfpool test RPCs. Those private-key operations serve testing,
not acquisition of an existing wallet's secrets. The large declaration file
also repeats the UI string as a TypeScript literal type; its size and extracted
URLs are not evidence of an additional loader.

The UI's temporary service worker hands the `Payment` credential to one
same-origin navigation and unregisters. The fetched `mppx@0.5.5` worker source
confirms the origin check, credential clearing and unregister operation.

Direct dependencies `@solana-program/compute-budget@0.15.0`,
`@solana-program/system@0.12.0` and `@solana-program/token@0.11.0`, plus peers
`@solana/kit@6.5.0` and `mppx@0.5.5`, were fetched and inspected. These provide
instruction builders, codecs, RPC/signing interfaces and payment handling.
They do not add an installation payload. Versions were chosen at the declared
lower bounds; the user's actual resolved versions and transitive installation
were not provided. Public RPC URLs, program addresses, stablecoin mints, asset
URLs and documentation links agree with those roles.

Wallet signatures, real transfer construction, a fetch patch, a service worker,
and large generated UI strings plausibly trigger broad wallet-drainer or
obfuscation heuristics. The traced flows, source comparison and packaging tip
the judgment toward a legitimate payment SDK. No unauthorized recipient,
secret-to-network flow, install-time loader or covert control channel was found.
The model's high score is not a substitute for that behavioral evidence.

## Trait changes and checks

`relocations.json` records the old-to-canonical mapping. Generic references,
source syntax and operator-count measurements were removed from attacker-goal
and misleading capability homes. Exact consumers were updated, including the
four selectors of the former Swagger-only identity directory. Existing scopes
and exclusions were retained except for the documented corrections: ordinary
cookie jars do not enter the browser-automation composite, and an amd64 ternary
operand does not establish a mapping key. Full cryptographic operations remain
notable; scrypt was corrected from baseline to notable. AES algorithm references
no longer claim that encryption actually occurred. SOL/SPL instruction building,
Solana Kit signing, generic transaction-signing calls and embedded Web Crypto
Ed25519 signing now have explicit notable coverage.

`atomscan` and `cleave facts` were run on every submitted path. Decoded string
surfaces and generated browser code were reviewed. Final scans against the
edited local traits have zero hostile and zero suspicious findings on all
three targets. Model scores were treated as leads throughout.

Thirteen small semantic controls cover the corrected distinctions and missing
operations, including nearby negative cases. Run:

```sh
cleave --traits-dir . --format json testdata/triage/web3-mpp > /tmp/web3-mpp-controls.json
python3 testdata/triage/web3-mpp/verify.py /tmp/web3-mpp-controls.json
```

All thirteen controls passed. `test-rules` independently confirms the operator
approval composite; ordinary scans intentionally filter this low-value OR
summary, so the fixture checks its underlying operation. The final repository
check is `make validate`.

# Implementation layers: technique-first audit

Follow-up to the [85-rule audit](PLAN.md), 2026-09-26. The reproducible
vocabulary snapshot is recorded in [layer-summary.json](layer-summary.json).
The original cap audit retains its earlier snapshot.

## Placement decision

**An embedded library implementation is specialized evidence for the technique
or capability group it supplies.** Put it alongside other implementations of
that capability. Static linking does not turn the containing executable into a
library artifact. Describe what the signature supports: “contains an AES
implementation” is different from “encrypts files,” and neither establishes
ransomware. These are the normative
[implementation contracts](../../TAXONOMY.md#implementations-and-library-fingerprints).

Use this order:

1. A signature establishes embedded implementation code or a specific API:
   choose the supported operation, primitive, protocol, or capability group.
   Keep the implementation name in the trait/file, not an extra taxonomy layer.
2. Only a declaration, import/reference, attribution or build requirement is
   established: record that actual fact. A crypto-provider name cannot choose
   AES over RSA; a documentation mention cannot prove either implementation.
3. The analyzed artifact itself is an independently identified named library,
   tool or app: use its canonical `well-known` identity. An individually analyzed
   archive member may qualify; its enclosing application does not inherit that
   identity merely by containing it.

Broad signatures need honest broad capability claims. Reuse or define a
coherent capability group only if the evidence supports it; do not create
`library`, `implementation`, `provider`, or `misc` as overflow leaves. Split
multi-purpose roll-ups into their existing canonical observations where
possible. Do not duplicate one opaque signature into every function a vendor
offers, or infer invocation from an implementation's presence.

## Coverage and reproducibility

[layer-inventory.csv](layer-inventory.csv) inventories **271 candidate nodes**:
95 exact directory names and 176 compound names containing the reviewed terms.
There are **146 outside `well-known`**: 62 capability nodes, 68 objective nodes
and 16 metadata nodes. The inventory includes internal directories; nested
subtree counts overlap and must not be added. It is a vocabulary search, not
271 findings of poor organization.

The semantic review sampled matcher/composite bodies across the 146 external
nodes, inspected the nine exact-name `well-known` nodes, and traced the specific
identity/exclusion examples below. It does not claim line-by-line adjudication
of every descendant rule. The other 116 `well-known` compound-name nodes mostly
contain product/function names; their spelling is not evidence of a bad layer.
Every literal `library` directory is assessed below. Per-rule migration maps
and final destination counts remain prerequisites to YAML moves.

Reproduce the vocabulary inventory with PyYAML available:

```sh
python3 scripts/audit-taxonomy.py --layers-only --out /tmp/taxonomy-layers
```

The matching vocabulary is recorded in the summary. Matches use an entire
directory segment or hyphen/underscore-delimited words, so an arbitrary
substring does not classify a product name. Empty directories are excluded.
CSV examples are pointers into the tree, not automatic semantic decisions.

## All literal `library` directories

Counts include atomic and composite rules. An asterisk marks a subtree total,
not a single leaf. Paths in this table are current source paths; destinations
describe claims to reconcile with existing siblings before creating children.

| Current directory | Rules | Disposition and boundary |
|---|---:|---|
| `micro-behaviors/communications/http/client/library` | 49 | Retire the implementation layer. HTTP/3 support and HTTP-client diagnostics stay with the protocol/capability they establish. WinRM command execution must not be classified as an HTTP request merely because its implementation transports over HTTP. |
| `micro-behaviors/communications/proxy/library` | 29 | Route proxy configuration reads, settings changes and actual relay mechanisms separately. `SCDynamicStoreCopyProxies` establishes configuration access; a provider name alone does not establish relay. |
| `micro-behaviors/communications/websocket/library` | 33 | Route connection, send/receive and protocol-support observations to their WebSocket subjects. Feishu `im.message.receive_v1` is a messaging event, not sufficient evidence of WebSocket transport. |
| `micro-behaviors/crypto/library` | 403* / 19 leaves | Retire the parent. Separate symmetric/asymmetric/hash/KDF/key operations, TLS, ledger RPC, transaction handling, dependency declarations and artifact identities. Neither promoting everything to `crypto/blockchain` nor moving everything to `well-known/lib/crypto` fixes it. |
| `micro-behaviors/crypto/symmetric/aes/library` | 76 | Reconcile with `aes/runtime-library` (48) and algorithm/mode siblings. A .NET AES implementation and an mbedTLS AES implementation belong with AES. A generic cipher API or Go CFB stream type needs AES evidence before receiving an AES claim. The two implementation leaves total **124**, so simply merging them violates the cap. |
| `micro-behaviors/data/archive/library` | 16 | Route archive creation, extraction and member access by the operation. A bare package reference supports less than a call extracting an archive. |
| `micro-behaviors/data/runtime/library` | 35 | Retire this mixed subject with its parent/siblings: samples include HTTP/2, ASN.1 and Go/WASM interop. Those are communication, data-format and foreign-interface claims. |
| `micro-behaviors/data/string/library` | 24 at audit / retired | Twenty-one string API observations moved to operation leaves (measure, compare, copy, case, search, concat). Javassist, cglib and Byte Buddy are specialized code-generation fingerprints used by reflection guards, so their explicit reference-only traits moved to `micro-behaviors/metaprogramming/generation`; `string/runtime` still needs a separate review. A dynamic `CallByName` observation is reflection, not necessarily string handling. |
| `micro-behaviors/dylib/library` | 155* / 8 leaves | Retire the mixed parent: ABI attribution, graphics APIs, editor/tool names and library references are not all dynamic-loading behavior. `XCreateWindow` belongs with window creation; a dependency reference alone stays a dependency reference. |
| `micro-behaviors/fs/delete/file/library` | 51 | File deletion APIs remain deletion observations alongside their non-library equivalents. Backend/language is not a deletion subtechnique. |
| `micro-behaviors/fs/path/library` | 18 at audit / 6 now | **Keep the resource meaning.** Shared-library paths are a real path class. Apple's `/Library/Caches`, font, app-data, log and OSRecovery paths have been moved to their resource directories; the remaining path rules describe shared-library files. |
| `objectives/discovery/network/scan/library` | 17 | Actual probing/enumeration chooses the scan mechanism. A scanner source filename or crate layout alone is not scanning intent. Dependencies and artifact identities retain their actual scope. |
| `objectives/privilege-escalation/elevation-control/uac-bypass/library` | 19 | Actual bypass evidence chooses the bypass mechanism. A `go-escalate` import/name alone does not prove UAC bypass. Neutral elevation APIs must be referenced from a contextual objective. |
| `objectives/supply-chain/install-hook/library` | 6 | Separate import-time activation, installer activity and actual results. Import-time PATH persistence is not necessarily a package-install hook. Put the durable change under its persistence mechanism and reference activation context. |
| `objectives/supply-chain/trojanized/library` | 259* / 17 leaves | Classify the proven trust violation/modification, not the carrier being a library. Plain jQuery/Vue identity, a dependency declaration, or an Express-related license is not evidence of trojanization. Real source patching/substitution must be separated from those neutral facts. |

Thus **14 of 15 literal `library` nodes need redistribution/retirement of that
layer**; the remaining resource node now describes shared-library paths. The
current tree has completed an initial path-resource migration: 12 atoms moved
to cache, system, font, app-data, log and metadata-store subjects, and 8
composite-reference occurrences were updated. The moves preserve all effective
matcher predicates, file/platform scope, severity, confidence and other rule
metadata; only IDs and descriptions changed. The 14 dispositions are not a
claim that every rule in every subtree is wrong.

The exact path-resource moved IDs are:

| Former ID | Current ID |
|---|---|
| `fs/path/library::library-caches-path` | `fs/path/cache::system-library-cache-path` |
| `fs/path/library::hidden-library-caches` | `fs/path/cache::hidden-system-cache-file` |
| `fs/path/library::user-library-caches-apple-path` | `fs/path/cache::apple-named-user-library-cache-path` |
| `fs/path/library::system-library-caches-apple-path` | `fs/path/cache::apple-named-system-library-cache-path` |
| `fs/path/library::library-osrecovery-path` | `fs/path/system::osrecovery-path` |
| `fs/path/library::library-fonts-path` | `fs/path/font::system-font-directory-path` |
| `fs/path/library::hidden-library-fonts` | `fs/path/font::hidden-system-font-file` |
| `fs/path/library::library-group-containers` | `fs/path/app-data::system-group-container-path` |
| `fs/path/library::library-application-support` | `fs/path/app-data::system-application-support-path` |
| `fs/path/library::user-library-application-support` | `fs/path/app-data::user-application-support-path` |
| `fs/path/library::library-logs-path` | `fs/path/log/system::system-library-log-path` |
| `fs/path/library::ds-store-path` | `fs/path/metadata-store::ds-store-path` |

Five cache/recovery atoms moved in the first step; seven additional path atoms
moved in the second. The counts differ from the reference count because most
atoms had no direct YAML consumers.

The string-library move retained the same matcher, effective scope, severity,
confidence and metadata for every rule. String API references now land with
their operation; three known bytecode-manipulation library fingerprints now
use `micro-behaviors/metaprogramming/generation` and explicitly claim only a reference,
not execution. Their references in reflection composites were rewritten,
preserving their role as exclusions for ordinary framework behavior. The .NET
`Combine` and `GetDirectoryName` method-name fingerprints were separately
moved out of string concatenation to `fs/path-ops/join` and
`fs/path-ops/parse`; exact text matching is retained and does not claim
invocation.

## Crypto and blockchain: narrow the actual capability

The 403-rule `crypto/library` subtree demonstrates why deletion of one path
component is insufficient:

| Evidence encountered | Owner |
|---|---|
| AES-specific implementation constants/calls | `crypto/symmetric/aes`, with an honest implementation/API description; mode refinement requires mode evidence. |
| RSA, Diffie–Hellman, Ed25519, key derivation or mnemonic/PBKDF2 code | The actual asymmetric/key/KDF primitive. Wallet branding does not change that home. |
| TLS implementation/API (including rustls) | Communication TLS capability, not a generic crypto-provider bucket. |
| Ledger RPC request | Communication request/RPC; preserve service/ledger specificity in the rule. |
| Construct/sign/submit/query transaction data | The guide's planned `data/transaction` operation contracts; the cryptographic signing primitive is separately canonical under crypto. A node-status query is not a transaction query. |
| Wallet-provider interface | Its supported interface operation, key access or transaction operation. `window.ethereum` alone does not mean credential theft. |
| Provider import, dependency declaration, upstream source path | The actual import/dependency/provenance observation unless stronger evidence supports embedded functionality. |
| Independent identified wallet/library artifact | Its single canonical `well-known` home, subject to the existing recognition and specificity bars. |

The Ethereum client cohort is now split by those claims: JSON-RPC methods,
batching and provider-list composition live under `communications/rpc`;
transaction recipient fields and recipient-byte reconstruction live under
`data/transaction/query`; explorer URL/API signatures live under
`communications/http/url/rpc`; generic array mapping atoms live under
`data/collection/array`. The source-vs-language distinction remains in
`for:` scopes and filenames. Remaining Python wallet, key, signing and
transaction-submission rules and the other `crypto/library/blockchain/*`
siblings still require the same per-rule disposition.

The current `crypto/library/implementation` roll-up combines several primitive
references with broad library context. Refactor its supported claims; don't
recreate the same ambiguous bucket under another name. The `provider`, `stdlib`
and `wrapper` children likewise describe implementations rather than crypto
subtechniques. Compare their actual predicates before deduplicating.

## Other misleading implementation layers

These are audit groups, not automatic whole-directory moves. Mixed rules in a
row may have different destinations. The CSV provides source pointers/counts.

| Current family | Proposed correction |
|---|---|
| HTTP `lib` (192 rules / 14 leaves), server `framework`, download `helper`, request `agent-tools` / `request-wrapper` | Request/response, route handling, streaming, upload or download where established. Tool labels and manifest dependency names alone do not establish these operations. Compare HTTP method vs body/source mechanics using the guide's ordered contract. |
| Socket `wrapper-connect` / `wrapper-create`, FD `dup-wrapper`, file-write `runtime` / `stdlib`, `mem/c-runtime` | Put the observed connect/create/dup/write/copy operation with equivalents. `File::create` need not write content; a C# or ctypes memory copy is not specifically a C-runtime operation. |
| `dylib/load/{binding,runtime}`, `process/interpreter/reflection/runtime`, `process/interpreter/runtime`, `process/create/{stdlib,wrapper}` | Refine native loading, FFI, member enumeration, interpreter hosting/dispatch and subprocess creation by actual mechanics. Merely naming Java `Runtime` is not a process launch. |
| `process/create/shell/bridge` (89), `process/inject/runtime`, objective injection/interpreter `runtime` | Separate transport, process launch, foreign-memory access and actual cross-process execution. A computed same-process Go call does not establish injection. A bare `/bin/bash` label does not establish bridging. |
| `os/container/runtime` (87), `os/sysinfo/platform/runtime` (67), `os/random/prng/stdlib` | Container control/configuration/authority/path observations; OS vs language-runtime version queries; actual PRNG observations. Backend is not the distinguishing technique. |
| `ui/framework`, data `string/runtime`, metadata `binary/framework` / `build/framework` | UI operation, string operation, language/runtime requirement, build output or independent artifact identity, according to what the matcher establishes. Framework-specific code alone is not the framework artifact. |
| Anti-analysis `environment-detect/runtime`, `sandbox/tool-references`; anti-static `self-modify/runtime`, `pack/runtime`, `name-mangling/lib-mimic` | Probe the actual environment property; identify the actual modification/unpacking/concealment mechanism. Neutral runtime structures and familiar library symbols are not automatically obfuscation. |
| `obfuscation/native-api-hash`, evasion `anti-av/{api-hashing,api-resolution}`, dropper `execution/api-hash-loader` | Reconcile hashed import/API resolution under its concealment mechanism. Export walking alone is a neutral capability; neither hashing nor sparse DLL imports alone proves defense bypass or payload activation. |
| C2 `backdoor/dispatch/{bridge,runtime}`, `infrastructure/framework`; dropper `runtime-eval`, `pyinstaller-runtime-loader` | Require command dispatch or payload activation before choosing an objective. A WebView bridge or a builder description is not C2. Route actual activation by the planned sink contracts; build packaging is context. |
| Credential wallet `provider`, `credential-manager/store-api`, `env/secrets/{ai-provider,api-key}`, `exfiltration/cloud/sync-tool` | Canonical interface/store/secret-source facts first; capture/transmission claims require their additional evidence. Certificate enumeration is not inherently credential theft; a sync-tool name is not exfiltration. |
| Evasion `masquerade/wrapper`, impact `cryptojacking/miner/runtime`, `ransom/encrypt/runtime-generated`, privilege `setuid/runtime` and `suid/runtime` | Actual impersonation, mining, destructive generation/encryption, or privilege transition. Reconcile synonymous setuid branches. Compiler banners, generic runtime names and prompts alone do not establish those outcomes. |
| Supply-chain `hidden-payload/runtime`, install-hook `runtime` / `dropper/runtime`, `recon-exfil/runtime`, trojanized `framework` / `provider-shim` / `provider-lure` / `runtime-patch` | Use the documented result/trust-violation contract. An install/import trigger is context; source modification, dependency substitution and theft are separate claims. Requiring a package or provider name does not establish malicious modification. |
| Metadata `package/files/runtime`, `package/testing/harness/runtime`, `binary/symbols/runtime`, `permission/runtime`, `file/format/managed-runtime` | Member layout, test role, symbol property, actual declared authority or actual format structure. Arbitrary filenames, .NET API text and an extension-manifest test are insufficient for stronger runtime/format/permission claims. |

`metadata/build/bundler/runtime` (40) and `wrapper` (47) deserve a more careful
decision than automatic flattening: runtime bootstrap/loader output and module
wrapper shape can be real build-output properties. Define their predicates and
reconcile shared signatures with other bundler children. Their **87 combined
rules** also make a blind merge invalid.

## Names that can describe real resources or mechanisms

Do not turn this audit's vocabulary into a forbidden-word list.

| Example | Why the layer can be meaningful; required cleanup |
|---|---|
| `fs/path/library` | Resource is a shared library path; remove cache/recovery paths misread from the word `Library`. |
| `os/env/runtime`, `os/security/runtime-restrictions` | Runtime configuration variables and interpreter restrictions are actual resources/settings. A secret key belongs with secret-name/access observations instead. |
| `os/security/auth/provider`, `os/telemetry/logging/provider` | Authentication/logging extension interfaces can define a mechanism. Generic log field names do not prove provider registration. |
| `communications/ipc/content-provider`, `os/bpf/program/helper` | Android content-provider access and BPF helper ABI are concrete interfaces; qualify the actual operation and compare neighboring API subjects. |
| `data/embedded/runtime`, `process/lifecycle/runtime-init` | Embedded runtime images and startup/lifecycle mechanics can refine their parent; remove unrelated implementation/source paths and compare existing initialization siblings. |
| Objective `hijack/api-hook`, credential `ssh/runtime-hook` / `theft/auth-provider` | Hooking/interposition can be the actual attack mechanism when the required evidence proves interception or substitution; neutral loading APIs remain capabilities. |
| Persistence `login/winlogon/credential-provider`, privilege `hijack/library-stage` | Provider/plugin activation or substituted shared-library loading can be meaningful. Verify the real activation owner instead of assuming every authentication plugin is Winlogon. |
| Metadata `lang/runtime`, `package/runtime`, `import/framework`, `binary/linking/api-set` | Runtime attribution/requirements, dependency containers and linker interfaces are legitimate properties. Clean up unrelated package names, keywords and unsupported invocation claims. |
| `well-known/lib`, named System Bridge, runtime/stdlib function catalogs | Entity class, actual product name, or primary function. Preserve one canonical artifact identity; audit mixed embedded markers separately. |

The useful review test is **substitution**: if the same observed operation is
implemented by another backend, should its directory change? If only the
implementation label changes, remove that taxonomy layer. This is a human
contract check, not a reliable name-based validator heuristic. Single-child
count likewise remains inventory information, not a validation warning.

## Mixed artifact identity and embedded-code presence

The current tree predates the clarified boundary; `well-known` needs an audit
along with the capability directories.

- [OpenSSL rules](../../well-known/lib/crypto/openssl/traits.yaml) explicitly
  include `openssl-embedded-static-build`. Its HTTP diagnostics plus EVP
  encrypt/PKEY references establish embedded capability context, not that every
  matching application is the OpenSSL library. Some symbol-based identity rules
  also need import/export and analyzed-artifact scope reviewed. Other source
  rules already restrict copyright evidence to avoid binary-wide suppression.
- [zlib rules](../../well-known/lib/format/zlib/traits.yaml) mix source-file
  identity and inflate implementation markers. An independently identified
  zlib source artifact can retain identity; embedded inflate evidence goes with
  decompression. Do not relabel it compression simply from the library name.
- [SQLite rules](../../well-known/lib/data/sqlite/traits.yaml) mix exports and
  product resources with dependency references and embedded assembly/loading
  context. Separate actual SQLite artifact identity, database capability,
  declared dependency and payload loading; one relocation cannot preserve all
  four claims.
- `well-known/lib/crypto/{implementation,sdk}`, `lib/ai/llm/provider`, and
  `tool/development/runtime` need the same review. Broad source markers,
  multiple SDK package names or generic token-provider functions are not one
  independently identified entity.

**Exclusion migration is a semantic change, not just an ID replacement.**
Current objectives use the OpenSSL directory in exclusions. Replacing those
references with an AES/HTTP capability prefix would suppress unrelated malicious
programs using those capabilities. Inventory exact and directory references,
compare their resolved sets, and preserve only justified benign context via
precise named exception composites. Test a benign standalone library, an
ordinary linked application, and a malicious program with the same embedded
implementation. The latter must not become benign because of the library.

## Migration order and acceptance

1. Apply the new TAXONOMY contracts before choosing destinations. Document any
   uncovered operation/resource boundary with positive and negative examples.
   The path-resource move above is the first completed migration tranche;
   update any external ID consumers during the release that adopts it.
2. Start with crypto/library plus AES implementation siblings, HTTP library
   layers, string operations and file deletion. Reconcile existing canonical
   matchers before adding rules or directory levels.
3. Map every affected rule to keep/move/merge/retire; record defaults, exact
   matcher scope and verdict repairs. Compare both source siblings and
   destination residents. Calculate destination totals; do not flatten the
   124-rule AES or 87-rule bundler groups into oversized leaves.
4. Migrate mixed `well-known` identities and all their consumers together;
   preserve legitimate artifact identities and correct embedded-code claims.
   Objective composites then reference the canonical capabilities and supply
   the intent/context they previously assumed from library names.
5. Rewrite references, fixture expectations and ML mappings; compare findings
   modulo pure ID moves and test intended semantic changes separately. Finish
   with the original plan's strict validation and fixture acceptance criteria.

No automatic singleton warning or blanket vocabulary ban is proposed. The
confirmed matcher-deduplication gap and proposed predicate-aware improvements
remain documented in the [validator findings](PLAN.md#duplicate-validator-findings-and-proposed-improvements).

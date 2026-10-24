# Sample review: manifest, Nx JS, and Stagehand

All three supplied samples are **BENIGN** on the balance of the available evidence.
The external hostile label was treated as a lead, not as a behavioral conclusion.
No original sample was executed. Package code, bundled source, manifests, entry
points, relevant call chains, source maps, extracted strings, nested members,
URLs, and dependency install hooks were inspected statically.

## Identification and execution paths

- **002650a80750 — generic Java archive manifest.** Exactly 85 bytes: a
  `Manifest-Version: 1.0` header and a comment saying a build will add Main-Class.
  There is no Main-Class, Class-Path, URL, script, or executable stage. Nothing
  identifies the parent application. This shared build artifact could have been
  collected from a malicious JAR, but its own bytes are inert metadata.
- **6fa2b0d436fd — @nx/js 23.3.0-beta.5.** The supplied gzip archive is
  byte-identical to the exact npm release recovered with forager. Its CommonJS
  index exports generators, compiler helpers, and package/lockfile utilities.
  Executor paths compile TypeScript/SWC, launch user projects, run package
  managers, publish requested releases, and start/configure Verdaccio for tests.
  The npm-config helper invokes `npm config get` through a Promise-wrapped
  child_process.exec; this is shell execution and remains detected as such.
  Local-registry auth tokens are installed for that registry and removed on
  shutdown. The module-loader hooks implement configured workspace mappings.
  This package declares no install hook. Its Nx core dependency's postinstall
  checks platform support and, only for an Nx Cloud-configured workspace,
  verifies/downloads/loads the cloud runner. No hidden credential harvesting,
  automatic hostile command chain, or concealed second stage was found.
- **6f6b4144d2ec — @browserbasehq/stagehand
  4.2.0-alpha-0721ee22d8cff5358075bf5130217d487e7b58f0.** The archive also
  matches the exact npm release byte for byte. All eight nested extension ZIP
  members equal their counterparts in dist/extension. The SDK launches local
  Chrome or connects to a caller-specified local/Browserbase session, provisions
  its extension, and routes typed JSON-RPC methods to browser controllers.
  The service worker starts its RPC transport and heartbeat; browser connection
  and LLM configuration arrive through initialization. Cookie retrieval,
  clipboard read/write, screenshots, page evaluation, script installation,
  synthetic input, and network interception are explicit automation methods.
  The default local launch creates a temporary profile and removes it on close;
  caller-selected profiles and existing sessions are also supported. Page data
  and images can be sent to configured model providers. These are consequential
  dual-use capabilities, without a demonstrated unauthorized acquisition/send
  chain. Base64 handles attachments, images, and provider data; Function use
  includes a runtime capability check. Bundled Zod/AI SDK code is readable,
  rather than a concealed loader. There is no install lifecycle hook.

The supplied deployment context does not establish who installed either SDK,
what workspace tasks were requested, whether browser profiles were authorized,
or which models/endpoints a caller configured. The verdicts concern these
artifacts, not every possible use of them. Nx's command execution, npm-token
configuration, and Stagehand's broad extension permissions/data access can
plausibly explain heuristic suspicion. The source's actual labeling rationale
was not supplied; ordinary shared manifest provenance or overmatching remains
possible and cannot be distinguished conclusively here.

## Provenance and dependency follow-up

Forager retrieved both exact npm releases and 33 direct runtime dependencies
(the explicit version or the declared range's lower bound), plus Nx core
23.3.0-beta.5. All 34 dependency archives were scanned, and relevant install
hooks and execution/network paths were inspected. None had hostile or suspicious
traits in the recorded baseline. This is supporting triage, not proof from a
clean scan: the substantive decisions above come from the traced code.
There is no supplied lockfile or installed dependency tree, so these downloads
do not establish the versions actually installed in an unknown deployment.

Both project homepages were fetched separately: Nx describes monorepo/build
infrastructure and Stagehand describes a browser-agent SDK. Provider/API URLs
are service endpoints, not static payload links; their actual caller settings
and authenticated runtime responses are unavailable. No embedded payload URL
requiring another executable stage was found. Artifacts and original
`.forage.json` provenance are retained under the named scratch directory:
`/usr/local/var/cyclotron/tmp.noindex/cyclotron-90084b2c/scratch/bad-review/`.
It also contains complete before/after scans, facts, per-member comparisons,
dependency scans, and focused-test output.

## Matcher corrections and retained observations

- Schema enums such as `["disabled", "allow"]` are not selftest verdict rows.
  The selftest rule now requires a nested array row; genuine existing VSS
  selftest fixtures still match. Objects passed to `issues.push` with
  `expected: "string"` are schema errors, not a table. The renamed
  expected-string-case-table rule requires object rows in an actual array.
- `java.lang.RuntimeException` is not `java.lang.Runtime`; a word boundary
  preserves Runtime/ProcessBuilder references and the reflective-process
  composite while excluding the exception-class example.
- `typeof output.value === "string"` is a comparison, not an amount assignment.
  Assignment matchers reject comparison/arrow operators. All three output
  property atoms moved to data/property/assign, since generic output fields
  do not establish a financial transaction. The transaction-drainer consumers
  retain their attack-specific legs and pass the positive control.
- `setup-prettier/` is an Nx generator directory, not Prettier's package.
  The matcher requires the complete `prettier` directory component. Positive
  Prettier-directory and near-miss setup-prettier controls both pass.
- A helper named execAsync does not establish argument-vector execution or
  util.promisify usage. The exec atom now covers execFileAsync. Existing
  shell/bridge atoms retain Nx's execAsync and child_process.exec execution.
- A diagnostic mentioning "Tool approval response" is not an approval policy.
  The policy matcher now requires explicit requirement wording. Its consumer
  remains an approval-guideline exception, and affirmative policy wording is
  retained by the positive control.
- An inner extension ZIP must not borrow `package/dist/...` provenance across
  an archive-member separator. The runtime inventory matcher rejects those
  separators; the missing-manifest composite compares inventory at leaf scope
  and tests the archive manifest member directly. Genuine missing-manifest and
  nested-extension controls pass. The old inherited runtime-code-member
  finding disappears; accurate direct dist-runtime/tree observations remain.

## Placement corrections

Matcher scopes and observations were preserved while moving generic evidence:

| Former home | Canonical home and supported claim |
|---|---|
| Selenium identity | process/create/flags: Chromium automation launch flags |
| Coding-assistant identity | data/llm/wire-marker: mcp_tool_use field reference |
| OpenAI identity | data/llm/wire-marker: Google safety-threshold API names |
| Upload-client identity | http/header/custom: the three tus header names |
| Next runtime identity marker | metadata/lang/runtime: EdgeRuntime name reference |
| Transaction construction | data/property/assign: output destination/value assignments |
| Autorun keyword | metadata language vocabulary: installed/managed near init/autostart |
| Process flags | metadata language vocabulary: deferred-uninstall maintenance wording |
| Custom header | HTTP auth: api-key; security header: CSP; accept header: Accept-Encoding |

The header and flag catalogs were audited at their 100-rule budgets. The
maintenance-wording and authentication/security/negotiation header moves correct
real placement errors; no budget increase or arbitrary taxonomy split was used.
Exact consumers were updated. Behavioral consumers of the browser-automation
ancestor selector retain explicit references to the moved flag composite where
applicable. Generic launch flags no longer establish recognized-library metadata;
redundant or overbroad catch-all suppressors were not expanded. The complete
validation corpus is the final check for changes in those consumers.

## Coverage additions and verification

A parser-extracted string containing `navigator.clipboard.readText(` is now
visible as a browser clipboard source-expression observation. Existing CDP
Page.captureScreenshot coverage now also applies to JavaScript/TypeScript.
Both are notable, with no theft inference. Existing cookie reads, script
execution/evaluation, browser input, HTTP operations, permissions, encoding,
process launches, and profile cleanup remain visible.

`python3 testdata/taxonomy/npm-sdk-review/check.py` passes all 11 positive and
near-miss controls. These include existing selftest and actual VSS execution
fixtures outside this batch, a transaction drainer, reflective JVM execution,
browser capabilities, and both manifest-inventory cases. These small controls
are regression fixtures, not reconstructed original malware specimens.

## Before/after results

Counts are unique trait IDs across the input and every analyzed member. No
member had a hostile or suspicious finding before or after.

| Sample | Hostile before → after | Suspicious before → after | Notable before → after | Raw ML probability before → after |
|---|---:|---:|---:|---:|
| Java manifest | 0 → 0 | 0 → 0 | 1 → 1 | 0.000021974 → 0.000021974 |
| @nx/js | 0 → 0 | 0 → 0 | 151 → 149 | 0.81395215 → 0.8015234 |
| Stagehand | 0 → 0 | 0 → 0 | 434 → 430 | 0.6164224 → 0.6638359 |

All calibrated ML levels remain -1 (benign); raw probabilities are not verdicts.
There is no remaining verdict disagreement. Atomscan 2.13.0 reports an older
v18 feature specification versus expected v21; this model-version limitation is
recorded rather than compensated with inaccurate traits.

Stagehand notable counts: outer 431 → 427; nested ZIP 335 → 331; each service
worker copy 296 → 293; index.mjs 124 → 123. Its content scripts and heartbeat
scripts retain their original counts. Full comparisons cover all 25 Stagehand
and 278 Nx analysis units, including auxiliary units emitted by the analyzer.
The ordinary manifest still has its original single notable header trait.

No supported hostile behavior or attack detection was removed. Material losses
are the unsupported test/Java-process/financial-assignment/policy/package-identity
claims described above. Relocated facts retain their correct observations;
Nx shell execution and Stagehand runtime code remain detected. Final validation
is run after the judgement markers and all repository edits.

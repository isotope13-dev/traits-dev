# npm library review, 2026-10-26

All three original artifacts are **BENIGN** on the available evidence. This
judgment follows examination of their entry points, callers, data flow and
packaging, rather than their classifier scores. No deployment history, lockfile,
project configuration or user authorization context accompanies the artifacts.

## Identification and execution paths

* **217b08481e05 — @voiceflow/verror 1.1.3.** The collected basename omits the
  package scope. Its sole runtime file imports `http-status`, subclasses `Error`,
  calls `super(message)` and optionally `Error.captureStackTrace`, then attaches
  the code, caller-supplied data and current timestamp. `HTTP_STATUS` exposes the
  imported constants. `http-status@1.3.2` supplies a static status-code table;
  this import is not an HTTP request. The manifest's lint/test/documentation and
  Husky development commands do not install a payload or execute on consumer
  installation. There is no npm install lifecycle hook. The error implementation
  and its dependency explain the executable contents; no remote stage was found.
  Added the missing stack-capture capability.

* **111d9eaa8fce — @rspack/core 2.2.5.** The ESM entry exports the Rspack compiler
  and webpack-compatible plugins. The local `612~*.js` chunks implement module
  registration and caching. Compilation invokes the native binding selected by
  the package or the explicit `RSPACK_BINDING` override. Loader pools initialize
  Tinypool with the local `dist/worker.js`; its worker uses caller-selected local
  loader paths and executes their pitch/normal methods. Tinypool's process
  implementation uses `child_process.fork` with IPC and relays worker output;
  shutdown kills its own worker. Its thread implementation creates worker
  threads. The Watchpack bundle watches/stats paths and includes graceful-fs
  compatibility wrappers. These are build-system operations.

  `ExecuteModulePlugin` evaluates compilation-generated JavaScript through
  `vm.runInThisContext` and calls the returned wrapper with module/runtime
  arguments. `HttpUriPlugin` supplies an HTTP(S) GET client for configured URI
  imports, decompressing gzip, Brotli or DEFLATE responses into buffers and
  returning status, headers and body to the compiler. Lazy-compilation clients
  POST a newline-separated set of active module identifiers to the developer's
  configured server; they consume the response rather than evaluating it.
  Module-federation code builds an inline data-URL resource from generated
  runtime source. These paths fit the exported compiler/plugin interface, with
  caller-provided inputs and configuration; they are not covert tasking or
  host-data collection.

  The two long Base64 literals decode to 2,156-byte MD4 and 1,170-byte xxHash64
  WebAssembly modules, repeated in the main and worker bundles. Both have no
  import section and export `init`, `update`, `final` and `memory`. The wrapper
  feeds build-input bytes into their memory and obtains a digest. The decoded
  modules cannot directly import host filesystem/network/process APIs. The
  Unicode escapes are pathname escaping/sentinels and terminal colors. No
  concealed OS payload, miner, credential collector, persistence or cleanup
  path was recovered. Added missing gzip/DEFLATE stream-factory calls; retained
  the existing VM, worker, HTTP, hash and Base64 observations.

* **568f49d0a318 — @nx/devkit 23.3.0-pr.37068.f95e11e.** The CommonJS entry
  re-exports Nx's devkit API and local generator utilities. `generateFiles`
  recursively reads a caller-selected template directory, preserves binary
  files, renders text through EJS and writes into the caller's Tree using the
  selected overwrite policy. Configuration loading selects CJS/ESM/TypeScript
  handling by file extension and available Nx transpiler support, invalidates
  local module caches and retries specific loader errors. The `Function`
  constructor wraps `import(modulePath)` for compatibility.

  Dependency helpers edit workspace manifests/catalogs. `ensurePackage` first
  resolves the requested package locally, otherwise delegates installation to
  Nx's temporary-package installer and adjusts `NODE_PATH`. The returned install
  task uses the selected package manager's install command through `execSync`
  after a package change, with explicit workspace cwd and stdio settings. It
  removes a default public-registry environment override in the documented temp
  installation case. Migration code rewrites project configuration/imports and
  verifies inferred targets; formatting calls Prettier. No install hook is
  declared by this devkit artifact. A Base64-looking prose word in a comment
  decodes to meaningless bytes; it has no decoder or execution sink. Added the
  missing EJS-render capability and preserved shell execution, configuration
  loading and environment modification observations.

## Provenance and dependency review

Forager recovered all three original versions from npm. Each recovered archive's
SHA-256 exactly equals its supplied sample hash, not merely an archive rebuilt
from source. The code paths above, not that agreement alone, determine the
verdicts. Artifacts and `.forage.json` records are retained under the session's
`scratch/triage/fetched` and `scratch/triage/urls` directories.

Fetched and inspected `http-status@1.3.2`, `@rspack/binding@2.2.5`,
`nx@23.3.0-pr.37068.f95e11e`, `ejs@5.0.1`, `tslib@2.3.0`, `semver@7.6.3`,
`yargs-parser@21.1.1`, `minimatch@10.2.5`, optional
`@module-federation/runtime-tools@0.24.1` and `@swc/helpers@0.5.23`.
The binding's generated loader chooses platform packages, with an `ldd --version`
fallback for libc detection. Nx's postinstall is a bounded platform/cloud-client
setup routine; the cloud update path loads the configured Nx Cloud client.
EJS compiles and invokes caller-supplied templates. The remaining inspected
dependencies provide parsing, matching, transpiler helpers or module-federation
re-exports. No installation was performed and no sample code was executed.
This is not an exhaustive audit of every platform-native binary or transitive
dependency. Ranges were examined at these explicit versions; without a lockfile,
an actual installation's full graph cannot be reconstructed.

Referenced Rspack/Nx homepages and the verror source URL were fetched, together
with official Ext JS source and Tabby's terminal-plugin manifest for controls.
Dynamic plugin/HTTP endpoints depend on project configuration that was not
provided. No endpoint or deployment was invented.

The external label's origin is unknown. Scope stripping/name confusion is a
plausible explanation for verror. Broad build-tool heuristics or historical
package reputation may explain the other labels: the upstream
[Rspack compromise notice](https://github.com/web-infra-dev/rspack/issues/8767)
identifies 1.1.7, and the
[Nx postmortem](https://nx.dev/blog/s1ngularity-postmortem) identifies older
compromised releases, including devkit 20.9.0/21.5.0. These do not establish
malicious contents in the versions reviewed here. They are hypotheses about
mislabeling, not proof of how the external source made its decision.

## Corrections and preservation

* A generic `builtin-plugin` path incorrectly identified 103 Rspack declaration
  members as Tabby and rolled an AI-assistant identity into their archive.
  Moved the plugin observations to the existing **Tabby terminal** identity,
  requiring its `builtin-plugins/tabby-*` layout. Added its manifest keyword
  alternative from the fetched
  [upstream plugin manifest](https://github.com/Eugeny/tabby/blob/master/tabby-plugin-manager/package.json).
  Updated all six direct path consumers. Existing AI-release/source identities
  remain separate. Actual terminal plugin paths remain detected.
* `Sencha Inc.` alone cannot identify Ext JS: Connect carries that copyright.
  Ext JS identity now requires its `Ext.setVersion('extjs', ...)` registration;
  a separate notable license property retains the supported copyright
  attribution. The full official Ext JS 4.2.1 source remains detected.
* Both JavaScript data-URL regexes retain their exact matchers, file types,
  confidence and notable criticality. Moved them from process creation to
  `communications/url/scheme` and described URL references without claiming
  loading or percent encoding. Updated both exact objective consumers. Bare
  URL text no longer satisfies broad process-creation selectors. Actual loaders
  retain their independent execution evidence.
* Added four distinct capabilities: error stack capture, EJS rendering, gzip
  decompression stream creation, and DEFLATE stream creation. Comments and
  quoted API names alone do not trigger those call matchers.

Exact references and ancestor selectors were searched before editing. Ext JS
had no exact consumers. The old process-creation directory selectors were reviewed:
mere data-URL text is intentionally removed from their execution evidence,
while genuine process/evaluator APIs remain eligible. No generic URL-scheme
directory selector gains a new conviction. AI-specific suppressors no longer
mistake terminal plugins for an AI assistant; terminal-specific path suppressors
follow the corrected IDs. The existing documented legacy placement holds for
whole-file archive entropy and other encoding properties remain unchanged;
their accurate observations and all consumers are preserved.

## Reproduction and results

`atomscan --no-update --analyze local --mode slow --format json <original>` and
`cleave facts <original>` were run for each artifact. Parser facts were also
collected for all 97 JavaScript/JSON members (2, 35 and 60 respectively), with
no reported parser errors. Decoded text and the embedded WASM sections were
inspected. Final scans bypass analysis-report reuse. The [saved machine-readable
summary](scan-summary.json) contains root counts and classifier probabilities; member comparison
includes every analyzed archive member.

Run the focused controls with:

```
python3 testdata/triage/npm-libraries-20261026/check.py --scratch-dir <scratch>
```

The controls cover the original Connect/Rspack near misses, official Ext JS
version registration, actual Tabby manifest, terminal layout, call-versus-text
capabilities, inert data URLs, an inline XHR/eval loader, and the existing
cookie-exfiltration corpus positive. Hostile controls are scanned under
neutral paths because the shared URL rules intentionally exclude test paths.
No hostile detection was weakened or removed. Material attack losses: **none**.

Result: **10 focused controls passed**, including the hostile loader and the
pre-existing cookie-exfiltration control. The full official Ext JS source also
retains its identity finding.

All original samples have **0 hostile and 0 suspicious traits before and after**,
including archive-member findings. Classifier calibrated level remains `-1`
(benign) for all three; no rule/classifier disagreement with these verdicts
remains. Raw model probabilities are not verdict thresholds. The installed
model warns that its feature specification is older than the engine; this
remains a classifier limitation, not a reason to alter accurate traits.

Final required validation is `make validate` after the verdict markers and
review records have been written.

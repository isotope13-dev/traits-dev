# Google API Extensions release comparison

Verdict: **BENIGN**, `google-gax@5.0.0-rc.3`.
SHA-256: `8d26c0ecd6d6a36c4e59ee7bd38caaad50fe4bff11a80f32ca1b29e1596cdd62`.
The sample is byte-identical to the exact-version npm registry tarball.

## Decisive diff

Forager fetched the previous release, `5.0.0-rc.2`, the exact current registry
artifact, the npm version record, and source commit
`6660948f5227a4a4a0b2f8047335669e49d5fd07` from the version record's `gitHead`.
Artifacts, provenance sidecars, member facts, scans and the full release diff
are retained in the task scratch directory `gax-review`.

All 273 archive-member paths are unchanged. Only three files differ:

- `package.json`: increments the version and adds `google-logging-utils: ^1.1.1`.
- `build/src/index.js`: adds a CommonJS import and namespace re-export of that
  declared dependency, plus its generated exports initialization.
- `build/src/index.d.ts`: declares the same namespace re-export.

Every other distributed member is byte-identical, including all generated
protobuf modules and schemas. The prepare hook is exactly unchanged. Scanning
the earlier release under the current rules reproduces the original suspicious
finding; the supplied historical clean scan does not establish a new behavior.
The upstream source manifest matches the distributed one apart from its release
version (`rc.0` in that commit); its source entry point has the logging export.

## Execution paths

The package provides Google API gRPC/REST transport, authentication, retries,
pagination, streaming and protobuf serialization. Its module entry point loads
and re-exports these modules. The new logging utility's exact `1.1.1` artifact
was fetched and inspected: it creates cached loggers, optionally reads
`GOOGLE_SDK_NODE_LOGGING`, and writes formatted diagnostics to console or a
caller-provided backend. Its built-in backends do not send logs to a server.

In the source repository the package is `gax/`, beside `tools/`. Prepare first
compiles the package, enters `../tools`, installs that tooling's declared
dependencies with bare `npm i`, compiles it, and returns to `../gax`.
`tools/src/prepublish.ts` refreshes `protos/google` from `google-proto-files`;
the hook copies those schemas into `build/protos`. `tools/src/minify.ts` reads
and minifies the generated JavaScript and JSON there. These paths perform
ordinary author build operations; the hook does not name an injected dependency
or rewrite an unrelated consumer project's manifest.

Existing REST code derives the URL/method/body from RPC encoders and caller
configuration, adds authentication headers and handles response streams.
The unchanged certificate-provider path in `grpc.js` calls `execFile` with
the executable and argument vector from configured certificate-provider
metadata when client-certificate use is enabled. That execution capability is
retained; it is not evidence of a new payload.

Member facts were collected for 47 distributed JavaScript files, the manifest,
and four logging-utility modules. Encoded-string searches also checked the five
minified protobuf modules, the changed entry point and the stream-array parser.
The IAM module's ten Base64 candidates are repeated `BindingDelta` identifiers
in ordinary generated serializer calls, decoding to the same non-code bytes.
There is no new encoded execution path. Minification is build output, and all
five generated modules are unchanged from the earlier release.

The balance of executable behavior, the narrowly scoped release diff and the
matching upstream tooling supports BENIGN. No machine deployment context was
provided; the review does not assert the integrity of every future dependency
version that a semver range might resolve.

## Rule correction and preservation

The old `prepare-parent-directory-escape` matcher proves a parent-relative
directory-change command in `scripts.prepare`. It does not establish consumer
project rewriting, supply-chain compromise or an absolute boundary escape:
an earlier descent may change the starting directory. The matcher and all
private/local-dependency/Husky exclusions are preserved under
`micro-behaviors/fs/directory/chdir::npm-prepare-parent-directory`, at notable.
This is an operation-bearing command observation, rather than the mere presence
of a lifecycle declaration. Its unsupported ATT&CK/MBC supply-chain mappings
were removed. No package identity or particular helper name gates detection.

The escape-only `install-hook-parent-directory-escape` grouping was removed.
Its four alternatives were inlined into `install-hook-injects-consumer-dependency`
alongside the unchanged required package-install leg. This preserves the
consumer-injection predicate, including prepare navigation combined with an
install leg elsewhere in the manifest. Exact references and ancestor selectors
were inspected: the only broad objective consumer is a JavaScript-scoped MCP
config-write rule, and broad filesystem consumers are scoped to unrelated
PE/PowerShell/autorun evidence. None gains or loses a matching manifest path.

The fixture retains the actual build commands with generic identity fields.
The Husky verifier checks 25 positive and near-miss command forms and asserts
notable navigation. The nested-install verifier passes all three controls,
including retained hostile consumer injection. The existing VS Code drift
suite passes all 23 controls. The real out-of-batch Adyen `5.32.0` manifest
retains its bounded Husky exclusion.

## Before and after

Both `atomscan --mode slow --format json` and explicit local-rule Cleave scans
were compared across the archive and its members. All other findings remain.
The only removed observations are the misleading prepare objective and its
escape-only grouping; the same navigation is now notable. There is no material
loss of attack coverage. No suspicious or hostile finding remains in this
sample. The earlier release receives the same corrected navigation finding.

Current local atomscan risk scores change from 78 to 43 for the archive and
47 to 11 for its manifest (the queue reported 40 using its earlier context).
ML class remains benign: archive probability changes from 0.9550346 to
0.84283036 and the npm-specific model from 0.3815556 to 0.021288922; both have
`cls: 0`, with calibrated level `-1`. Manifest probability changes from
0.002962023 to 0.00002916654. The calibrated classifier agrees with the manual
verdict before and after; the original suspicious rule was the disagreement.
The scanner reports flow-analysis limitations and an older model feature
schema, so the verdict rests on the source/diff review, not scan completeness.

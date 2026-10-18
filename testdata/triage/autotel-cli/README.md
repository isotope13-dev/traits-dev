# autotel-cli 0.21.1 triage

Sample: `autotel-cli-0.21.1.tgz`

SHA-256: `1deb54c0dcf9ced55e2eac13c1fc36453a248b3713420b270dd2ad8c2240673f`

Disposition: **benign** for the supplied archive. The archive contains six
members: package metadata, Apache license/notice, README, an empty TypeScript
declaration, and one readable 334,582-byte JavaScript CLI bundle. No lifecycle
install hooks or opaque payloads are present. The sample is kept outside git.

## Static review

The entrypoint calls Commander. User-selected commands generate instrumentation
and dotenv examples, install telemetry dependencies, check local configuration,
analyze project source, apply a tracing codemod, and query observability backends.
The source parser and code generators account for embedded source examples;
they do not evaluate downloaded code.

All process launches are package-manager installs or `git rev-parse` / `git show`
for a requested baseline. Doctor fixes use commands constructed by the CLI.
`init --scan-env` permits key-based backend detection; doctor also parses local
dotenv files to check required-key presence. These paths do not send dotenv
contents. Source writes implement the requested instrumentation/codemod changes;
configuration writes include backup/root checks, while codemod paths are supplied
by the caller. Telemetry writes its preference/outbox under `~/.autotel`.

The two direct fetch sites send a synthetic OTLP freshness span to a configured
collector or command usage events to a configured telemetry endpoint. Usage
telemetry defaults to disabled, honors opt-out preferences, sanitizes flag values,
and hashes a platform/architecture/USER-derived identifier. No fixed attacker
destination, secret-harvesting transfer, persistence, hidden loader, or destructive
routine was found in the shipped bundle. External dependency implementations
are not included in this archive and are outside this disposition.

`cleave facts` was checked alongside source, including imports, calls, literals,
metrics, and parser diagnostics. The JavaScript parser reported no errors. The
sample and its dependencies were not executed.

## Detection corrections

- Require the actual `process.env` spread operand. Conditional spreads and
  spreads of individual environment members are not full-environment copies.
- Require parsed name assignments on conventional package-object receivers;
  remove the package.json proximity matcher that matched equality comparisons.
  The neutral observation lives in `data/property/assign`, since receiver naming
  alone proves neither a manifest write nor publication.
- Move generic `getBody()` calls to `data/control-flow/dispatch` and assigned
  results to `data/property/assign`. The receiver may be an AST node. Keep the
  ServiceNow constructor co-occurrence composite and avoid claiming value flow.
  The result-assignment matcher also excludes comparison operators.
- Bound for-of/fetch evidence to a source loop AST or a brace-bounded markup
  loop body. A completed logging loop cannot reach a later sender function.
  This supports fetch-call syntax, not a claim that each iterated URL is fetched.
  The markup fallback handles simple braced bodies, not arbitrary nested syntax.
- Require an actual `isCI` property access instead of a bare token, and remove
  the unsupported ci-info library attribution.
- Consolidate JavaScript/TypeScript and Python chat-completion calls into one
  provider-neutral, parsed-call trait. Groq attribution still requires its own
  constructor; source example text is not a call.

The dispatch leaf was at its 100-rule budget. Its save/send plugin OR and
unreferenced save-only atom were consolidated into an anchored union matcher,
retaining the separately consumed send-only trait. Both alternatives retain
their `.text` section and PE/DLL/Windows scope. No budget was increased.

## Verification

Run `python3 testdata/triage/autotel-cli/check.py --sample /path/to/sample.tgz`.
The 15 static controls cover JavaScript, TypeScript, Python, HTML, SVG, and inert
PE strings; they preserve real operations and reject the observed false matches.
The script also checks every scanned archive member for suspicious/hostile
findings and verifies the corrected bundle observations.

The final sample target is zero suspicious and zero hostile traits. Raw facts,
before/after scans, traces, and validation logs are retained under
`/tmp/triage/autotel-cli-0.21.1`.

Results: all 15 controls and the supplied sample passed. `make validate` passed
in `/tmp/triage/autotel-cli-validation`, an isolated snapshot of repository HEAD
plus this triage's changes, using the Makefile's sibling release binary. The
shared checkout's validation encountered unrelated concurrent edits; those were
excluded from the isolated check and left untouched. The final Atomscan run
reported zero suspicious and zero hostile traits. Hopper moved this SHA-256 to
`good/mislabeled-unknown/autotel-cli-0.21.1.tgz`; the local archive was moved to
`/tmp/triage/misplaced-good/autotel-cli-0.21.1.tgz`.

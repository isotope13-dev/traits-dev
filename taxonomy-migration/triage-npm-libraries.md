# npm library triage

All three samples are **BENIGN**. Their SHA-256 hashes and bytes match the
exact-version tarballs returned by the npm registry. This establishes provenance;
the behavioral conclusions below also rely on source review.

| Sample prefix | Published identity | Observed behavior |
| --- | --- | --- |
| de0ff4a8db37 | @nx/eslint 23.2.0-pr.36866.449f6f3 | ESLint executor, workspace config discovery, AST-based config migration and generator package installation helper |
| d489fac68f5f | @tanstack/react-router 1.167.0 | Routing, React rendering, SSR hydration and application-provided script assets; installation examples inside exported documentation strings |
| d29fa5862922 | posthog-js 1.424.1 | Configurable analytics capture, feature flags, persistence, compression, opt-in site apps, remotely configured session replay and dynamic SDK asset loading |

No hidden install payload, credential theft or attacker-specific command channel
was identified. PostHog's CVV/CVC vocabulary participates in masking sensitive
fields. Its telemetry and replay capabilities are real and remain notable;
neutral identifier/schema references do not establish malicious collection.

Registry manifests and tarballs, facts output, initial and final scanner reports,
and source review artifacts are retained in the environment's
`scratch/triage-bad/` directory. Twenty direct runtime dependency tarballs were
also fetched for inspection. Because these archives do not lock dependency
resolution, range-bound dependency versions inspected here are examples, not a
claim that every future resolution is safe. Core-js's published postinstall is
a donation banner and CI/cache handling. Prepare scripts generally describe
maintainer build workflows.

The versioned PostHog recorder.js and surveys.js fetched from
`https://us-assets.i.posthog.com/static/1.424.1/` are byte-identical to the
corresponding bundled files. The referenced ESLint migration source at
`https://raw.githubusercontent.com/eslint/rewrite/e2a7ec809db20e638abbad250d105ddbde88a8d5/packages/migrate-config/src/migrate-config.js`
contains config transformation logic, with no fetch, eval, exec or spawn payload.
Samples and fetched scripts were inspected without executing them.

Possible explanations for the external labels: prerelease/package reputation
for Nx, scope-stripped package names and executable documentation examples for
TanStack, and minification plus tracking/session-replay capabilities for PostHog.
The original labeling rationale is unavailable; these are hypotheses.

Trait changes move lexical/schema references out of malicious objectives and
software identity into their actual capabilities or metadata. Named cloud
provider references belong under HTTP service identity; they do not demonstrate
public-suffix policy. JSON/Base64 proximity belongs under encoding, not an HTTP
body without transport evidence. Actual response parsing, React rendering and
function declarations use symbol matching to avoid quoted examples. Wrangler's
installPackages helper requires its autoconfig path context. Directory matching
excludes `.vscode/extensions.json`. A pre-existing curl exfiltration composite
was moved from lifecycle metadata into the HTTP upload objective, preserving its
conditions and severity while freeing the full lifecycle leaf.

The relocation mapping is in `triage-bad-moves.json`. Nineteen focused fixtures
exercise 37 positive/negative assertions, all passing. Final scans show zero
hostile and zero suspicious traits for each archive. Judgement markers are
written adjacent to each original sample, outside the traits checkout.

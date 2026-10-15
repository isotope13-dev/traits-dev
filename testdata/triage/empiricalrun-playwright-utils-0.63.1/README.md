# Empirical Run Playwright utilities 0.63.1 triage

Sample: `@empiricalrun/playwright-utils@0.63.1`

SHA-256: `5e82578c9b5940ecd84a7263e3fc383c3766853cb0b591c6744c4b130b8be10f`.

## Verdict and reviewed behavior

Benign browser-testing utilities. The supplied archive contains 214 regular
files and no links: 67 JavaScript files, one MJS harness, 68 TypeScript files
(mostly declarations), 66 declaration maps, two JSON files, eight Markdown
files, one patch and one TypeScript build-info file. Atomscan reports 205 entries
including the archive. JSON and maps parse successfully; the maps contain no
embedded source payloads. There are no npm installation lifecycle scripts.

The exported helpers and their implementation account for the notable behavior:

- Authentication helpers consume caller-provided Google credentials and an
  authenticator key; `AuthStore` saves and restores its own `auth/<key>.json`
  browser state. Extension state uses `chrome.storage.local`. No unrelated
  browser profiles, credential databases or user home secrets are searched.
- The configurable API client defaults to `api.empirical.run`, authenticates
  with `EMPIRICALRUN_API_KEY`, and serves test events, project KV, email,
  webhooks and the LLM proxy. Telemetry includes test/repository identifiers,
  overlay text and timing/token statistics; it does not dump the environment.
- Visual assertions and overlay dismissal send browser screenshots to the
  configured LLM proxy or the explicitly configured TypeSafe API. A CAPTCHA
  helper proxies solver tasks through the application's API. These are
  openly implemented automation capabilities; no hidden browser fingerprint
  evasion or unauthorized collection was found.
- Overlay dismissal caches generated code locally and executes matching cached
  actions using `AsyncFunction`. The existing compile trait records this
  capability as notable. The code is not an encoded package-install payload.
- Reporters upload configured test attachments, blob/HTML reports and event
  metadata. R2/S3 uploads require project/run and backend configuration.
  Credentials are supplied to the upload library; they are not separately
  posted to a collector. Uploaded attachments can be deleted to cap disk use.
- Child processes run Playwright test/merge commands or fixed disk-usage
  diagnostics. The shipped upstream oracle is an explicitly run parity harness
  that patches an upstream test fixture and compares report output.

Static source inspection and `cleave facts` were used; the package and its
network-facing helpers were not executed. This review covers the supplied
archive, without following registry dependencies or claiming publisher trust.

## Trait repairs

1. Moved both R2 environment-member matchers and their transparent union from
   `objectives/credential-access/env/secrets/cloud-access` to
   `micro-behaviors/os/env/cloud`. Matchers, platforms, file types and notable
   criticality are preserved. Their presence establishes credential-variable
   access rather than theft. Exact consumers now reference the neutral IDs.
2. Moved the CAPTCHA/taskId lexical association to
   `micro-behaviors/communications/http/services/captcha`, naming its actual
   evidence: CAPTCHA text near a taskId field. The image-result consumer now
   references the relocated trait. This does not establish submission or abuse.
3. Added `micro-behaviors/os/security/auth/session::browser-storage-state-save`
   for parsed `storageState({path: ...})` calls. A snapshot with no file
   destination, a configuration property, comments and strings do not match.
   An AST query is needed because the current symbol projection omits call
   targets rooted in `this`, including this sample's chained storageState call.

The six source-ancestor selectors use ordinary `any` clauses. Appending the
three exact moved R2 members preserves their original selectable member sets
and cardinality. Effective file-type gates still apply to Python/Ruby consumers.
The five destination-ancestor references intentionally recognize R2 as another
cloud-credential access: one credential-read roll-up, one credential-flow rule,
and three exclusions preventing generic telemetry/OAuth suppression in the
presence of cloud credentials. None gains a new threshold-counting role.
`selector-audit.json` records these references. No CAPTCHA or session ancestor
selectors were present. No package-specific exclusion was added.

## Checks

Run the focused cases from the repository root:

```sh
python3 testdata/triage/empiricalrun-playwright-utils-0.63.1/check.py
make validate
```

The ten cases cover R2 reads, its Cloudflare-prefixed spelling, literal/comment
near misses, CAPTCHA/task vocabulary versus unrelated task IDs, and browser
state saves versus passive references and snapshots. Transparent union findings
are elided from JSON by the engine; a separate `test-rules` trace verifies that
the R2 union remains available to consumers.

The final archive scan has zero suspicious and zero hostile findings, and emits
the relocated R2/CAPTCHA observations plus the new browser-state save finding.
Raw facts, scan outputs and validation logs are under
`/tmp/triage/empiricalrun-playwright-utils-0.63.1/`.

Validation completed successfully: all 10 focused cases passed, the R2 union
matched in `test-rules`, and `make validate` passed every configured corpus
(including hostile 668/668, benign 1478/1478 and does-nothing 176/176).

Hopper moved the sample from incoming to `good/mislabeled-unknown`.
The local archive was moved to
`/tmp/triage/misplaced-good/@empiricalrun-playwright-utils-0.63.1.tgz`.

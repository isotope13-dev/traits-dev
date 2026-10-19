# Argent engine version drift

Verdict: **BENIGN**, `@whyshu/argent-engine@0.7.4`.
Sample SHA-256: `3f9a86a0a823257a9fa71c0c69adbba61c26a22423bf37ca8a0b49686770fdb8`.

Compared the supplied archive with registry-fetched `@whyshu/argent-engine@0.7.3`.
The previous tarball has SHA-256
`3f59d3df735774bbdf7ebf0dc3ea3749585e666d33a6510c30776313b75083b0`;
its npm SHA-1 was verified against the registry packument. Across 341 old and
352 current files, there are 14 additions, 3 deletions, and 28 modified files.

## Decisive code differences

`daily-report.mjs` adds report tables, comparison windows, advertising summaries,
and `publishReportPayload()`. The new function reads the configured bridge
secret, returns without sending if none is available, and authenticates a POST
to the configured ERP service using `x-appointment-secret`. Its body is
`JSON.stringify({ reportDate: payload.date, payload })`. `buildReportPayload()`
selects store names, sites, sales totals, comparisons, stock and alert rows;
it does not copy the store's OAuth credentials or the environment object.
The ERP upload can also be disabled through the existing configuration picker.
The prior release lacked this upload, explaining the new credential-flow lead.

Reviewed execution order through `main()`, report collection/building, ERP
publishing, and Lark notification helpers. Dry-run and JSON-output paths return
before publishing. The environment passed as a helper argument is configuration,
not a serialized environment dump. Source-local may-flow events conflated the
header secret with the body. An isolated V8 probe of the reviewed builder and
publisher, with mocked network and synthetic credentials, confirmed that the
bridge credential appears only in the header and store access/refresh tokens
are absent from the request body. No package entrypoint was executed.

The rest of the diff adds configured ERP job/appointment workers, explicit
browser automation for shipment scheduling, read-only advertising reports,
order pagination/completeness fixes, a local persistent browser, and session
format compatibility checks/patches. Workers use configured tenant credentials
and typed business operations; the runner restricts its task-board destination
to loopback. Browser JavaScript literals operate on calendar/booking DOM state.
The old ad hoc installers are removed. These changes fit the ecommerce
workflow engine's purpose; the reviewed changes contain no concealed payload
or unauthorized credential collection.

`engine/scripts/init-ml.sh` is byte-identical to 0.7.3. It installs the missing
Lark CLI as an explicit setup operation. The fetched `@larksuite/cli@1.0.98`
archive matches the supplied dependency SHA-1
`e322326488f05ad2afd8e0381b6a4c5e1e8e6206`.
Compared it with registry-fetched 1.0.97 (SHA-256
`2b95fd9a534df8cafb41099f1a9f22c3121ea5b5dc162904d6563b61840ef6a6`).
Both have nine files: only package version, release checksums, changelog and
READMEs change. `scripts/install.js`, `scripts/run.js` and
`scripts/install-wizard.js` are byte-identical between releases.

The CLI's postinstall invokes **install.js**, which downloads a platform release
archive, verifies its bundled SHA-256 checksum, extracts the binary and sets
executable permissions. It never loads the wizard. **run.js** loads the wizard
only for the explicit `install` subcommand; that wizard invokes global skill
setup. The previous detector pooled the lifecycle declaration with a command
in a wizard's retry message, without connecting the two execution paths.
Release binaries and remote skill contents are outside these npm artifacts;
this review does not claim to have executed or analyzed those external bytes.

## Trait corrections and coverage

- The environment-body objective now requires explicit secret-environment JSON
  serialization or a returned credential-environment object for JavaScript/TypeScript,
  instead of a credential read anywhere in the file. The returned-object alternative
  retains helper-built payloads such as the existing npm-agent secret fixture. Its description states material plus HTTP-body evidence, rather
  than claiming proven data flow. The existing Go alternative remains intact.
  This deliberately narrows the candidate inference; it is not a universal
  interprocedural taint analysis.
- The skill objective matches an actual `scripts.postinstall` declaration with
  `npx skills add` at command position. It does not correlate an arbitrary
  archive member with a lifecycle hook. Direct and chained hook declarations
  still fire; helper-script reachability requires separate evidence and is not
  inferred by this rule.
- Global npx skill-add/remove command text moves to
  `micro-behaviors/os/package-manager/reference-install`, at notable severity,
  with descriptions limited to command references. Matcher and effective file
  scopes are retained. Command text deliberately stops contributing to
  `process/create` ancestor selectors, since it does not prove a launch.
  Optional agent-name and registration-wording fragments
  are retired: neither proves registration or hook reachability, and the new
  declaration matcher no longer consumes them. This is an intentional removal
  of weak corroboration, not a benign-package allowlist.

Run `python3 testdata/argent-version-drift/check.py` for seven static controls:
header-only authentication, direct and helper-built environment collectors, an explicit CLI wizard,
direct/chained lifecycle skill commands, and a quoted diagnostic in a hook.
The command-reference observation is required on the explicit wizard. Fixtures
are generated outside `testdata` to avoid test-path suppressors; no fixture code
runs. Use `--staging-parent PATH` to choose the temporary directory parent.

The broad `json-stringify-env-alias-body` composite also fired on the report:
its required evidence was only a secret-request candidate and a JSON call.
It is renamed to `secret-http-flow-with-json-call` with a co-occurrence description;
its matcher, scope, criticality and consumers are preserved. Consumer references
and the existing alias regression case IDs follow the rename. No claim that
an alias or body is flow-bound remains in this neutral finding.

The existing `testdata/taxonomy/github-api-auth-env-body/check.py --cleave cleave`
controls also pass. After the corrections, an `atomscan` rescan completed and
Cleave JSON confirmed **zero suspicious and zero hostile traits** across all
353 analyzed units of the supplied package and the 10 units of the flagged CLI
dependency. Engine-reported flow limitations remain; manual source tracing and
the release diff supplied the decisive evidence.

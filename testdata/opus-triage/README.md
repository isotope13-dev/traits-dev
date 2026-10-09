Triage regression controls
==========================

Positive and negative controls were scanned with `cleave --traits-dir . --format json`.

* Wallet validator: `wallet-validator.js` matches the wallet seed validator;
  `database-seed.js` does not.
* Shell profile: `profile-path.js` matches the shell login path;
  `profile-property.js` does not.
* Port listener: `listener.js` matches the JavaScript port-3000 call;
  `listener-comment.ts` does not.
* AWS bundle: `aws-bundle.js` matches the bundled SDK module marker;
  `aws-consumer.ts` does not establish SDK identity.
* ClawMetry: `clawmetry.js` matches product observability wording;
  `observability-consumer.ts` does not establish product identity.

The two project-rewrite composites moved from the install-hook objective leaf
into the existing filesystem write target leaf. Their evidence establishes
archive-wide setup co-occurrence, not a supply-chain compromise. The generic
initProject call atom was removed: neither the call name nor the manifest
postinstall name binds that helper to the install entrypoint. All exact and
ancestor references were audited. The removed objective directory only had an
ancestor consumer in windsurf-mcp-injection, which still has explicit lifecycle
alternatives. The write-directory consumer js-build-config-near-file-write
continues to require a nearby build config reference; these archive-scoped
setup composites do not establish direct configuration modification.

Both provided Opus archives have identical postinstall, materializer and Stop
hook bytes. Setup installs local skills, instructions and checking hooks,
checks the resolved dependency instance, preserves changed managed files,
and has an OPUS_SKIP_INIT opt-out. Runtime networking belongs to normal HTTP,
S3, Anthropic, PostgreSQL and application adapters. No hostile payload or
credential exfiltration was found. Both were judged BENIGN.

The fetched react-resizable-panels 4.14.3 dependency is a benign React layout
library. Its localStorage reads/writes persist panel and grid geometry; there
is no install hook, outbound client or executable payload. Its scan also
reported zero hostile and suspicious traits.

Full validation exposed two historical expectation errors. The synthetic
local setup archive only writes empty settings, instruction files and a
shell shebang: it moved to the benign corpus with both setup capability
traits required. The wallet theft fixture still requires both wallet seed
and mnemonic header exfiltration traits. Its minimum is two hostile
findings rather than three: a generic seed validation function name does
not independently prove wallet handling. The suspicious HTTP header
observations and original score floor remain required.

Validation also exposed a generic tiny Node postinstall manifest being
classified as a supply-chain loader. That unchanged manifest matcher moved
to metadata/package/scripts/lifecycle at notable, without an attack mapping.
Its only exact reference was a comment; ancestor install-hook consumers
still have explicit lifecycle observations. Local setup now has no
suspicious or hostile intent finding.

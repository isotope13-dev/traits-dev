# Canonical observations: nine duplicate pairs, 2026-09-27

This report preserves the nine-pair checkpoint. The subsequent
[member-name consolidation](MEMBER-NAME-CONSOLIDATION.md) resolves three more
pairs and implements the platform-equivalence validator correction below.

The improved validator exposed 14 shared-matcher pairs. **Nine pairs now use
nine canonical observations instead of 18 definitions.** Five pairs remain for
context/scope review. The [original candidate list](duplicate-review.json)
records each disposition; the [mapping ledger](duplicate-consolidation-mapping.json)
records effective definitions before and after consolidation.

## Canonical homes

| Observation | Home and boundary |
|---|---|
| sqlite3, express, request and expresso dependency declarations | `metadata/package/dependencies/manifest/identity`. A declaration proves neither attacker intent nor identity of the analyzed library. |
| Preact dependency declaration | The same manifest leaf. It proves neither an executed import nor a test fixture. Helper-fixture composites retain their independent private-package/path/manifest evidence. |
| `BASH_ENV` | `micro-behaviors/os/env/runtime`. This shell-startup setting exists outside CI; CI objectives add CI-specific evidence. |
| At least 256 exports | `metadata/binary/symbols/count`. URLMon and registry consumers share the exact count observation, with their other requirements unchanged. |
| `java.io.tmpdir` in class strings | `micro-behaviors/fs/path/temp`. A property reference does not prove reading the property or writing a staged file; the staging composite retains its write requirement. |
| `Zone.Identifier` | `micro-behaviors/fs/path/stream`. A stream name does not establish removal; removal composites retain their additional evidence. |

The Preact pair revealed a circular suppression: a bare declaration was itself
filed as fixture evidence, then the ordinary dependency observation excluded
the fixture directory. Removing that duplicate fixture atom lets ordinary
packages keep their declaration without claiming to be test fixtures.

## Scope and intentional changes

Predicate bodies and quantitative bounds are preserved. The canonical npm
declarations retain the broader Unix coverage, using the larger former
confidence where values differed. sqlite3 retains its existing JSON scope;
this intentionally makes a neutral declaration observable in JSON on the
additional Unix platforms too. The other declarations have the same file scope.

The BASH_ENV observation retains GitHub Actions coverage. Directory-based CI
consumers intentionally lose BASH_ENV-only evidence: shell-startup configuration
does not establish CI. Exact consumers now reference the runtime observation.
The export-count and Zone.Identifier atoms retain the union of file scopes
with unchanged platform scope. The temporary-directory property retains its
existing path scope and baseline criticality. The Preact declaration becomes
notable, consistent with neighboring named dependencies, and loses the circular
fixture exclusion. These are documented changes to placement/verdict weighting;
they are not a claim that every prior score stays identical.

All five destination directories remain leaf-only and contain respectively
74, 6, 40, 85 and 5 rules. No exemption or overflow directory was introduced.
All 18 original definitions resolve to the nine verified effective definitions
in the ledger, and active references no longer name retired IDs.

## Verification

**1,623 fixture checks pass in soft mode:** 248 hostile, 348 benign,
175 does-nothing, 45 drop-exec, 572 supply-chain, 66 impact-wipe,
82 obfuscation, 22 reverse-shell and 65 simple-stealer.

Four new controls cover ordinary shell startup configuration, a stream-name
reference without removal, an ordinary Preact manifest and a private declaration
helper. They require their canonical findings and distinguish actual fixture
context from mere dependency presence. Local `atomscan --format=json` confirms
scores 2, 1, 4 and 3 respectively and the expected category boundaries.

One full-suite attempt caught a concurrently edited reflection YAML file in an
unparseable state. It parsed normally on reinspection; rerunning passed without
editing that unrelated file. The latest policy inventory still has **176
oversized directories**. Five duplicate-review pairs remain; a passing soft
fixture run does not imply strict validation passes.

## Remaining pairs and validator follow-ups

- Three key-member pairs span credential-member and fixture directories, with
  different file-type/platform combinations. Establish one ownership contract
  and review every suppressing consumer before merging; a Cartesian scope
  union can change where an exception applies.
- Archive parser errors have different format/exclusion conditions. Factor
  shared raw error evidence while retaining contextual conditions; unioning
  exclusions can suppress legitimate diagnostics, and intersecting them can
  expose expected wrapper diagnostics as corruption.
- The DOS pair's `B4 52 E8` prefix alone does not prove that the called routine
  invokes DOS interrupt 21h. Inspect specimens and consumer requirements before
  keeping an API claim merely because its two bodies match.
- Platform equivalence deserves a regression test using Unix and BSD members.
  Symmetric platform-filter overlap is not set equivalence: `[unix, windows]`
  covers more concrete platforms than `[linux, macos, windows]`. A duplicate
  diagnostic must not hide that difference when suggesting a merge.
- Fixture-directory evidence used as an exclusion should be audited for
  circular or overly broad suppression, as the Preact example demonstrates.
  Treat this as a candidate semantic check; raw directory size alone cannot
  decide whether an exclusion is valid.

# Supply-chain engine review

Reviewed 2026-09-14. This supersedes the initial blanket implementation list.
Low detection counts do not establish a parser or engine defect. The initial
review did not demonstrate a defect from that list. Resumed analysis found
and fixed a narrower Elixir argument-extraction bug, documented below.

## Decision rule

Fix reproducible loss or corruption of facts the engine already promises to
provide. Prefer existing literal, symbol, argument, value, metric, tree-sitter,
and scoped-composite matchers for detection logic. Add a new engine feature
only when a concrete detection needs information those mechanisms cannot
express, and the benefit justifies parsing cost, maintenance, and ambiguity.
Do not require recognizing the benchmark's environment gate for detection.

## Current corpus triage (2026-09-16)

- [x] Preserve positive random-file gates as activation controls; keep them out
  of hostile composites so static findings do not depend on the gate.
- [x] Repair and validate AUR, C, Homebrew, and Go coverage using existing
  cached values, symbols, arguments, and scoped composites. No engine feature
  was needed.
- [x] Full scan: 599 roots, 227 with hostile IDs and 372 without. Evidence:
  `/tmp/sc-current-gopass2.XXXXXX.jsonl` (SHA-256
  `8b30153bff22ac8b71bdc2cce642684db6b7160c852c5d20e54b415939103dfa`).
- [ ] Continue semantic review of the remaining zero-hostile roots; do not
  promote a package from suspicious to hostile on a gate, schedule, or network
  fetch alone.

## Cron review follow-up (2026-09-15)

- [x] Reproduce ordinary recurring HTTP scheduling falsely labeled hostile in
  Node. Remove the unsupported hostile composite and its disconnected
  credential-filter derivative; retain the actual exfiltration rule.
- [x] Replace the generic suspicious crontab-string observation with a neutral
  cached call-argument matcher under `micro-behaviors/os/autorun/cron`.
  No parser or engine feature is needed. The benign control scores 6 with no
  suspicious or hostile findings; all eight validation suites pass.
- [x] Rescan all 600 current-corpus packages with copied rules and verify every
  report path/hash against the unchanged inventory. 179 have 1–3 hostile IDs;
  421 have none. Evidence: `/tmp/sc-cron-review.4a6Iyo/` and the audit document.
- [ ] Review the 421 zero-hostile packages and recheck the semantic accuracy of
  positive results. A recurring heartbeat establishes a persistence mechanism
  but does not by itself establish C2, exfiltration, or hostile intent.
- [ ] Review surviving Node cron-plus-process and native multi-surface
  persistence composites for disconnected evidence and legitimate scheduled
  maintenance. Do not strengthen verdicts from scheduling alone.

## GNOME review follow-up (2026-09-15)

- [x] Detect Kelpstreamsync's keyring stdout-to-HTTP pipeline with one hostile
  objective and meaningful neutral source/transport observations. Use cached
  provenance for the source and tree structure only for the otherwise missing
  adjacent-literal pipeline relationship. No engine feature is necessary.
- [x] Verify disconnected, discarded-output, literal-body, and help-text
  controls, plus gate removal, hostname replacement, and API alias/sync variants.
- [x] Repair the keyring package's legacy-module compatibility metadata without
  altering its script or gate. Revalidate the repacked archive and all suites.
- [x] Rescan five roots: 941 reports, 957 inventory entries, no unexpected or
  duplicate reports, all reported hashes correct. Current corpus: 180/600 with
  1–3 hostile IDs and 420 without. Evidence: `/tmp/sc-gnome-review.47Tiuz/`.
- [x] Repair the other nine GNOME fixtures' incorrect 45/46 declarations.
  Preserve all gates. Move the bus-address-only fixture out of hostile data;
  do not infer keylogging from its label or active persistence from an unenabled
  systemd unit.
- [x] Repair D-Bus's digit-leading well-known-name component and Nautilus's
  API-version, GObject inheritance, and single-FileInfo handling mistakes.
  Static syntax/member checks pass; runtime integration remains unverified.
- [x] Add neutral cached GLib process-spawn and file-write observations, with
  a negative control that distinguishes documentation strings from API calls.
  All validation suites pass. Five-root comparison has no hostile-ID changes
  among retained files; corpus now 599 with 184 hostile packages and 415 zero.
- [ ] Continue GNOME screenshot, overview-text, and Nautilus filename-upload
  coverage. D-Bus naming is repaired, but actual activation remains a separate
  question. Evidence: `/tmp/sc-gnome-quality.q7xJXA/`.

## Item-by-item disposition

| Original proposal | Assessment | Decision |
| --- | --- | --- |
| Recursive package archives | Existing functionality; the suspected Hex failure did not reproduce. A fresh scan analyzed and extracted the Elixir source inside `contents.tar.gz`. Existing nested ZIP/tar tests are also present. | Close the blanket task. Reopen only for a specific failing archive or extraction mode. |
| Container identity and member lineage | Nested paths are preserved in the fresh report. Rules already support `scope: outer`, `scope: archive`, and sibling-file value lookup. Copying ancestor identity into every member is unnecessary for those uses. | Use the existing scope mechanisms. Fix propagation only if a correctly scoped rule demonstrably loses evidence. |
| JVM strings and process arguments | `class.strings` and resolved imports already exist. Recovering ordered arguments or runtime concatenations would require additional bytecode analysis; unrelated pool strings do not prove a call relationship. | Use existing pool values/imports when sufficient. Defer bytecode argument reconstruction until a concrete rule requires that relationship. |
| Environment comparison / activation facts | Source calls, argument predicates, tree-sitter queries, literals, and `is: random_like` are available. A dedicated activation schema would encode benchmark-oriented interpretation. An environment read plus a random string does not prove a comparison or gate. | Drop the new schema. Use accurate trait-level observations where useful; the harmful-behavior verdict must stand without the gate. |
| Embedded shell / PowerShell reconstruction | Embedded-code analysis and source escape decoding already exist. Broader concatenation or interpreter handling may be a feature, but low match counts alone do not establish a missing path. | Drop the blanket implementation. Reduce a failing case first; repair an existing decoder if wrong, or justify a bounded extension if essential. |
| Invisible Unicode normalization / metrics | `text.invisible_chars`, `text.unicode_escape_count`, and decoded source literals already exist. Actual invisible source bytes and escape spellings are distinct measurements and should not be conflated. | Use existing metrics/literal predicates. Only fix demonstrated incorrect language-specific decoding; do not add duplicate counters. |
| Universal build/lifecycle facts | Manifest value predicates, source symbols/tree shape, and existing lifecycle traits can describe the concrete ecosystem behavior. A second normalized schema would duplicate much of this. | Drop the schema; address actual missing lifecycle coverage in traits. |
| Image-channel, LSB, write, and execution facts | PNG dimensions/channel count, pixel/channel entropy, and other image metrics already exist. Source API/argument/tree predicates can describe bit extraction, writes, and execution. Pixel statistics alone cannot establish a payload. | Drop the combined schema and speculative LSB metrics. Require a concrete unavailable relationship before extending flow analysis. |
| First-party versus build-cache provenance | Member paths already expose cache locations. A directory name does not establish authorship or trust; cache content can itself be modified. | Drop inferred first-party attribution. Use path metadata for context and inspect/report member evidence without automatic cache-based suppression. |

The code inspections above establish available mechanisms, not exhaustive
language coverage or proof that every existing implementation is correct.

## Evidence and corrections

- The earlier `/tmp/sc-corpus-320-cleave.json` contains **42** top-level reports,
  despite its filename. Its absence of Elixir reports cannot establish that
  nested Elixir files were skipped. The separate
  `/tmp/supply-chain-corpus-after-pass3.jsonl` contains 320 reports; it is a
  different artifact.
- A fresh static scan, with both caches disabled, of
  `elixir/hex-ambercore-systemd-timer-linux.tar` produced an Elixir member at
  `...tar!!contents.tar.gz!!lib/ambercore.ex` and extracted it successfully.
  Report: `/tmp/sc-engine-hex-audit.json`; extracted tree:
  `/tmp/sc-engine-hex-audit`. No package code was executed.
- Archive recursion is already implemented and tested in
  `../cleave/src/analyzers/archive/mod.rs`
  (`test_nested_archive_zip_containing_tar_gz`).
- `RULES.md` documents call/argument predicates, tree-sitter queries, composite
  scope, and sibling-file value lookup. The distribution composite originally
  inspected in `objectives/supply-chain/trojanized/dist/portable-package.yaml` had no explicit
  scope; the later precision review below removed this redundant verdict
  wrapper rather than adding another identity-propagation feature.
- `../filefacts/src/formats/class.rs` emits `class.strings`, class references,
  and resolved imports. Its constant pool is not an ordered process argument
  list; do not infer those relationships from co-occurrence.
- `../filefacts/src/formats/source/escapes.rs` supplies decoded literal and
  argument values; `source/text_metrics.rs` emits invisible-character and
  escape counts. `../cleave/src/analyzers/embedded_code_detector.rs` already
  analyzes embedded code with resource bounds.
- `../filefacts/src/formats/png.rs` already emits `image.channels`,
  `image.pixel_entropy`, `image.r_entropy`, `image.g_entropy`,
  `image.b_entropy`, and related metrics.

## Revised TODO

- [x] Assess all nine proposals for existing support and trait alternatives.
- [x] Reproduce the suspected Hex recursion/extraction failure: it did not fail.
- [x] Correct the inference drawn from the incomplete extraction scan artifact.
- [x] Remove unconditional engine-feature and rebuild requirements.
- [x] Resume analysis using existing fact surfaces, checking composite scope and
  matcher choice first. This is follow-up analysis, not an engine prerequisite.
- [ ] For any remaining suspected defect, record a minimal reproducer, expected
  fact, actual fact, and why a trait cannot solve it; fix confirmed bugs with a
  focused regression test. This is a conditional workflow, not a feature backlog.

## Resumed analysis: Elixir

### Confirmed parser bug: dropped call arguments

`System.cmd("printf", ["hello"])` produced a correctly named call with an empty
argument list. Elixir's grammar exposes `arguments` as an immediate named child,
not a field. Both symbol and value-flow extraction incorrectly used field-only
lookup. A shared grammar lookup in `../filefacts/src/formats/source/langs.rs`
now handles this node shape; both consumers use it. No new fact schema or
activation-gate inference was introduced.

- Two regression tests failed before the fix and passed afterward. They cover
  parenthesized and unparenthesized calls, agreement between symbols and flow,
  nested calls, zero-argument calls, and excluding do-block contents.
- Filefacts integration suite: 39 passed.
- Filefacts unit suite: 1,353 passed, 4 ignored.
- `cargo clippy --offline --all-targets -- -D warnings`: passed.
- Cleave rebuilt using a command-line local dependency override. Its lockfile
  was restored afterward; the parser fix remains a local source change, not a
  published dependency update.
- End-to-end positive/negative scanner checks confirm first-argument matching
  and HTTP method matching. Comments, quoted examples, later arguments, and
  HTTP GET do not trigger the new shell/systemctl/POST traits.
- Rebuilt `../scan/target/release/atomscan` with local cleave/filefacts overrides
  and restored its lockfile afterward. The final verification run produced 22
  reports: 19 retained Elixir packages, two harmless matcher controls, and the
  relocated timer package. Results: `/tmp/sc-elixir-verified.jsonl`.
- Final `make validate` passed: hostile 54/54, benign 20/20, does-nothing
  176/176, drop-exec 43/43, impact-wipe 66/66, obfuscation 80/80,
  reverse-shell 25/25, simple-stealer 65/65. Log:
  `/tmp/sc-traits-validate-complete.log`.

### Trait coverage and false positives

- Added fact-based Elixir observations for external programs, shell invocation,
  systemctl, HTTP POST, DNS resolution, environment reads, file reads, and
  Base64 decoding. Consolidated the prior text-based shell atom from the
  reverse-shell directory into the neutral shell capability.
- Existing encoded-shell indicators excluded Elixir even though the decoded
  payload was already available. Extended those existing rules and composed
  them with Elixir decoding and shell invocation. The Base64 reverse-shell
  fixture now receives a hostile finding without an activation-gate predicate.
- Removed the false hostile systemd-timer composite and its misplaced atoms.
  Scheduling a timer and enabling a user unit do not establish remote-command
  execution or a dropper. Retained a neutral timer-directive observation.
- The ambercore timer fixture now has zero suspicious/hostile findings. It only
  installs an opt-in periodic HTTP request. Following x-triage-bad, moved it to
  `/tmp/triage/misplaced-good/hex-ambercore-systemd-timer-linux.tar` (recoverable).
  SHA-256: `725eb0e1afe1160ed111b7d8c80b64aaf19bad638501e81576840c2cade169bc`.

### Remaining work

- [ ] Finish the remaining Elixir behavior analysis; neutral capability coverage
  does not yet imply complete hostile-behavior coverage. In particular,
  `hex-duskwellstack-onload-env-exfil-linux.tar` now exposes POST, environment
  read, and file read, but still lacks an exfiltration verdict. Its piped
  transformations and credential selection need a precise trait-level review.
- [ ] Continue other languages from a fresh inventory. Other work is adding
  packages concurrently, so the old 320-package count is not a current baseline.
- [ ] Verify the normal release/install workflow includes the parser fix before
  assuming deployed binaries have it. Concurrent work has since committed the
  fix as filefacts `78811c8` and advanced cleave's dependency; local verification
  builds and dependency commits are not proof of deployment.

### Continued Elixir analysis: credential selection and lifecycle precision

- Fixed two existing path-coverage omissions: quoted `.netrc` source literals
  now match the canonical path rule, and Docker config paths apply to all
  supported source languages. Added the Elixir full-read atom to the existing
  file-read umbrella rather than introducing a second composite.
- Added a structural observation for selecting secret-named process environment
  entries. It requires `System.get_env()` piped into `Enum.filter`, tests the
  tuple key rather than its value, and requires the regex test to be the entire
  returned body. A discarded test followed by `false` reproduced a false
  positive in the initial query; anchoring the body fixes it in YAML.
- This observation belongs under `micro-behaviors/os/env/secret-name`, at
  notable severity. Selecting sensitive settings locally is not by itself a
  credential-theft objective. No exfiltration verdict was added from unrelated
  same-file POST/read calls, and no rule depends on the activation gate.
- Added an `@on_load` callback observation. Full validation exposed a separate
  pre-existing rule bug: `elixir-top-level-module-call` used a line-anchored
  regex, which also matched calls inside ordinary function bodies. It now
  matches a direct source-root, zero-argument call with the existing tree-sitter
  matcher. Ordinary entry calls remain baseline syntax; the explicit load
  callback is notable. No generic-call severity upgrade is necessary.
  This was not a new engine defect or a reason to add lifecycle facts.
- Fixed the generic low-bit-mask matcher treating Elixir's `&1` argument capture
  as bitwise AND. The infix form now requires a left operand and a numeric
  boundary. Moved the bit-mask and XOR syntax atoms to the existing neutral
  `micro-behaviors/data/source/arithmetic` directory and updated their consumers.
  Word boundaries also prevent XOR substrings inside unrelated identifiers.
- Added five harmless regression fixtures with hierarchy assertions: secret
  selection, redaction/non-process inputs/value tests/discarded tests, C parity,
  source-root calls, and module-load callbacks. Standalone controls have no
  suspicious/hostile findings. The environment-selection fixture has no gate.
- Verification artifacts: `/tmp/sc-elixir-load-controls.json`,
  `/tmp/sc-elixir-current-controls.json`, and `/tmp/sc-elixir-source-final.jsonl`.
  The source snapshot still lacks a proven credential-to-upload relation;
  capability coverage is not complete attack detection.
- Fresh scans of the two regenerated packages are in
  `/tmp/sc-elixir-packages-final.jsonl`: the encoded reverse shell retains one
  hostile and four suspicious findings; the credential-upload package has the
  new capability observations but still no exfiltration verdict. Both reports
  have no scan errors. Package code was not executed.
- Final validation passed: hostile 54/54, benign 25/25, does-nothing 176/176,
  drop-exec 43/43, impact-wipe 66/66, obfuscation 80/80, reverse-shell 25/25,
  simple-stealer 65/65. Log: `/tmp/sc-traits-validate-elixir-complete.log`.
  `git diff --check` also passed. No additional engine changes were required
  for this pass.
- Corpus packages are being regenerated concurrently, including a replacement
  at the previously relocated timer path. The earlier relocated bytes remain
  in `/tmp/triage/misplaced-good`; no replacement package was moved this pass.
  Fresh package verification is recorded separately from extracted snapshots.

### Confirmed parser bug: Elixir heredoc values

- While inspecting the keychain specimen's facts, a normal `@moduledoc`
  heredoc exposed a value-corruption bug: both literal and argument decoders
  removed one quote at each end instead of three, and retained heredoc margins.
  This can defeat exact/anchored literal and argument matchers. It is not a
  reason for trait authors to match incorrect values.
- Two harmless integration regressions failed before the fix. A shared,
  Elixir-only normalization helper in `../filefacts/src/formats/source/escapes.rs`
  now strips the delimiters, initial newline, and closing-delimiter indentation
  before existing escape decoding. Both literal and argument extraction use it;
  flow receives the same corrected argument value. Other languages keep their
  existing behavior. Source offsets and the single-parse contract are preserved.
- Semantics reference: [Elixir strings and charlists](https://elixir.hexdocs.pm/1.18.1/syntax-reference.html#strings).
  Tests cover strings/charlists, empty bodies, relative indentation, tabs,
  Unicode, escapes, malformed boundaries, and ordinary multiline strings.
- Filefacts verification: 41 integration tests and 1,354 unit tests passed,
  four unit tests ignored; clippy with `-D warnings` passed. Logs:
  `/tmp/sc-heredoc-before.log`, `/tmp/sc-heredoc-integration.log`,
  `/tmp/sc-heredoc-unit.log`, and `/tmp/sc-heredoc-clippy.log`.
- Trait validation passed with the same totals as the previous pass:
  `/tmp/sc-traits-validate-heredoc-pass.log`. This verifies the unchanged trait
  set, not downstream adoption of the new parser fix. No cleave/atomscan rebuild
  or dependency publication was performed for this fix in this pass.
- The credential-upload relationship remains open. Inspection confirms that
  Elixir's assignment, function-definition, and pipeline shapes are not covered
  by the existing shared-flow adapter in the way this specimen needs. Supporting
  that chain is a semantic-coverage feature, not the earlier argument-list bug;
  no co-occurrence shortcut or benchmark-specific flow fact was added.

### Corpus refresh and zero-width decoding triage

- Refreshed the growing corpus with static atomscan scans. The final snapshot
  contains 560 unique package reports across 16 languages, with no empty reports
  or scanner diagnostics: `/tmp/sc-corpus-triage-complete.jsonl` and
  `/tmp/sc-corpus-triage-complete.stderr`. No package code was executed.
- Snapshot counts: 205 packages have a hostile finding, 215 have a suspicious
  finding (these sets overlap), and 290 have neither. These are detection
  counts, not a ground-truth recall measurement or a completed semantic audit.
- The Elixir zero-width specimen had 340 invisible characters and a recovered
  literal consisting entirely of hidden symbols, but no suspicious/hostile
  findings. The relevant metric rule excluded Elixir; the old portable decoder
  matcher only recognized shifts, whereas this specimen multiplies indices.
- Added Elixir to the existing invisible-count observation. Added a neutral
  long-zero-width-string property, structural weighted-index arithmetic, and
  byte-list conversion observations. The new steganographic-decoding composite
  requires hidden data, a zero-width codepoint set, and both decoder mechanics.
  It is suspicious, not a claim that recovered bytes reach an execution sink.
  It requires no environment gate or gate name.
- Consolidated the duplicate supply-chain alphabet marker into
  `micro-behaviors/data/string/unicode::zero-width-format-codepoint-set` and
  updated all consumers. Cross-language verification caught and fixed a braced
  Unicode-escape regression before handoff. Existing JavaScript, PHP, and
  PowerShell package detections were preserved.
- Added one non-executing positive decoder fixture and three benign controls:
  hidden Unicode test data with documentation-only decoder code, an ordinary
  visible-alphabet decoder, and PHP braced escapes. The benign controls have no
  suspicious/hostile findings; the decoder pattern has one suspicious finding
  without inventing exfiltration or execution evidence.
- Verification artifacts: `/tmp/sc-zw-controls.json`,
  `/tmp/sc-zw-package-final.jsonl`, `/tmp/sc-zw-braced-final.jsonl`, and
  `/tmp/sc-elixir-zw-rescan.jsonl`. Full validation passed: hostile 55/55,
  benign 32/32, does-nothing 176/176, drop-exec 43/43, impact-wipe 66/66,
  obfuscation 80/80, reverse-shell 25/25, simple-stealer 65/65. Log:
  `/tmp/sc-zw-validate-complete.log`. `git diff --check` passed.
- Re-inspected the regenerated ambercore timer: still only an opt-in HTTP
  heartbeat, with no credential upload or downloaded-code execution. Following
  x-triage-bad, moved this replacement to
  `/tmp/triage/misplaced-good/26fadfa491ff/hex-ambercore-systemd-timer-linux.tar`.
  SHA-256: `26fadfa491ff3af38171efe9af5432af5e8d1514846460eb3f5c22f26bcb3703`.

### V1 Perl/PHP simulation-quality disposition

- [x] Review all 15 CPAN and 15 Packagist archives, including their package
  lifecycle triggers, resources, and decoded descriptions. Both ecosystems had
  real automatic execution paths, but every path terminated in the common
  temp-canary, fixed harmless child, and loopback-discard behavior.
- [x] Remove the 30 canary-only archives from hostile testdata. Meaningful repair
  would require behavioral replacement; all are recoverable from Git history.
- [x] Fix the PHP Run-key false positive without adding an engine feature. The
  duplicate objective atom treated a path string as persistence; the two actual
  persistence composites now reuse the canonical neutral registry-key atom and
  continue to require the `reg add` command plus payload context.
- [x] Review the 60 remaining v1 packages: Objective-C, Shell, Swift, and Zig.
  All had real lifecycle triggers but only canary behavior; all were deleted and
  remain recoverable from Git history. V1 now contains provenance metadata only.
  The earlier relocated copy was not overwritten. The retained corpus has 559
  packages; 289 of those had neither suspicious nor hostile findings in the
  final snapshot and remain candidates for review. This pass does not complete
  corpus-wide triage.

### Corpus refresh and hex-conversion classification fix

- A new static scan produced 434 unique package reports across 16 languages:
  `/tmp/sc-current-scan.jsonl`. Of these, 192 have at least one hostile finding;
  185 have neither suspicious nor hostile findings. These are observed verdict
  counts, not validated recall. The initial inventory contained 430 paths;
  concurrent additions occurred during scanning. Compare reports by package
  SHA-256 rather than treating successive inventories as identical.
- Confirmed a trait bug while inspecting a missed JavaScript DNS specimen:
  ordinary `Buffer.from(bytes).toString("hex")` was labeled as Ethereum
  recipient handling. The regex crossed the end of `Buffer.from` into the
  later encoding call, and did not require any recipient semantics.
- Removed that misplaced duplicate atom. Its recipient composite now reuses
  the existing neutral hex-decoding trait. Changed that canonical trait to a
  structured `Buffer.from` call with argument 1 equal to `hex`; this also fixes
  missed multiline calls and nested input expressions without an engine change.
- Four harmless regression fixtures cover encoding, multiline decoding,
  recipient decoding, and `hex` in the wrong argument or a nested call. All have
  zero suspicious/hostile findings. Genuine recipient conversion remains
  visible; ordinary converters no longer acquire blockchain identity.
  Before/after evidence: `/tmp/sc-hex-before.json`, `/tmp/sc-hex-after.json`,
  and `/tmp/sc-hex-negative.json`.
- Re-scanned all 35 JavaScript packages: `/tmp/sc-js-hex-after.jsonl`. All 35
  SHA-256 values match the initial scan. The misleading atom was removed from
  17 packages, with no hostile findings added or lost in the matched set.
- Full validation passed: hostile 55/55, benign 36/36, does-nothing 176/176,
  drop-exec 43/43, impact-wipe 66/66, obfuscation 80/80, reverse-shell 25/25,
  simple-stealer 65/65. Log: `/tmp/sc-hex-validate-final.log`.
- A temporary YAML-only provenance probe did not establish file bytes reaching
  the resolver in the DNS-case specimen. That miss is still open; no engine
  feature or hostile co-occurrence shortcut was added.
- Benchmark validity issue: static `ast.parse` rejects `amberlite/reach.py`
  inside `py/pypi-amberlite-dns-txt-cmdexec-linux.whl` at line 12 (unmatched
  closing parenthesis). Package SHA-256:
  `119bcddf5f4caa444306a9f44fa77c309240dd51d0f441ec3c3459a87be8c5ff`.
  The package was neither modified nor executed. Malformed source still needs
  defensive detection, but this artifact cannot establish runnable benchmark
  validity. Corpus-wide triage remains incomplete.

### Perl calls and encoded-payload evidence

- Reproduced two filefacts bugs using harmless Perl sources: static function
  and builtin callees were emitted without names, and a single argument's
  children were mistaken for separate arguments. A `function` leaf now names
  the callee, while dynamic code references remain unresolved. Both symbols
  and shared flow preserve a single argument as one value. No Perl assignment,
  pipeline, or interprocedural-flow feature was added.
- The name regression failed before the fix. After fixing names alone, the
  independent argument regression still failed; it passed after correcting
  argument handling. Tests cover qualified names, dynamic callbacks, comments,
  strings, zero/one/multiple arguments, and nested calls, with one parse shared
  across views. Filefacts: 43 integration tests and 1,354 unit tests passed,
  four unit tests ignored; clippy passed. Logs: `/tmp/sc-perl-parser-before.log`,
  `/tmp/sc-perl-names-only.log`, `/tmp/sc-perl-integration.log`,
  `/tmp/sc-perl-unit.log`, and `/tmp/sc-perl-clippy.log`.
- Decoder compatibility decision: missing Base64 terminal padding is a small
  justified extension, not a new security fact. It is used by the inspected
  Perl payload, and changing YAML file-type scopes cannot recover text the
  extractor rejects. Stng now permits partly or wholly omitted padding while
  rejecting excess/interior padding and nonzero unused trailing bits. Existing
  length, printable-text, quality, and short-token corroboration checks remain.
  Harmless regressions cover all length remainders, whole/embedded tokens,
  source offsets/extents, and malformed input. All 498 unit tests and clippy
  passed: `/tmp/sc-stng-padding-final-unit.log` and
  `/tmp/sc-stng-padding-final-clippy.log`.
- Confirmed a separate cleave propagation bug: the source analyzer dropped
  Base32/Base85 results already supplied by stng. Added the two omitted
  method/encoding mappings. The reproducer failed before the change; all 25
  unified-analyzer tests and clippy passed afterward. Logs:
  `/tmp/sc-source-codec-before.log`, `/tmp/sc-source-codec-tests.log`, and
  `/tmp/sc-source-codec-clippy.log`. This is preservation of existing decoded
  evidence, not a new decoder or schema.
- Added structured Perl Base64-decoder and Unix-shell-call observations,
  extended the existing encoded reverse-shell indicators to Perl, and added a
  payload-plus-capabilities composite. Its verdict does not inspect a gate,
  package API name, or exact endpoint. It does not claim proven value flow.
  Two harmless controls cover a decoder with a comment-only shell call and a
  `system` call to `printf`. The actual CPAN archive has a regression entry;
  package code was not copied into a new executable attack fixture.
- Development verification must disable **three** cache layers:
  `STNG_STRING_CACHE=0 FILEFACTS_CACHE=0 CLEAVE_SKIP_CACHE=1`. The string cache
  is independent of the filefacts and cleave cache switches; unchanged local
  library version numbers can otherwise reuse pre-fix decoded rows.
- Source snapshots for local cleave/atomscan builds live under
  `/tmp/sc-cleave-perl-build.f5Xw0W` and
  `/tmp/sc-atomscan-perl-build.gaE4Hn`. Their temporary lockfiles carry local
  dependency overrides; checkout lockfiles were not rewritten. The scan
  snapshot initially retained stng 1.11, so its temporary dependency was
  explicitly updated to the fixed local 1.12 before verification.
- The CPAN package changed during analysis: the original extracted source had
  wholly omitted padding, and the replacement had partly omitted padding.
  The extracted snapshot and replacement archive are separate verification
  targets; a successful standalone source scan does not establish archive
  coverage. Final archive/corpus validation is recorded separately below.

### Reclassified cron health checks

- Inspected every executable source member and package entry point in the
  JavaScript emberkit, Go foxtailpro, and Python wicklowcore cron packages.
  These expose opt-in scheduler/HTTP-health-check helpers, not secret uploads,
  fetched-code execution, or destructive actions. Do not strengthen a cron
  rule solely to force hostile verdicts on this behavior.
- Following x-triage-bad, verified their hashes and moved the three packages
  recoverably to `/tmp/triage/misplaced-good/cron-health-1a7904f7c5f0/`:
  - `npm-emberkit-crontab-persist-linux.tgz`:
    `1a7904f7c5f0ef686565842d99542bd6cd0e66c18769973ff43094a93579ba38`
  - `gomod-foxtailpro-crontab-persist-linux.zip`:
    `c42b6a5a9748ee9e427e2dc89016350e64914463322dd4d54d2c417ebcd93694`
  - `pypi-wicklowcore-cron-persist-linux.whl`:
    `6f3625c5ce7a99d1b0c9870fcce6cd3cce9047bcba67f39984ecadd5c703bde8`
  No package code was executed. Other cron specimens still require individual
  review; the three inspected packages do not establish their classification.

### Verification while corpus regeneration continues

- The user confirmed that another process is regenerating the corpus. Continue
  static triage against hash-identified evidence, defer a final coverage claim
  until the inventory is stable, and do not repeatedly relocate recreated
  packages. No generator or payload changes were made in this verification.
- Full regression validation passed: hostile 56/56, benign 38/38,
  does-nothing 176/176, drop-exec 43/43, impact-wipe 66/66, obfuscation 80/80,
  reverse-shell 25/25, simple-stealer 65/65.
  Log: `/tmp/sc-perl-validate-complete.log`.
- Fresh atomscan verification of the CPAN archive reports one hostile encoded
  reverse-shell trait. Its observed SHA-256 is
  `1550c6e6f108fa3f34b0b69507cde123b276a0903099b32277ca938a40d6da95`.
  Evidence: `/tmp/sc-perl-atomscan-package.jsonl`; stderr was empty.
- The concurrent corpus scan produced 546 unique package hashes across 16
  languages: `/tmp/sc-perl-corpus-current.jsonl`. Of these, 204 had hostile
  findings (192 had 1–3; 12 had more than 3), and 278 had neither suspicious
  nor hostile findings. These are observed verdict counts, not verified recall
  or a stable inventory. The CPAN result above also appears in this scan.
- Only 177 reports matched both path and hash in the earlier 434-report scan;
  none gained or lost a hostile verdict in that comparable subset. Changes in
  aggregate counts cannot be attributed to the parser/trait fixes while the
  generator and other trait work are active. Corpus-wide triage remains open.

### CPAN build-file routing and Perl method targets

- Confirmed a filename-routing bug, not a missing analysis feature:
  `Makefile.PL` matched the broad `Makefile*` filename rule before its Perl
  extension. Filefacts now recognizes that canonical CPAN entry point as Perl.
  Ordinary Makefiles and their `.debug`/`.in` variants retain their type;
  mixed-case names and `Build.PL` have regression coverage. A harmless
  integration test verifies that the original basename reaches the Perl parser,
  retains `WriteMakefile`, and shares one parse across fact views.
- Both filename and integration regressions failed before the correction.
  Logs: `/tmp/sc-makefile-unit-before.log` and
  `/tmp/sc-makefile-integration-before.log`.
- Confirmed a second call-projection bug: Perl method calls used the receiver
  as the callee, dropping the method. Both symbols and shared flow now resolve
  the method-call node itself. Simple scalar receiver spellings are retained,
  while computed receivers and variable method names remain unresolved. This
  names lexical calls; it does not infer receiver types or add assignment,
  collection-mutation, or interprocedural-flow support.
- The method regression failed before the fix and passed afterward. It covers
  qualified constructors, scalar receivers, chained calls, dynamic methods,
  computed receivers, comments, quoted examples, shared flow targets, and the
  single-parse guarantee. Final filefacts results: 1,355 unit tests passed,
  four ignored; 45 integration tests passed; formatting and clippy passed.
  Logs: `/tmp/sc-perl-method-before.log`, `/tmp/sc-perl-method-after.log`,
  `/tmp/sc-perl-method-unit.log`, `/tmp/sc-perl-method-integration.log`, and
  `/tmp/sc-perl-method-clippy.log`.
- Corrected two misleading POST observations: neither a `->post(...)` token
  nor a POST URL establishes LWP identity or exfiltration. Their canonical
  replacements live under `micro-behaviors/communications/http/post`, use
  structured method targets and URL argument positions, and are reused by the
  existing objective composites. The LWP beacon composite still requires its
  separate LWP import. No gate name or randomness check was added.
- Added harmless HTTP::Tiny and comment/dynamic-method controls. Both have
  zero suspicious/hostile findings; only the genuine static POST call receives
  HTTP POST observations, and neither is mislabeled LWP. Added a regression for
  the real CPAN archive without copying or modifying its executable payload.
- Verified the original archive, not just a renamed source probe:
  `cpan-hexaret-brackenstack-makefilepl-exfil-linux.tar.gz`, SHA-256
  `e24f6a5090478f927ea37325c2d4b4b1f20fb040d2642fcef6a4a9d4446ae81a`.
  Its `Makefile.PL` is now Perl, exposes `HTTP::Tiny.new` and `$http.post`,
  and gains one existing hostile credential-exfiltration finding (archive risk
  120). Static inspection confirms that the upload body contains the collected
  environment/file values; the composite itself remains a proximity signature,
  not proven value flow. Before/after: `/tmp/sc-makefile-before.json` and
  `/tmp/sc-makefile-after.json`; facts: `/tmp/sc-makefile-after-facts.json`.
- Rebuilt local cleave and atomscan through the existing temporary source and
  dependency snapshots; checkout lockfiles were not changed. Scanned a copied,
  stable set of all 35 Perl archives at `/tmp/sc-perl-routing-snapshot.fqhV6R`.
  Final evidence: `/tmp/sc-perl-routing-final.jsonl`, with empty stderr.
  All 35 hashes match the preceding Perl scan: one gained a hostile verdict,
  none lost one. Fifteen have 1–3 hostile findings; 18 have neither suspicious
  nor hostile findings and still require review. These are verdict counts,
  not validated recall.
- Full validation passed: hostile 57/57, benign 40/40, does-nothing 176/176,
  drop-exec 43/43, impact-wipe 66/66, obfuscation 80/80, reverse-shell 25/25,
  simple-stealer 65/65. Log: `/tmp/sc-makefile-validate-final.log`.
  An earlier scan encountered a transient, concurrently edited Nemucod YAML
  indentation error; it was already corrected on reinspection. A concurrent
  encoded-shell regex used a prohibited noncapturing group; replacing it with
  an ordinary group preserved its matching behavior and cleared validation.
- Remaining precision caveat: `test-rules` reports 1.0 for the existing broad
  `simple-developer-secret-stealer` composite. Current cleave code uses 1.6 as
  its default hostile warning threshold and emits a warning, not a downgrade;
  RULES.md/TAXONOMY.md still describe 3.5 and automatic downgrading. Do not
  treat an emitted hostile verdict or passing validation as proof of signature
  precision. No threshold, severity, or policy was relaxed in this pass.
- Additional classification evidence: the Perl Zephyrinemesh cron package,
  SHA-256 `2297231588f6484637d09adaea9077379968adbd6495e5b805d8f5fddd0571d6`,
  exposes an explicit, opt-in HTTP-health-check installer. Its module, build
  entry point, and test contain no secret upload or downloaded-code execution.
  Do not force a hostile verdict on this behavior. Record this hash for the
  misplaced-good reconciliation after active regeneration settles; package
  contents were not executed or changed.

### Perl list calls, process classification, and DNS command syntax

- Confirmed another call-routing bug: the grammar emits ordinary calls without
  parentheses as `ambiguous_function_call_expression`, but the Perl adapter
  omitted that node kind. Added it to the existing call-kind list; it already
  carries the same `function` and `arguments` fields. No new fact schema,
  security vocabulary, or flow feature was introduced.
- A harmless regression compared parenthesized and bare `notify`, `system`,
  and `open` calls, including argument equality, shared flow targets/arity,
  comment/string exclusions, and one shared parse. Before the fix it saw only
  the three parenthesized calls; afterward all six matched. Filefacts results:
  1,356 unit tests passed, four ignored; 46 integration tests passed; formatting
  and clippy passed. Logs: `/tmp/sc-perl-list-call-before.log`,
  `/tmp/sc-perl-list-call-unit.log`,
  `/tmp/sc-perl-list-call-integration-final.log`, and
  `/tmp/sc-perl-list-call-clippy-final.log`.
- The DNS command-execution specimen now exposes its bare `system` call and
  ordered shell arguments. Facts: `/tmp/sc-perl-dns-before-facts.json` and
  `/tmp/sc-perl-dns-after-facts.json`. This repairs a missing observation; it
  does not establish cross-file flow from the separate DNS helper module.
- Consolidated the obsolete, parenthesis-only Perl `system` regex into the
  existing neutral system-call trait and updated all four objective/umbrella
  consumers. Removed its unused shell umbrella: `system('printf', ...)` is
  process execution, not necessarily shell execution. Added a structured Perl
  `exec` observation to the shared process-execution umbrella.
- Removed the misleading `perl-fork-fileless-exec` atom. It detected only
  `my $pid = fork()`, not fileless execution; its consumer now references the
  canonical neutral fork observation. A symbol-only replacement missed Perl's
  special zero-argument builtin node, so used an AST query instead of adding
  another engine feature. Verified distinct evidence spans for `fork()`,
  `fork`, and `CORE::fork()`; heredoc and comment examples do not match.
- Added a neutral TXT-lookup observation for backticks/qx calling nslookup.
  These are `command_string` nodes rather than named call facts. An AST query
  was sufficient and joins the existing TXT-query umbrella; it neither treats
  ordinary quoted examples as execution nor promotes a lookup alone to C2.
- Five harmless regression fixtures cover normal process launches, documented
  call examples, worker forks, TXT lookup, and DNS documentation/A-record
  lookups. All have zero suspicious/hostile findings. Evidence:
  `/tmp/sc-perl-list-call-controls-final.json`, with empty stderr.
- Fresh atomscan scan of the same 35 package hashes:
  `/tmp/sc-perl-list-call-final.jsonl`, with empty stderr. Recovered system-call
  observations in seven packages; the new exec observation appears in 21 and
  TXT-lookup observation in 15. Removed the misleading fileless atom from 21
  packages while retaining neutral fork evidence. No package gained or lost a
  hostile verdict; 15 still have 1–3 hostile findings. This pass improves
  evidence accuracy, not demonstrated hostile recall.
- Rebuilt local cleave/atomscan using the existing temporary snapshots and
  dependency overrides; checkout lockfiles were not rewritten. Logs:
  `/tmp/sc-perl-list-call-cleave-build.log` and
  `/tmp/sc-perl-list-call-atomscan-build.log`.
- Full validation passed after the generator restored a configured CPAN
  fixture: hostile 57/57, benign 45/45, does-nothing 176/176, drop-exec 43/43,
  impact-wipe 66/66, obfuscation 80/80, reverse-shell 25/25, simple-stealer
  65/65. Log: `/tmp/sc-perl-list-call-validate-restored.log`. Earlier attempts
  saw a transient concurrent PowerShell regex edit (already corrected on
  reinspection) and a missing archive during corpus regeneration. Neither was
  bypassed by excluding validators, lowering expectations, or restoring old
  payloads over generator output.
- Clarified the precision documentation after inspecting current code and
  cleave commit `7f111530`: precision warnings no longer change criticality.
  RULES.md/TAXONOMY.md retain the 3.5 authoring bar but now distinguish it from
  the runtime's 1.6 advisory threshold. No thresholds or severity policy were
  changed. Existing broad composites below the authoring bar still need
  precision review; passing validation does not establish that review.
- Remaining DNS tasking gap: command execution and lookup are in different
  source members, linked by a package-local helper. Do not solve this by pooling
  arbitrary archive-wide lookup and shell-call findings or matching the helper
  name/gate. Perl source-local relationship coverage remains limited. The
  regenerating full corpus is not yet a stable, audited inventory.

### Go history upload, written loader context, and diagnostic consistency

- Continued against 30 copied Go archives in `/tmp/sc-go-triage.7bwy1F`;
  manifest: `/tmp/sc-go-triage.sha256`. The user confirmed regeneration is
  ongoing. Neither these 30 archives nor earlier inventories are the final
  corpus inventory, and previously quarantined benign packages were not moved
  again when regenerated.
- Closed the missed history-upload/LaunchAgent case using existing YAML flow
  predicates, without adding source-analysis features. The HTTP-body atom
  follows `os.ReadFile` through path construction, local helpers, string casts,
  truncation, and reader wrapping. A second neutral atom requires a download
  pipeline literal to contribute to `os.WriteFile`'s data argument, including
  formatted helper returns. `SOURCE_ANALYSIS.md` now documents the already
  implemented `from.value` alternative used for this relationship.
- The hostile composite combines those relationships with LaunchAgent loading
  and RunAtLoad configuration in the same source member. It does not claim
  whole-program reachability or cross-file flow, and does not use a package
  identity, collector hostname, or environment gate. Final precision diagnostic:
  7.5, independently checked with benign controls rather than treated as proof
  of accuracy. Log: `/tmp/sc-go-history-writeflow-debug.log`.
- Split Go launchctl detection out of the text matcher: program and subcommand
  must be distinct, correctly positioned arguments to `exec.Command`. The
  existing canonical launchctl trait remains an umbrella for disjoint Go and
  other-source matchers. Direct-argument rules currently use the written call
  target, whereas canonical names are available to provenance queries; using
  the existing direct spelling was sufficient here. Aliased process imports and
  `CommandContext` remain unmodeled variants, not justification for another
  engine feature in this pass.
- Added eight benign controls: synthetic history upload; overwritten body;
  an unrelated read through the same helper; an opaque external transform;
  documentation-only loader examples; ordinary service configuration plus
  installer documentation; normal launchctl command preparation; and wrong
  program/subcommand positions. All have zero suspicious/hostile findings.
  In particular, even a real history-body relationship plus ordinary agent
  configuration does not trigger the hostile rule just because a comment
  mentions a curl installer. Results: `/tmp/sc-go-controls-pinned.jsonl`.
- Added the real Go ZIP expectation. Archive SHA-256
  `e58a3945a2b03f8faebf91943a7e34c60f7d3b1b691deb642bf9030cb6aab403`
  now has one hostile finding (risk 130). Final frozen atomscan scan:
  `/tmp/sc-go-history-atomscan-pinned.jsonl`, empty stderr. Eleven of the 30
  archives have hostile findings: one has one, eight have three, one has four,
  and one has five. Nineteen still have none, including a previously identified
  benign cron helper; this is a verdict distribution, not validated recall.
  The four-/five-finding recovery and boot-wipe packages also need redundancy
  review. No global completion claim is warranted.
- Fixed a real cleave diagnostic bug in `src/test_rules.rs`: the condition
  explanation searched flattened import/export names, ignoring symbol kinds,
  argument predicates, and canonical flow targets. It could show a matched
  rule with an unmatched call condition. Replaced that diagnostic matcher with
  the existing production evaluators; detection semantics and fact schemas
  were not changed. The new harmless regression fails on the old explanation
  and passes after the fix. All 16 rule-diagnostic tests passed. Logs:
  `/tmp/sc-go-debug-before.log`, `/tmp/sc-go-debug-after.log`,
  `/tmp/sc-go-debug-cli-final.log`, and `/tmp/sc-go-debug-negative-cli.log`.
- Clippy passed with the repository's `clippy.toml` included in the temporary
  build snapshot (`/tmp/sc-go-debug-clippy-final.log`); the initial snapshot
  lacked that config and used Clippy's lower argument-count limit. The sibling
  filefacts checkout emits an unrelated unused-function warning. Formatting
  and targeted diff checks passed.
- Another process replaced the shared analyzer executables during triage.
  The shared cleave then missed the existing unpadded-Base64 CPAN regression;
  a separately named build with the local decoder fixes detects the exact
  same archive with one hostile finding (risk 159). No payload or expectation
  was weakened to accommodate the shared binary. Comparison archive SHA:
  `0db03f9f7e5b2ad5e9c3db636b7381a5fadaa92fcd0324652ebfd7f3866ce1ed`.
  Evidence: `/tmp/sc-perl-recheck-fixed.json` and
  `/tmp/sc-go-history-validate-final.log` (shared-binary failure).
- Built `cleave-triage` using the existing temporary manifest and local
  dependency overrides, leaving checkout manifests/lockfiles and the shared
  `cleave` executable untouched. Frozen executables are in
  `/tmp/sc-perl-recheck.KGt25e`; hashes: `/tmp/sc-go-analyzers.sha256`.
  Earlier before/after files used the mutable executable paths, so do not
  interpret their deltas as an engine-pinned performance experiment.
- Full validation with the pinned build passed after the written-content
  tightening and eighth control: hostile 58/58, benign 53/53, does-nothing
  176/176, drop-exec 43/43, impact-wipe 66/66, obfuscation 80/80,
  reverse-shell 25/25, simple-stealer 65/65. Final log:
  `/tmp/sc-go-history-validate-complete.log`. All 30 copied archive hashes
  were rechecked successfully at the end of the pass.

### Go command destinations, duplicate verdicts, and if initializers

- [x] Snapshot the then-current 480 archives before triage. Directory:
  `/tmp/sc-corpus-precision.gSqlBy/corpus`; manifest: `inventory.sha256` in its
  parent. Regeneration remains active; this is not the final inventory.
- [x] Remove the package-extension hostile wrapper and its two source-package
  wrappers. They restated existing hostile verdicts without adding distinct
  harmful behavior. No other rules or expectations consumed those IDs.
  Comparing the same 480 hashes with the same pinned atomscan binary, this
  reduced hostile findings from 299 to 221 and packages above three hostile
  findings from 12 to one. The number with any hostile finding stayed 181.
  Reports: `before.jsonl` and `without-wrappers.jsonl` in the snapshot parent.
  The removed tracked distribution YAML is recoverable through Git.
  Validation also identified its now-orphaned archive-extension component;
  removed that unused YAML rather than inventing another consumer. Its broad
  `.zip`/`.tar` matcher did not establish package identity. That tracked file
  is likewise recoverable through Git.
- [x] Fix a demonstrated parser bug, not a new analysis feature:
  `filefacts::source::value_flow` skipped Go's `if` initializer while already
  evaluating the condition and branches. The real boot-write specimen lost
  its local helper call and therefore the destination's provenance. A minimal
  harmless regression failed before the fix. The initializer now executes
  once before condition/branches in the graph; `:=` names remain local to the
  if scope, while `=` updates existing bindings. Ten cases cover conditions,
  both branches, tuple declarations, overwrites, and outer-variable shadowing.
  Source parser tests: 111 passed, four ignored; Clippy and formatting passed.
  Logs: `/tmp/sc-go-if-init-before.log`, `/tmp/sc-go-if-init-after.log`,
  `/tmp/sc-go-if-init-source-tests.log`, `/tmp/sc-go-if-init-clippy.log`.
- [x] Repair the Go disk-image false positive using existing trait predicates.
  The old rules called `dd if=/dev/zero ... bs=446` a boot/device wipe without
  checking its destination. The simplest regular-file control scored 159
  with one hostile and two suspicious findings. Four controls now score 3–4
  with no suspicious or hostile findings: ordinary image prefix, unrelated
  mount diagnostics, overwritten destination, and an if-local shadowed name.
  No filename, gate, or benign-output-path exclusion was added to the rules.
- [x] Add a neutral Go call-argument relationship: the command is `dd`, its
  first operand is `if=/dev/zero`, and its next operand derives from both an
  `of=` prefix and a `findmnt` result through explicitly modeled output/string
  transfers. Existing device-wipe composites consume this atom. This remains
  source-local may-flow, not execution proof or full path evaluation. Go no
  longer uses the three bare/co-occurrence atoms that produced the false
  positive; other-language migration is still outstanding.
- [x] Preserve the original boot-write archive unchanged as
  `testdata/hostile/supply-chain-regressions/go-boot-device-write.zip`, since
  regeneration removed its old corpus pathname while validation was running.
  Its README records provenance and SHA-256. It retains one hostile finding
  (risk 120), versus the original five, and has a regression expectation.
  Report with the four benign controls: `/tmp/sc-go-dd-controls.jsonl`.
- [ ] Resolve the newly exposed Go iterator/helper-return gap in the copied
  `gomod-nettlenode-disk-wipe-linux.zip`. The old verdict depended only on a
  mount-table mention near zero-input arguments. The stricter Go rules do not
  claim the iterated output is a device until that relationship is established.
  Inspect existing tree-shape predicates before considering new loop/container
  flow semantics; do not restore the loose conjunction merely for recall.
- [x] Full validation exposed two pre-existing scanner-based Go wiper
  regressions (`impact-wipe/12-linux-dd.go` and `63-linux-mounts-dd.go`). Their
  scanner/field relationships already exist in the flow graph, so added a
  separate neutral YAML model for `os.Open("/proc/mounts")`, `bufio.NewScanner`,
  receiver `Text`, and `strings.Fields`; no loop-analysis feature is needed
  for these cases. A fifth benign control scans the mount table but overwrites
  the destination before preparing an image command. Expectations were not
  weakened. Final validation of this correction is recorded below when done.
- [x] The scanner cases also revealed a second genuine bug in cleave's
  call-to-flow join. `exec.Command(...).Run()` has two calls at one byte offset;
  imported canonical targets differ from their source spelling, so offset/name
  alone rejected the inner call. Filter candidates using the existing argument
  count as well. Truly ambiguous same-offset/same-arity calls still require an
  exact target; do not guess between them or borrow the outer call's arguments.
  The harmless imported-call regression failed before and passes after the
  fix, alongside all 103 symbol/string matcher tests. Logs:
  `/tmp/sc-go-calljoin-before.log` and `/tmp/sc-go-calljoin-after.log`.
  This is a lookup correction, with no new fact schema or language policy.
- [ ] Migrate the remaining non-Go portable mount/boot and dynamic-dd atoms.
  They still infer destinations too broadly and contain neutral evidence in
  objective directories. The Go correction is not a cross-language fix.
- [x] Recheck the frozen corpus after this precision/parser change and run
  full validation. Report any true-sample losses separately from duplicate
  finding reductions; do not interpret a verdict distribution as recall.
  Intermediate `after-go-destinations.jsonl`: 181/480 have hostile findings,
  219 hostile findings total. This is not the same set of 181 as the baseline:
  the Go iterator specimen loses its unsupported verdict, while the newer
  pinned atomscan recovers the previously fixed unpadded-Base64 Perl case.
  Only those packages and the Go boot specimen changed hostile IDs; hashes
  match. Final `final-calljoin.jsonl` has the same verdict counts and same
  three-package hostile-ID delta. All 480 reports contain raw analysis with
  no report-level errors; stderr is empty. All inventory hashes were rechecked
  successfully (`hash-recheck.log`). This includes a real outstanding Go miss,
  not merely a cosmetic reduction in duplicate findings.
- [x] Final controls and full validation pass with the separately named,
  frozen build in `/tmp/sc-go-calljoin.HDWITl`; executable checksums:
  `/tmp/sc-go-calljoin-analyzers.sha256`. The two existing scanner-based wipers
  each have one hostile finding (risk 118), the packaged boot writer has one
  (risk 120), and all five benign image controls have no suspicious/hostile
  findings (risk 3–4). Report: `/tmp/sc-go-dd-final-controls.jsonl`, empty stderr.
  Full validation: hostile 59/59, benign 58/58, does-nothing 176/176,
  drop-exec 43/43, impact-wipe 66/66, obfuscation 80/80, reverse-shell 25/25,
  simple-stealer 65/65. Log: `/tmp/sc-go-dd-validate-calljoin.log`.
  Clippy passed (`/tmp/sc-go-calljoin-clippy.log`); targeted diff checks passed.
  Shared analyzer executables and checkout manifests/lockfiles were not
  overwritten. No hostile package content was changed or executed.
- [x] Inventory is now stable; completed a hash-pinned live inventory audit.
  This closes the inventory check, not the outstanding detection triage.
  See the following section and `SUPPLY_CHAIN_AUDIT.md`.

### Stable inventory and package-canary precision (2026-09-14)

- [x] Hash all five supply-chain test roots: 1,294 files before triage, with
  1,278 analyzer root reports. The 16 unreported files are documentation and
  package bookkeeping. Input hashes matched before/after the frozen scans.
  Current `supply-chain-corpus`: 622 specimens across 30 categories; 197 have
  hostile findings, 196 have 1–3, and one has five. 425 still lack a hostile
  finding; these are not yet individually verified misses.
- [x] Freeze rules as well as binaries. The initial mutable-rule scan crossed
  a concurrent rewrite of `go-dd.yaml`, so its lost Go verdict does not prove
  a memo/cache bug. Discard that comparison. Authoritative reports are
  `/tmp/sc-stable-audit.YGIZcs/frozen-baseline.jsonl` and
  `frozen-complete.jsonl`; exact binary, input, rule and report hashes are in
  `SUPPLY_CHAIN_AUDIT.md`. Both scans retain the in-process memo, produce no
  report-level errors, and have empty stderr. No engine changes this pass.
- [x] Fix the rewritten Go trait's variable-name false positive using the
  existing value-flow predicates. New benign `go-dd-image-device-name.go`
  failed before (risk 118, one hostile) and passes after (risk 4, no high
  findings). It differs meaningfully by assigning a regular-file destination
  to `dev`; the identifier itself is not evidence of a device. All six benign
  image controls are clean; boot writer and two scanner wipers retain their
  correct hostile findings. No filename/gate exception or new engine feature.
- [x] Remove five unsupported hostile package wrappers and their orphaned
  components, rather than adding more conjunctions or gating on fixture IDs.
  A gate-free local-index bootstrap had four hostile findings (risk 510) for
  ordinary decoding, hidden temp data, a harmless child, and loopback HTTP.
  It now scores 8 with no high findings and retains the useful behavior facts.
  Hidden-file writes remain notable; removed a misplaced unused hex keyword
  atom and retained the existing Python call-based decode fact in test paths.
- [x] Compare identical specimen hashes using frozen before/after rules: all
  315 v1 artifacts lose unsupported hostile wrappers. No artifact outside v1
  changes its hostile finding set. The current 622-specimen corpus still has
  235 hostile findings. The apparent v1 drop from 315 detected packages to two
  is correction of benchmark overfitting, not evidence of lost attack recall.
- [x] Statically review three v1 canaries and move them unchanged to
  `/tmp/triage/misplaced-good/supply-chain-benchmark-v1` per `x-triage-bad`:
  Python Pathweaver, JavaScript Resourcecove, Elixir Fontstream. Verify hashes
  after moving; document provenance in the audit and v1 README. Final inventory
  differs only by those three moves and the README note. All 622 current
  corpus hashes are unchanged. No package was activated or executed.
- [x] Full pinned `make validate` passes: hostile 59/59, benign 60/60,
  does-nothing 176/176, drop-exec 43/43, impact-wipe 66/66, obfuscation 80/80,
  reverse-shell 25/25, simple-stealer 65/65. Log:
  `/tmp/sc-stable-audit.YGIZcs/precision-checked-validate.log`.
  New fixtures and expectations cover both demonstrated false positives.
- [x] Repair the two remaining v1 Run-key false positives: Ruby Profileloom's
  `spec` string is not the argument passed to `system`; PowerShell's `$spec`
  is written as data, while `Start-Process` invokes harmless output. Inspect
  `ruby-reg-add-run-key-persistence`, `extconf-windows-persistence`, and
  `run-key-persistence-ps` / `run-key-write-ps`. Prefer call/argument facts;
  preserve legitimate Run-path reference facts without claiming a write.
  Completed with actual-command/destination predicates and the argument-shape
  engine bug fix recorded below. Both archives were moved unchanged to the
  recoverable misplaced-good directory after static review and hash checks.
- [x] Review and delete the 14 remaining JavaScript v1 canary-only archives.
  Manifests, entrypoints and decoded resources show no attack implementation;
  repair would require wholesale replacement. Hashes match original provenance,
  the prior audit and Git HEAD, so deletion is recoverable from Git history.
  This is fixture-quality cleanup, not an engine gap or detection success.
- [x] Review and delete all 15 TypeScript v1 canary-only archives. They repeat
  the JavaScript template with type annotations and likewise never perform the
  decoded attack descriptions. Exact hashes match original provenance, the
  preceding inventory and Git HEAD; deletion is recoverable from Git history.
- [x] Review and delete all 15 C v1 archives. They declare CMake executables but
  contain no `main`, cannot link, never perform their decoded attack descriptions,
  and never read their purported PNG payloads. Hash-verified deletion is
  recoverable from Git history.
- [x] Remove two disconnected token-order inferences exposed by the C cohort.
  `shell-command-buffer` and `format-string-injection` inferred flow between
  unrelated calls. Keep the precise shell-command format-string observation;
  remove the dead hostile consumer rather than add unnecessary AST machinery.
  A benign C regression now stays free of the self-extract objective.
- [x] Review and delete all 15 C# v1 archives. Their NuGet build target depends
  on an undeclared external `dotnet script` tool; more importantly, every module
  only writes the decoded attack description to a temp file, starts a fixed
  print-only child and contacts loopback. Hash-verified deletion is recoverable.
- [x] Remove the unconsumed `schtasks-create-source` objective atom. It claimed
  task creation from command text alone and duplicated existing neutral command
  reference observations. No new AST or engine behavior was warranted.
- [x] Review and delete all 15 Go v1 modules. Six plain variants cannot compile
  due to unused imports; all 15 `init` functions merely write an attack sentence,
  launch a no-op/echo child and contact loopback. Hash-verified deletion is
  recoverable from Git history.
- [x] Review and delete all 15 Rust v1 crates. Cargo would execute each build
  script, but the script only writes decoded description data to temp, starts a
  print-only child and contacts loopback. Hash-verified deletion is recoverable.
- [x] Review and delete the 14 remaining Python v1 packages. Their setup-time
  `exec` reaches only the temp-canary, print-only child and loopback routine.
  Hash-verified deletion is recoverable from Git history.
- [x] Remove the zero-use `windows-schtasks-payload` composite. It contradicted
  its own comment by using line proximity to infer that an unrelated subprocess
  was the task payload. Existing cached calls exposed the disconnect; no AST
  feature was justified for an unconsumed rule.
- [x] Review and delete the 14 remaining PowerShell v1 packages. Their module
  import path executes only the common temporary-canary write, print-only child,
  and loopback pulse. Taskglider's scheduled-task sentence is data, not a command
  argument. Hash-verified deletion is recoverable from Git history; the generic
  scheduled-task capability and persistence composite remain correctly modeled.
- [x] Review and delete the 14 remaining Ruby v1 packages. Both their genuine
  `extconf.rb` install hook and importable library duplicate the common canary;
  decoded attack descriptions are written as data and never reach `system`.
  Hash-verified deletion is recoverable from Git history.
- [x] Review and delete the 14 remaining Elixir v1 packages. `mix.exs` really
  evaluates the gated bootstrap, but its only command is `sh -c :`; decoded
  attack descriptions remain temporary-file data. Hash-verified deletion is
  recoverable from Git history.
- [x] Disassemble and delete all 60 Java, Groovy, Kotlin, and Scala v1 JARs.
  Every compiled class is a valid annotation processor with a static trigger,
  but invokes only a description write, `java -version`, and loopback. The
  bundled sources omit the processor superclass and are not authoritative.
- [x] Fix the JVM `reboot-string` false positive exposed by all four Cacheharbor
  JARs. A cron `@reboot` schedule is not a system-reboot command. Relocate the
  retained command-string observation to the neutral shutdown capability family,
  use cached `class.strings[*]`, require command position, and preserve both RAT
  consumers. No AST or engine feature was needed; all four rescans have no high.
- [x] Review and delete all 15 Lua v1 packages. Their LuaRocks build command
  executes the gated bootstrap, but decoded attack descriptions never reach
  `os.execute`; the only command prints a fixed message. Taskglider's complete
  scheduled-task string remains a valid generic persistence-intent signal.
- [ ] Review the remaining 90 v1 artifacts for individual disposition. The
  corpus README documents canary sinks, so do not treat its original intended
  scenario labels as proof of executable malicious behavior.
- [ ] Continue actual current-corpus misses and duplicate verdicts. The audit
  records per-category coverage and the three roots still above three hostile
  findings. Do not declare the goal complete from these inventory counts.

### Ruby/PowerShell argument precision (2026-09-14)

- [x] Fix a real cleave matcher bug, not an extraction feature: string, numeric,
  and identifier argument constraints must reject incompatible shapes even
  when `kind` is omitted. Before, unknown call/identifier arguments could
  satisfy literal predicates by skipping their match arm. The new regression
  fails before and passes after; all 104 symbol/string matcher tests, clippy,
  and rustfmt checks pass. Shape/provenance-only predicates remain supported.
- [x] Replace Ruby's parenthesis-dependent `system` regex with existing call
  facts. Merge the identical Perl/Ruby fact instead of duplicating matchers.
  Require actual command arguments for Ruby Run-key and pipeline findings;
  ordinary version-printing calls near quoted examples no longer trigger them.
- [x] Express PowerShell Run-key destinations using existing AST predicates.
  Literal destination arguments and an immediate same-variable assignment/use
  are supported; overwritten bindings and Run-key strings used as data do not
  imply persistence. No general PowerShell flow feature was necessary here.
- [x] Add four harmless negative controls and four real-sample expectations.
  Full pinned validation passes: hostile 63/63, benign 64/64, does-nothing
  176/176, drop-exec 43/43, impact-wipe 66/66, obfuscation 80/80,
  reverse-shell 25/25, simple-stealer 65/65. All new controls have zero high
  findings. Log: `/tmp/sc-ruby-triage.tbgxXt/validate-final-tree.log`.
- [x] Audit frozen rules, binaries, and unchanged inputs over 1,275 reports.
  Exactly six hostile-ID sets change: three recovered detections (two Brew
  hooks and Ruby Gablepro), one applicable additional Perl encoded-execution
  finding, and two corrected v1 Profileloom false positives. Current corpus:
  200/622 have hostile findings; 199 have 1–3, one has five; 422 still need
  review. Input/rule/binary hashes and report hashes are in the root audit.
  No hostile sample was modified, activated, or executed.
- [x] Detect launcher replacement (Quilltreebyte) using existing call arguments;
  see the follow-up below.
- [x] Detect the written launch agent pipeline (Basaltstack); see the
  adjacent-statement solution below.
- [x] Detect browser-storage secret posting (Larkspurlite) using existing AST
  relationships as recorded below. Check existing facts first;
  neither telemetry nor a displayed install command alone proves an attack.

### Homebrew launcher and Ruby rule correctness (2026-09-14)

- [x] Necessary detection gap, no engine feature: bind `inreplace` argument 0
  (executable target) and argument 2 (inserted pipeline) in one call. A neutral
  Formula subclass observation supplies package context. Do not mistake the
  old shell installer-marker composite for Ruby Formula identity. Quilltreebyte
  now has one hostile finding, risk 123; its control covers ordinary patching,
  removing a pipeline, and updating documentation rather than an executable.
- [x] Necessary rule bug: Net::HTTP method facts searched quoted literals and
  missed the actual calls. Replace the three literal matchers and write-method
  text umbrella with receiver-aware AST queries. Both actual-call and quoted-
  example controls are clean; retain neutral HTTP facts without inferring theft.
- [x] Necessary rule bug: a semicolon inside a Ruby string satisfied the `exec`
  statement regex. Use existing call nodes, exclude unrelated receivers, and
  retain actual bare/Kernel calls. Remove the redundant suspicious/dropper
  method-name atom and update its sole consumer to the canonical neutral fact.
- [x] Necessary precision correction: a method returning a harmless launchd
  plist example scored 120 (one hostile, two suspicious). Remove the unsupported
  source path/KeepAlive/RunAtLoad conjunction and its three orphaned atoms.
  Reuse neutral service-configuration facts instead; the same control now has
  no high findings, risk 3. No filename/gate exemption or weakened cap.
- [x] Add six benign controls and one positive expectation. Full pinned
  validation passes: hostile 64/64, benign 70/70, does-nothing 176/176,
  drop-exec 43/43, impact-wipe 66/66, obfuscation 80/80,
  reverse-shell 25/25, simple-stealer 65/65. Log:
  `/tmp/sc-brew-triage.jlcKqK/validate-complete.log`.
- [x] Freeze rules and recheck all five roots: 1,289 unchanged input files,
  1,273 reports, empty stderr. Only Quilltreebyte changes hostile IDs; no
  previously hostile artifact loses its verdict. Current corpus: 201/622
  detected, 200 with 1–3 hostile findings, one with five; 421 require review.
  Exact hashes and intermediate/final evidence are in `SUPPLY_CHAIN_AUDIT.md`.
- [x] Resolve the keychain-to-POST relationship, not merely keywords.
  Saved evidence in `/tmp/sc-brew-triage.jlcKqK`: `brew-calls.jsonl`,
  `plist-ast-flow.txt`, `keychain-ast-flow.txt`. Basaltstack's heredoc argument
  is an expression with its body outside the call node. Larkspurlite's Ruby
  flow omits the nested receiver call and treats interpolation as literal
  text. These are observed coverage limits, not justification for an unbounded
  Ruby-flow feature. First test whether existing structural predicates can
  prove the intended relationships without conflating overwrites or examples.
  Basaltstack's written-loader relationship is now covered as recorded below.
  Larkspurlite is subsequently covered by the bounded AST relationship below;
  this does not claim that the general Ruby flow projection was extended.
- [x] Review the remaining JVM launchd constant-only composite in
  `objectives/persistence/system/launchd/bootstrap/ios-source.yaml` against a
  harmless compiled plist constant. This turn proved and removed the source
  conjunction. The following pass proves the JVM false positive and removes it.

### Written LaunchAgent relationships and JVM constants (2026-09-15)

- [x] Necessary missing detection, expressible by a trait author: use one AST
  sequence for the destination assignment, directory creation, write, and its
  heredoc. Match the same path binding and the actual ProgramArguments payload,
  not a nearby example. The Formula objective adds package context. Basaltstack
  now has one hostile finding (risk 125), with no engine expansion. This is a
  bounded structural pattern; unquoted URL and literal basename are current
  restrictions, not general Ruby flow coverage.
- [x] Add two Ruby controls covering ordinary local services, quoted URL pipe
  characters, overwritten bindings, and unrelated destination variables. They
  score 9 without high findings; the documentation-only control stays clean.
  Fix the neutral RunAtLoad fact's `for:` scope: `source` excludes Ruby, so
  explicitly include `scripts`. This corrects the prior migration's coverage
  omission rather than adding another duplicate fact.
- [x] Prove the JVM constant-only false positive with a harmless compiled class
  and disassembly. It scored 118 (one hostile, two suspicious) for configuration
  strings alone. Remove the unsupported conjunction and two orphaned atoms;
  the now-empty legacy `ios-source.yaml` is deleted and recoverable in Git.
  Existing neutral facts retain configuration observations. Source and class
  controls score 1 without high findings. The class rebuild is byte-identical;
  only harmless regression code was compiled, never a hostile package.
- [x] Add one positive expectation and four benign expectations. Full pinned
  validation passes: hostile 65/65, benign 74/74, does-nothing 176/176,
  drop-exec 43/43, impact-wipe 66/66, obfuscation 80/80,
  reverse-shell 25/25, simple-stealer 65/65. Log:
  `/tmp/sc-launchagent-triage.vjmz6y/validate-jvm.log`.
- [x] Recheck the full unchanged five-root inventory with frozen rules/binaries:
  1,289 files, 1,273 reports, empty stderr. Only Basaltstack changes hostile
  IDs; no existing hostile verdict is lost. Current corpus: 202/622 detected,
  201 with 1–3 hostile findings, one with five, and 420 awaiting review. Exact
  input, rule, report, and compiled-control hashes are in the root audit.
- [x] Resolve the keychain-result POST miss using the saved Ruby
  call/AST/flow evidence. Do not substitute keychain/HTTP co-occurrence for an
  actual relationship, and require failing semantic controls before deciding
  whether an extractor correction is necessary.

### Browser-keychain result to HTTP body (2026-09-15)

- [x] Necessary detection gap, solvable by a trait author: connect the literal
  keychain command result and its trim operation to the request body's single
  identifier interpolation. Require a distinct URI assignment feeding the URL.
  Only the optional net/http require may additionally intervene. The Formula
  composite supplies package context. No engine facts or feature expansion.
- [x] Reject the demonstrated confounders: public command output, overwritten
  values, unrelated body values, URI assignment replacing the secret, local
  migration, and value mutation in endpoint/body interpolation. All seven
  cases in the new benign fixture have no high findings (file risk 3).
  A harmless structural probe verifies the optional require and bare body
  interpolation forms; no new attack specimen was generated or executed.
- [x] Record boundaries instead of claiming generic flow support: static
  command strings, trim/chomp, adjacent statements, literal HTTP(S) DNS endpoint,
  and one direct interpolation. General helpers, intervening control flow,
  dynamic command interpolation, and arbitrary endpoints are not covered by
  this relationship. Existing AST facilities suffice for the confirmed sample.
- [x] Add positive and negative expectations; full pinned validation passes:
  hostile 66/66, benign 75/75, does-nothing 176/176, drop-exec 43/43,
  impact-wipe 66/66, obfuscation 80/80, reverse-shell 25/25,
  simple-stealer 65/65. Log:
  `/tmp/sc-keychain-triage.bwaXRq/validate-complete.log`.
- [x] Freeze and recheck all five roots: 1,289 unchanged files, 1,273 reports,
  empty stderr. Larkspurlite alone gains a hostile verdict (risk 122); no
  existing hostile verdict is lost. Current corpus: 203/622 detected, 202 with
  1–3 hostile findings, one with five; 419 still require review. Hashes and
  evidence paths are in `SUPPLY_CHAIN_AUDIT.md`.
- [ ] Triage the 11 GitHub Actions packages next. Reports already traverse and
  recognize action.yml as github_actions, so do not call this an archive bug.
  Basaltbyte's composite run step visibly pipes token/key environment data to
  HTTP upload. Inspect structured step values and existing trait support first.
  Other scenarios require independent review; creating a service file without
  enabling it or sending secrets is not automatically a hostile implant.

### GitHub Actions environment-pipeline review (2026-09-15)

- [x] Recheck stability: all 1,289 input hashes match the preceding audit.
- [x] Confirm composite run values are already emitted at
  `runs.steps[*].run`. No archive or structured-value extraction fix is needed.
- [x] Fix the demonstrated precision bug in the legacy environment-exfiltration
  rules: comments, documentation, and `env | curl` without a stdin-upload option
  are not evidence of an environment upload. Preserve only relationships the
  available matcher actually establishes; add harmless regression controls.
- [x] Validate the rules and compare the unchanged full inventory for lost
  hostile verdicts before resuming broader GitHub Actions analysis.
- [x] Resolve the grouped/filtering pipeline separately. The original manifest
  facts contain run strings but no shell calls or AST; broadening a file-wide
  regex would conflate command examples and disconnected operations. Do not
  add a shell-parser feature merely to force this sample to match.

Results: the two counterexample files went from risk 39 / three suspicious
findings each to risk 4 / no high findings. Four bounded neutral observations
cover direct `env`/`printenv` stdin uploads in workflow and composite run values;
the two local-diagnostic controls retain these observations without a theft
verdict. Entire-scalar matching intentionally excludes filters, compound
commands, extra curl options, and quoted forms. The three unsupported legacy
atoms and their inference-only umbrella were removed, not demoted or renamed.
No new engine facts or features. Validation: hostile 66/66, benign 79/79 and all
six other suites pass. Evidence: `/tmp/sc-gha-triage.fBjnBR/validate-final.log`.
The memo-disabled before/after full scans have identical suspicious/hostile
IDs; 1,289 input hashes are unchanged and no hostile verdict is lost.

### Path-sensitive analysis-cache reuse (2026-09-15) — fixed

- [x] Necessary correctness investigation, not an extractor feature: repeated
  full scans with identical inputs, rules and binaries produced different
  build-script findings on three Rust files. Byte-identical `lib.rs`,
  `bootstrap.rs`, and `build.rs` fixtures have different path-dependent rules.
  With `CLEAVE_ANALYSIS_MEMO_MB=0`, both rule snapshots agree on every high ID.
  `CLEAVE_SKIP_CACHE=1` alone does not disable this in-process memo.
- [x] Identify unsafe existing paths in cleave: report-cache fast paths in
  `src/lib.rs` replace `target.path` without the path-equivalence check already
  used for single-flight results. Per-file cache stores erase the source path
  when no path-dependent finding fired; absence of a finding is also
  path-dependent. Source inspection is not a passing regression test.
- [x] Add a deterministic harmless reproduction covering both scan orders,
  matched and unmatched filename conditions, and cache-on/off parity.
- [x] Fix cache acceptance using the existing path-equivalence machinery;
  preserve the origin needed to check negative results as well as positive
  ones. Audit report fast paths, per-file caches and archive-member reuse.
  Retain sharing for equivalent paths; no new detection facts are needed.
- [x] Run focused cache regressions and full validation, then repeat the
  frozen-inventory scan with caching enabled and disabled. Do not resume
  broader corpus triage until this correctness issue is addressed.

The cache reproduction failed before the fix: scanning identical harmless
source as lib.rs then build.rs lost the build-name finding; reversing the order
incorrectly added it to lib.rs. The retained integration tests cover three
orders with memo on/off, archive members, all memory/file APIs, an atomic path
suppressor, and successful sharing for equivalent paths. Compact cache entries
now retain origins even for negative results; full and compact lookups check
path equivalence before reuse. Composite unless/downgrade path inputs are also
included. The obsolete positive-finding-only dependency index was removed.
Tests: 29 cache unit tests, one composite path-input unit test, and two
end-to-end tests pass. The cache-only full comparison agrees on all 67,503
emitted trait IDs/criticalities across 3,868 root/member reports; it exposed the
independent one-point scoring discrepancy below, which is now also fixed.

### Deterministic risk summation (2026-09-15)

- [x] Necessary arithmetic bug, not a new scoring feature: the cache-fixed
  full scans agree on every root/member trait ID and criticality, but the
  Duskwellpro npm archive scores 55 versus 56. Its confidences are identical.
  `FileAnalysis::compute_summary` sums group maxima as unordered f32 values
  and then takes ceil; accumulation order can cross an integer boundary.
- [x] Add a harmless confidence-permutation regression, stabilize summation
  without changing the group-max scoring policy, and rerun score/cache parity.

The confidence-permutation test failed with score 4 instead of 3 before the
fix. Canonical-order wider accumulation, rounded once to the existing f32
score precision before ceil, makes it deterministic. Additional controls retain
score 1 for five baseline contributions and round a genuine fractional excess
up to 4. All 26 file-summary tests pass. No confidence, criticality weight,
grouping policy, trait predicate, or specimen changed. Cache revisions invalidate
older entries rather than reusing potentially contaminated verdicts/scores.

Final verification for both fixes:

- Cache tests: 29/29; composite path-input test: 1/1; end-to-end cache tests:
  2/2; file-summary tests: 26/26. Final clippy and diff checks pass.
- Full validation: hostile 66/66, benign 79/79, does-nothing 176/176,
  drop-exec 43/43, impact-wipe 66/66, obfuscation 80/80,
  reverse-shell 25/25, simple-stealer 65/65.
- Final memo-on/off scans: 1,273 roots, 3,868 root/member records, identical
  trait IDs, criticalities, confidences and risk scores. Empty stderr;
  all 1,289 input hashes and the frozen rule manifest are unchanged.
- No suspicious or hostile IDs differ from the preceding memo-disabled
  baseline. Corpus counts remain 203/622 detected, 202 with 1–3 hostile
  findings, one with five; 419 still need review. This is a correctness fix,
  not a new-coverage claim.
- Evidence: `/tmp/sc-cache-path-triage.0lBOUW`, final analyzers under
  `bin-final/`, rules `/tmp/sc-gha-verified-rules.or35Vw`. Source, binary,
  input and rule hashes were rechecked. Checkout manifests/lockfiles and
  pre-existing symbol-matcher changes were preserved.

The subsequent declared-script pass below resolves the grouped
credential-filter pipeline using actual command relationships, without
marker gates or speculative engine metrics.

### Declared manifest scripts (2026-09-15)

- [x] Necessity review: YAML values and archive traversal work. This is missing
  format support, not a YAML parser bug. Trait authors cannot apply existing
  shell AST predicates to a run scalar; regex approximations lose command,
  quoting, redirection and step boundaries. A narrow declared-script handoff
  is warranted for ordinary workflow/action code, independently of this sample.
- [x] Have filefacts expose declared run bodies and their known language,
  borrowing the existing parsed values. Do not invent security-specific facts,
  reparse YAML in cleave, infer dynamic shells, or fetch referenced actions.
- [x] Analyze each body separately with the existing source analyzer and bounded
  resources. Keep virtual-source locations honest; unknown shells and exhausted
  budgets must leave an analysis gap, not an implied clean result.
- [x] Add harmless parser/traversal controls for separate steps, quoting,
  shell selection and budgets; then repair shell pipeline detection with actual
  same-pipeline source/filter/upload evidence and negative controls.
- [x] Validate and compare the frozen full corpus; record improvements and
  limitations before resuming other ecosystems.

Implemented the narrow handoff, not a second YAML parser or security-specific
fact schema. Supported explicit/inherited shells reuse existing analyzers;
decoded bodies have JSON-Pointer logical locations and independent scopes.
Limits are 100 bodies, 1 MiB each, 10 MiB total. Unknown shells, expressions
and exhausted budgets surface `embedded-source-incomplete`; nested string
reanalysis is deliberately not enabled. Cache revision 15 invalidates older
manifest-only results.

- [x] Fix a demonstrated nested-member reporting bug: fill absent parent links
  from immediate wrapper paths after finalization. Preserve explicit links.
  The archive integration test asserts that each parent resolves correctly.
- [x] Replace loose environment-upload text rules with shared shell AST
  observations joined at common source offsets. The 13-step control fixture
  rejects quoting, redirection, disconnected filters, non-upload data options,
  localhost and intervening transformations. Accommodate the tree-sitter root
  wildcard optimizer quirk in the query; no engine feature or vendor fork.
- [x] Resolve the genuine VSIX Amberbyte detection regression. Inspect
  existing constant/binding/argument evidence before adding source support;
  assess whether a precise trait suffices. Its shell command is assembled
  across JavaScript strings. Do not restore broad regex proximity, detect the
  gate/hostname, or count this executable credential upload as benign.
  Resolved by the bounded Node argv trait pass below, without an engine bridge.
- [x] Review the Indigoprime service finding: its unit runs an HTTP client,
  but is not enabled/started and does not execute the HTTP response. The rule
  also fired on a loopback health check and on `ExecStart=/usr/bin/printf curl`.
  Replace the inference with a correctly placed, command-position-constrained
  service-directive text observation; no engine change is necessary.
- [x] Repair the existing `quiet-fetch-hidden-stage` inference. Its predicates
  establish a quiet download to a hidden path, not execution. Dunelinebyte
  does execute the same downloaded path, so preserve that real relationship
  with a precise rule rather than treating quiet/hidden output alone as hostile.
  Inspect existing same-path AST/fact matching before adding engine features.

Final validation passes all eight suites (hostile 67/67, benign 80/80).
Parser 4/4, analyzer 4/4, gap 1/1, core 47/47, archive/step-scope 1/1 and
cache-context 2/2 tests pass. Full memo-on/off reports agree across 1,273
roots, 3,862 members and 67,764 trait instances, with unchanged 1,289-input
hash inventory. Five benign GHA control files have zero high findings.
The gate/hostname independence probe passes without executing or writing
derived payloads. Corpus counts: 205/622 with hostile findings, 204 with
1–3, one with five; 417 still require review. One genuine VSIX hostile
verdict was lost and remains open; this is not a no-regression claim.
Evidence: `/tmp/sc-gha-sources.RjSAuA`, final rules
`/tmp/sc-gha-final-v2-rules.JCHldj`; see the audit for manifests and deltas.

### VSIX evidence review and service-rule correction (2026-09-15)

- [x] Inspect the actual Amberbyte call, not just its missing verdict. The
  archived JavaScript calls `execFile("/bin/sh", ["-c", <concatenated text>])`.
  `symbols()` records the bare `execFile` target and an array-shaped argument;
  the two source literals are separate. Imports lack the destructured binding.
  `build_arg` does not fold this binary expression; generic flow merges do not
  express an ordered, resolved argv string. Existing stng concatenation support
  is for encoded strings and does not establish this call's interpreter input.
- [x] Prototype a precision-preserving fix for that call boundary. Required
  controls include quoted examples, logging an identical string, a local or
  shadowed `execFile`, argument-position changes, concatenation, dynamic input
  and overwrite. Determine whether existing AST matching suffices before adding
  a bridge. Do not mistake import/text proximity for a resolved execution edge.
  The bounded Node argv trait pass below resolves this reviewed form. It was
  not an archive bug or justification for security-specific metrics or a second
  parser. Broader constant folding and binding forms remain unsupported.
- [x] Reproduce service-rule false positives with two harmless fixtures, then
  remove the two loose curl/wget atoms and their payload/escalation composite.
  The replacement under `micro-behaviors/os/service/config` describes directive
  text only and constrains the executable position. Retain the existing service
  context consumer through an updated reference. No broad taxonomy migration,
  sample gate exclusion, engine feature, or specimen modification is needed.

Service-rule verification: final validation passes hostile 67/67, benign 82/82
and all six other suites. The controls score 6/2 instead of 40/36 and have no
high findings. Full frozen scan: 1,273 roots, 3,862 members; all root/member
hostile IDs and confidences agree with the preceding baseline. Four misleading
suspicious service findings were removed; all 1,289 input hashes are unchanged.
The VSIX gap and quiet-hidden-download inference remain open. Final evidence:
`/tmp/sc-service-precision.rA7JZL` (`*-v3` outputs), rules
`/tmp/sc-service-v3-rules.rBbEku`. No engine sources were changed this pass.

### Hidden-download relationship correction (2026-09-15)

- [x] Reproduce download-only false positives and remove the loose hostile rule.
  Relocate its generic download-output context into the neutral HTTP download
  taxonomy and update consumers. Preserve visible observations, not false intent.
- [x] Use existing shell AST predicates and capture equality for the downloaded
  path's shell invocation; no new engine matcher, metric or fact was needed.
  Separate hidden-output and invocation observations join at shared offsets.
  Dunelinebyte retains one hostile finding; measured precision is 5.7.
- [x] Verify nine negative steps and eight static, in-memory positive variants.
  Gate, actor hostname, quiet flags and sample path are not detection predicates.
- [x] Review validation failures instead of inflating findings: 33 drop-exec
  samples each retain two hostile findings. Change the suite floor from three
  to two, matching the user's 1–3 target. Add positive and negative execution
  assertions. Final validation is green (hostile 68/68, benign 83/83, drop-exec
  43/43 and the other five suites); no sample bytes changed.
- [ ] Review remaining proximity-based download/chmod/background pairings.
  The new relation deliberately does not claim variable-path, mixed-quoting,
  alternate argument-order or intervening chmod-chain coverage. Existing high
  findings in those cases still need independent accuracy checks.

### macOS PKG inner CPIO and installer relationship (next)

- [x] Necessity review: Clovermarksync's script is stored in a gzip-wrapped
  `070707` old-ASCII CPIO archive. Reports expose the opaque `Scripts!!Scripts`
  body rather than a named postinstall member. The extracted original script
  has a shell AST; the opaque CPIO body does not. Trait authors cannot repair
  member boundaries and archive safety checks with a text rule. This is a
  missing package-container capability, not grounds for security-specific facts.
- [x] Add bounded ASCII CPIO recognition/member extraction with syntax owned
  by filefacts and traversal/limits owned by cleave. Reuse `ArchiveMember`
  extents, ownership and paths rather than a security-specific projection.
  Cover old-ASCII/newc layouts, malformed/truncated headers, paths, links,
  duplicate names, limits and cancellation. The real XAR → gzip → CPIO chain
  now exposes named installer scripts in all ten macOS packages. See the
  ASCII CPIO follow-up below for validation and intentionally unsupported forms.
- [x] Reproduce and fix the existing newc reader's silent `InvalidData` success
  and failure to consume alignment padding. Harmless tests reproduced both:
  malformed input was accepted and an unaligned first file hid later members.
  Finish every drained entry, propagate truncation/errors, preserve original
  paths for sanitization, and bound name allocation and skipped-data processing.
  Eleven focused tests and an end-to-end RPM test pass, as does strict clippy.
- [x] Review same-path download → `installer -pkg` in Clovermarksync. Its source
  and cached arguments show the same pathname, but the downloaded package is
  absent from the supplied artifact and a legitimate updater can do this.
  Do not restore the loose hostile verdict or add an AST relationship solely
  for an unsupported verdict. Fix the missing neutral absolute-path installer
  call using cached arguments; retain other-format command references separately.
  Static controls and the real nested member pass in
  `/tmp/sc-pkg-installer-review.ueQofw`. Payload-level disposition remains unknown.

Final evidence: `/tmp/sc-download-execution.7iXpkP`, rules
`/tmp/sc-download-rules.O7Mc0n`. The unchanged five-directory inventory contains
1,289 files; the frozen scan has 1,273 roots and 3,862 members. High deltas are
exactly the Dunelinebyte finding replacement and Clovermarksync's lost loose
finding. Corpus totals are 204/622 with hostile findings, 203 with 1–3, one with
five; 418 need review. Both the macOS package and VSIX misses remain open.

### CPIO reader correctness repair (2026-09-15)

- [x] Necessity review: lost archive members, swallowed parser errors and
  unbounded parser allocations are engine bugs. Trait authors cannot recover
  missing member boundaries or enforce extraction limits. Repair the existing
  reader without introducing security-specific metrics or a second parser.
- [x] Cover padding, malformed headers, every truncated prefix, skipped names,
  links, duplicate paths, oversized name allocations, metadata byte budgets,
  cancellation and trailers claiming data. End-to-end checks cover plain/gzip
  RPMs, later shell-member analysis, partial errors and retained header facts.
- [x] Preserve parsed RPM header facts when payload extraction fails; use the
  existing notable incomplete-analysis diagnostic, not a hostile verdict.
  Invalidate old incomplete cached results with analysis-cache version 16.
- [ ] Implement missing CPIO formats separately from this repair. A reviewed
  corpus RPM uses `07070X`, whose file indexes require metadata from the RPM
  header ([RPM format documentation](https://rpm-software-management.github.io/rpm/manual/format_v4.html)).
  All ten current-corpus RPM payload signatures were checked and use this
  format. It is unsupported, not inherently malformed. Old-ASCII `070707` macOS
  PKG traversal is completed in the follow-up below. Reuse filefacts archive
  metadata and cleave's extraction limits; do not infer payload coverage from
  header-only findings.

Final verification: `/tmp/sc-cpio-repair.SocDAV`. All eight validation suites
pass (hostile 68/68, benign 83/83); 11 CPIO tests, one end-to-end RPM test and
29 cache tests pass, with strict clippy clean. The frozen-rule scan retains
all 1,273 roots and 3,862 root/member records. All suspicious/hostile IDs,
criticalities and confidences agree with the previous baseline. Ten RPM roots
gain the existing notable incomplete-extraction diagnostic; seven consequently
stop displaying three baseline-only metadata/fixture traits under the existing
low-tier suppression policy. RPM identity/fact fields remain unchanged.
Corpus counts remain 204/622 with hostile findings; 418 still need review.
All 1,289 input hashes, frozen rules and pinned binary hashes were rechecked.
No specimens or detection rules were changed in this repair.

The raw reports are not byte-identical: in addition to those intended RPM
deltas, 112 Java member import lists have ordering-only differences and 16 Zig
object context excerpts differ. Neither changes the normalized detection
comparison; context excerpt reproducibility has not been diagnosed here.

### ASCII CPIO traversal follow-up (2026-09-15)

- [x] Necessity: trait authors cannot restore a missing named member boundary.
  Add `FileType::Cpio`, generic archive classification and bounded filefacts
  indexing for `070707`, `070701`, `070702`. Use existing `ArchiveMember` fields.
  `cpio.variant` and `cpio.complete` describe syntax/index state, not intent.
- [x] Bound entries at 65,536, names at 1 MiB, and headers/names/retained link
  targets at 16 MiB. Preserve complete member bodies when only following
  padding is truncated; retain the incomplete-index diagnostic separately.
- [x] Extract only regular-file extents and directories under cleave's existing
  budgets. Sanitize original names, disambiguate collisions, refuse overwrites,
  never create links/devices, and retain non-executable filesystem permissions.
  Version 17 invalidates previously opaque CPIO cache results.
- [x] Recover Riftwoodkit's actual credential-filtered environment upload with
  the existing shell relationship rule, without gate/hostname predicates or
  new detection rules. Add a root-package expectation requiring its credential
  exfiltration hierarchy. Other macOS scripts are now available for real review.
- [x] Review Larkspursync's deletion of Documents/Desktop/Pictures: fixed in
  traits using existing shell AST and symbol facts; see the follow-up below.
- [x] Review Fennellite's keychain-command substitution → printf → HTTP upload:
  existing AST and call arguments establish the bounded relationship; see the
  follow-up below. No engine feature is necessary for this specimen.
- [x] Review Tidecrestforge's heredoc → same-path launchctl load. Cached
  symbols/values/flow omit the body-to-write link; an existing structural query
  expresses the bounded relationship without an engine feature. See the
  shell heredoc-to-launchd audit in `/tmp/sc-launchagent-shell.2QawRH`.
- [ ] Disposition before assigning hostile labels: Pumicestack only defines a
  function in `.zshrc`; Junipeerkit writes a downloader under `/etc/profile.d`
  on macOS without demonstrated execution; Indigocore forgets its own package
  receipt. Also review Clovermarksync's fetch-and-install relationship and
  Larkspursync's background HTTP loop. Filenames and comments are not proof of
  the behavior claimed by the fixture name.

Limits remain explicit: the newc checksum layout is indexed without checksum
verification; hardlink aliases expose their stored bodies, not reconstructed
aliases; binary CPIO and RPM stripped `07070X` are unsupported. The existing
RPM newc stream reader is not migrated by this change. These are not claims of
complete archive-format or supply-chain recall.

Final evidence: `/tmp/sc-cpio-members.Y7aTWu` (`*-v3` scans/binaries). Parser
tests pass 7/7, extraction safety tests 4/4, recognition tests 291/291, both
end-to-end CPIO/RPM tests and strict lint checks. All eight validation suites
pass, including hostile 69/69 and benign 83/83. The frozen scan retains 1,273
roots, 3,871 compact root/member records and 68,097 trait instances. All earlier
root-level high IDs, criticalities and confidences survive; Riftwoodkit's upload
is the only new high finding. Corpus totals: 205/622 with hostile findings,
204 with 1–3, one with five; 417 without hostile findings still need review.
The full macOS member scan exposes 20 CPIO containers and all ten installer
scripts. Inputs, frozen rules, targeted source snapshots and pinned binaries
were rechecked; no specimen bytes changed.

### Personal-folder deletion follow-up (2026-09-15)

- [x] Necessity: the shell recursive-delete text matcher missed indentation
  and could read quoted examples as commands. Replace it with an existing AST
  query, preserving the neutral capability. Require recursive options before
  any option terminator, and an operand on that command. No engine change.
- [x] Use AST only where facts are insufficient: shell call arguments flatten
  double-quoted HOME expansions and single-quoted literal dollars to the same
  string. Require actual HOME expansion nodes and two distinct, exact top-level
  personal-folder operands. Join that atom with recursive deletion at the same
  command offset. Local HOME rebinding or an rm function makes host-target
  inference uncertain and suppresses the targeting atom.
- [x] Remove `shell-delete-user-docs`, which inferred deletion solely from
  Desktop/Documents text in a particular order. Its existing macOS composite
  references the canonical behavioral objective instead. This fixes quoted
  documentation and subtree-cleanup false positives without another detector.
- [x] Correct the validation-discovered `rm-dash-prefix-file` placement:
  ordinary option-terminator handling is a file-deletion capability, not
  masquerading intent. Move the observation to the existing file-command
  hierarchy, constrain it to command syntax, and update its dropper consumer.
- [x] Add a real installer-package expectation, ten benign fixture controls,
  and static in-memory gate/hostname-independence probes. No specimen bytes
  were changed and no specimen was executed.
- [ ] Embedded-source follow-up, not a blanket grammar override: the Zig
  Yarrowguard sample passes a formatted/concatenated command to `/bin/sh -c`.
  Its old neutral shell finding came from heuristic plain-string analysis;
  that path deliberately re-detects the virtual source rather than forcing a
  shell AST. Switching the rule to syntax matching therefore exposes a real
  coverage gap (one notable lost, no high findings lost). A future solution
  must establish the interpreter/argv/value relationship and exclude logging,
  shadowing, reassignment and wrong-position controls. Inspect the existing
  declared-source/flow mechanisms before proposing any new facts or bridge;
  do not force every shell-looking string into executable-source analysis.

Evidence: `/tmp/sc-home-delete.HGyN4t`; frozen rules:
`/tmp/sc-home-delete-rules.BEYqsj`. This is a rule-level repair, not a new
engine metric or a claim that embedded-command coverage is complete.
Final validation passes all eight suites (hostile 70/70, benign 93/93).
All 18 in-memory probes pass; the objective's reported precision is 6.8.
The final scan retains 1,273 roots/3,871 records with no lost high findings;
Larkspursync is the sole recovered hostile package. Current corpus totals:
206/622 with hostile findings, 205 with 1–3, one with five; 416 need review.

### Keychain-result upload follow-up (2026-09-15)

- [x] Necessity: Fennellite's actual password-to-request-body relation is
  missing, not merely a keyword or gate match. Existing call arguments select
  the Safe Storage query; an existing AST matcher follows its stdout through
  command substitution, a binding, printf expansion and curl stdin. No new
  metrics, security-specific facts or shell flow engine are needed here.
- [x] Keep the transport relation neutral under HTTP request/body: the same
  mechanism posts health checks and ordinary API credentials. Join it to the
  Safe Storage query's call offset to infer browser-keychain exfiltration.
- [x] Restrict to consecutive top-level statements, with either a direct
  pipeline or a side-effect-free nonempty-variable test. Require the same
  assigned/printed variable, actual stdout (optional stderr discard only),
  actual stdin as the HTTP body and a syntactically non-local domain URL.
  Local shadowing of the participating commands and background assignments
  conservatively exclude uncertain relationships. HTTP domains are not fetched.
- [x] Move the old keychain text reference from the trojanized-library intent
  hierarchy to neutral keychain observations, and update its existing consumer.
  Merely mentioning a browser query does not prove it executes or exfiltrates.
- [x] Add a package-level hostile expectation and thirteen benign controls.
  Twenty-seven in-memory probes cover gate/hostname changes, removed gates,
  direct and guarded uploads, renamed variables, another browser, tool paths,
  options, redirections, overwritten/disconnected variables, background
  assignments, command shadowing and ordinary service authentication.
- [ ] Broader coverage remains unproven: helper functions, reordered CLI
  arguments, braced/concatenated printed values and general shell dataflow are
  outside this bounded rule. Consider existing trait mechanisms first; do not
  infer a need for engine changes from these untested forms alone.

Evidence: `/tmp/sc-keychain-upload.UWRkhL`; frozen rules:
`/tmp/sc-keychain-rules.BRSZ3N`. The initial `full.jsonl` is invalid because it
started before snapshot copying finished (6,737 unresolved references). It is
not a detector-regression baseline. Only a completed-snapshot scan with empty
stderr and verified inventory can replace the preceding authoritative audit.
Final `full-v2.jsonl` meets those requirements: 1,273 roots, 3,871 retained
records, 68,117 trait instances, empty stderr, unchanged input hashes and a
rechecked frozen rule manifest. All eight validation suites pass (hostile
71/71, benign 106/106). No existing hostile finding is lost; Fennellite gains
one, and the only removed high ID is the relocated text-only query observation.
Current corpus: 207/622 with hostile findings, 206 with 1–3, one with five;
415 require review. C Sablewoodworks loses its old suspicious text claim and
still needs actual behavior detection/disposition, not an automatic benign label.

### RPM header-scriptlet follow-up (2026-09-15)

- [x] Necessity: package headers declare code that payload traversal cannot
  supply. Expose it through filefacts' existing embedded-source contract and
  cleave's bounded adapter; do not introduce another parser or security metrics.
- [x] Decode nine lifecycle body/program/flags triplets; preserve independent
  valid bodies on malformed tags. Unknown programs, extra argv and processing
  flags remain explicit coverage gaps. Keep separate script scopes.
- [x] Fix the initial decoder's rejection of scalar interpreter strings.
  Real RPMs and upstream rpmbuild use STRING/count-one for one interpreter;
  normalize it alongside STRING_ARRAY. Add scalar, array and malformed controls.
- [x] Verify all ten real RPM scriptlets reach source analysis with unchanged
  rules. Add a package-level neutral-behavior regression for Eldergroveworks.
  Parser tests: 10 passes; three cross-container integrations pass; strict
  filefacts linting passes. Cache version 18 invalidates pre-scriptlet reports.
- [x] Review newly exposed overly strong SSH-key, cron/network and preload
  labels. Misplaced atoms were corrected; broken simulations were removed.
- [ ] Address actual curl-pipe and base64-intermediate environment-upload
  rule gaps using existing facts first. No new engine feature is established.
  The old silent-curl regex requires a literal `-s` spelling and misses grouped
  `-fsSL`; its consumer also requires a `/bin/sh` path reference or bash call,
  despite a visible bare `sh` pipeline. Existing source-call/pipeline facts
  already expose the operations. Fix relationships and benign controls rather
  than inserting a synthetic shebang or treating every installer as hostile.
- [ ] RPM stripped 07070X payload traversal and trigger arrays remain separate,
  explicitly unsupported work. Header coverage is not complete RPM coverage.

Evidence: `/tmp/sc-rpm-scripts.OTqfjQ`, final `bin-v2` / `full-v2.jsonl`.
Stable input manifest matches the preceding pass. Final corpus totals are
210/622 with hostile labels, 209 with 1–3 and one with five; 412 lack hostile
labels and the three newly labeled RPMs also need verdict review. No prior high
finding is lost. See SUPPLY_CHAIN_AUDIT.md for limitations and reproducibility.

### Encoded environment upload / cron precision (2026-09-15)

- [x] Necessity: the base64-intermediate miss is a trait relationship gap.
  Extend the existing bounded pipeline query, not the engine. Preserve the
  same-node credential-filter/HTTP-body join and reject redirected/file-input
  encoders, decoders, disconnected flows and locally shadowed tools.
- [x] Verify 28 in-memory static probes and nine benign controls. Add real RPM
  Gableutils and DEB Gablekit expectations: each gains one credential-upload
  hostile finding. Reported objective precision: 6.4.
- [x] Review all three portable-cron hostile matches. Their scheduled requests
  discard response bodies; curl plus crontab is not sufficient hostile evidence.
  Remove the composite and relocate its neutral atoms by observed behavior.
  Add a benign recurring-health-check regression, not an environment-gate bypass.
- [x] Complete the three affected cron packages' disposition. Two have broken
  quoted-tilde gates; the third is only a response-discarding heartbeat. They
  were deleted as poor hostile simulations and remain recoverable from Git.
- [x] Resolve RPM Fennelbyte by simulation-quality disposition; its broken gate
  and heartbeat-only body do not justify retaining the package to tune a
  misleading archive-family observation.
- [x] Resolve SSH placeholder-key and preload-library verdict accuracy. The 17
  malformed-key packages and two nonfunctional preload samples were removed;
  the bare Swift path and preload-rootkit taxonomy errors were repaired without
  engine additions.
- [ ] Remote-shell
  pipeline verdicts, and the broader unresolved corpus remain in scope.

Evidence: `/tmp/sc-env-encoding.vNGTRy`; final `full-v2.jsonl`; frozen rules
`/tmp/sc-env-encoding-rules.M9xMLs`. Only high changes: two credential-upload
gains and three unsupported cron-label removals. Current corpus: 209/622 with
hostile labels; 208 have 1–3, one has five, 413 have none. This is not verified
recall. The stable 1,289-input inventory is unchanged.
Final `make validate` passes all eight suites, including hostile 74/74 and
benign 116/116. Evidence: `validate-final.log`; prior intermediate validations
do not include both final package expectations.

### SSH references and Ed25519 framing (2026-09-15)

- [x] Necessity: do not add key-validation engine facts just to recognize the
  fixed Ed25519 wire layout. Tighten the existing literal regex instead.
  Ten static structural probes cover truncation, extra data/padding, algorithm
  and length-field changes, complete framing and changed public-key bits.
- [x] Remove the portable SSH backdoor and generic credential-access composites
  that inferred intent from nearby public-key/path text. Relocate their two
  reference atoms by observed behavior; preserve their matchers as neutral facts.
- [x] Fix the JS path-reference taxonomy error found by validation at notable
  severity. Relocate it and update consumers, rather than weakening the benign
  fixture's forbidden-hierarchy assertion. All 99 old occurrences have neutral
  replacement findings.
- [x] Add five benign controls and a real legacy npm package expectation. The
  old npm source retains two hostile findings and its archive four. Complete
  public-key documentation is not a backdoor; malformed key text is still visible.
- [ ] Disposition: 16 matching current-corpus source packages and an additional
  Java package carry malformed keys. They are not proof of functional SSH access,
  but file writes/timestamp restoration can still merit detection. Do not mark
  entire packages benign, repair payloads or move archives without full review.
  The C sample additionally formats a literal `%s` path using `%%s`.
- [ ] Continue actual write/restore relationship coverage, RPM preload/payload
  review, remote fetch-to-shell verdicts and the rest of the full corpus goal.

Evidence: `/tmp/sc-ssh-verdict.o3VpA7`, final `full-v3.jsonl` and
`key-structure-final.jsonl`; frozen rules `/tmp/sc-ssh-rules-final.7OuMyo`.
Current corpus: 194/622 with hostile labels, 193 with 1–3 and one with five;
428 need review. PHP's separate stealth-rewrite finding remains. No unrelated
high finding is lost and the input inventory is unchanged. Final validation
passes all eight suites (hostile 75/75, benign 121/121); this is not completion
of corpus triage or a verified recall figure.

### Shell response-to-interpreter relationship (2026-09-15)

- [x] Necessity: use an existing tree query for the actual pipeline edge, not
  new engine metrics/facts. Command-name/argument co-occurrence cannot establish
  which command supplies the shell's input.
- [x] Cover bare/absolute shells, grouped and long quiet curl flags, `nohup`,
  and output redirection. Reject explicit commands, syntax-only modes, input
  redirection, disconnected commands, quoted examples and shadowed tools.
  All 41 static in-memory probes pass, independently of environment/file gates.
- [x] Verdict: retain this complete capability at notable severity. Remove the
  curl-only hostile wrapper and its duplicate bash branch: quiet remote-script
  installation alone does not prove malicious intent. Do not add an actor-host
  signature, random-gate signal, or duplicate atom to manufacture a hostile score.
- [x] Verify the five durable benign controls, both real RPM header observations,
  all eight regression suites and the frozen five-root scan. Validation passes
  hostile 76/76 and benign 126/126; no suspicious/hostile finding changes.
- [ ] Review independent intent evidence and full package disposition for both
  RPMs. Foxtailpro's visible verify script downloads and executes; its filename
  does not establish wiping. Stripped RPM payload traversal remains unsupported.
- [ ] Apply the same relationship/verdict review to legacy wget and spawned
  download-execution rules. Do not generalize those verdicts from this curl pass.
- [ ] Relocate the older neutral curl/installer text references still under
  dropper objectives, preserving consumer behavior and useful notable findings.
  The five controls expose this placement issue despite having no high findings.

Final evidence: `/tmp/sc-curl-pipe.E1aYoF` (`full.jsonl`, `probe-final.log`,
`durable-controls.log`, `validate-final.log`); rules
`/tmp/sc-curl-pipe-rules.gNUR7A`. Inventory recheck matches all 1,289 baseline
files (manifest SHA-256 `64f1398ffcf15b16679bbc83678e918698677d715db0314cdbfaf012dd9e4009`).

### Bounded Node argv credential-upload detection (2026-09-15)

- [x] Recheck actual Amberbyte source, current symbols and flow. Its argv array
  lacks resolved contents in the shared facts; unqualified `execFile` alone is
  insufficient. This is not an archive extraction failure.
- [x] Necessity: use a bounded AST relationship and binding-syntax observation.
  No new engine facts, metrics, constant-folding API or embedded-language bridge.
  Keep neutral syntax distinct from the combined exfiltration verdict.
- [x] Support direct/two-literal command bodies, known shell modes and curl data
  options, and reject lexical replacements, unrelated data, unknown options and
  dynamic scope. In particular, another child_process export renamed to execFile
  must not masquerade as the imported API.
- [x] Verify 48 in-memory probes and eight durable benign controls. Gate removal
  and hostname replacement preserve detection. The actual VSIX gains exactly one
  hostile trait; measured authoring precision is 6.6.
- [x] Full frozen comparison and `make validate`: only the actual VSIX's high
  finding is added (source and package roll-up), no finding is lost. All eight
  suites pass, including hostile 77/77 and benign 134/134. Inventory unchanged.
- [ ] Broader alias/import, variable argv and dynamic/escaped/multi-part string
  forms still require evidence-driven coverage. The bounded exclusions are not
  complete JavaScript binding analysis; unknown forms are not benign verdicts.
- [ ] Continue the remaining VSIX packages and the full supply-chain corpus.

Final evidence: `/tmp/sc-vsix-call.770Cc9` (`full-final.jsonl`, `probe-v7.log`,
`controls-final.jsonl`, `rule-test-final.log`, `validate-final.log`); frozen rules
`/tmp/sc-vsix-final-rules.FVxzy5`. Current corpus: 195/622 with hostile labels,
194 with 1–3 and one with five; 427 need review. See SUPPLY_CHAIN_AUDIT.md for
scope, limitations, unchanged input inventory, hashes and the Node API contract.

### Skipped callback flow diagnostics (2026-09-15)

- [x] Inspect Tidecrest's real source and both evidence views. `symbols()` has
  `dns.resolve4`; `flow()` omits that call because it is in an anonymous callback
  inside `activate`. The graph also omitted its existing `anonymous-function`
  limitation. This diagnostic omission is a bug, not evidence of benign behavior.
- [x] Repair the bug in filefacts `source/value_flow.rs`: skipped anonymous
  definitions report their limitation from the evaluator, including inside
  named bodies. Skipped nested named functions report `nested-function`, so
  another wrapper does not silently hide the unsupported body. Do not model
  callback invocation, parameters or captures as part of this diagnostic fix.
- [x] Verify JavaScript/TypeScript, Python and Go controls, a nested wrapper,
  and a supported named-function control. All 1,377 active filefacts library
  tests pass (four ignored); clippy passes. On the real source, values/functions
  are unchanged and only `anonymous-function` is added (`flow-delta.json`).
- [x] Rebuild and pin the existing analyzers using an isolated parser-source
  copy. Full frozen corpus comparison preserves all 68,408 trait instances and
  every root risk/high-ID set. All eight validation suites pass with these builds.
- [ ] Tidecrest typed-text → hex/case helper → DNS detection remains unresolved.
  Do not replace the missing relationship with file-wide keyboard/encoding/DNS
  co-occurrence. Callback/capture modeling would be a separate feature; first
  assess a precise existing fact/AST rule. No specimen was executed or repaired.
- [ ] General report propagation of flow limitations remains separate: the
  flow API/CLI now tells the truth about this omission, but this does not claim
  every ordinary cleave report emits a corresponding analysis-gap finding.

Final evidence: `/tmp/sc-vsix-dns.W71MNi` (`flow-final.json`, `flow-delta.json`,
`filefacts-tests-final.log`, `filefacts-clippy.log`, `full.jsonl`,
`traits-added.jsonl`, `traits-removed.jsonl`, `validate-final.log`). Rules are
unchanged at `/tmp/sc-vsix-final-rules.FVxzy5`; new pinned analyzers are in
`bin/` with `analyzers.sha256`. The 1,289-input inventory is unchanged. Corpus
counts remain 195/622 with hostile labels, 194 with 1–3 and one with five;
427 require review. This is a diagnostic repair, not a new exfiltration detection.

### Compound-assignment provenance repair (2026-09-15)

- [x] Necessity: a genuine language-modeling bug, not a new security fact.
  Accumulating into an existing identifier with `+=` could retain a stale
  binding or discard its previous origin. A trait author cannot repair missing
  provenance for general call-argument queries in YAML.
- [x] Recognize the tested compound-assignment syntax and merge the old binding
  with the right-hand value. Read the old binding before evaluating the RHS;
  evaluate the RHS once. Unwrap Go's singleton assignment-place list. Preserve
  ordinary overwrite semantics. Flag unsupported member/indexed targets with
  `compound-assignment-target`; do not invent mutable object relationships.
- [x] Test JavaScript, TypeScript, Python, Go, Rust and C: accumulation, ordinary
  assignment, later overwrite, unrelated sink and opaque-call controls. Add
  RHS-reassignment/evaluation-count and unsupported-member controls. All 1,378
  active parser-library tests pass (four ignored); clippy passes.
- [x] Verify the six-language, five-case matrix through ordinary YAML `arg.from`
  rules in cleave's `tests/source_compound_flow.rs`. No production test-only
  traits or security-specific facts were added. Invalidate old analysis results
  with cache salt v19 because this repair can change provenance-based findings.
- [x] Finish the pinned, frozen-rule corpus comparison: all 68,408 trait
  instances and every root risk/high-ID set are unchanged. All eight
  `make validate` suites pass, including hostile 77/77 and benign 134/134.
- [ ] Resume Tidecrest review. Anonymous callback flow remains unsupported;
  fixing compound assignment does not itself establish typed-text exfiltration.

Final evidence: `/tmp/sc-type-dns-rule.SEmAtS`. Before/after inventories match
all 1,289 baseline inputs exactly. No specimen was executed or changed. Corpus
counts remain 195/622 hostile-labeled (194 with 1–3, one with five); 427 need
review. This restores tested provenance, not a demonstrated corpus recall gain.

### macOS script review / receipt operation (2026-09-15)

- [x] Read the ten named installer scripts. Record actual behavior separately
  from filenames and fixture claims in SUPPLY_CHAIN_AUDIT.md. A function
  definition, discarded HTTP response, staged dylib and executed command are
  not equivalent evidence. Do not activate gates or repair specimen payloads.
- [x] Inspect Indigocore's PackageInfo, payload listing, metadata and cached
  command arguments. Its own-receipt invocation is present in ordinary facts;
  no engine bug or new fact is needed for this visibility gap.
- [x] Strengthen the existing receipt trait: neutral notable severity and a
  cached same-call option predicate replace the baseline literal substring.
  No new trait family or AST query; preserve the existing canonical ID.
- [x] Add six benign controls and a static regression test. Direct, standard
  absolute-path and multiline invocations match; comments/examples, unrelated
  arguments and similarly named executables do not. No control has high findings.
- [x] Complete the frozen five-root comparison. All root risks/high IDs remain
  unchanged; only Indigocore's neutral/low-tier compact output changes. All 1,289
  input hashes are unchanged. Evidence: `/tmp/sc-macpkg-review.cIjB3s`.
- [x] Finish `make validate` for the new control expectations: all eight suites
  pass, including hostile 79/79 and benign 149/149 (`validate.log`). No new
  hostile-coverage claim is made for the neutral receipt observation.
- [x] Review the portable-dylib hostile composite: six staging packages do not
  show library loading, and four benign controls reproduce its unsupported
  hostile/suspicious pair. Remove that composite and its misleading atoms;
  retain neutral source literals and class-string references in capability
  directories. No gate, hostname or additional engine feature is needed.
- [x] Preserve compiled-string consistency with Go: JVM rules use existing
  cached `class.strings`, not a Java-only extension of source literals. The
  class pool includes identifiers/descriptors; do not claim execution or treat
  the entire pool as language-level string constants.
- [x] Validate the dylib precision fix: 13 package/control roots pass the static
  regression; all eight validation suites pass (hostile 79/79, benign 155/155).
  Frozen five-root audit retains 1,273 roots and 3,882 records, changes only six
  root high-ID sets, and preserves all 1,289 input paths/hashes. Corpus counts
  are now 190/622 hostile-labeled, all with 1–3; 432 need further disposition.
  Evidence: `/tmp/sc-dylib-precision.7mqTJB` (`full-complete.jsonl`,
  `high-complete-delta.json`, `regression-final.log`, `validate-complete.log`).
- [x] Tidecrestforge's write/load relationship is covered by the shell-heredoc
  query and installer-hook context in `/tmp/sc-launchagent-shell.2QawRH`.
  Twenty-three structural probes and four benign controls pass. Validation
  rejected the draft single-leg/direct-atomic objectives; this was intentional
  engine policy, not a precision bug. The final rule uses actual installer
  context rather than changing that policy. Final five-root scan changes only
  Tidecrestforge's high verdict (one hostile), preserves all existing findings,
  and adds neutral hook-filename observations to the ten macOS packages.
  Frozen validation fails only the concurrently added stage2 expectation;
  its pre/post snapshot scans are identical. Worktree validation separately
  fails an unrelated oversized registry-access directory. Focused regression passes;
  full validation is not being claimed green.
- [x] Clovermarksync's supplied script has a same-path download/install attempt,
  but no supplied payload establishes malicious purpose. Preserve that uncertainty;
  the hidden path and ignored failure do not by themselves warrant hostile.
  Fixed neutral installer-call visibility and quoted-documentation false
  positives without an engine feature. Eight controls pass; the full scan adds
  only four neutral installer-call instances and preserves every existing
  finding and high verdict. Worktree validation fails two unrelated control-port
  descriptions; corrected frozen validation reports only the existing stage2
  expectation failure, with no new-control failures. Full validation is not
  green. Evidence:
  `/tmp/sc-pkg-installer-review.ueQofw`.

### Archive-wide environment exfiltration consolidation (2026-09-15)

- [x] Inspect Cobaltcraft's actual package, member source and cached facts; its
  environment/file reads feed the serialized HTTP body. Five hostile labels
  do not represent five independently established behaviors.
- [x] Reproduce a real rule-authoring false positive using a harmless install
  hook, separate local environment-name diagnostic and fixed-status HTTP client.
  Two archive-scoped hostile rules incorrectly pool those unrelated members.
- [x] Remove the two pooling rules and the redundant file-finding-plus-hook
  wrapper. Keep the canonical detections and lifecycle observations. No engine
  bug, new fact, new AST query or gate/hostname exception is needed for this fix.
- [x] Move the unchanged neutral HTTPS/POST source matcher out of the credential
  stealer directory; remove inherited theft tags and update its three consumers.
  Do not pretend a textual pattern proves body provenance.
- [x] Add a readable benign package, real-package validation expectation and
  static semantic regression script. A broad directory assertion exposed the
  misplaced HTTP trait; relocating the observation allows retaining that check
  without suppressing or deleting the underlying capability.
- [x] Finish final frozen-rule comparison and validation after the neutral
  matcher migration. All 1,273 roots and 3,881 retained records remain; only
  Cobaltcraft loses high IDs (five hostile findings become two). The 82 neutral
  HTTP-source instances move one-for-one; two low-tier serialization instances
  cease to be retained, while the more specific serialization trait remains.
  All 1,289 input hashes are unchanged. Coverage stays 196/622 hostile-labeled,
  now all 196 with 1–3; the other 426 remain unresolved. All eight validation
  suites pass (hostile 79/79, benign 143/143), as does the static semantic script.
  Evidence: `/tmp/sc-env-consolidation.gd8K4R` (`full-final.jsonl`,
  `traits-final-*.jsonl`, `high-final-delta.json`, `validate-complete.log`).
- [x] Independently test same-file disconnected environment/HTTP code. A local
  environment-name filter plus fixed JSON status upload reproduces the hostile
  `javascript-environ-json-http-exfil` verdict, even without reading secret
  values. A second control also checks whether NPM_TOKEN is configured locally
  and reproduces four additional hostile labels. Evidence and static controls:
  `/tmp/sc-env-disconnected.o8qs70`. This is rule co-occurrence overreach, not a
  demonstrated engine bug; source facts retain the fixed status-body value.
- [x] Remove `javascript-environ-json-http-exfil`; all its component observations
  remain. Add a durable name-only diagnostic/status-upload control and extend
  the existing static npm regression. Cobaltcraft's expectation no longer
  requires that false-positive rule; its developer-file finding remains.
- [x] Finish the post-removal frozen comparison and validation. All 1,273 roots
  and 3,882 records remain; only Cobaltcraft and Clovermarkkit lose the removed
  hostile ID, retaining one hostile finding each. Corpus labels stay 190/622,
  all with 1–3. Five generic HTTP-body umbrella instances also cease compact
  retention; their more specific request-end-body observations remain. All
  1,289 input paths/hashes are unchanged. Static regression passes, as do all
  eight validation suites (hostile 79/79, benign 156/156). Reject the first full
  report (`full-final.jsonl`): it raced the snapshot copy and logged invalid
  references. Only the complete snapshot's `full-complete.jsonl` establishes
  this result; the frozen rules differ from the dylib pass in one file.
- [x] Repair the four additional hostile false positives reproduced by the local
  NPM_TOKEN presence check plus disconnected fixed-body upload:
  `env-token-stealer`, `npm-token-stealer-comp`, `npm-runner-recon-http` and
  `npm-supply-chain-attack`. Removed their unsupported co-occurrence inference
  and orphaned `npm-token-env-access` helper; the hook composite that consumed
  one now references the existing credential-upload finding. No new engine
  fact, query, source/sink model or sample/hostname exception was added.
- [x] Check independent positive coverage: all 65 simple-stealer samples retain
  hostile findings in the focused scan. Only the npm-token-to-Telegram sample
  changes high IDs, retaining two hostile findings instead of five (the fourth
  removed rule was already downgraded to suspicious there). The local token
  check retains neutral token-read and HTTP facts and no hostile findings.
  Durable control: `testdata/benign/env-http-controls/local-diagnostic.js`;
  static regression: `scripts/test-npm-token-precision.sh`.
- [x] Complete the final post-orphan-removal five-root scan for the four-rule
  repair in `/tmp/sc-npm-token-precision.fWfZqk`: all 68,400 trait instances are
  byte-identical after sorting, and root risks/high-ID sets are semantically
  identical. All 1,273 roots, 3,882 records and 1,289 input hashes remain.
  Corpus labels stay 190/622, all with 1–3. The final 66-root static regression
  passes. `full-final.jsonl` is the authoritative post-cleanup report.
- [x] Finish isolated-snapshot validation: all eight suites pass (hostile 79/79,
  benign 156/156, does-nothing 176/176, drop-exec 43/43, impact-wipe 66/66,
  obfuscation 80/80, reverse-shell 25/25, simple-stealer 65/65;
  `validate-frozen.log`). Workspace `make validate` still
  fails on two unrelated PHP/media duplicate-matcher issues after removing
  this pass's orphan (`validate-worktree-final.log`). Preserve those concurrent
  changes; do not describe the workspace validation as passing.
- [x] Consolidate the suspicious NPM-token read aliases (`env-npm-token`,
  `npm-token`, `node-npm-token`) and equivalent `env-npm-auth-token` /
  `node-auth-token` wrappers. Keep the three existing cached member facts and
  add one neutral registry-token family for breadth-counting consumers. Migrate
  all references; preserve the CI detector's registry exclusion and put the
  publishing exception on the actual publishing composite, not token reads.
  Remove two now-unused exceptions. No new matcher, AST query or engine fact.
- [x] Extend the durable regression to seven benign controls and all 65
  simple-stealer samples (72 roots). The disconnected diagnostic, bracket
  reads, all three registry-token spellings and ordinary publishing now have
  no suspicious/hostile findings. The three-spelling control retains three
  neutral atoms without satisfying cross-provider credential breadth. All 65
  positive samples retain hostile detection; the Telegram token sample keeps
  two hostile findings and loses only its duplicated suspicious read aliases.
  Add six benign expectations, including the previously pending diagnostic.
- [x] Finish the post-cleanup five-root comparison: 1,273 roots, 3,882 records,
  all 68,400 trait instances and every root risk/high-ID set are unchanged.
  All 1,289 input paths/hashes match. Evidence:
  `/tmp/sc-npm-read-facts.noqUva` (`full-complete.jsonl`,
  `traits-complete.sorted`, `complete-index.json`, `regression-complete.log`).
- [x] Finish final isolated/workspace validation of the neutral-read migration.
  All eight isolated suites pass: hostile 79/79, benign 162/162, does-nothing
  176/176, drop-exec 43/43, impact-wipe 66/66, obfuscation 80/80, reverse-shell
  25/25 and simple-stealer 65/65 (`validate-frozen-complete.log`). Initial
  validation exposed a now-removed orphan exception and an overly broad
  publishing expectation that incorrectly forbade the publishing exception.
  Workspace `make validate` still fails on unrelated concurrent authoring
  issues (`validate-worktree-final.log`); no unrelated work was changed.
- [ ] Review remaining file-level source/sink composites, including
  `simple-developer-secret-stealer`, against short same-file disconnected code.
  Check cached facts/flow first; do not add a general mutable-object/callback
  engine feature merely to fit a fixture.

### Generalization review (2026-09-15)

- [x] Re-read the authoring guidance and inspect cached call/import/bind/value
  facts for the terminal and curl samples. Calls and scalar arguments are
  present; array/object contents and callback relationships are not all exposed
  in those projections. This is not a justification for every AST subpattern.
- [x] Withdraw the unvalidated curl binding/chain/hostile-composite draft;
  recoverable copies are in `/tmp/sc-deferred-rule-design.u0tzIG`. No previously
  validated detection or sample was removed. Do not count a pending draft as a
  recall improvement.
- [x] Record behavior-first admission criteria in SUPPLY_CHAIN_AUDIT.md.
- [x] Check for dangling draft references and run `make validate` after
  withdrawal: all eight suites pass (hostile 78/78, benign 142/142,
  does-nothing 176/176, drop-exec 43/43, impact-wipe 66/66, obfuscation 80/80,
  reverse-shell 25/25, simple-stealer 65/65). Log:
  `/tmp/sc-deferred-rule-design.u0tzIG/validate.log`. This is validation of the
  working rules, not a new frozen corpus-wide audit or generalization score.
- [ ] Reassess the terminal detector against independent variants and benign
  terminal integrations. Keep justified receiver/mutation constraints, but
  minimize live AST work and document syntax-related false negatives honestly.
- [ ] Redesign the remote-file launch detection only if it earns its keep
  beyond the curl fixture. Require a real download-to-launch relationship and
  severity justified against legitimate installers; do not patch in extra modes,
  flag orders or package names just to raise the synthetic detection count.

### Homebrew download precision and remaining disposition (2026-09-15)

- [x] Review the five remaining formulas against source and cached call facts.
  Distinguish discarded-response HTTP contact, hostname telemetry, printed
  installation instructions, and an unavailable resource installer from
  demonstrated malicious execution or credential theft. Preserve unresolved
  samples rather than moving them merely because no hostile rule fires.
- [x] Necessity check: this is an existing taxonomy false-positive bug, not an
  engine feature request. Public hosting plus a process command does not prove
  a malicious Formula. Existing neutral facts already cover the observations.
- [x] Reproduce hostile false positives on public CSV download and quoted
  install documentation. Remove `homebrew-formula-attack`, its two textual
  atoms, orphan environment wrapper and sole umbrella consumer reference.
  Do not add an AST query, gate-specific exception or generic downloader alias.
- [x] Add two benign expectations and a twelve-root static regression. Both
  controls are clean (risk 3 and 2); all five established Homebrew hostile
  detections survive. Full five-root scan removes only three misleading
  suspicious instances; no hostile finding changes and all input hashes match.
- [x] Frozen validation passes all eight suites (79 hostile, 164 benign).
  Worktree `make validate` fails three unrelated concurrent DuckDB/PHP
  authoring errors; leave them untouched and do not claim worktree success.
  Logs and reverified snapshot hashes: `/tmp/sc-brew-disposition.nK1BD9`.

### VS Code concealed terminal submission (2026-09-15)

- [x] Inspect Onyxfieldcore's archive and entrypoint. A startup extension creates
  a terminal, sends a hidden PowerShell download/evaluate command with execution
  enabled, and hides that same terminal. The command's unquoted pipe leaves
  actual runtime behavior dependent on the parent shell; label the concealed
  attempt, not successful payload delivery or execution.
- [x] Necessity: existing AST queries express this bounded relationship; no
  engine feature, metric, callback model or package-specific gate is required.
  Keep const namespace binding and submitted command syntax in micro-behaviors;
  combine them for the hostile intent finding.
- [x] Require the same adjacent const receiver; allow intervening comments,
  explicit `true` or the API's default execution flag, and ordinary no-options,
  name-string or name-only options. Exclude custom ptys, unknown shell options,
  displayed/logged commands, changed receivers and intervening mutations.
- [x] Verify 48 static probes, including gate removal, hostname replacement,
  direct/two-literal text, standard flag variants and lexical shadow controls.
  Optional query matching initially admitted `false` and extra arguments;
  the tested argument guard now rejects both. No engine change was necessary.
- [x] Add eight durable benign controls and a real VSIX expectation. Focused
  scanning finds one hostile objective on the package; controls have no high
  findings. No specimen was executed or changed.
- [x] Finish the frozen five-root comparison: only Onyxfieldcore gains a high
  finding, exactly one hostile objective. No trait instance is lost. The other
  additions are neutral namespace-binding observations and package roll-ups.
  Precision is 6.6. All eight validation suites pass, including hostile 78/78
  and benign 142/142; focused controls score 4–6 without high findings.
- [x] Audit placement after the shell-bridge directory limit failed. Existing
  creation/name-based dispatch regexes and raw module-import text do not prove
  this binding/receiver/argument relationship. Place the distinct new rules in
  `micro-behaviors/process/create/shell/terminal`; no existing trait is moved or
  demoted. Shorten descriptions to the authoring limit and revalidate.
- [ ] Broader callback cases (Tidecrest, Cobaltkit) remain open. This terminal
  rule does not claim callback flow, arbitrary aliases/monkeypatch resolution,
  dynamic strings, quoted/escaped command bodies, or all terminal configurations.

Final evidence: `/tmp/sc-vsix-terminal.M8XhsF`; frozen rules
`/tmp/sc-vsix-terminal-final-rules.RA4G6h`. Reuses the compound-assignment pass's pinned
analyzers in `/tmp/sc-type-dns-rule.SEmAtS/bin/`. Input inventory matches the
1,289-file baseline before and after scanning. Corpus counts are 196/622 with
hostile labels, 195 with 1–3 and one with five; 426 still require review.

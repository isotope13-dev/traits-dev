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
- [ ] Perform the final live inventory audit only after regeneration stops.

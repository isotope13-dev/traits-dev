# Supply-chain audit — through 2026-09-15

Status: inventory stabilized and baseline audited; detection triage is **not
complete**. The current `supply-chain-corpus` has 622 specimens, of which 190
have hostile findings (all 190 have 1–3). The other 432 require further disposition;
malformed SSH-key fixtures still need behavior-level disposition, and the preload
RPM label also requires verdict-accuracy review;
these counts are not a measurement of verified recall. No package was installed,
imported, built, activated, or executed during this pass.

## Rule admission: generalization before corpus coverage

Future-attack detection takes priority over matching these synthetic packages.
The target of 1–3 meaningful hostile findings is not a quota: an unresolved
sample must remain unresolved when the evidence does not justify that verdict.

Before admitting or extending a rule:

- State the behavior and its benign lookalikes independently of the specimen.
  Download, chmod, and detached launch can also describe a legitimate updater;
  neither their co-occurrence nor a hidden temporary filename proves hostility.
- Inspect cached values, symbols, arguments and flow first. Document the exact
  missing relationship before using a structural query. Preserve same-value,
  same-receiver and same-call relationships; unrelated observations must not
  supply a missing source-to-sink link.
- Separate behavioral invariants from template accidents. Gates, hostnames,
  package names, chosen local identifiers, and incidental flag ordering must
  not become identity signatures. Necessary analysis bounds (such as rejecting
  intervening unknown mutations) are coverage limits, not attack definitions.
- Test behavior-preserving variants independently of the original template:
  renamed locals, changed destinations, equivalent literals/flags, and harmless
  formatting. Record unsupported aliases, callbacks and layouts as misses, not
  benign classifications. Do not relax safety checks merely to pass a variant.
- Pair positive variants with broken-link controls: different output and launch
  paths, different receivers, overwrite before use, download without execution,
  displayed/quoted commands, shadowed APIs, and legitimate installer behavior.
  Review all new matches, not just the expected hostile fixture.
- Reuse canonical atoms. Do not add a parallel matcher for each package or a
  new engine fact when existing trait predicates suffice. Report coverage gains
  separately from demonstrated generalization and false-positive testing.

The unvalidated Pumicesync curl draft was withdrawn from the active taxonomy
after this review. It bound too much of one template (API variable names,
adjacent statements, temporary-path construction and argv layout), and its
hostile severity lacked a sufficient benign-updater distinction. Three draft
YAML files are preserved, byte-for-byte, in
`/tmp/sc-deferred-rule-design.u0tzIG`; no specimen or validated rule was removed.
The validated terminal rule remains a bounded syntax detector, not evidence of
general terminal-command or callback coverage. Neither change establishes an
engine bug. Corpus counts above remain the last completed audit, not a new scan.

## Reproducible comparison

The five supply-chain test directories contained 1,294 files before triage.
Their SHA-256 inventory was identical before and after both frozen-rule scans.
Each scan produced 1,278 root reports, with no report-level errors or stderr.
The 16 unreported inputs were README/manifest/checksum files, Cargo.toml.orig,
and wheel RECORD/WHEEL bookkeeping, not additional attack specimens.

Evidence directory: `/tmp/sc-stable-audit.YGIZcs`.

| Input or output | SHA-256 |
| --- | --- |
| `inventory.before.sha256` | `6c252ba85e0403f8b38a0711f5b34d7dde2dcc685c006b2d083620108d97c457` |
| `rules.frozen-before.sha256` | `b0ff6afa1306b41b6fca098921c72294dd865468c59e20d7fc554d952d0c9001` |
| `rules.frozen-complete.sha256` | `50682a36e99c8967ecd41b65dd2138aa60462f4b5c597b0de1a9070bbd4249ff` |
| `frozen-baseline.jsonl` | `03569a5ada499919a6c069d4713b35bd35b03e76f95b947d9d1147cd563c8680` |
| `frozen-complete.jsonl` | `862b084c1fbfdfe8d466a9fa6eb270764ffaf0f1cdfd11b9385253a7cb4d4a1f` |

Pinned binaries in `/tmp/sc-go-calljoin.HDWITl`:

- `atomscan-triage`: `992d811a17ef74f37f7cf0545c2314c0ef50ff2b9dbcc803fced501b39319848`
- `cleave-triage`: `cd24b86331497530c137cbe9a64c7b2e4d3420f2d0a6f8688959978ec4e7559c`

Both binary hashes were rechecked. Rule snapshots are
`/tmp/sc-stable-rules.BTeWjK` (before) and
`/tmp/sc-stable-rules-complete.SmjRWA` (after). The after snapshot contains only
this pass's rule changes, excluding concurrent unrelated PowerShell edits.

Scans used `atomscan-triage path --no-update --mode slow --follow=none
--format json`, with `CLEAVE_TRAITS_DIR` selecting the snapshot and
`STNG_STRING_CACHE=0 FILEFACTS_CACHE=0 CLEAVE_SKIP_CACHE=1`.
The in-process analysis memo remained enabled for both frozen scans.

An earlier scan against the mutable working rules is **not** a valid baseline:
the Go destination rule changed during that scan. Its differing Go verdicts
do not establish an engine/cache bug. No engine changes were made this pass.

## Initial root-report results

These totals precede the three documented canary moves below. Loose source and
support files under `supply-chain` are reports, not independent packages.

| Directory | Reports | With hostile findings | With 1–3 | With more than 3 |
| --- | ---: | ---: | ---: | ---: |
| supply-chain-corpus | 622 | 197 | 196 | 1 |
| supply-chain-benchmark-v1 | 315 | 2 | 2 | 0 |
| supply-chain | 338 | 116 | 115 | 1 |
| supply-chain-regressions | 1 | 1 | 1 | 0 |
| optinmonster-supply-chain | 2 | 2 | 1 | 1 |

All 315 v1 packages changed hostile finding sets after removing the unsupported
wrappers. No specimen outside v1 changed its hostile finding set. The 622-file
current corpus has 235 hostile findings total, unchanged by this precision pass.

### Initial current-corpus counts by category

| Category | Specimens | With hostile findings |
| --- | ---: | ---: |
| aur | 10 | 2 |
| brew | 10 | 0 |
| c | 30 | 12 |
| choco | 10 | 2 |
| crx | 10 | 2 |
| csharp | 30 | 9 |
| deb | 10 | 3 |
| elixir | 30 | 10 |
| gha | 11 | 0 |
| gnome | 10 | 0 |
| go | 30 | 10 |
| java | 30 | 6 |
| jetbrains | 10 | 0 |
| js | 30 | 14 |
| kotlin | 30 | 10 |
| macpkg | 10 | 2 |
| perl | 30 | 14 |
| php | 30 | 14 |
| pwsh | 30 | 15 |
| py | 30 | 16 |
| rpm | 10 | 0 |
| ruby | 30 | 10 |
| rust | 30 | 10 |
| shell | 10 | 1 |
| swift | 30 | 10 |
| ts | 30 | 8 |
| vsix | 11 | 3 |
| wordpress | 10 | 1 |
| xpi | 10 | 0 |
| zig | 30 | 13 |

## Precision corrections and controls

- Go: replaced a variable-name regex with existing call-argument provenance
  predicates. A command preparing an ordinary image with a variable named
  `dev` previously scored 118 with one hostile finding; it now scores 4 with
  no suspicious/hostile findings. All six benign Go image controls are clean.
  The preserved boot-device writer still has one hostile finding (risk 120),
  and the two existing scanner-based Go wipers retain one each (risk 118).
- Package canaries: removed five hostile co-occurrence wrappers, their five
  internal components, and 15 newly orphaned automatic-execution components.
  Hidden temp-file writes, decoding, a child process, and a network client do
  not alone prove payload execution, theft, beaconing, or anti-analysis.
  The removed tracked YAML files remain recoverable through Git.
- Hidden temporary writes remain observable as notable behavior, not a
  suspicious verdict by themselves. A gate-free local-index bootstrap control
  drops from risk 510/four hostile findings to risk 8/no high findings.
- Removed the unused, misplaced `source-hex-decoder` keyword matcher from
  supply-chain objectives. The existing Python call-based hex-decoding fact
  now remains visible in test/upstream contexts instead of being suppressed.

Full `make validate` with the pinned cleave passed: hostile 59/59, benign 60/60,
does-nothing 176/176, drop-exec 43/43, impact-wipe 66/66, obfuscation 80/80,
reverse-shell 25/25, simple-stealer 65/65. Log:
`/tmp/sc-stable-audit.YGIZcs/precision-checked-validate.log`.

## Ruby and PowerShell follow-up

Evidence: `/tmp/sc-ruby-triage.tbgxXt`. The follow-up starts after the three
initial canary moves: 1,291 input files and 1,275 root reports. Input hashes
matched before and after scanning. Frozen final rules are in
`/tmp/sc-ruby-verified-rules.oXbljA`; four unrelated working-tree PowerShell
edits were excluded from both sides of the comparison, not reverted locally.
Rule and executable hashes also matched after scanning; stderr was empty and
there were no missing root analyses or report-level errors.
This is not complete semantic coverage: 47 member reports carry analysis gaps
(23 `flow-graph-limited` and 34 `flow-query-incomplete` flags, with overlap).
Their per-member gap sets are unchanged from the engine-only comparison.

| Input or output | SHA-256 |
| --- | --- |
| `inventory.before.sha256` | `d15a36ace0166f841b04ffb98cd5cd751826738fe773d0efdfff2215e48e5eb8` |
| `rules.final.sha256` | `16e9c292028b50e7aa00ea1db98fddbae660a5c38b19a55e3eca0ef14216508e` |
| `engine-only.jsonl` | `45d0f2ea4773a802d95c34d8fe8bddb5c3e62208d85fcd4914638eadedbd73c1` |
| `final.jsonl` | `45ff728e397591543d23aa571d40433209c6e0d709f487f03e5b9ecd483ec647` |

Pinned follow-up binaries in `/tmp/sc-ruby-triage.tbgxXt/bin`:

- `cleave-triage`: `6d4e344e8797968e8efa9573902a872c3d9810308814b12bf770c6c3469bb2a8`
- `atomscan-triage`: `fd68341b00868b9dee7c6f856f0a5076ddefa310e602c30729275ac5f01a4143`

Confirmed engine bug: argument value constraints silently accepted incompatible
argument shapes when `kind` was omitted. A string regex could therefore match
an unknown call or identifier instead of a literal. Cleave now requires string,
numeric, and identifier filters to have compatible shapes, while preserving
shape-only and provenance-only filters. The failing regression now passes,
alongside all 104 symbol/string matcher tests; clippy and rustfmt checks pass.
No new fact schema or language-specific engine policy was added.

Trait corrections use existing symbol/argument and tree-sitter predicates:

- Ruby's optional call parentheses no longer hide `system` calls. The identical
  Perl/Ruby neutral call predicates were merged and their consumers updated.
- Download-to-shell and Run-key findings require the actual Ruby command
  argument, not a nearby quoted example plus an unrelated process call.
- PowerShell registry findings require the destination argument. The supported
  assigned-variable form requires adjacent statements using the same binding;
  this is not a claim of general PowerShell dataflow support.
- Four harmless controls cover bare Ruby calls, quoted examples, overwritten
  or unused PowerShell bindings, and Run paths used as data rather than as the
  destination. They score 1, 7, 7, and 5 with no suspicious/hostile findings.

`final-hostile-delta.json` records exactly six changed hostile finding sets:

- Clovermarkstack's install hook and Onyxfieldlite's test hook each gain one
  download-to-shell finding. Test-time execution remains distinct from install.
- Ruby Gablepro gains one canonical Run-key persistence finding.
- Perl Larkspurlite retains its encoded reverse-shell finding and gains an
  applicable encoded-subprocess finding: decoded content is passed to `sh -c`.
- Ruby and PowerShell Profileloom lose their unsupported registry-persistence
  findings. Their registry command is only data; both score 11 with no high
  findings. No gate, specimen-name, or hostname exclusion was introduced.

The current corpus now has **200/622** specimens with hostile findings and
239 hostile findings total. Brew rises from 0 to 2 and Ruby from 10 to 11;
other category detection counts do not change. All 312 scanned v1 packages
have zero hostile findings; that does not establish their individual disposition.
Other roots retain the initial table's counts, including unresolved duplicates.

Full pinned `make validate` passes: hostile 63/63, benign 64/64,
does-nothing 176/176, drop-exec 43/43, impact-wipe 66/66, obfuscation 80/80,
reverse-shell 25/25, simple-stealer 65/65. Log: `validate-final-tree.log` in the
follow-up evidence directory. Four positive expectations and four benign
controls were added without weakening prior expectations.
Validation also passed after the canary moves (`validate-post-disposition.log`).

## Homebrew launcher and Ruby precision follow-up

Evidence: `/tmp/sc-brew-triage.jlcKqK`. All 1,289 input files stayed unchanged;
the final scan produced 1,273 root reports. Binaries are the same pinned
Ruby-fix builds listed above. The baseline is the preceding follow-up's
`final.jsonl`, restricted to the shared inventory after its two canary moves.
Frozen final rules: `/tmp/sc-brew-complete-rules.891hFE`. These contain only
this follow-up's rule changes on the previous frozen snapshot, preserving
unrelated working-tree changes outside the comparison. No engine change or
hostile-sample modification, move, activation, or execution occurred this pass.

| Input or output | SHA-256 |
| --- | --- |
| `inventory.before.sha256` | `64f1398ffcf15b16679bbc83678e918698677d715db0314cdbfaf012dd9e4009` |
| `rules.complete.sha256` | `bf5ec947ccd6a6671c9b1c0750d2ecdf9973143e2cca1e517d81ea07502818ca` |
| `complete.jsonl` | `ccfbf8bbc9ba9c1eca0304b1f1109f355e92aca08ea4a988267a862d960e6154` |
| `controls-complete.jsonl` | `59ba4f1ecd211fb13fbed82debe6080f9a0e1f3f3680c9412ea54dce877d2f7d` |

Corrections and why they were necessary:

- Quilltreebyte's `inreplace` call exposes both the executable target and the
  replacement text in existing argument facts. The new detector requires the
  pipeline in replacement argument 2, not search argument 1, and an executable
  directory target in the same call. A Formula subclass fact supplies package
  context. The previous `homebrew-context` fact is shell-only and describes
  installer markers, so it was not broadened to mean a different observation.
- Three Net::HTTP rules searched string literals for API names, missing actual
  `get`, `post`, and `new` calls while matching documentation. Existing AST
  predicates fix this, including the text-based write-request umbrella. The
  named receiver is not available in these Ruby call/member projections.
- The Ruby `exec` regex treated a semicolon inside a string as a statement
  boundary. Actual call-node predicates now distinguish bare/Kernel/Process
  calls from quoted examples and unrelated receiver methods. Removed the
  redundant dropper-tagged `ruby-ast-exec-in-method` atom and changed its one
  consumer to the canonical neutral process fact.
- A harmless method returning a plist example scored 120 with one hostile
  and two suspicious findings. Removed the unsupported source-level
  path/KeepAlive/RunAtLoad conjunction and its three atoms. Existing neutral
  LaunchAgent facts retain the configuration observations and source/constant
  coverage; their presence alone does not establish malicious persistence.

All six new controls have no suspicious/hostile findings (risk 1–5): launcher
maintenance/documentation, HTTP examples and calls, launchd documentation,
and exec examples and calls. The launcher gains one hostile finding (risk 123)
and loses its unsupported process-cluster finding. **It is the only shared
artifact whose hostile finding set changes.** Current corpus: 201/622 with
hostile findings, 200 with 1–3, one with five, and 240 hostile findings total.
Brew is now 3/10; other category detection counts are unchanged. All 310 v1
artifacts remain without hostile findings, pending individual disposition.

Full pinned validation passes: hostile 64/64, benign 70/70, does-nothing
176/176, drop-exec 43/43, impact-wipe 66/66, obfuscation 80/80,
reverse-shell 25/25, simple-stealer 65/65. Log: `validate-complete.log`.
Rule, binary, and input hashes were rechecked; scanner stderr is empty.

The other two confirmed Brew misses remain explicit: Basaltstack's written
LaunchAgent loader now scores 10; Larkspurlite's keychain-result POST scores 5.
The removed generic verdicts did not establish either attack. Saved call/AST/
flow evidence shows the missing heredoc-to-write and receiver/interpolation
relationships. Inspect existing AST solutions and failing semantic controls
before deciding whether any parser extension is necessary.

## Written LaunchAgent and JVM precision follow-up — 2026-09-15

Evidence: `/tmp/sc-launchagent-triage.vjmz6y`. Existing AST predicates now
connect Basaltstack's LaunchAgents destination binding, `File.write`, and
that call's adjacent heredoc body. The body must enable RunAtLoad and put a
download-to-shell command in ProgramArguments. Formula context supplies the
package-specific objective. No new engine facts or language-analysis feature
was needed. This is a bounded adjacent-statement pattern, not general Ruby
dataflow or a proof of runtime reachability. The current command pattern
requires an unquoted URL and a literal plist basename.

Two Ruby controls distinguish a local service, a pipe quoted inside a URL,
overwritten destinations, and an unrelated LaunchAgents variable from the
actual write target. They have no suspicious/hostile findings (risk 9 each).
The existing documentation-only control also remains clean (risk 3).
Validation caught a scope omission in the previous neutral-fact migration:
`source` does not include Ruby scripts. The canonical RunAtLoad setting fact
now explicitly covers `scripts` as well as compiled-source/Java-class types.

A separately compiled harmless Java constants class proved the pending JVM
precision issue: two configuration constants produced one hostile and two
suspicious findings (risk 118). `javap -c -private` shows only the ordinary
Object constructor; there is no main method, file write, or service call.
Removed the keyword-only JVM conjunction and its two orphaned atoms, completing
removal of `objectives/persistence/system/launchd/bootstrap/ios-source.yaml`.
The original file remains recoverable through Git. Canonical neutral service
facts retain both observations. Java source and class controls now score 1
with no high findings. The class rebuilds byte-for-byte from the supplied
source with `javac -g:none`; SHA-256:
`80f5e5a7101963f9e17f307890c012f566e0958fa90bdb8e551fd5322688de19`.
Only this harmless control was compiled; no hostile artifact was built or run.

The frozen comparison covers the same 1,289 unchanged input files and 1,273
root reports. Its sole hostile-ID change is Basaltstack gaining one hostile
finding (risk 125, previously 10). No existing hostile verdict is lost.
Current corpus: **202/622** with hostile findings, 201 with 1–3, one with five,
and 241 hostile findings total. Brew is now 4/10; other category detection
counts are unchanged. This distribution is not verified recall.

Final rules: `/tmp/sc-launchagent-rules.ZLb3Mq`, based on the preceding frozen
snapshot. Binaries remain the pinned Ruby-fix builds above. Input, rule, and
binary hashes were rechecked; scanner stderr is empty.

| Input or output | SHA-256 |
| --- | --- |
| `inventory.before.sha256` | `64f1398ffcf15b16679bbc83678e918698677d715db0314cdbfaf012dd9e4009` |
| `rules.final.sha256` | `6781712dbcb7a98afb1d7e3ac18f76dcd4a461d9f5400de382f670160efb5adf` |
| `final.jsonl` | `a4a2306307d74240383fd23875e549f6283f1edf7808dd9e2fc971921ba6c773` |
| `controls-final.jsonl` | `5b2489864e699d2f9e766d3ef4626026f98905b3582187cd75f23de37d667f61` |

Full pinned validation passes: hostile 65/65, benign 74/74, does-nothing
176/176, drop-exec 43/43, impact-wipe 66/66, obfuscation 80/80,
reverse-shell 25/25, simple-stealer 65/65. Log: `validate-jvm.log`.
The next confirmed Brew miss is Larkspurlite's keychain-result POST; its
source-to-body relationship still needs a precise solution.

## Browser-keychain POST relationship — 2026-09-15

Evidence: `/tmp/sc-keychain-triage.bwaXRq`. Existing AST queries now connect
Larkspurlite's browser-keychain command result, `strip`/`chomp`, and the value
interpolated into `Net::HTTP.post`'s body. The URI assignment must use a different
binding and feed the request URL; it cannot overwrite the secret. Formula
context supplies the package-specific objective. No new engine facts or flow
feature was required. The temporary query diagnostic reads source bytes only;
no hostile code was executed.

This is deliberately bounded structural coverage: literal or statically joined
command strings, optional `require "net/http"`, a literal HTTP(S) DNS endpoint,
and a single direct body interpolation in adjacent statements. Dynamic command
interpolation, IP/loopback endpoints, arbitrary intervening statements, helpers,
and general Ruby dataflow are not claimed. Structural probes also verify the
omitted-require and bare-interpolation forms without constructing another attack.

The new benign control exercises public command output, overwritten values,
an unrelated body value, a URI assignment overwriting the former secret, local
migration, and mutation inside the body or endpoint interpolation. All seven
counterexamples remain without high findings (file risk 3). The unchanged real
sample gains one hostile finding (risk 122, previously 5). No gate, specimen
name, operator hostname, or scenario-label predicate was added.

Frozen rules: `/tmp/sc-keychain-verified-rules.Pl5uzQ`, layered on the preceding
snapshot; binaries are unchanged. The full five-root scan contains 1,273 reports
over 1,289 unchanged inputs. Larkspurlite is the **only** hostile-ID change;
no existing hostile verdict is lost. Current corpus: 203/622 detected, 202 with
1–3 hostile findings, one with five, and 242 hostile findings total. Brew is now
5/10. Other categories and roots retain their preceding hostile counts.

| Input or output | SHA-256 |
| --- | --- |
| `inventory.before.sha256` | `64f1398ffcf15b16679bbc83678e918698677d715db0314cdbfaf012dd9e4009` |
| `rules.complete.sha256` | `5ca2c459036925b348c4036a0487441ae152763a280881eb86e97613ca5cfc37` |
| `complete.jsonl` | `325d879fb00185e342a7d1f049b6c6a99286b5aa0d3279189e737c6849ec5804` |
| `controls-complete.jsonl` | `a06b92fad921e57a48064a3435bb37f0aeadaa6a5fe631220caa420ae64c35f2` |

Input, rule, and binary hashes were rechecked; scanner stderr is empty.
Full pinned validation passes: hostile 66/66, benign 75/75, does-nothing
176/176, drop-exec 43/43, impact-wipe 66/66, obfuscation 80/80,
reverse-shell 25/25, simple-stealer 65/65. Log: `validate-complete.log`.

Next category: the 11 GitHub Actions packages. Existing reports already include
their `action.yml` members as `github_actions`; traversal is not the demonstrated
gap. A read-only inspection of Basaltbyte's composite action shows token/key
environment values piped into an HTTP upload inside `runs.steps[*].run`.
Inspect the available structured step facts before proposing engine changes.
Do not infer hostile behavior from the other packages' scenario labels.

## GitHub Actions pipeline precision and cache isolation (2026-09-15)

Evidence: `/tmp/sc-gha-triage.fBjnBR`; final frozen rules:
`/tmp/sc-gha-verified-rules.or35Vw`. The two GitHub Actions YAML rule files are
the only changes layered onto the preceding snapshot. Pinned analyzers remain
unchanged and their hashes were rechecked. All 1,289 hostile-input hashes still
match the preceding audit; no sample was changed or executed.

The legacy environment-exfiltration atoms matched documentation, comments,
`printenv curl` (a variable-name lookup), and `env | curl` without a stdin-upload
option. Both harmless counterexample fixtures initially scored 39 with three
suspicious findings; they now score 4 with none. Replace those loose atoms and
their unsupported umbrella with neutral, whole-run-value matches for direct
`env`/`printenv` uploads using curl `-d`, `--data`, or `--data-binary` and `@-`.
Both `jobs.*.steps[*].run` and `runs.steps[*].run` are covered. Two static-only
loopback diagnostic controls retain the actual upload observations (risk 3/4),
without a theft verdict. Four regression expectations were added.

These are bounded rules, not general shell parsing: filters, groups, other curl
options, and quoted forms remain outside their coverage. Basaltbyte's grouped
token/key upload is still a confirmed miss. Its action manifest already exposes
the run value but no shell symbols; extracting that value as a standalone shell
file produces the five expected calls (`echo` twice, `env`, `grep`, `curl`). No
metric or gate check substitutes for the missing command relationship.

The initial full scan revealed three unrelated Rust high-ID differences. The
same source bytes occur under `lib.rs`, `bootstrap.rs`, and `build.rs` names;
content-keyed analysis-cache reuse can lose filename-dependent findings. The
existing report-cache fast paths overwrite the target path without checking
path equivalence, and per-file cache stores can discard the original path when
no path-dependent finding fired. This needs a deterministic regression and a
cache fix, not a new trait feature. It is now the next task in the engine TODO.

For this rule comparison, explicitly disable the in-process memo as well as
persistent caches: `CLEAVE_ANALYSIS_MEMO_MB=0`, `CLEAVE_SKIP_CACHE=1`,
`STNG_STRING_CACHE=0`, `FILEFACTS_CACHE=0`. Both full scans contain 1,273 reports
with empty stderr and agree on **every suspicious and hostile ID**. Current
corpus counts remain 203/622 with hostile findings, 202 with 1–3, one with five,
242 hostile findings total, and 419 requiring further review. GitHub Actions
remains 0/11 with hostile findings; no coverage gain is claimed for this pass.

| Input or output | SHA-256 |
| --- | --- |
| `inventory.after.sha256` | `64f1398ffcf15b16679bbc83678e918698677d715db0314cdbfaf012dd9e4009` |
| `rules.after.sha256` | `f7e6488d40721c172c4e013cafc1a2940796bf544f614e263df5769494950991` |
| `memo-off-before.jsonl` | `dc2bda661ebba71096f545afb4674a1952994d385543fc72856628ad2a3f5c09` |
| `memo-off-after.jsonl` | `19329d6ddcdaf14522635bb642297e604be36bdc835a206bdfd9a9391e977656` |
| `controls-verified.jsonl` | `4523f8474559f861c9b39ae8284afe023cf13ce2820a36bd9e7628e66624a6ab` |

Full pinned validation passes: hostile 66/66, benign 79/79, does-nothing
176/176, drop-exec 43/43, impact-wipe 66/66, obfuscation 80/80,
reverse-shell 25/25, simple-stealer 65/65. Log: `validate-final.log`.

## Path-sensitive caches and deterministic risk (2026-09-15)

Both correctness issues identified by the preceding audit are fixed in cleave.
No trait predicates or hostile specimens changed in this pass.

The cache bug has a harmless failing-before/passing-after reproduction:
identical source scanned as lib.rs then build.rs lost the build-script finding;
the reverse order incorrectly assigned that finding to lib.rs. Full-report and
compact-file cache lookups now validate the original path with the existing
path-equivalence checks. Compact entries preserve their origin even when no
path-dependent rule matched. Composite suppressor/downgrade path inputs are
included, and equivalent paths still share results. The obsolete index of
positive path-dependent findings was removed rather than expanded.

The first cache-fixed scan agreed on every trait but exposed a separate risk
score instability (55 versus 56 for Duskwellpro). A confidence-permutation test
reproduced it with four neutral contributions scoring 4 instead of 3. Group
maxima are now accumulated in a canonical order with wider arithmetic, then
rounded once to the existing f32 score precision before ceil. Existing weights,
grouping and criticalities are unchanged. Controls preserve baseline totals and
genuine fractional rounding. Result-cache revision 14 prevents reuse of older
possibly misattributed verdicts or order-dependent scores.

Final evidence: `/tmp/sc-cache-path-triage.0lBOUW`. The rebuilt analyzers are in
`bin-final/`; the unchanged rule snapshot is
`/tmp/sc-gha-verified-rules.or35Vw`. Both full scans use the same inputs and
rules, with persistent/string/filefacts caches disabled; only
`CLEAVE_ANALYSIS_MEMO_MB=64` versus `0` differs. They produce 1,273 root reports
and 3,868 root/member records with identical trait IDs, criticalities,
confidences and risk scores. `final-parity.json` has an empty changed list;
both stderr files are empty. This comparison normalizes ordering, not the
semantic fields above; raw JSON byte identity is not claimed.

All 1,289 input hashes are unchanged. No suspicious or hostile IDs differ from
the previous memo-disabled baseline. Current corpus counts remain 203/622 with
hostile findings, 202 with 1–3, one with five, and 242 hostile findings total;
419 require further review. GitHub Actions remains 0/11 with hostile findings,
and its grouped credential pipeline remains the next analysis target.

Verification: cache unit tests 29/29; composite path-input test 1/1; end-to-end
cache tests 2/2; file-summary tests 26/26; final clippy and diff checks pass.
Full validation: hostile 66/66, benign 79/79, does-nothing 176/176,
drop-exec 43/43, impact-wipe 66/66, obfuscation 80/80,
reverse-shell 25/25, simple-stealer 65/65 (`validate-final.log`).
The new integration test is `../cleave/tests/cache_path_context.rs`.

| Input or output | SHA-256 |
| --- | --- |
| `inventory.after.sha256` | `64f1398ffcf15b16679bbc83678e918698677d715db0314cdbfaf012dd9e4009` |
| `engine-source.sha256` | `65b664de7a2b4e46fa19a6946aab57f727584db5c53111806a945d673aebe84e` |
| `bin-final/cleave-triage` | `82862672408201dd37f8a8a3ef3015bae98a774cb58d6e2bc12eefd6482ad6fa` |
| `bin-final/atomscan-triage` | `6c40aa1a849feb83b54e16f2a4f5721c3802ce1a3f3b1d0b65d88f06eefd5bc3` |
| `final-on.jsonl` | `c8e093b7d610d47d100fbe0298da007a1e06a5f840a07f99179736f8fdad29cc` |
| `final-off.jsonl` | `d7072930adf43be162aa97a6f3b72a131e276478315a7c10ae158fa7418e0a0f` |
| `final-parity.json` | `ef27ba8baf83090417c73e2a5fdf2a2483e143b6adb6b4633f6658c7a838e468` |

Rules retain manifest hash
`f7e6488d40721c172c4e013cafc1a2940796bf544f614e263df5769494950991`.
Source and binary hashes were rechecked. Local cleave/filefacts/stng build
overrides were confined to temporary build trees and command-line settings;
checkout manifests/lockfiles and unrelated working-tree edits were preserved.
No hostile package was installed, built, activated or executed.

## Inventory stability reconfirmed (2026-09-15)

After the user confirmed regeneration had stopped, a fresh five-directory scan
reproduced the latest baseline. All 1,289 input hashes match both the preceding
audit and the post-scan inventory. The pinned analyzer binaries and frozen rule
manifest also match the preceding audit.

Evidence: `/tmp/sc-stable-inventory.tjMmih`. `parity.json` records 1,273 roots
with identical paths and an empty changed list. Across 3,868 root/member records,
all 67,503 emitted trait instances agree on IDs, criticalities and confidences;
risk scores agree too. Comparison preserves finding multiplicity and normalizes
only ordering. Scan stderr is empty. Current-corpus totals remain 622 packages,
203 with hostile findings, and 202 with 1–3; this is reproducibility evidence,
not additional detection coverage or a completed triage audit.

The input-manifest SHA-256 remains
`64f1398ffcf15b16679bbc83678e918698677d715db0314cdbfaf012dd9e4009`.
The fresh `scan.jsonl` SHA-256 is
`dd15f08a0a012d52296e39cb22df74985af665eedc125f58aab39fc4e213b2c1`.
No specimens, rules or engine code were changed during this reconfirmation.

## Declared GitHub Actions scripts and precise shell uploads (2026-09-15)

Necessity review distinguished a missing format handoff from a parser bug:
filefacts already decodes run scalars, but shell AST rules could not inspect
them. `ParsedFile::embedded_sources()` now borrows declared bodies and known
shell types from those values. Cleave analyzes each as a separate bounded
logical source member. Unknown shells, runner expressions and exhausted limits
leave an analysis gap. Arbitrary YAML strings are not promoted to executable
code; no interpreter, package installer or remote action is invoked.

This also exposed a real reporting bug: nested members could have no parent
after archive report finalization. Missing parent links now resolve from their
immediate wrapper paths; existing explicit links are preserved. Regression
tests verify the resolved parent, not merely the presence of an ID.

The shell upload rule now joins two observations at shared AST offsets:
credential-like environment filtering and an actual stdin-to-HTTP pipeline.
Removed loose text/proximity rules had mistaken quoted commands, redirected
stdin, disconnected operations and non-upload curl calls for exfiltration.
Thirteen benign composite steps exercise these boundaries, including a
names-only intermediate transformation. A tree-sitter wildcard-root optimizer
quirk is handled by query structure, without a new matcher DSL or parser fork.
The canonical rule deliberately does not model arbitrary intermediate commands.

Final evidence is `/tmp/sc-gha-sources.RjSAuA`, with pinned `bin-final/`
analyzers and frozen rules `/tmp/sc-gha-final-v2-rules.JCHldj`. Earlier
`full-final.jsonl` results are superseded by `full-v2-{off,on}.jsonl`.
Unrelated concurrent PowerShell edits remain excluded from the frozen rules.

- All 1,289 input hashes are unchanged; input manifest SHA-256 remains
  `64f1398ffcf15b16679bbc83678e918698677d715db0314cdbfaf012dd9e4009`.
- Frozen rule manifest SHA-256:
  `551f558eeba774732065c0ce0dc658e94ebed56cc8c3809fb29cc2da900de9c7`.
- Memo-on/off scans agree on 1,273 roots, 3,862 root/member reports and all
  67,764 emitted trait instances, including criticalities, confidences and
  risk scores. `v2-parity.json` has an empty changed list. Both stderr files
  are empty. Rule and analyzer hashes were rechecked after scanning.
- Nine declared script reports were added. Fifteen LICENSE/README reports
  disappeared through compact report retention; no input or source member was
  removed. `v2-path-delta.json` records the exact paths.
- Current corpus: 205/622 with hostile findings, 204 with 1–3, one with five,
  244 hostile findings total. GitHub Actions now has 2/11 with hostile findings.
  These are detector counts, not verified recall or completed dispositions.
- The shared pipeline rule covers Basaltbyte's GHA upload and the reviewed
  AUR/Debian pipelines. Dunelinebyte also gains an existing download-stage
  finding; Indigoprime gains a suspicious service-related finding whose
  privilege/escalation wording still needs review.
- Removing the loose rule exposes a **genuine unresolved VSIX regression**:
  Amberbyte's task provider passes a shell credential-upload command assembled
  from JavaScript string fragments. The complete interpreter argument is not
  handed to shell analysis. Do not restore the loose regex or classify the
  fixture as benign. This is the next precision-preserving detection target.
- The Basaltbyte rule remains hostile with its gate removed and hostname
  replaced in a static, in-memory probe. No ungated specimen was written or
  executed, and no gate or actor hostname is part of the detection predicate.

Verification: filefacts parser tests 4/4; declared-source analyzer tests 4/4;
gap serialization 1/1; report/core tests 47/47; archive/step-scope integration
1/1 and cache-context integration 2/2. Clippy passes for the changed libraries
and integration target; diff checks pass. Final `validate-v2.log` is green:
hostile 67/67, benign 80/80, does-nothing 176/176, drop-exec 43/43,
impact-wipe 66/66, obfuscation 80/80, reverse-shell 25/25, simple-stealer 65/65.
All five GHA benign control files have zero suspicious or hostile findings.

## Service-directive false-positive correction (2026-09-15)

The follow-up confirmed that Indigoprime's newly visible service finding was
overstated. Its unit runs curl, but the package neither starts that unit nor
executes the response. Two harmless controls reproduced the broader rule bug:
an unactivated loopback health-check unit scored 40, and documentation containing
`ExecStart=/usr/bin/printf curl` scored 36. Both had a suspicious privilege-
escalation finding despite containing no such behavior.

Removed the two loose curl/wget atoms and their payload composite from
`objectives/privilege-escalation/modify-service`. The replacement
`micro-behaviors/os/service/config::systemd-http-client-command-text` describes
configuration text only, constrains the executable position and handles escaped
newlines in generated unit text. Existing service-context references were
updated. No engine feature, gate exclusion or specimen change was needed.

The controls now score 6 and 2, with zero high findings. The actual curl
directive retains the new notable observation; the printf/echo/logger examples
and curl-wrapper do not. Hierarchy expectations are in `expectations.toml`.
Final validation passes: hostile 67/67, benign 82/82, does-nothing 176/176,
drop-exec 43/43, impact-wipe 66/66, obfuscation 80/80, reverse-shell 25/25,
simple-stealer 65/65. Diff checks pass.

Final evidence: `/tmp/sc-service-precision.rA7JZL`, frozen rules
`/tmp/sc-service-v3-rules.rBbEku`, unchanged pinned analyzers from the preceding
pass. Only `full-v3.jsonl`, `controls-v3.jsonl` and `validate-v3.log` are final;
earlier attempts failed rule/schema checks and are not accepted verification.

- The five-directory scan has 1,273 roots, 3,862 members and 67,756 trait
  instances, with empty stderr. Root/member hostile IDs and confidences are
  unchanged. The only high-finding deltas are removal of the misleading service
  finding from Indigoprime, Wicklowcore, Basaltguard and Junipeersync.
- Static review confirms those four units invoke HTTP clients, not fetched
  response bodies. Wicklowcore and Junipeersync also contain scheduler/activation
  behavior; removing the false escalation claim does not establish benignness.
- All 1,289 input hashes still match the stable inventory. The rule manifest
  SHA-256 is `a9b15aada01a49bc8e0afca4d72610e103563537a58a0b9b2a95440a85d65f0d`;
  `full-v3.jsonl` SHA-256 is
  `2297cc77b87731b35d2f91213cf155299aa53eb4372d88615e4a1f93d0c8f979`.
  Analyzer and rule hashes were rechecked after scanning. Corpus totals remain
  205/622 with hostile findings, 204 with 1–3, one with five; 417 need review.

The VSIX gap remains unresolved. Inspection found array-shaped arguments,
separate literal fragments and no destructured import binding in the available
symbols; a broad string join would not prove an interpreter execution edge.
Required binding/argument/overwrite controls are recorded in the engine TODO.
No speculative bridge or security-specific metrics were added this pass.
The Dunelinebyte sample really executes its downloaded path, but the current
`quiet-fetch-hidden-stage` rule does not establish that relationship. Correcting
that inference while preserving real download-and-execute detection is also
open; the current hostile count must not be represented as verified recall.

## Hidden download versus execution (2026-09-15)

Removed `quiet-fetch-hidden-stage`: quiet download options plus a hidden output
path did not establish execution. A nine-step harmless control fixture previously
scored 124 with that hostile finding; it now scores 9 with no high findings.
Controls cover download-only, a different invoked path, an intervening overwrite,
failure fallback, opposite conditional branches, syntax-check-only invocation,
quoted examples, heredocs and an option-value ambiguity. Download observations
remain visible. The generic `fetch-output-hidden-stage` component also moved out
of objectives to the notable
`micro-behaviors/communications/http/download/cli::hidden-output-download-context`;
its consumers were updated instead of suppressing that neutral evidence.

The new `hidden-download-shell-execution` composite joins an actual hidden curl
output with a following shell invocation of the same literal path. Both atoms
use shell AST structure; the composite joins shared source offsets at zero-byte
distance. Dunelinebyte retains one hostile finding for its real download/run
sequence. Precision is 5.7, verified independently of the benign controls.
An in-memory static probe passes eight cases: original, gate removed, hostname
and path changed, quiet flags removed, top-level commands, compound body,
conditional body and consistently quoted paths. No derived payload was written
or executed. Variable paths, mixed quoting, additional curl argument layouts and
intervening chmod chains are not covered by this new relation; they are not
claimed as analyzed merely because other findings exist.

The initial validation run exposed 33 **count-only** drop-exec failures: each
retained two hostile findings after removal of the false third observation.
The walked drop-exec floor is now two, consistent with the user's 1–3 target.
No duplicate hostile trait was invented to preserve a three-finding floor.
Positive Dunelinebyte and negative execution-relationship assertions were added.
Final `validate-fixed.log` passes: hostile 68/68, benign 83/83, drop-exec 43/43,
does-nothing 176/176, impact-wipe 66/66, obfuscation 80/80, reverse-shell 25/25,
simple-stealer 65/65. The older delivery/chmod/background pairings still need
relationship review; passing their count floor does not establish their accuracy.

Evidence: `/tmp/sc-download-execution.7iXpkP`, frozen rules
`/tmp/sc-download-rules.O7Mc0n`, unchanged pinned analyzers from the GHA pass.
The five-directory memo-disabled scan has 1,273 roots, 3,862 members and 67,764
trait instances, with empty stderr. Root high-finding changes are exactly the
Dunelinebyte replacement and loss of the loose finding on Clovermarksync's
macOS package. All 1,289 input hashes are unchanged; rule and analyzer hashes
were rechecked. Rule-manifest SHA-256:
`1f107d7e25db22289114daebfbb5ae4c6814c099e17e657eb651832fde1b0adf`.
Scan SHA-256:
`58fbdf03f7f2c08ee01c36e4502f086dfda61d5285475e3ed320a4c0e5e45311`.
Current corpus: 204/622 with hostile findings, 203 with 1–3, one with five,
243 hostile findings total; 418 without hostile findings require review.

**Clovermarksync remains a genuine detection gap, not a benign disposition.**
Its actual postinstall script downloads a hidden `.pkg` and invokes
`/usr/sbin/installer -pkg` on that path. The archive report instead retains
`Scripts!!Scripts`, an opaque decompressed old-ASCII CPIO body beginning with
`070707`, rather than its named postinstall member. The existing CPIO reader is
newc-only and is reached through RPM extraction; decompression has no CPIO
container dispatch. A manually extracted original postinstall has a shell AST,
but still has no high finding with the corrected rules. Consequently this needs
both proper inner-container traversal and a precise download-to-installer
relationship—not just another broad download regex. The VSIX string/argument
gap remains open too. No engine changes or specimen moves occurred this pass.

## CPIO reader correctness and stable-inventory recheck

The user's stable-inventory confirmation was verified: all 1,289 hashes match
the preceding pass before and after this scan. Following `x-triage-bad`, this
pass repaired missing-analysis behavior in the scanner without changing or
executing specimens, adding gate-based exclusions, or inflating trait counts.

Two harmless regressions failed before the repair: an ordinary unaligned newc
file body hid the following member, and an invalid header was accepted as a
successful end of archive. The reader now consumes each entry's alignment
padding and propagates malformed/truncated input errors. It also bounds name
allocation before the dependency parser allocates, applies cancellation and
byte limits to skipped data, and passes original names to the shared sanitizer
instead of removing absolute-path prefixes. Analysis-cache version 16 prevents
reuse of old silently incomplete results. No new metrics or matcher features
were needed.

RPM header facts now survive an unreadable payload, accompanied by the existing
**notable**, not hostile, incomplete-extraction diagnostic. Static decompression
confirmed that all ten corpus RPMs begin with `07070X`. This is the RPM stripped
CPIO format: member indexes refer to metadata in the RPM header, rather than
carrying ordinary newc headers ([RPM format documentation](https://rpm-software-management.github.io/rpm/manual/format_v4.html)).
It is not proof of corruption. These payloads remain untraversed; the padding
repair must not be claimed as new detection coverage for them. Old-ASCII
`070707` macOS PKG traversal and the download-to-installer relationship also
remain open, as does the VSIX interpreter-argument gap.

Verification passes: 11 focused CPIO tests, one end-to-end RPM test covering
plain/gzip and valid/partial/unsupported payloads, 29 cache tests, strict clippy,
and all eight validation suites: hostile 68/68, benign 83/83, does-nothing
176/176, drop-exec 43/43, impact-wipe 66/66, obfuscation 80/80, reverse-shell
25/25, simple-stealer 65/65.

The memo-disabled frozen-rule scan retains 1,273 roots and 3,862 root/member
records, with empty stderr. All suspicious/hostile IDs, criticalities and
confidences agree with the preceding scan. Only ten RPMs change their normalized
finding inventories: each gains the incomplete-extraction diagnostic. Seven
stop displaying three baseline-only metadata/fixture traits because an existing
low-tier suppression policy now sees a notable finding; RPM identity and fact
fields are unchanged. Three RPM risk scores increase by one. There are now
67,753 displayed trait instances, not additional verified detections. Current
corpus counts remain 204/622 with hostile findings, 203 with 1–3, one with five,
243 hostile IDs total; 418 still require review.

This is not byte-for-byte report equality: 112 Java member import lists differ
only in order, and 16 Zig object context excerpts differ. No other compact
member fields differ after normalizing import order and excluding the documented
traits/risk/context fields. Context excerpt reproducibility was not diagnosed
in this repair.

Evidence: `/tmp/sc-cpio-repair.SocDAV`, including pinned binaries and targeted
build-source hashes, red/green tests, validation, payload signatures and deltas.
The build snapshot differs from the final checkout only by a subsequent comment
clarification among the four targeted files; no executable code changed after
the final build. Frozen rules remain `/tmp/sc-download-rules.O7Mc0n` and their
manifest and binary hashes were rechecked.

- Input-manifest SHA-256: `64f1398ffcf15b16679bbc83678e918698677d715db0314cdbfaf012dd9e4009`.
- Rule-manifest SHA-256: `1f107d7e25db22289114daebfbb5ae4c6814c099e17e657eb651832fde1b0adf`.
- Scan SHA-256: `2e00e0a1012dabfaedb33067920e375511a27424f1c30d55501a0c54b2a05f70`.

## ASCII CPIO members and recovered macOS credential upload

The next `x-triage-bad` pass adds the missing member boundary rather than a
marker-based rule. Filefacts now identifies and indexes the old/new ASCII CPIO
layouts through its existing archive-member API; cleave handles extraction,
path safety, budgets and recursive analysis. This ownership follows
`SOURCE_ANALYSIS.md`. Parser limits cover 65,536 entries, 1 MiB names and 16 MiB
of headers/names/retained link targets. Complete bodies remain available even
when subsequent alignment padding is truncated. No links or devices are
created, no archive execute bits are applied, and collisions cannot overwrite
earlier extracted evidence. Cache version 17 invalidates old opaque results.

The full-members scan of ten macOS packages now reports 80 root/member records,
including 20 CPIO containers and all ten named preinstall/postinstall scripts,
without incomplete-extraction diagnostics. Compact output retains only nine of
the ten scripts because Indigocore's low-risk script is omitted by the existing
report-retention policy, not because parsing failed.

Riftwoodkit is a verified recovered detection: its preinstall script runs an
environment listing through a credential-name filter and pipes that output into
an HTTP request body. The existing source relationship rule now gives the root
package one hostile finding, at risk 119 instead of 1. Its gate and hostname
are not detection predicates. A package-level expectation was added. No new
detection rules or specimen bytes were needed.

Other newly visible behaviors still need accuracy work: Fennellite's keychain
secret upload, Larkspursync's deletion of user folders, and Tidecrestforge's
written/loaded launch-agent downloader. Pumicestack's function definition must
not be mislabeled as immediate execution; Junipeerkit's macOS `/etc/profile.d`
file and Indigocore's own-receipt removal need disposition before hostile labels
are assigned. Clovermarksync's now-visible downloaded-package installation
still needs a precise relationship and criticality review.

The checksum layout is indexed without verifying its additive checksum;
hardlink aliases retain their stored bodies rather than reconstructed content.
Binary CPIO and RPM's stripped `07070X` remain unsupported, and the older RPM
newc reader remains a separate legacy path. This is missing package-format
support with demonstrated benefit, not a claim of general archive parity.

Final evidence: `/tmp/sc-cpio-members.Y7aTWu`, pinned binaries in `bin-final-v3`.
Parser tests pass 7/7, extraction safety tests 4/4 and file identification tests
291/291; gzip/CPIO and RPM end-to-end regressions and strict lint checks pass.
All eight validation suites pass: hostile 69/69, benign 83/83, does-nothing
176/176, drop-exec 43/43, impact-wipe 66/66, obfuscation 80/80, reverse-shell
25/25, simple-stealer 65/65.

The final memo-disabled frozen-rule scan (`full-v3.jsonl`) retains all 1,273
roots with 3,871 compact root/member records and 68,097 trait instances. Only
the ten macOS packages change normalized findings/risk relative to the preceding
CPIO-reader repair. Earlier root high IDs, criticalities and confidences all
survive; Riftwoodkit is the sole added high finding. Final normalized reports
also agree with this pass's pre-hardening scan. The full macOS member scan is
`macpkg-all-members-v3.jsonl`. Both final scans have empty stderr.

Corpus totals are 205/622 with hostile findings, 204 with 1–3, one with five,
244 hostile IDs total; 417 still require review. All 1,289 specimen/support-file
hashes are unchanged. Frozen rules remain `/tmp/sc-download-rules.O7Mc0n`;
their manifest, pinned binary hashes and source snapshots were rechecked. No
detection rules changed, and no specimens were modified or executed.

- Input-manifest SHA-256: `64f1398ffcf15b16679bbc83678e918698677d715db0314cdbfaf012dd9e4009`.
- Rule-manifest SHA-256: `1f107d7e25db22289114daebfbb5ae4c6814c099e17e657eb651832fde1b0adf`.
- Scan SHA-256: `9519ec1512fe755729cc09e2e5520d969c7c5112ec49701e2fa5cb893ac49e03`.

## Personal-folder deletion: behavior, not gates or path mentions

The stable inventory still matches the preceding CPIO pass byte for byte.
Larkspursync's macOS postinstall script actually invokes recursive deletion of
Documents, Desktop and Pictures. The old shell capability missed indentation,
while the old `shell-delete-user-docs` detector merely searched for Desktop and
Documents text in one order. Neither was an adequate behavioral detector.

The recursive capability now uses a command AST. A second neutral atom requires
actual HOME expansions and distinct, exact top-level personal-folder operands;
their same-command join produces one hostile user-data wipe finding. Existing
call facts flatten single-quoted literal dollars and double-quoted expansions
to the same string, so the already-supported AST matcher is necessary here.
Locally rebound HOME and an rm function conservatively suppress host-target
inference. No engine fields, metrics or parser changes were added.

The order-dependent document text rule was removed and its macOS composite now
references the canonical behavioral objective. Validation also exposed ordinary
`rm -- -filename` handling labeled as masquerading; that observation was moved
to the existing neutral file-command hierarchy, with its dropper consumer
updated. These are taxonomy/precision corrections, not additional hostile
signals added to reach a count.

Larkspursync now has one hostile finding at risk 123 (previously 7). Eighteen
static in-memory probes pass: eight positive forms include renamed/removed
gates and hostname, absolute rm, braced HOME, split/long options and two-folder
targets; ten negative forms cover quoting, literal dollars, repeated operands,
nonrecursive operations, option termination, subdirectories, rebinding,
shadowing and disconnected commands. Ten committed benign fixture controls
have no suspicious or hostile findings, at risk 3–4. No specimen was changed,
activated, installed or executed.

The final frozen-rule scan retains 1,273 root reports, 3,871 compact root/member
records and 68,105 trait instances. All earlier suspicious/hostile IDs,
criticalities and confidences survive at both root and retained-member levels;
the only added high finding is Larkspursync's wipe, propagated through its
container hierarchy. Current corpus: 206/622 with hostile findings, 205 with
1–3, one with five, 245 hostile IDs total; 416 remain for review. These are
coverage counts, not verified recall.

One lower-severity regression is explicit: Zig Yarrowguard loses its neutral
shell-recursive-delete finding (risk 33 → 32). The real command is assembled
and passed to `/bin/sh -c`, but the heuristic plain-string path deliberately
does not force the detected shell grammar. Its old text finding therefore
does not transfer to the AST rule. A declared interpreter/argv/value handoff
needs investigation; blindly parsing shell-looking strings would revive
quoted-example false positives. This limitation remains on the TODO list.

Final validation: hostile 70/70, benign 93/93, does-nothing 176/176, drop-exec
43/43, impact-wipe 66/66, obfuscation 80/80, reverse-shell 25/25 and
simple-stealer 65/65. Evidence: `/tmp/sc-home-delete.HGyN4t` (`*-v3` results);
rules: `/tmp/sc-home-delete-rules.BEYqsj`; binaries remain the preceding pinned
`/tmp/sc-cpio-members.Y7aTWu/bin-final-v3` pair. Final scan/control stderr is
empty; all 1,289 specimen/support-file hashes remain unchanged.

- Input manifest SHA-256: `64f1398ffcf15b16679bbc83678e918698677d715db0314cdbfaf012dd9e4009`.
- Rule manifest SHA-256: `0c6642f1ed8b6f124ddc3412ba1b43d6fe569914b60954cb31522282c8967035`.
- Final scan SHA-256: `1b15f9207c146f52853eda6e84024a80f504de306f593c40803f51ed3d6ef26f`.

## Keychain result uploaded through shell stdin

Fennellite's postinstall script captures a browser Safe Storage password and
uses that same variable as printf output piped into curl's HTTP request body.
The new rule requires that actual relationship, joining the source call's
ordered arguments with a bounded syntax-based transport observation. Existing
facts and AST matching suffice; no engine changes or security-specific metrics
were added. The transport atom lives under HTTP request/body because the same
mechanism legitimately posts health checks and ordinary service credentials.

The match is independent of the activation file, original variable name and
hostname. It handles direct upload or an intervening side-effect-free nonempty
test, and rejects reassignment, disconnected variables, literal dollars,
stdout/stdin redirection, header-only requests and shadowed commands. An
asynchronous assignment cannot update its parent's variable; the probe that
exposed that rule error now passes, with a committed benign regression.

The old text-only `keychain-safe-storage-query` was moved from trojanized-library
intent into neutral keychain command references, and its consumer was updated.
Its text alone proves neither a query nor exfiltration. This removes that
unsupported suspicious claim from six roots (15 retained root/member records),
without losing any hostile finding or any other high ID/criticality/confidence.
C Sablewoodworks consequently drops from risk 45 to 6 and remains pending
behavioral review; this correction is not a benign disposition for that package.

Fennellite now has one hostile finding at risk 122 instead of 45, propagated
through four retained container/member records. All 27 in-memory probes pass
(11 positive, 16 negative), and all thirteen committed benign controls have
zero suspicious/hostile findings at risk 3–7. The objective reports precision
6.2. Scope remains bounded: consecutive top-level statements, supported literal
CLI forms and simple variable expansions, not general shell dataflow.

Final frozen scan: 1,273 roots, 3,871 compact root/member records and 68,117 trait
instances, with empty stderr. Corpus totals: 207/622 with hostile findings,
206 with 1–3, one with five, 246 hostile IDs total; 415 still require review.
The sole changed hostile root verdict is Fennellite's recovered upload.
Validation passes all eight suites: hostile 71/71, benign 106/106, does-nothing
176/176, drop-exec 43/43, impact-wipe 66/66, obfuscation 80/80, reverse-shell
25/25 and simple-stealer 65/65. No specimen bytes changed or executed.

Evidence: `/tmp/sc-keychain-upload.UWRkhL`; final scan `full-v2.jsonl`; frozen
rules `/tmp/sc-keychain-rules.BRSZ3N`. Binaries are unchanged from
`/tmp/sc-cpio-members.Y7aTWu/bin-final-v3`. The initial `full.jsonl` was started
before the snapshot copy completed and reported 6,737 unresolved references;
it is invalid and excluded from all final counts. The final snapshot differs
from the preceding one in exactly the five task rule files, and its manifest
was checked after scanning. All 1,289 input hashes still match the baseline.

- Input manifest SHA-256: `64f1398ffcf15b16679bbc83678e918698677d715db0314cdbfaf012dd9e4009`.
- Rule manifest SHA-256: `2724cafe35f875800cf75853ce38d13f5b753a8836fac2f1ad7b20a09f364f23`.
- Final scan SHA-256: `1ccfaa3d52301e03e87cfee491ca28eef73c5bfbc036f225be66078d6e6e4eb5`.

## RPM header-scriptlet follow-up (2026-09-15)

The user confirmed regeneration was finished. The five-root inventory still
matches the preceding baseline: 1,289 inputs, SHA-256 manifest
`64f1398ffcf15b16679bbc83678e918698677d715db0314cdbfaf012dd9e4009`.
No specimen was changed or executed.

Header scriptlets were omitted from source analysis independently of the known
stripped-payload gap. Filefacts now exposes the nine scalar lifecycle bodies
through its existing declared-source API, and cleave reuses its existing bounded
adapter. No new security metric or duplicate RPM parser was introduced.
Real-package checking caught a bug in this implementation before acceptance:
the interpreter decoder initially required STRING_ARRAY, while these ten RPMs
use STRING with count one. Both supported forms now normalize to argv; malformed
present fields remain unknown, never a default shell. See SOURCE_ANALYSIS.md.

Evidence: `/tmp/sc-rpm-scripts.OTqfjQ`. Use `bin-v2`, `full-v2.jsonl`,
`rpm-members-v2.jsonl`, `final-index-v2.json`, and `high-delta.json`.
The earlier unsuffixed scan used the faulty interpreter decoder and is not the
final result. The unchanged rule snapshot is `/tmp/sc-keychain-rules.BRSZ3N`.

The final scan retains 1,273 roots, 3,881 records and 68,445 trait instances.
All ten RPM bodies appear as separate shell members. Only RPM roots change
in the risk/high-ID comparison; no prior suspicious or hostile finding is lost
across roots or members. Stderr contains only the debug-build performance warning.
Scan SHA-256: `440521232d69f0c3c5cd588682a4c4c60abaedc3ff987e0324497b604005c58c`.

The three new hostile labels are **not verified recall gains**:

- Duskwellpro writes a truncated Ed25519 key. The existing authorized-key
  composite does not establish that this is a functional backdoor.
- Fennelbyte schedules curl with its response discarded, not executed. Its
  generic cron/network combination does not by itself establish hostile intent.
- Brackenworks modifies `/etc/ld.so.preload`; the referenced shared object's
  contents remain unavailable through unsupported stripped-payload traversal.
  The rootkit claim needs stronger evidence or corrected classification.

Eldergroveworks and Foxtailpro reveal remote fetch-to-shell behavior but still
lack hostile verdicts; Gableutils' filtered environment upload has an intervening
base64 stage outside the existing pipeline rule. These are trait-level follow-ups,
not evidence that more engine metrics are needed. The new Eldergroveworks
expectation protects source visibility without pretending its verdict is solved.
Junipeerkit's log cleanup and the remaining RPMs still need full disposition.

Parser tests (10) and CPIO, GitHub Actions and RPM integration tests (3) pass;
strict filefacts linting passes. Trigger arrays and stripped payloads remain
unsupported, with partial-analysis diagnostics retained.
Final `make validate` also passes all eight suites, including the added RPM
visibility expectation: hostile 72/72, benign 106/106, does-nothing 176/176,
drop-exec 43/43, impact-wipe 66/66, obfuscation 80/80, reverse-shell 25/25 and
simple-stealer 65/65 (`validate-final.log`). Frozen rule hashes, pinned binaries
and the final input manifest were rechecked; all match.

## Encoded environment upload and cron precision (2026-09-15)

Evidence: `/tmp/sc-env-encoding.vNGTRy`; final scan `full-v2.jsonl`; unchanged
analyzers `/tmp/sc-rpm-scripts.OTqfjQ/bin-v2`; frozen rules
`/tmp/sc-env-encoding-rules.M9xMLs`. This is trait-author work, not new engine
metrics. The preceding RPM pass is the comparison baseline.

The existing source pipeline query now permits one argument-free base64 encoder
between the environment-name filter and curl's stdin body. Decoder flags,
file inputs, stage redirects and arbitrary intermediaries remain outside the
match. Existing same-node joining establishes credential selection and transport
in one pipeline. Local definitions of participating tools exclude uncertain
command identities. Neither gate names nor destination identities are selected.

All 28 in-memory static probes pass, including direct/encoded/grouped pipelines,
gate presence/absence, destination changes, redirects, disconnected credential
selection, ordinary environment names, shadowing and quoted examples. The first
probe expectation for a whole-group stdin redirect was wrong: env does not read
stdin, so redirecting the group's input does not sever its stdout upload. The
corrected positive expectation is in `probe-v2.log`; no rule broadening was
needed for it. The objective's reported precision is 6.4. Nine benign controls
have no suspicious or hostile findings.

Two actual upload chains gain one hostile finding each: RPM Gableutils
(risk 9 to 124) and DEB Gablekit (9 to 125). Both bodies filter environment
entries, encode their values and send them as an HTTP body. Both now have
package-level expectations.

The old portable cron composite inferred hostility from curl/crontab text alone.
All three matching package scripts were inspected: AUR Brackenworks, DEB
Basaltguard and RPM Fennelbyte schedule HTTP requests and discard the response.
They do not establish response execution or secret upload. Remove that composite;
relocate its two neutral reference atoms under HTTP download and cron, preserving
their matchers rather than hiding them with lower severity. A benign recurring
health-check regression verifies both capabilities without a hostile inference.
The package artifacts remain unchanged pending complete disposition; removing
one unsupported finding is not a declaration that their entire contents are safe.

Final five-root scan: 1,273 root reports, 3,881 retained records, 68,447 trait
instances. The only high-ID additions are credential-upload findings on the two
packages above; the only losses are the removed cron composite on three packages
(six root/member occurrences). No other suspicious or hostile findings are lost.
The current corpus has 209/622 hostile-labeled packages, 208 with 1–3 and one with
five. Counts decreased despite better detection accuracy; they are not verified
recall. Stderr contains only the debug-build performance warning. The 1,289-input
manifest is unchanged; frozen rule hashes were rechecked.
Final `make validate` passes all eight suites: hostile 74/74, benign 116/116,
does-nothing 176/176, drop-exec 43/43, impact-wipe 66/66, obfuscation 80/80,
reverse-shell 25/25 and simple-stealer 65/65 (`validate-final.log`).
Scan SHA-256: `bdcf6438bd132b8318fa980e86bfdba5452656207c05067b8869cb91b00927e5`;
rule manifest SHA-256: `1753f7768dd956caa8717c821c23d5aa455fd6703a6432fe2d4068e1f2e98702`.

Remaining RPM concerns include truncated SSH keys, uninspected preload libraries,
and a misnamed JVM crontab string observation at the RPM root. The latter follows
the engine's existing archive-family applicability behavior, not a new scriptlet
parser failure. Inspect neutral trait placement/format constraints before changing
the engine. Remote fetch-to-shell and log-cleanup verdict work also remains open.

## SSH reference and key-framing precision (2026-09-15)

Evidence: `/tmp/sc-ssh-verdict.o3VpA7`; final `full-v3.jsonl`; frozen rules
`/tmp/sc-ssh-rules-final.7OuMyo`; unchanged analyzers
`/tmp/sc-rpm-scripts.OTqfjQ/bin-v2`. Earlier scans/validations in the evidence
directory are intermediate results, not the final baseline. No engine change
was needed, and no hostile specimen was altered, installed or executed.

The portable authorized-key composite only combined nearby `authorized_keys`
and key-like text. It did not establish a write, key validity or unauthorized
access. Remove that composite and relocate its two reference matchers under
`micro-behaviors/communications/ssh/keys`, with names/descriptions that state
only what they observe. A second unreferenced credential-access composite
combined public-key and path references; it also mislabeled pure documentation
and has been removed. Its existing neutral constituent observations remain.

Validation caught a further taxonomy error even though the JS benign control
had no high findings: a generic SSH-path reference was filed under SSH backdoors.
Relocate it to `micro-behaviors/fs/path/secret-config` and update its three
consumers. Do not relax the forbidden-hierarchy expectation to hide that error.
All 99 prior root/member occurrences of these three relocated atoms retain their
neutral replacement findings in the final scan.

Read-only examination found malformed key literals in all 16 current-corpus
packages matched by the portable composite. A compiled Java package, found
during high-finding comparison, contains another malformed Ed25519 literal.
`key-structure-final.jsonl` records 17 malformed current-corpus literals and one
structurally complete key in the older npm installer. The audit checks the
algorithm/length framing specified by [RFC 8709 section 4](https://www.rfc-editor.org/rfc/rfc8709.html#section-4),
not private-key ownership or curve-point validity. Some literals are invalid
base64; others declare 32 key bytes but only contain four or 23.

The existing Ed25519 literal rule accepted these truncated values. Its regex
now requires the fixed algorithm/length prefix, 32-byte key field and token
boundary. Partial key-like text remains a neutral observation; it cannot satisfy
the complete-key atom. This is a bounded protocol-format rule, not a new metric,
parser API, gate signature or specimen repair. Ten static structural probes pass.
Five benign reference fixtures have no suspicious or hostile findings, including
complete-public-key documentation. Their expectations protect both recognition
of complete framing and rejection of truncated framing.

The 16 package source bodies are not automatically benign: most write access
configuration and several restore timestamps. PHP Dunelinekit retains its
separate stealth-rewrite hostile finding. C Junipeerflow also uses `%%s` in
its path format string, producing a literal `%s` path rather than substituting
HOME. These fixture/behavior issues require disposition, not invented successful
SSH access. RPM payload visibility remains incomplete. No package was moved
solely because its embedded key is malformed.

Final scan: 1,273 roots, 3,881 retained records, 68,366 trait instances. The
current corpus has 194/622 hostile-labeled packages: 193 with 1–3, one with five.
Fifteen packages lose their last hostile label; a sixteenth retains PHP's
stealth-rewrite finding. The older npm source retains two hostile findings and
its archive retains four (down from five); deduplication remains pending.

The high-ID comparison contains no additions. Losses are limited to the removed
portable/reference composites and relocated reference atoms, malformed-key
observations, and the Perl backdoor composite that depended on a malformed key.
No unrelated high finding is lost. The 1,289-input manifest is unchanged, and
frozen rule and analyzer hashes were rechecked. Stderr contains only the debug
build performance warning. Final `make validate` passes all eight suites:
hostile 75/75, benign 121/121, does-nothing 176/176, drop-exec 43/43,
impact-wipe 66/66, obfuscation 80/80, reverse-shell 25/25, simple-stealer 65/65.

- Scan SHA-256: `e01e374d8ecae79d904cea743534925ad8c9ebb6d1822f4180033f441ad3b219`.
- Rule manifest SHA-256: `42a022b7874681d0d5a898aa2b157f1846f9d0a0c3e2748bf8f6af5dcf7cdaec`.

## Shell curl response-to-interpreter precision (2026-09-15)

The stable inventory was rechecked against all 1,289 baseline inputs. This
pass uses the same pinned RPM-scriptlet analyzers as the SSH pass, frozen rules
`/tmp/sc-curl-pipe-rules.gNUR7A`, and evidence `/tmp/sc-curl-pipe.E1aYoF`.
The four unrelated PowerShell edits remain excluded from the comparison.
No specimen was executed, installed, modified, or moved.

The old shell fetch-exec rules combined file-wide curl/shell text, missed
grouped `-fsSL` flags and bare `sh`, and could confuse an explicit `sh -c`
command or redirected stdin with execution of the downloaded body. The new
notable capability `micro-behaviors/process/create/shell/pipeline::curl-response-shell-stdin`
checks the actual pipeline edge, bounded known curl options, shell stdin mode,
and redirections. Existing call facts do not express that edge; the existing
tree-query escape hatch is sufficient. No engine feature was added.

Quiet HTTP-to-shell execution is also a legitimate installer idiom. The
curl-only hostile wrapper and the curl alternative in its duplicate bash rule
were removed, not merely demoted or given a gate-based exception. The observed
capability remains visible. Independent evidence is still needed for hostile
delivery or a complete package disposition; no domain, filename or random gate
is treated as that evidence.

Forty-one static in-memory probes pass (`probe-final.log`), including gate-free,
environment-gated, file-gated and changed-host variants. Negatives cover
`sh -c`, script arguments, syntax checking, input redirection, saved downloads,
header-only requests, disconnected commands, unrelated quiet flags, quoted
examples and locally shadowed tools. Five durable benign fixtures have no
suspicious/hostile findings; only the bootstrap matches the new capability.
`scripts/test-shell-curl-pipeline.sh` asserts those individual-ID results without
changing the engine's deliberately hierarchy-only validation expectations.

The frozen five-root scan (`full.jsonl`) adds this observation to five packages:
RPM Elder Grove Works post-install, RPM Foxtailpro verification, DEB Pumicecraft
debconf configuration, DEB Dunelineguard post-install, and AUR Riftwoodkit build.
The ten new retained findings are those five root roll-ups and their five script
units, not ten distinct attacks. Foxtailpro's visible script downloads and
executes; its `wipe` filename is not evidence of wiping. Unsupported stripped
RPM payloads still prevent a complete package verdict.

Final scan counts: 1,273 roots, 3,881 retained records, 68,376 trait instances.
Suspicious/hostile findings are unchanged: 194/622 current-corpus packages have
hostile labels (193 with 1–3, one with five), with 428 still requiring review.
This is not verified recall or completion of the corpus goal. Stderr contains
only the debug-build performance warning. The input and frozen-rule manifests
were rechecked; `high-delta.json` is empty in both directions.

Final `make validate` passes all eight suites: hostile 76/76, benign 126/126,
does-nothing 176/176, drop-exec 43/43, impact-wipe 66/66, obfuscation 80/80,
reverse-shell 25/25 and simple-stealer 65/65 (`validate-final.log`). The initial
run rejected leaf IDs incorrectly used as hierarchy prefixes; those assertions
were corrected and exact-ID checks pass in the dedicated static regression script.
It also exposed older neutral command-reference traits still filed under
dropper objectives. Their placement remains tracked for a bounded follow-up;
passing the score caps is not a claim that all existing labels are organized.

- Scan SHA-256: `9c1774fac18e8292b0ea39e2115151bab611eee621713c57066de847ef5c9f05`.
- Rule manifest SHA-256: `3b7b624cf105e836d461118ad63df2a1cce06ca9174ca0d9cfa80a54567d5bae`.
- Input manifest SHA-256: `64f1398ffcf15b16679bbc83678e918698677d715db0314cdbfaf012dd9e4009`.

## VSIX Node interpreter-argument boundary (2026-09-15)

Amberbyte's task provider really passes `/bin/sh`, `-c`, and a credential-filtered
environment-to-HTTP pipeline to Node's `execFile`. The command is assembled from
two adjacent JavaScript string literals. Existing symbol facts retain the array
shape but not its ordered contents, and the flow graph retains separate literal
inputs under merges. Joining every nearby string would not prove this call edge.

The necessity review found that an existing AST query can express the reviewed
form without new engine metrics, value-graph changes, a second parser or a
general embedded-code bridge. Two neutral observations establish a top-level
const destructuring of a `require("child_process")` result and the exact shell
argv at the call. The binding observation is named as syntax, not an assertion
that any function named `require` is genuine. The hostile composite combines
the two, with conservative whole-file exclusions for lexical replacements and
dynamic lookup. Its measured authoring precision is **6.6**.

The matcher accepts a direct literal or a two-literal `+` expression, known
shell paths with `-c`, no options object, and an optional inline callback.
Options are not harmless extra arguments: Node documents that `execFile` runs
the executable directly by default, while `options.shell` can select another
interpreter. Unknown options are therefore not assumed to preserve execution.
See the [Node child-process contract](https://nodejs.org/api/child_process.html#child_processexecfilefile-args-options-callback).
Known curl data options and flags, whitespace variations, changed hosts and
`printenv` are covered. Selection, upload body and destination must be parts of
the same complete command; file-wide text proximity cannot satisfy the rule.

All 48 static in-memory probes pass (`probe-v7.log`). They cover the actual
package source, gate removal, changed host, direct/concatenated strings, shell
and flag variants, and negative controls for logging, quoting, wrong argument
positions, syntax-only invocation, replacement shell options, dynamic/overwritten
values, local functions, nested destructuring, class/generator/parameter/catch
bindings, `with`, `eval`, and a different module export renamed to `execFile`.
Eight durable benign fixtures score 4–5 with no suspicious or hostile findings
(`controls-final.jsonl`). The real VSIX has a hostile expectation requiring the
credential-exfiltration hierarchy. No specimen was executed or modified.

The frozen five-root scan changes only Amberbyte's high findings: one new
hostile ID on its source member and its package roll-up. There are no losses
at any severity. Other additions are neutral binding-syntax observations;
`traits-added.jsonl` contains 28 binding observations and the two source/root
pairs for argv and credential-upload observations. These are retained findings,
not counts of independently verified attacks.

Final totals: 1,273 root reports, 3,881 retained records, 68,408 trait instances.
Current corpus: **195/622** hostile-labeled, 194 with 1–3 and one with five;
427 remain to review. This is still not verified recall or completed triage.
Final `make validate` passes all eight suites: hostile 77/77, benign 134/134,
does-nothing 176/176, drop-exec 43/43, impact-wipe 66/66, obfuscation 80/80,
reverse-shell 25/25 and simple-stealer 65/65. Earlier intermediate scans and
validation attempts are not the final evidence.

Reproduction: `/tmp/sc-vsix-call.770Cc9`, `full-final.jsonl`, `final-index.json`,
`high-delta.json`, `probe-v7.log`, `rule-test-final.log`, `controls-final.jsonl`
and `validate-final.log`. Frozen rules: `/tmp/sc-vsix-final-rules.FVxzy5`.
The pinned analyzers and all 1,289 input hashes match the preceding pass; frozen
rules were rechecked. Stderr contains only the debug-build performance warning.
The four unrelated PowerShell edits remain excluded from the frozen comparison.

- Scan SHA-256: `7f9ba0ad5ce3805fad956d3751d44262c29b0d8c329cb33ec26813040f399398`.
- Rule manifest SHA-256: `1e4a1c6de8d9ad1e2702cff1725547892ec7a588e30d1b2bf5009209260b91cc`.
- Input manifest SHA-256: `64f1398ffcf15b16679bbc83678e918698677d715db0314cdbfaf012dd9e4009`.

Limitations: this is not general JavaScript lexical or dataflow resolution.
Other import/alias forms, templates/escapes, multi-part/dynamic concatenations,
variable argv, arbitrary shell commands and interpreter options remain outside
this matcher. Conservative exclusions can omit otherwise valid calls. Those
omissions are not benign verdicts or a claim of complete VSIX coverage.

## Nested callback diagnostic repair (2026-09-15)

Continuing VSIX source review found that Tidecrest registers a typing callback,
accumulates `args.text`, hex-encodes a slice, passes the hostname through a
case-changing helper, and calls `dns.resolve4`. Its call-symbol view includes
the resolver call; its flow graph does not. The callback body is deliberately
unsupported by the current flow builder, but the graph incorrectly omitted
the existing `anonymous-function` limitation when the callback was nested inside
the named `activate` function. The graph therefore failed to disclose its gap.

Filefacts' evaluator now records that limitation when it skips an anonymous
definition. Skipped nested named functions also report `nested-function` rather
than silently hiding an additional wrapper. No callback invocation, capture,
parameter binding, dataflow edge, security metric or new schema was invented.
The real specimen's graph values and function relationships are byte-for-byte
equivalent as JSON values; only the missing limitation is added. This is not
yet Tidecrest exfiltration detection, nor a claim that the complete proposed
DNS transport works. No specimen or DNS request was executed.

Tests cover JavaScript arrow/function callbacks, TypeScript arrows, Python
lambdas and Go function literals, plus a nested named wrapper and supported
direct named-function flow. All 1,377 active parser-library tests pass (four
ignored); clippy and diff checks pass. SOURCE_ANALYSIS.md records the boundary.
General propagation of flow limitations into ordinary cleave reports remains
separate; the current repair is observable through the flow API/CLI.

The existing frozen analyzer sources were rebuilt against an isolated parser
copy containing the fix. With unchanged frozen rules, the full five-root scan
preserves all 1,273 root reports, 3,881 retained records, 68,408 trait instances,
and every root risk and suspicious/hostile ID set. Both trait-delta files are
empty; sorted root indexes compare identically. All 1,289 input hashes and the
rule manifest remain unchanged. No artifact was modified or moved.

Final `make validate` with the rebuilt analyzer passes hostile 77/77, benign
134/134, does-nothing 176/176, drop-exec 43/43, impact-wipe 66/66, obfuscation
80/80, reverse-shell 25/25 and simple-stealer 65/65. Counts remain 195/622
hostile-labeled packages; 194 have 1–3 and one has five. The remaining 427 still
need review. No detection gain or verified-recall improvement is claimed.

Evidence: `/tmp/sc-vsix-dns.W71MNi`, including `flow.json` (before),
`flow-final.json`, `flow-delta.json`, `filefacts-tests-final.log`,
`filefacts-clippy.log`, `full.jsonl`, `index-before.sorted.json`,
`index-after.sorted.json`, both `traits-*.jsonl` deltas and `validate-final.log`.
New pinned analyzers are in `bin/`; their hashes are in `analyzers.sha256`.
Rules remain `/tmp/sc-vsix-final-rules.FVxzy5`. Stderr contains only the debug
build performance warning. Scan SHA-256:
`ae252815b65da7cbdbcca17b72bde58a65d928b16147c747de93de42653104fb`.

The other inspected VSIX entrypoints include response-to-VM evaluation,
download/chmod/spawn, terminal PowerShell injection, debug-configuration writes
and a legacy terminal-setting rewrite. Those source observations are not
completed package verdicts. In particular, response execution must not be
inferred from downloading alone, and writing a setting does not establish that
the declared VS Code versions honor it. These reviews remain open.

## Compound-assignment provenance repair (2026-09-15)

Continued Tidecrest review exposed a separate, reproducible flow bug: compound
assignment could fail to update a local binding or discard its previous origin.
Filefacts now retains the old value and RHS as contributing operands for the
tested JavaScript, TypeScript, Python, Go, Rust and C forms. Ordinary assignments
still replace the binding. RHS evaluation occurs once, after reading the old
binding. Unsupported member/indexed compound mutation is explicitly diagnosed;
this is not object-mutation, operator-overloading or callback modeling.

This repairs existing language semantics rather than adding a security fact or
rule feature. Tests cover accumulation, overwrite, unrelated sink, opaque call,
RHS reassignment and unsupported target cases. All 1,378 active parser-library
tests pass (four ignored), as does clippy. A six-language, five-case cleave
integration matrix confirms that ordinary YAML call-argument provenance queries
receive the corrected relationships. Cache salt v19 invalidates old verdicts.

The pinned analyzers, rebuilt against an isolated parser copy, were compared
with the previous pass using unchanged frozen rules. All 1,273 root reports,
3,881 retained records, 68,408 trait instances and root risk/high-ID sets are
preserved. Both trait-delta files are empty. The 1,289-file inventory matches
before and after the scan; the frozen rule manifest also verifies unchanged.
No specimen was modified, moved or executed. The only scan warning concerns
debug-build performance.

Counts remain 195/622 hostile-labeled packages: 194 have 1–3 hostile traits,
one has five, and 427 still need review. This bug fix does not establish a
corpus detection gain. Tidecrest's callback-flow gap and typed-text-to-DNS
relationship remain unresolved; no broad co-occurrence rule was substituted.

Evidence: `/tmp/sc-type-dns-rule.SEmAtS`, including `filefacts-tests.log`,
`filefacts-clippy.log`, `cleave-integration.log`, `full.jsonl`,
`index-after.sorted.json`, both `traits-*.jsonl` deltas, input manifests and
`rules-verify.log`. Pinned analyzer hashes are in `analyzers.sha256`; parser
source hash is in `parser.sha256`. Rules remain
`/tmp/sc-vsix-final-rules.FVxzy5`. Scan SHA-256:
`0b798c4c3923e3bc74674ff7ffba5cd4247dbe0b2645f591e90bad7296238a07`.
Final `make validate` passes hostile 77/77, benign 134/134, does-nothing 176/176,
drop-exec 43/43, impact-wipe 66/66, obfuscation 80/80, reverse-shell 25/25 and
simple-stealer 65/65; see `validate-final.log`. Parser/source-copy comparisons,
analyzer/parser hash rechecks and owning-repository diff checks also pass.

## Concealed VS Code terminal submission (2026-09-15)

Onyxfieldcore's six-member VSIX declares `onStartupFinished` activation and
`./out/extension.js` as its entrypoint. The entrypoint creates a shell-backed
terminal, submits a hidden PowerShell download/evaluation command with `true`
as the execution flag, then hides the same terminal. The file-existence gate
and endpoint identity are not detection signals.

This is a concealed remote-evaluation **attempt**, not verified payload
execution. VS Code documents that `sendText` writes to the terminal's input and
adds a newline when the execution flag is true (also its default), while `hide`
only hides the panel. See the [Terminal API](https://code.visualstudio.com/api/references/vscode-api#Terminal).
The specimen's unquoted pipe can be interpreted by the parent shell, rather
than becoming part of the child PowerShell command. The resulting pipeline,
command availability and response conversion depend on that shell; the sample
does not establish successful script execution. This inference follows
[PowerShell parsing](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_parsing?view=powershell-7.4)
and the [PowerShell executable argument contract](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_powershell_exe?view=powershell-5.1).
No command, terminal or specimen was executed, and the fixture was not repaired.

The new AST matcher requires adjacent statements with the same const receiver,
a normal terminal constructor, a recognized hidden PowerShell download/evaluate
command submitted with execution enabled, and a subsequent `hide()` on that
receiver. Comments may separate the statements. Direct literals and two literals
split before the URL are supported, along with ordinary terminal naming forms
and the default execution flag. Explicit display-only `false`, extra arguments,
custom ptys, unknown shell configurations, changed receivers, intervening calls,
local/logged commands and tested lexical shadow forms are excluded.

No engine feature or security-specific fact was needed. Const namespace binding
and submission syntax live in `micro-behaviors/process/create/shell/terminal`;
their hostile combination is
`objectives/command-and-control/dropper/execution/terminal::vscode-hidden-terminal-remote-eval`.
The initial shell-bridge placement crossed the 75-trait directory limit. A
duplicate audit found that the existing creation/name-based dispatch regexes
and raw `require('vscode')` observation do not establish this binding and
receiver/argument relationship. The new rules therefore use the more precise
terminal directory; no existing trait was relocated or demoted to hide a match.

All 48 static probes pass, including gate/hostname independence, renamed
receivers, direct/concatenated strings, flag variants, omitted execution flags,
comments, shadowing and disconnected controls. Eight durable benign controls
are registered in `expectations.toml`, alongside the actual VSIX. Final focused
controls have no suspicious/hostile findings. Precision is 6.6, independently of
those controls; this score does not establish a general false-positive rate.

Limits remain explicit: this is not general alias/monkeypatch resolution,
JavaScript constant folding, quoted/escaped-command parsing or arbitrary terminal
configuration analysis. Tidecrest and Cobaltkit's callback relationships remain
open. Their additional neutral namespace-binding observations are not restored
hostile detection or proof that those packages are benign.

The final five-root comparison retains 1,273 root reports and 3,881 records.
Exactly 26 trait instances are added: the const binding on eleven VSIX sources
and their package roll-ups, plus Onyxfieldcore's submission observation and
hostile objective at both levels. No trait instance is removed; the total is
68,434. Onyxfieldcore is the only root with a changed suspicious/hostile ID set
and now has exactly one hostile trait. Counts are 196/622 hostile-labeled,
195 with 1–3, one with five, and 426 still requiring review. These are label
counts, not verified recall for the whole corpus.

All eight `make validate` suites pass: hostile 78/78, benign 142/142,
does-nothing 176/176, drop-exec 43/43, impact-wipe 66/66, obfuscation 80/80,
reverse-shell 25/25 and simple-stealer 65/65. The eight focused benign controls
score 4–6, with no high findings. Input hashes match before/after for all 1,289
files. Frozen rules differ from the previous pass only by the two new YAML
files; final source-copy comparisons and analyzer/rule hash checks pass.

Evidence is in `/tmp/sc-vsix-terminal.M8XhsF`: `full-final.jsonl`,
`final-index.json`, `high-delta.json`, both `traits-*.jsonl` deltas,
`probe-final-v2.log`, `controls-final-v2.jsonl`, `rule-test-final-v2.log`,
`validate-v2.log`, input manifests and `rules-verify-final.log`. Final rules are
`/tmp/sc-vsix-terminal-final-rules.RA4G6h`. The pinned analyzers remain
`/tmp/sc-type-dns-rule.SEmAtS/bin/` (no engine changes in this pass).
Scan SHA-256: `529d581780c2d1f3318645d116a636be7d6559b761e8c455507b8705c910d7d2`.
Rule manifest SHA-256: `213bd7748def0f054beca2856311274716481ca4270f4d5fa8094ce67239b812`.
Input manifest SHA-256: `64f1398ffcf15b16679bbc83678e918698677d715db0314cdbfaf012dd9e4009`.
Stderr contains only the debug-build performance warning.

## Archive-wide environment exfiltration false positives (2026-09-15)

The existing Cobaltcraft package reads selected environment values and local
developer credential files, serializes them, and writes the body to an HTTPS
request. Its random gate was neither activated nor used as detection evidence.
Static inspection confirms the underlying hostile behavior; the five old
hostile findings did not represent five independently established behaviors.

Two archive-scoped rules combined an install-hook declaration, environment
filtering and HTTP POST observations across unrelated members. A new benign
control demonstrates the error: its postinstall script only prints a message,
its local diagnostic returns environment **names**, and an independent HTTP
function sends a fixed build-status document. No file transmits secrets. Before
the change the archive scored 247 with two hostile exfiltration findings, while
all its individual members had no suspicious or hostile findings.

Removed the two unsupported pooling rules:

- `objectives/supply-chain/credential-theft/package::npm-install-hook-credential-env-exfil`
- `objectives/supply-chain/recon-exfil/npm-install-targeting::npm-postinstall-env-secret-exfil`

Also removed
`objectives/supply-chain/credential-theft/package::npm-install-hook-environment-credential-exfil`.
That wrapper added a hook declaration to the existing file-level finding, but
neither proved the hook invokes the detected file nor added a distinct behavior.
Canonical file-level detections and package lifecycle observations remain.
No filename/hostname allowlist, random-gate condition, severity demotion or
engine feature was introduced. The unchanged control now scores 14 with no
suspicious or hostile findings; Cobaltcraft scores 173 with two hostile findings.

The control additionally exposed a misplaced neutral trait:
`node-https-post-exfil` matched HTTPS/POST source text but lived under credential
theft and inherited credential-theft ATT&CK/MBC tags. Its matcher, confidence and
criticality are preserved as
`micro-behaviors/communications/http/request/verb::https-post-option-source`;
all three consumers now reference it there. Its description says what it
observes, and the unrelated theft tags are gone. This is a taxonomy correction,
not a claim that the legacy text matcher establishes call ownership or body flow.

Cached calls expose imports, scalar arguments, request creation and `req.end`;
the inspected values projection does not expose the request object's method
field. A structured replacement for the legacy source pattern requires separate
equivalence/precision tests, especially for callback bodies. The remaining
file-level co-occurrence composites also need broader broken-link testing;
retaining their correct findings on this reviewed specimen is not proof of
general source-to-sink precision.

Durable controls: `testdata/benign/npm-install-env-unrelated.tgz`, its readable
source directory, the Cobaltcraft expectation, and
`scripts/test-npm-env-consolidation.sh`. The script enforces no high findings in
any benign member, retention of the neutral HTTP observation, absence of all
three removed wrappers, and 2–3 hostile findings with both canonical source
categories on the real package. It scans bytes only. The test README is not in
the archive, so explanatory prose does not influence its verdict.

Evidence directory: `/tmp/sc-env-consolidation.gd8K4R`. The frozen rule snapshot
is `rules-after/`, derived from the previous verified snapshot with only this
pass's rule edits; unrelated current-worktree changes are excluded. The initial
wrapper-only five-root comparison preserved all 1,273 roots, all 3,881 retained
records, and hostile-label coverage (196/622), changing only Cobaltcraft's high
ID set. Besides its three removed wrappers, two low-tier `json-stringify-call`
instances stopped being retained; the more specific notable
`json-stringify-identifier` observation remains. No source capability definition
was removed.

The final frozen comparison (`full-final.jsonl`, `complete-index.json`,
`high-final-delta.json`) confirms the same root/member counts and high-ID delta.
There are 68,429 trait instances: 82 old HTTP-source IDs are replaced by the
82 correctly placed neutral IDs, three hostile wrappers disappear, and two
low-tier serialization instances disappear as described above. Normalizing
only the relocated ID makes the final trait set byte-identical to the
wrapper-only comparison. All 196 hostile-labeled current-corpus packages now
have 1–3 hostile traits; 426 still need review. No verified recall increase is
claimed, and no other package loses a suspicious/hostile finding.

All 1,289 supply-chain input hashes match before/after. The analyzer hashes
still match the previously pinned compound-assignment builds. The final frozen
snapshot differs in exactly five rule files (three HTTP-observation relocation
files and the two wrapper files). Changed source files match their frozen copies.

| Final artifact | SHA-256 |
| --- | --- |
| `full-final.jsonl` | `ba084773c74d748d3b117142eac7d1722444bb915542a357dc421b52ef9eccb3` |
| `rules-final.sha256` | `36932f2cfd291234ecc5516b1a1500c1458aca2101afb81b0331e54e500a295e` |
| `inventory-final.sha256` | `64f1398ffcf15b16679bbc83678e918698677d715db0314cdbfaf012dd9e4009` |

The static semantic regression passes (`regression-complete.log`,
`controls-complete.jsonl`). The post-migration `make validate` run passes all
eight suites: hostile 79/79, benign 143/143, does-nothing 176/176, drop-exec
43/43, impact-wipe 66/66, obfuscation 80/80, reverse-shell 25/25 and
simple-stealer 65/65 (`validate-complete.log`). No specimen was installed,
imported, activated or executed, and no network endpoint was contacted.

## macOS installer script review and receipt visibility (2026-09-15)

The next x-triage-bad pass inspects the named scripts in all ten current macOS
packages, without running an installer or any script. This is a script-level
review, not a completed disposition of every member in all ten packages.

| Package stem | Observed script behavior | Remaining distinction |
| --- | --- | --- |
| Tidecrestforge | Writes a RunAtLoad launch-agent plist containing a shell download/evaluate pipeline, then loads its path | Need the written configuration-to-loaded-service relationship, not loose launchctl/curl co-occurrence |
| Pumicestack | Appends a function definition to `.zshrc`; that function contains curl piped to a shell | Defining the function is not automatically invoking it at shell startup |
| Clovermarksync | Downloads a hidden `.pkg`, then passes that pathname to `installer -pkg` | Same-path relationship and legitimate updater controls are still required |
| Larkspursync uninstall | Writes, chmods and backgrounds a periodic HTTP client whose response is discarded | The shown helper does not evaluate the response; do not label it remote command execution |
| Junipeerkit | Writes an `/etc/profile.d` file containing an HTTP request with discarded response | No script in the inspected installer body sources that file; no response execution is shown |
| Indigocore | Calls `pkgutil --forget` with its own package identifier | Real receipt manipulation, not enough by itself for a hostile verdict |
| Onyxfieldmesh | Downloads a `.dylib`, chmods it and clears extended attributes | No load of that library is shown; the existing portable-dylib hostile composite still needs precision review |
| Larkspursync docwipe | Recursively deletes Documents/Desktop/Pictures | Existing harmful-deletion finding remains |
| Fennellite | Pipes a retrieved Safe Storage secret into an HTTP request body | Existing credential-upload finding remains |
| Riftwoodkit | Pipes filtered environment output into an HTTP request body | Existing environment-upload finding remains |

Indigocore's `PackageInfo` and payload metadata use the same package identifier
as the receipt argument. Its listed payload consists of application directories,
an `Info.plist`-named JSON metadata file and AppleDouble metadata, not an app
executable. These observations do not justify inventing a theft, execution or
persistence verdict. The [pkgutil manual](https://keith.github.io/xcode-man-pages/pkgutil.1.html)
states that forgetting a receipt leaves installed files alone and warns against
using it inside installer scripts to compensate for package-design problems.
The same contract appears in the local `/usr/share/man/man1/pkgutil.1`.
No package was moved based on a missing hostile label.

The existing `macos-pkg-forget-receipts` trait used a baseline text substring.
The current cached facts already contain a `pkgutil` call with a `--forget`
identifier argument, so no engine change or live AST query is necessary.
The trait now uses a same-call symbol/argument predicate, supports the standard
absolute executable path and ordinary whitespace/line-continuation variations,
and is notable: a receipt operation is useful standalone information rather
than universal baseline behavior. Its description reports an invocation, not
successful deletion, a resolved receipt target or malicious intent.

Six static benign controls exercise direct/absolute/multiline invocations,
quoted documentation/heredoc examples, an unrelated option in another command,
and a similarly named executable. The three invocations retain the notable
finding; the other three do not. All six have no suspicious or hostile findings.
The rule deliberately does not yet cover quoted/dynamic option words or command
wrappers such as sudo; those are coverage limits, not evidence of benignity.
The durable semantic test is `scripts/test-pkgutil-receipts.sh`, with six
additional `make validate` expectations.

The frozen five-root comparison retains all 1,273 root reports. Root risk/high
ID sets are identical, and coverage remains 196/622 hostile-labeled (all 196
with 1–3). Exactly four notable receipt instances appear on Indigocore's script
and its archive ancestors. Seven low-tier metadata instances cease to be
retained by compact-report selection once the notable behavior is available;
they are all on that same package. No capability definition or parser fact was
deleted. Compact retention changes from 3,881 to 3,882 records: three script-chain
records replace two low-tier payload-container records. There are 68,426 trait
instances. No suspicious or hostile finding is added or removed.

Evidence: `/tmp/sc-macpkg-review.cIjB3s`, with `full-final.jsonl`,
`final-index.json`, `root-delta.json` (empty), `traits-added.jsonl`,
`traits-removed.jsonl`, `rule-test.log` and `regression.log`. The frozen
`rules-after/` differs from the preceding snapshot only in the existing macOS
package-manager YAML. All 1,289 supply-chain input hashes remain unchanged.
The same pinned analyzers are reused. No gate, actor hostname or package name
was made a detection condition, and no specimen was installed or executed.

| Final artifact | SHA-256 |
| --- | --- |
| `full-final.jsonl` | `c9a6da02c5d9eadefc71a4451407a4c095018e4147a029eab8f327507763fdde` |
| `rules-final.sha256` | `0073b516470b0e826d0289e3e2df63ae6d82c6235667c6c9ab3395a58236f5a0` |
| `inventory-final.sha256` | `64f1398ffcf15b16679bbc83678e918698677d715db0314cdbfaf012dd9e4009` |

All eight `make validate` suites pass (`validate.log`): hostile 79/79,
benign 149/149, does-nothing 176/176, drop-exec 43/43, impact-wipe 66/66,
obfuscation 80/80, reverse-shell 25/25 and simple-stealer 65/65. The static
receipt regression also passes; this is a neutral visibility improvement and
does not increase verified hostile coverage.

## Misplaced canaries

The v1 README describes canary-only sinks, and the reviewed packages confirm
this: the named action is data written to a temporary file, not performed.
Three non-hostile archives were moved unchanged, per `x-triage-bad`, under
`/tmp/triage/misplaced-good/supply-chain-benchmark-v1/`:

| Relative destination | SHA-256 |
| --- | --- |
| `python/pypi-pathweaver-python-install-env-report-linux.tar.gz` | `0899739673c9d3899f4ecca61b266fc52291f0e230342b7c21e032250d82fa61` |
| `javascript/npm-resourcecove-javascript-rundll-resource-stage-windows.tgz` | `1aea02bfb5fe7a3dd3fce21c27e67b9894bd056b791025e5a8ef8518922e7872` |
| `elixir/hex-fontstream-elixir-png-resource-loader-linux.tar` | `4c93c7fff8f6f086237bd62f2dc7171edaee810fd08b37e4563af00bad5ee59b` |

All three destination hashes were verified. Python retains one suspicious
module-scope `exec` observation; JavaScript and Elixir have no high findings.
The Elixir PNG's appended encoded marker remains a parser fact, but no package
code reads or executes that resource. No random gate exclusion was introduced.

Post-triage inventory: 1,291 files. The only changes are these three moves and
the v1 README's disposition note. **All 622 current corpus files are unchanged.**
The original v1 manifest/checksum list is retained as historical provenance.

The follow-up moved two more fully reviewed non-hostile archives unchanged
under the same recoverable destination:

| Relative destination | SHA-256 |
| --- | --- |
| `ruby/rubygems-profileloom-ruby-runkey-telemetry-windows.gem` | `0c48a1fab1b9ed53a346ab6c3481493ed668484e9ff14d7539736652225cc57e` |
| `powershell/psgallery-profileloom-powershell-runkey-telemetry-windows.nupkg` | `67ded2142fc194646ba51b34265f14e8f242812466747a85a9bf1f34a87c6190` |

Both destination hashes were verified. They write specification text to a
temporary index, invoke only harmless output, and connect only to loopback.
Final inventory after five total moves: 1,289 files, with 310 v1 packages
remaining. The two follow-up moves and README note are the only input changes
since the follow-up baseline. All 622 current-corpus files remain unchanged.

## Dylib verdict precision and compiled-string consistency (2026-09-15)

Removed `portable-dylib-dropper` and its two misleading source atoms. Their
matchers required only `.dylib` and one of `xattr`, `dlopen`, an injection
variable or an audio-plugin path; they did not establish the described remote
staging/loading relationship. Four harmless controls (attribute inspection,
local plugin loading, plugin configuration and command examples) reproduced
both the hostile and suspicious false positives.

Static review of Marrowlite (Python), Pumiceforge (Go source), Cobaltstack (PHP),
Cobaltkit (Rust), Sablewoodforge (JavaScript) and Onyxfieldmesh (macOS installer)
found download, permission setting and extended-attribute clearing, but no
library load. Removing the unsupported verdict is not a declaration that these
packages or their unknown remote payloads are safe. All specimens remain
unchanged and in scope; no gate or endpoint contributed to the replacement.

Neutral observations now live under `micro-behaviors/fs/path/library` and
`micro-behaviors/fs/attributes/xattr`. Source constants use cached literal
matching. JVM classes use the existing `class.strings` value array: the initial
source-only replacement missed Indigoprime's class reference, while this cached
array also exposes an `xattr` entry the former text matcher missed. That array
contains all UTF-8 constant-pool strings, including names and descriptors, so
the class rules describe references, not runtime literals or executed commands.
Per the user's compiled-Go consistency decision, no Java-only expansion of the
literal interface, bytecode analysis, new metric or live AST query was added.

The final frozen five-root comparison retains all 1,273 root reports and 3,882
member/root records. There are 68,410 trait instances: 28 new neutral instances
replace 44 instances of the three removed IDs. Exactly six root high-ID sets
change, losing only the unsupported hostile/suspicious pair; no other high-ID
set changes. Current-corpus hostile labels decrease from 196 to 190, all with
1–3 findings. This is a precision correction, not a recall improvement.

The static regression `scripts/test-dylib-source-precision.sh` passes for seven
packages and six harmless controls (including Java source and compiled class).
It requires retained neutral observations, forbids the removed IDs and forbids
high findings on the controls; it does not forbid future justified hostile
findings on actual packages. All eight validation suites pass: hostile 79/79,
benign 155/155, does-nothing 176/176, drop-exec 43/43, impact-wipe 66/66,
obfuscation 80/80, reverse-shell 25/25 and simple-stealer 65/65.

Evidence: `/tmp/sc-dylib-precision.7mqTJB`, using the previously pinned analyzers
in `/tmp/sc-type-dns-rule.SEmAtS/bin`. The frozen rules differ from the receipt
pass in exactly three files; unrelated worktree changes are excluded. All
1,289 inventory paths and hashes still match the baseline after scanning.

| Final artifact | SHA-256 |
| --- | --- |
| `full-complete.jsonl` | `a5c0539ae017f9bf0b5136fbc1bc2379950921d2869c76c9f727df114b4167ce` |
| `rules-complete.sha256` | `b98d4041930b0e7b0678e378b4f673edcb5bc1b2191e23288c76c87ad2b3cdd8` |
| `inventory-complete.sha256` | `64f1398ffcf15b16679bbc83678e918698677d715db0314cdbfaf012dd9e4009` |

Comparison details are in `traits-complete-added.jsonl`,
`traits-complete-removed.jsonl` and `high-complete-delta.json`; verification logs
are `regression-final.log`, `validate-complete.log` and `inventory-verified.log`.

## Disconnected environment diagnostic / status upload (2026-09-15)

A new harmless control lists credential-named environment keys for local use
and separately sends the fixed JSON body `{"status":"ready"}`. It never reads
or transmits the variables' values. The prior `javascript-environ-json-http-exfil`
rule nevertheless labels it hostile: its three legs and 2,048-byte proximity
window do not establish the complete data path claimed by its comment. Cached
calls and the source flow graph expose the fixed status-body construction.
This is a rule-design bug, not evidence that the engine needs a new feature.

Removed that composite without deleting its component observations or adding
an exception. The durable control is `testdata/benign/env-http-controls/names-only.js`.
The existing npm regression now checks both separate-file and same-file
disconnected code, preserving neutral enumeration and HTTP observations and
requiring no high findings on the controls. The Cobaltcraft expectation no
longer requires the unsupported ID; its developer-credential-file finding
remains. The static regression passes and the control scores 6 without high
findings. All eight validation suites pass, including hostile 79/79 and benign
156/156; the other six suite counts are unchanged from the dylib pass.

Final evidence: `/tmp/sc-env-disconnected.o8qs70`. The frozen snapshot differs
from the completed dylib pass in exactly one rule file. Its full comparison
retains all 1,273 root reports and 3,882 records, with 68,400 trait instances.
There are no added instances. Five instances of the removed hostile ID and
five instances of its generic HTTP-body umbrella disappear from compact output;
the more specific `node-http-request-end-body` and request-end call observations
remain on every affected source/root. No parser fact or HTTP rule was removed.
Only Cobaltcraft and Clovermarkkit change high-ID sets, each retaining one
hostile finding. Corpus labels remain 190/622 (all 190 with 1–3), with 432
requiring further disposition. This preserves labels, not verified recall or
proof that every retained composite has sound data-flow semantics.

The first full report, `full-final.jsonl`, is invalid and excluded: the scanner
started before copying the rule snapshot finished, and logged invalid trait
references. After confirming the copy was complete and differed in only the
intended file, a new scan produced `full-complete.jsonl` with no such errors.
All 1,289 input paths and hashes match the previous baseline after that scan.

| Final artifact | SHA-256 |
| --- | --- |
| `full-complete.jsonl` | `fac572a4143703e6cd54da227110ead31686a66428c5689ce195af6e28308eb2` |
| `rules-final.sha256` | `83d28c685f15b29923e96ffd6147bb058ddd669cf3949c77d63df994978fd844` |
| `inventory-final.sha256` | `64f1398ffcf15b16679bbc83678e918698677d715db0314cdbfaf012dd9e4009` |

A second control (`local-diagnostic.js` in the evidence directory) additionally
checks whether NPM_TOKEN is configured, without sending its value. Before the
repair it gets five hostile labels: the removed rule plus `env-token-stealer`,
`npm-token-stealer-comp`, `npm-runner-recon-http` and `npm-supply-chain-attack`.
Those four rule-design false positives are addressed in the next section; none
occurs in the completed five-root baseline. Repair them with independent
positive controls and actual relationships, not status-host or fixture-name
allowlists. Do not infer a need for generic callback/mutable-object analysis
from this example. No specimen or control was executed or installed.

## Npm/CI token co-occurrence precision (2026-09-15)

Removed four hostile composites that inferred token theft from a nearby token
read and HTTP operation: `env-token-stealer`, `npm-token-stealer-comp`,
`npm-runner-recon-http` and `npm-supply-chain-attack`. The local diagnostic
control only returns token presence/names and sends a fixed status body, so
proximity does not support their verdicts. No new source/sink model, engine
fact, live AST query, hostname exclusion or fixture-specific exception was
added. The one hook composite consuming a removed rule now references the
existing `credential-http-upload` finding. Validation identified the unused
`npm-token-env-access` helper left behind; that helper was removed as well.

All 65 independently maintained simple-stealer samples retain hostile findings
in the final focused scan. Only `39-npm-token-telegram.js` changes its high-ID
set: the four removed rules disappear (one had already been downgraded to
suspicious), leaving two hostile findings instead of five. The other 64 high-ID
sets are unchanged. This checks retained coverage outside the generated
supply-chain corpus, not the universal accuracy of every remaining detector.

The durable local diagnostic lives at
`testdata/benign/env-http-controls/local-diagnostic.js`; it retains neutral
token-read and HTTP observations and no hostile verdicts. Two suspicious
token-read aliases still surface (risk 45), so it is not yet a completely clean
benign regression. Three overlapping definitions (`env-npm-token`, `npm-token`,
`node-npm-token`) require neutral-placement/consolidation review. The new
`scripts/test-npm-token-precision.sh` deliberately asserts absence of hostile
verdicts only, and requires all 65 simple-stealer samples to retain at least
one hostile finding. Its 66-root final run passes (`regression-final.log`).

Evidence: `/tmp/sc-npm-token-precision.fWfZqk`. The final frozen snapshot differs
from the previous completed pass in three rule files. The final five-directory
scan retains all 1,273 roots and 3,882 records; the sorted set of all 68,400
trait instances is byte-identical to the previous pass. Root risk/high-ID maps
are semantically identical (JSON key/report ordering is not significant).
All 1,289 input paths/hashes remain unchanged. Corpus labels stay 190/622, all
with 1–3; 432 require further disposition. No package or control was executed,
installed or modified to make its behavior more detectable.

Workspace `make validate` was rerun after removing the orphan and still fails
on two unrelated PHP/media duplicate-matcher issues
(`validate-worktree-final.log`). These concern the overlapping image/media
PHP-open-tag atoms, not the supply-chain repair. The concurrent work is left
untouched. Isolated snapshot validation passes all eight suites: hostile 79/79,
benign 156/156, does-nothing 176/176, drop-exec 43/43, impact-wipe 66/66,
obfuscation 80/80, reverse-shell 25/25 and simple-stealer 65/65
(`validate-frozen.log`). Do not equate that result with workspace validation.

| Final artifact | SHA-256 |
| --- | --- |
| `full-final.jsonl` | `eb6cf7d2b8b83f26996dc843553b38c27c6434930644ea0d5e43df8e3fd163a5` |
| `rules-complete.sha256` | `68f27791cb5f5d8f20810965eb5707961876f1421e06163aa169586ca7fc1c10` |
| `inventory-complete.sha256` | `64f1398ffcf15b16679bbc83678e918698677d715db0314cdbfaf012dd9e4009` |

## Neutral registry-token reads (2026-09-15)

Consolidated five suspicious wrappers around ordinary registry-token access:
`env-npm-token`, `npm-token`, `node-npm-token`, `env-npm-auth-token` and
`node-auth-token`. The underlying NPM_TOKEN, NODE_AUTH_TOKEN and NPM_AUTH_TOKEN
member matchers already exist under `micro-behaviors/os/env/package-manager`.
Consumers now reference those cached facts, with one neutral
`node-registry-token-env-read` grouping for credential-category counts. Three
spellings of the same registry credential must not satisfy three independent
credential-source categories. No engine code, live query or new atomic matcher
was added.

The CI-token detector retains its registry-token exclusion using the neutral
group. The ordinary-publishing exception now lives on the consuming
`npm-token-npmrc-publish-worm` composite, whose NPM-token leg was mandatory,
instead of hiding neutral reads everywhere. The exception is not applied to
the other worm composites whose registry-token leg is only one alternative;
doing that could suppress independent evidence. Removed two now-unused
exception composites; their underlying configuration observations remain.

Seven durable benign controls now cover the disconnected local diagnostic,
name-only enumeration, bracket access, the three registry-token spellings,
their combined fallback and ordinary registry publishing. All seven have no
suspicious or hostile findings (risk 3–13), while the expected neutral facts
remain. The three-spelling control explicitly retains all three atomic reads
without firing credential-breadth objectives. Six new benign expectations and
the strengthened 72-root `scripts/test-npm-token-precision.sh` guard these
properties; its final static run passes (`regression-complete.log`).

All 65 simple-stealer samples retain hostile detection. Their hostile-ID sets
are unchanged. Only the npm-token-to-Telegram sample changes risk/high findings:
two suspicious read aliases disappear, while its two hostile findings remain
(risk 314 → 277). This is removal of duplicated neutral evidence from a
suspicious tier, not loss of the underlying token access.

Evidence: `/tmp/sc-npm-read-facts.noqUva`. The final frozen snapshot differs
from the previous pass in twelve rule files. The five-directory scan retains
1,273 roots and 3,882 records. All 68,400 sorted trait instances and every root
risk/high-ID set are unchanged; all 1,289 input paths/hashes also match. Corpus
labels remain 190/622, all with 1–3; 432 still require further disposition.
The control/positive scans do not establish universal soundness of all
consuming composites or eliminate the remaining source/sink review work.

Initial isolated validation found the obsolete local-release exception, which
was removed. A second run found an overly broad publishing expectation: it
forbade the entire registry hierarchy, including the expected publishing
exception. The corrected expectation keeps the worm-hierarchy exclusion;
the static regression separately forbids all suspicious/hostile findings.
Final isolated validation passes all eight suites: hostile 79/79, benign
162/162, does-nothing 176/176, drop-exec 43/43, impact-wipe 66/66, obfuscation
80/80, reverse-shell 25/25 and simple-stealer 65/65
(`validate-frozen-complete.log`).
Workspace validation (`validate-worktree-final.log`) separately reports
unrelated concurrent authoring issues, including file-type and binary identity
constraints; those changes were left untouched.

| Final artifact | SHA-256 |
| --- | --- |
| `full-complete.jsonl` | `0fddecc9a9b68ceb630d2e9a62bc617d61c9967a849b16ccd72077e76e017326` |
| `rules-complete.sha256` | `5341ebf87d5adceff2a4aea565c98133b72d04cf4a410042f5a761b90e31247e` |
| `inventory-final.sha256` | `64f1398ffcf15b16679bbc83678e918698677d715db0314cdbfaf012dd9e4009` |

No package or control was installed, imported, built, activated or executed.

## Remaining Homebrew disposition and download precision (2026-09-15)

Evidence: `/tmp/sc-brew-disposition.nK1BD9`; frozen rules: `rules-after` in
that directory, layered on `/tmp/sc-npm-read-facts.noqUva/rules-after`.
The pinned analyzers remain those in `/tmp/sc-type-dns-rule.SEmAtS/bin/`;
their hashes match the preceding pass. RULES.md and TAXONOMY.md hashes also
match the previously read versions. The remaining five formulas were read
statically; all ten formulas' cached call facts are saved as `*.calls.json`.
No package code was run,
installed, imported or fetched, and no gate or endpoint was used as a signature.

The five remaining formulas do not establish five additional hostile attacks:

| Formula | Observable behavior | Evidence limit / disposition |
| --- | --- | --- |
| Gableguard | Declares a resource and invokes `sh installer.sh` in its stage block. | Resource contents are absent. The supplied URL alone establishes neither typosquatting nor a malicious installer; payload-dependent, unresolved. |
| Foxtailstack | A method named `pour_bottle?` issues a conditional curl request and discards both output streams. | No downloaded-code execution, sensitive request body or tasking is present. Network contact is visible, hostile intent not established. |
| Brackenstack | A livecheck URL is declared; a separate install method issues curl and discards its response. | The request is in `install`, not the livecheck block. No secret transfer or response execution is present; an enrollment/beacon label alone cannot establish hostility. |
| Vermilionguard | A method named `audit` posts `Socket.gethostname` through Net::HTTP. | Hostname telemetry is present, but no credential theft or other malicious purpose is established. Invocation by a particular Homebrew lifecycle is not proven by the method name. |
| Riftwoodguard | `caveats` returns text containing a curl-to-shell installation instruction. | Call facts contain no process launch. Human-followed installation advice is not automatic execution; unknown remote content prevents a safety claim. |

These remain in place, not reclassified as proven benign and not counted as
verified hostile misses. The zero-valued digests and conditional file checks
were not used to dismiss behavior. No engine feature or live tree query was
needed for this review.

The review exposed a real rule defect: `formula-system-exec` matched a textual
`def install` followed by a curl/wget/shell prefix, including quoted examples,
and filed that neutral observation as suspicious registry credential theft.
Its consumer `homebrew-formula-attack` combined this with a URL containing
`raw.`, `github.io` or `pastebin`, incorrectly making an ordinary public-data
download hostile. Two new static controls reproduced one hostile and two
suspicious findings each (risk 111 and 110), including a documentation-only
heredoc with no system call.

Removed the unsupported composite, the two textual atoms and the now-unused
`formula-env-access` wrapper; removed the consumer reference from
`ruby-supply-chain-attack`. Existing canonical Formula identity, URL, process,
environment and postflight observations remain. There is no new replacement
matcher, AST query, exception or engine change. The controls now score 3 and 2
with no suspicious/hostile findings. The actual download retains the cached
system-call observation; the quoted example correctly lacks it.

`scripts/test-homebrew-download-precision.sh` passes over the two controls and
all ten unchanged formulas. It checks an exact twelve-file inventory, absence
of the removed IDs, retained neutral observations, and the five existing
hostile-labeled formulas with 1–3 findings. The five unresolved formulas are
not asserted to be benign by that regression. Added two benign expectations.

The full five-root comparison has 1,273 unique root reports, 3,882 retained
root/member records, and 68,397 trait instances over the same 1,289 input
files. Exactly three suspicious `formula-system-exec` instances disappear:
Brackenstack, Clovermarkstack and Onyxfieldlite. There are no added instances,
no other removals, and no hostile-ID changes anywhere in the comparison.
Current corpus remains **190/622** hostile-labeled, all 190 with 1–3 findings;
these labels are not verified recall. Scanner stderr contains only the debug
build warning. All 310 v1 packages still require individual review.

| Artifact | SHA-256 |
| --- | --- |
| `full-complete.jsonl` | `e8a53d469628376e794684b8731f5a75829ef347c97281cc4e0f1722436cd3cb` |
| `rules-complete.sha256` | `9aa713c0539872ddf066c3febe85cc496d9de3620eb8b24e74b1ed72d2f2c397` |
| `inventory-final.sha256` | `64f1398ffcf15b16679bbc83678e918698677d715db0314cdbfaf012dd9e4009` |

Full frozen-rule validation passes all eight suites: hostile 79/79, benign
164/164, does-nothing 176/176, drop-exec 43/43, impact-wipe 66/66,
obfuscation 80/80, reverse-shell 25/25 and simple-stealer 65/65.
Log: `validate-frozen.log`. Rule hashes were reverified against the frozen
snapshot; shell syntax and the scoped worktree diff check also pass.

Worktree `make validate` was run separately and fails on three unrelated
concurrent authoring errors: two unnecessary regex groups in DuckDB package
identification and a raw/text policy error in the PHP source-write rule.
Log: `validate-worktree.log`. Those changes were not edited or reverted in
this pass. The worktree is not being reported as fully validated.

## Shell heredoc-to-launchd loader relationship (2026-09-15)

Evidence: `/tmp/sc-launchagent-shell.2QawRH`; frozen rules: its `rules-after`,
layered on `/tmp/sc-brew-disposition.nK1BD9/rules-after`. Static extraction
of Tidecrestforge's `Scripts` member recovers the postinstall script. It writes
a quoted-heredoc plist with RunAtLoad and a shell-command curl-to-shell pipeline,
then immediately calls `launchctl load -w` with the same destination expression.
No installer, script, downloaded content or opt-in gate was executed.

The cached `facts.json` exposes cat and launchctl calls, arguments and path
literals, but no heredoc contents or content-to-write relationship. `flow.json`
likewise does not associate the plist body with a file write. That is a bounded
reason to use tree-sitter under RULES.md, not a reason to add an engine feature
or reinterpret arbitrary strings as executable code. The new neutral
`shell-load-written-autostart-fetch-pipe` rule connects the redirect destination,
literal heredoc configuration and immediately following load argument; the
objective `installer-launchagent-shell-loader` combines it with the independent
installer-hook filename observation. The new cached basename matcher recognizes
preinstall/postinstall/preflight/postflight shell files; it does not claim
execution solely from a filename. This follows the existing Formula-context
pattern for Ruby, without requiring specimen names, gates or operator hosts.
Outside those installer-hook filenames the loader relationship remains notable;
general non-installer loader verdicts are not claimed by this objective.

Coverage is deliberately structural: quoted heredocs, direct cat output
redirection, identical double-quoted pathname expressions, adjacent launchctl
load with optional `-w`, and a direct curl-to-shell command in ProgramArguments.
Absolute tool paths, ordinary supported curl flags, shell names and renamed
path bindings work. The matcher rejects another write or binding change between
creation and load, cat input operands, stderr-only redirection, append mode,
XML comments/declarations other than the XML header, nested dictionaries,
duplicate ProgramArguments, Program overrides and disabled RunAtLoad values.
It does not claim general shell flow, filesystem identity, custom command
implementations, arbitrary XML, curl option forms, bootstrap syntax, unquoted
heredocs, or dynamic path resolution. These omissions are coverage limits,
not assertions that unmatched programs are safe.

Twenty-three in-memory structural probes pass (`probes-final.log`), including
gate removal and hostname/path-binding renaming. The diagnostic only parses
sample bytes; it does not evaluate shell code. Four durable benign controls
cover a local service, a separately written guide, an overwritten configuration,
and a command present only in an XML comment. All score 4–7 with no suspicious
or hostile findings. `scripts/test-launchd-written-loader.sh` verifies the
exact five-root control/package inventory and requires the new finding both
on the actual postinstall member and on the package root. It passes. Four benign
expectations and one hostile package expectation were added.

The first draft used an invalid single-leg composite; a subsequent direct
objective matcher was also rejected. Inspection of `apply_trait_defaults`
and `docs/BARE_OR_COMPOSITE_VALIDATOR.md` corrected the initial diagnosis:
**the downgrade is the intentional ceiling for atomic rules, not precision
scoring or an outdated engine bug.** Current and pinned implementations agree.
The final composition adds actual installer context, not a redundant API leg.
No engine feature, severity-policy relaxation, or analyzer rebuild was needed.
The local Xcode selection began requiring license acceptance during diagnostic
compilation; using the existing CommandLineTools compiler built the read-only
parser probe without changing system settings or accepting any license.

The final full comparison (`full-context.jsonl`) has 1,273 unique root reports,
3,882 retained root/member records and 68,445 trait instances over 1,289
unchanged inputs. Tidecrestforge alone gains a hostile finding (risk 6 to 122).
There are 48 additions and no removals: 40 neutral installer-hook filename
observations across ten macOS package scripts and their containing archive
levels, plus the loader relationship and objective at four levels. The other
nine package risk changes reflect only the neutral filename observation; no
other high finding set changes. The current corpus is **191/622** hostile-labeled,
all 191 with 1–3 findings. This is not verified recall. Scanner stderr contains
only the debug-build warning.

| Final artifact | SHA-256 |
| --- | --- |
| `full-context.jsonl` | `fe7b0f5eadf9094ff252c78e11fb52367cdbc768c249ba694a8bbb3c3a116c2d` |
| `rules-context.sha256` | `a2356c4109ac20ad33aad19149cac93daa9e88644c66b2594ddc552158df2dac` |
| `inventory-final.sha256` | `64f1398ffcf15b16679bbc83678e918698677d715db0314cdbfaf012dd9e4009` |

Final frozen validation (`validate-context.log`) reports one failed check:
the concurrently added `stage2.sh` hostile expectation is not met by the
frozen rules. Static scans with the preceding and final snapshots produce
identical stage2 risk and `{id,crit,conf}` findings (`stage2-before.jsonl` and
`stage2-after.jsonl`), so this is not a regression from this change. It is
outside the five supply-chain roots and was left untouched. The newly added
package/control expectations produce no validation failures. The final
validation result is **not green**, and is not described as eight passing suites.

Worktree `make validate` (`validate-worktree-context.log`) separately fails an
unrelated oversized `micro-behaviors/os/registry/access` directory (76 traits).
The new rule files are byte-identical
to the frozen versions, the frozen rule manifest verifies, all five-root input
hashes still match, and the scoped diff/shell syntax checks pass.
The earlier `full-complete.jsonl` / `full-direct.jsonl` and corresponding
validation logs document rejected intermediate designs, not the final rule.
The initial expectation schema error (missing `min_suspicious`) was also
corrected. The final focused regression passes (`regression-context.log`).

## Nested package disposition and installer-call facts (2026-09-15)

Evidence: `/tmp/sc-pkg-installer-review.ueQofw`; frozen rules: `rules-after`,
layered on `/tmp/sc-launchagent-shell.2QawRH/rules-after`. The pinned analyzers
and the RULES.md/TAXONOMY.md versions are unchanged. Source, archive listings
and `PackageInfo` were inspected without activating an installer or gate.

Clovermarksync's registered postinstall script downloads a fixed remote `.pkg`
into a hidden temporary pathname, then invokes `/usr/sbin/installer -pkg` with
that same pathname under an executable-existence check. The body suppresses
installer output and ignores installer failure. Cached call arguments confirm
the two path spellings; this is static review of this script, not a new general
same-path flow detector. Its payload archive lists application directories,
metadata and an Info.plist, but no downloaded sub-package. The remote payload,
its signer and its behavior are unavailable in the supplied artifact.

That is an install attempt, not demonstrated successful malicious installation.
A hidden temporary name, ignored failure and a network-fetched package can
also occur in a legitimate updater. Do not restore the withdrawn loose hostile
rule or add a structural matcher merely to label unknown payloads. This sample
remains unresolved, not proven benign and not moved out of the corpus.

The review found a concrete observation bug: the existing
`micro-behaviors/os/package-manager/sideload::macos-installer-pkg` text matcher
missed the absolute tool path and line continuations. Cached call/argument
matching now recognizes bare `installer` or `/usr/sbin/installer` with a bare
`-pkg` argument in the same invocation. This is neutral, not proof of success,
payload origin or intent. Quoted/dynamic option words and wrappers are explicit
coverage limits; no parser extension or tree query was necessary.

Other-language and compiled command text retains a separate, accurately named
`macos-installer-pkg-command-reference` observation, including absolute paths
and quoted command strings. It does not masquerade as a shell call. A second
text rule, formerly `micro-behaviors/process/create/installer::macos-pkg-root-install`,
made shell heredoc documentation a suspicious package dropper (risk 40).
That reference now excludes shell files, is named `macos-pkg-root-command-reference`,
and its two consumers use the renamed observation. The retained non-shell
matcher is unchanged. The broader non-shell dropper composites still require
their own intent review; no claim of comprehensive precision was added here.

Eight durable controls cover bare/absolute/multiline invocations, quoted
documentation, a disconnected option, a similarly named tool, and C/Objective-C
command references. `scripts/test-installer-pkg-precision.sh` checks the exact
nine-root inventory including Clovermarksync, the invocation/reference
distinction, absence of high findings on controls, and the nested postinstall
member's invocation finding. It passes. The documentation now scores 2 without
high findings; Clovermarksync gains the neutral invocation (risk 5 to 6).
Eight benign expectations were added. No sample was built, run, installed,
imported, fetched or modified.

The final five-root comparison contains 1,273 unique root reports, 3,882
retained root/member records and 68,449 trait instances. All 1,289 input hashes
match the preceding inventory. Only four observations are added: Clovermarksync's
installer call at its script and three containing archive levels. Nothing is
removed, and no suspicious/hostile ID set changes. Clovermarksync's risk is
the only root risk change (5 to 6). The current corpus remains 191/622
hostile-labeled, all 191 with 1–3 findings; this is not verified recall.
Scanner stderr contains only the debug-build warning. Frozen rule hashes verify.

| Artifact | SHA-256 |
| --- | --- |
| `full-complete.jsonl` | `4a28d065cccb1eac818b0e8a2cc053adf021673f0f9a80fb2f343d99039ba1d3` |
| `rules-complete.sha256` | `3b4309dfe58b1ff3f81d14727a0b628c43498f548549280203b8964eae1b01a8` |
| `inventory-final.sha256` | `64f1398ffcf15b16679bbc83678e918698677d715db0314cdbfaf012dd9e4009` |

Worktree `make validate` fails two unrelated overlong descriptions in local
Python control-port rules (`validate-worktree.log`). These concurrent changes
were not edited. Initial frozen validation also caught an overbroad new test
assertion: documentation legitimately retains neutral `.pkg` references in
the installer-objective directory. The final expectation only forbids the
invocation hierarchy; its score cap is unchanged, and the regression independently
requires no suspicious/hostile findings. Exact leaf IDs are not valid hierarchy
prefixes and are not used. The final frozen rerun
(`validate-frozen-verified.log`) now reports only the pre-existing stage2
expectation failure; none of the new controls fails validation. Full validation
is not green. Scoped diff and regression-script syntax checks pass, and all
four changed rule files still match the frozen versions byte-for-byte.

## JavaScript v1 simulation-quality disposition (2026-09-15)

The user authorized fixing poor simulations where practical and deleting them
otherwise. Static review of all 14 remaining JavaScript v1 archives found the
same canary-only implementation: an npm postinstall hook checks the random gate,
writes an attack description to a temporary `.idx` file, launches a child that
only prints `index refreshed`, and sends a fixed message to `127.0.0.1:9`.
None reads the named credentials or executes the described persistence commands.
The hex/XOR, reversed-hex, Unicode-separated and PNG-carried descriptions were
decoded as data for review, never evaluated. Concealment does not turn these
disconnected descriptions into realistic attacks. Making them useful hostile
simulations would require replacing their behavior, not a bounded repair.

Deleted packages (all under `supply-chain-benchmark-v1/javascript`): Buildtide,
Cacheharbor, Configquill, Dockwatch, Eventgrove, Fontstream, Keyringbridge,
Nativeledger, Pathweaver, Profileloom, Resolvermesh, Sessioncodec, Shortcutforge
and Taskglider. Before deletion, every archive hash matched the original
manifest, the preceding frozen audit inventory and Git HEAD. They are recoverable
from Git history; no replacement fixtures or detection rules were added.
The original manifest and checksum file remain historical provenance records.
Review evidence, including exact paths, hashes, archive membership, manifests,
decoded descriptions and entrypoints: `/tmp/sc-v1-javascript-review.VQE1SH/review.json`.

The preceding frozen scan correctly gave all 14 no hostile findings; Taskglider
had one suspicious command-text observation, not evidence of task creation.
These removals must not count as improved attack detection. No JavaScript v1
packages remain, and 296 other v1 packages still require individual disposition.
No package was executed, installed or imported, and no gate was activated.

The five-root inventory is now 1,275 files. Comparison with the preceding
1,289-file inventory confirms exactly these 14 removals, no additions and only
the v1 README changed among retained inputs. No other specimen hash changed.
No active test/rule references to the deleted archive names were found; scoped
`git diff --check` passes. `verification.json` records the inventory comparison
and the 14 preceding root verdicts. This is an inventory/disposition update,
not a new corpus-wide detection scan.

| Evidence in `/tmp/sc-v1-javascript-review.VQE1SH` | SHA-256 |
| --- | --- |
| `review.json` | `0d5ff59d66efd3a449ca8834b6c1b0ecfab355e66e08c95005a9af85d06d1d9c` |
| `inventory-after.sha256` | `6f4d793186aba4045bb537734a5eaf20c3d98c223921b84bdbc6ac97c61096e7` |
| `verification.json` | `d0fab886d875b799cac77d4133769529c1998d0cb0847defefbcb6e45a08db31` |

Worktree `make validate` fails during rule loading on the unrelated unknown
taxonomy directory `micro-behaviors/os/credentials` (`validate.log`). This
cleanup did not modify that directory or any rule. Full validation is not green;
the inventory and reference checks above passed independently.

## TypeScript v1 simulation-quality disposition (2026-09-15)

Static review of all 15 TypeScript v1 archives reached the same disposition.
Each is the JavaScript canary template with TypeScript annotations and an npm
postinstall command using Node's type stripping. The random gate controls only
decoding or copying an attack description into a temporary `.idx`; the only
child prints `index refreshed`, and the only network destination is
`127.0.0.1:9`. None executes the decoded description. Resourcecove adds a
reversed rundll32 description, but no DLL or rundll32 execution.

All plain, hex/XOR, reversed-hex, Unicode-separated and PNG-carried descriptions
were decoded during static review. Archive membership and package manifests were
also reviewed. Every archive hash matched the historical manifest, the preceding
inventory and Git HEAD. Repair would require replacing the implementation, so
all 15 TypeScript packages were deleted and remain recoverable from Git history.
No TypeScript v1 packages remain. No package was run, installed or imported; no
gate was activated, and no detection rule or engine code was changed.

The preceding frozen scan gave all 15 no hostile findings. Taskglider's sole
suspicious command-text observation describes disconnected data, not scheduled
task creation. Deletion is fixture-quality cleanup, not improved detection.
Review evidence is in `/tmp/sc-v1-typescript-review/review.json`.

The five-root inventory is now 1,260 files. Comparison with the post-JavaScript
inventory confirms exactly 15 TypeScript removals, no additions and only the v1
README changed among retained inputs. No other specimen hash changed, and no
active test/rule reference to a deleted TypeScript archive name was found.
Scoped `git diff --check` passes.

| Evidence in `/tmp/sc-v1-typescript-review` | SHA-256 |
| --- | --- |
| `review.json` | `4f3438f1e3f2b5a7134d018d345b1896b7507e450d7d695473671db3f4f72812` |
| `inventory-after.sha256` | `2b92bcecd4299bdd62c2b1f78ccc72923ea47500a6d0b8b87ed961829ca47268` |
| `verification.json` | `591b71771f6320db9585b7706c0ff11188df9251e10dab0c593c5269ef17787c` |

## C v1 simulation-quality and rule disposition (2026-09-15)

All 15 C v1 archives are unusable as package simulations. Each Conan recipe
configures a CMake executable and an `ALL` custom target that would run it, but
every `bootstrap.c` defines only a constructor and no `main`; the executable
cannot link. The constructor itself repeats the canary template: after the
random gate it writes a decoded description to a temporary `.idx`, runs a fixed
`printf 'index refreshed'` shell command and connects to `127.0.0.1:9`. It never
performs the described attack. The three archives carrying `assets/cache.png`
never reference that file; their encoded descriptions are duplicated in source.

Every manifest, build file, source file, archive member and decoded description
was reviewed statically. All hashes match the historical manifest, the preceding
inventory and Git HEAD. Repair would require replacing both build and runtime
behavior, so all 15 C archives were deleted. They remain recoverable from Git
history. No package was built or run and no gate was activated.

The review found a genuine rule bug. The suspicious objective atom
`shell-command-buffer` matched `snprintf` followed later on the same source line
by `system` or `popen`, without connecting the formatted destination to the shell
argument. Cached calls show that all 15 packages format a temp path in `p` while
passing an unrelated fixed literal to `system`. The atom had no other five-root
baseline hits, and its intended background-launch composite already requires the
distinctive hidden-tool template and background redirection. The inaccurate,
redundant atom was removed; no tree query was necessary.

A focused benign regression then exposed the same flaw in
`format-string-injection`: token order was treated as user-input flow. That atom,
its zero-hit disconnected hostile consumer, and a redundant umbrella were
removed. The remaining matcher is renamed `shell-command-format-string`, made
notable, and describes only what its within-call literal matcher proves. This
keeps useful command-construction visibility without claiming injection.
`testdata/benign/shell-command-buffer-controls/disconnected.c` drops from risk 33
with two misleading suspicious findings to risk 2 with no high finding. The 15 C
archives lose only the bad self-extract finding; after the fix 14 have no high
finding and Taskglider retains only its separate disconnected `schtasks` text
observation. Rule loading succeeds.

Full worktree validation proceeds through rule loading but fails the unrelated
concurrent hostile expectation for `simple-stealer/28-git-creds-httpx.py`, which
currently has no hostile finding. No file involved in that failure was edited.

The five-root inventory is now 1,245 files. Comparison with the post-TypeScript
inventory confirms exactly 15 C removals, no additions and only the v1 README
changed among retained inputs. No other specimen hash changed. Scoped diff and
dangling-reference checks pass.

| Evidence in `/tmp/sc-v1-c-review` | SHA-256 |
| --- | --- |
| `review.json` | `4c803f6ec26159d4db8959d60f0229477ba428cd6a56e9bce793ce0aea0aa2cf` |
| `after-rules.jsonl` | `b85ac1aa05675ab44b4ad87d46e6119371187757b1c3d3ed129002add1690f78` |
| `control-before.json` | `238c7679deb34c790fab3300f1cec716dc1902dfbe76f9c85dfd7019cbec9e0b` |
| `control-after.json` | `18e84ceba2ae6116c1eb237e476a5cfc9b2748764696547647fc3a6a4b34eebd` |
| `inventory-after.sha256` | `3e6e76e556b5085d11d5646839bbd88cd6268e2d23ccbfb59d631feadfb75fce` |
| `verification.json` | `0dbc4b6b716fdc35405af1278837d8e0b5e0fd667b39977eccd4ed6b3fdc1420` |

## C# v1 simulation-quality and scheduled-task disposition (2026-09-15)

All 15 C# v1 NuGet packages repeat the canary-only template. An imported
`build/*.targets` target runs `dotnet script` before build, although the package
does not carry that external tool. The C# module checks the random gate, decodes
or copies an attack description, writes it to a temporary `.idx`, launches only
`/usr/bin/printf index refreshed` or `cmd.exe /c echo index refreshed`, and sends
a fixed Host header to `127.0.0.1:9`. None executes the description, accesses a
named credential, writes persistence, or carries the described payload. All
manifests, targets, sources, resources and decoded descriptions were reviewed.

Every archive matched its historical manifest hash, the preceding inventory and
Git HEAD. Repair would require replacing package tooling and behavior, so all 15
were deleted; they remain recoverable from Git history. No C# v1 package remains.
No package was installed, built or run and no gate was activated.

Taskglider also demonstrated that
`objectives/supply-chain/trojanized/library/source::schtasks-create-source`
claimed task creation from disconnected command text. The atom had no consumers
and duplicated neutral `schtasks` command/reference observations, so it was
removed without adding an AST query. The retained scheduled-task objective says
only that a complete startup-task command is present; Taskglider therefore keeps
one suspicious finding rather than two. The other 14 C# packages have no high
findings. This removal also corrects the same textual overclaim in other source
languages; its corpus-wide effect will be measured in the next frozen comparison.

The five-root inventory is now 1,230 files. Comparison with the post-C inventory
confirms exactly 15 C# removals, no additions and only the v1 README changed
among retained inputs. No other specimen hash changed. Scoped diff checks pass.

| Evidence in `/tmp/sc-v1-csharp-review` | SHA-256 |
| --- | --- |
| `review.json` | `7ee122d50f8c031766f1550db60da93b4a0eaaa97f4981694b6a132485b29c78` |
| `after-rules.jsonl` | `422baf21353991ac2912d0b2783a72757880fb428987038422c870d8ddad8e98` |
| `inventory-after.sha256` | `e0806bfaf258c4cd53b030275976cf86d271da08da0576b3aea333c80b168542` |
| `verification.json` | `1bc59c90a202a1a79b1a29beec1ca3a6fde9729d3cfa0fbe1cdc50b5287f79e4` |

## Go v1 simulation-quality disposition (2026-09-15)

All 15 Go v1 modules repeat the canary-only implementation in package `init`.
After the random gate, each decodes or copies an attack description, writes it
to a temporary `.idx`, runs only `sh -c :` or `cmd /c echo index refreshed`, and
sends a fixed loopback pulse. No description is executed and no named target is
read or modified. Six plain variants also import `encoding/hex` and `strings`
without using them, which makes those packages fail Go compilation. The nine
concealed variants can compile but remain non-hostile canaries.

Every module file, source, resource and decoded description was reviewed
statically. All archive hashes match the historical manifest, preceding
inventory and Git HEAD. Repair would require wholesale behavioral replacement,
so all 15 were deleted and remain recoverable from Git history. No Go v1 package
remains. No package was built, imported or run, and no gate was activated.

After removal of the inaccurate `schtasks-create-source` atom, all 15 had no
high findings. The five-root inventory is now 1,215 files. Comparison with the
post-C# inventory confirms exactly 15 Go removals, no additions and only the v1
README changed among retained inputs. No other specimen hash changed.

| Evidence in `/tmp/sc-v1-go-review` | SHA-256 |
| --- | --- |
| `review.json` | `94b55d16f4ad9a8cda6f08b825256705017a2bc8a08fc5d828b506e6bed1399d` |
| `after-rules.jsonl` | `8baf80820963eea8a61dba9430fb5c1b0a1843cc9464ae244ab950f6589d68de` |
| `inventory-after.sha256` | `fc4ac518d8c23149ad211d007599a244d881e38028813299186133b5a1aa9a81` |
| `verification.json` | `bb820202cee62235f7da7235c510f765705a50f92ef22efbded668ec8b522530` |

## Rust v1 simulation-quality disposition (2026-09-15)

All 15 Rust v1 crates use a genuine Cargo `build.rs` hook, but the invoked code
is still the common canary template. The random gate leads only to decoding or
copying an attack description into a temporary `.idx`, running `printf` or an
echo command, and sending a fixed pulse to `127.0.0.1:9`. The description is
never executed and no named credential, persistence target or payload is opened.
Package metadata, build scripts, library source, resources and every decoded
description were reviewed statically.

All crate hashes match the historical manifest, preceding inventory and Git
HEAD. Because useful repair requires wholesale behavioral replacement, all 15
were deleted and remain recoverable from Git history. No Rust v1 package remains.
No crate was built or run and no gate was activated. After removal of the bad
scheduled-task text atom, all 15 had no high findings.

The five-root inventory is now 1,200 files. Comparison with the post-Go inventory
confirms exactly 15 Rust removals, no additions and only the v1 README changed
among retained inputs. No other specimen hash changed.

| Evidence in `/tmp/sc-v1-rust-review` | SHA-256 |
| --- | --- |
| `review.json` | `e5606f5bfcbdc8e0b505a5814a844a5e72f2a609ec50e0c43ecf6d0e21db0068` |
| `after-rules.jsonl` | `2e755ef52e70ba86cacc09e4ce2004dab1f54f1ffce3197a9edde1a91a75b1c3` |
| `inventory-after.sha256` | `615c86ed2ba9d982e4c85178d124d5e8b28451b2b39f195cd05669d8c31c0eb1` |
| `verification.json` | `26cc6f112243563cb76285e1c8535feacde808d2e2316d5e4fa1265442ae6a28` |

## Python v1 simulation-quality and task-payload disposition (2026-09-15)

The 14 remaining Python v1 source distributions use `setup.py` to execute their
bootstrap at build time, and `__init__.py` imports it again at package import.
Both routes reach only the common canary routine: the random gate controls a
temporary `.idx` write of decoded description data, a Python child that prints
`index refreshed`, and a fixed pulse to `127.0.0.1:9`. No description is
executed and no named attack target is opened. All package metadata, setup and
import files, resources and decoded descriptions were reviewed statically.

Each archive matches the historical manifest, preceding inventory and Git HEAD.
Because useful repair requires wholesale behavior replacement, all 14 were
deleted and remain recoverable from Git history. Together with the earlier
Pathweaver move, no Python v1 package remains in the hostile corpus. No package
was built, installed or imported and no gate was activated.

Taskglider exposed another existing rule bug. The zero-use
`windows-schtasks-payload` composite combined a textual task-create command with
any nearby subprocess, despite its own comment saying an unrelated subprocess
must not establish the task payload. Minified source put the temp-written spec
and harmless `subprocess.run([sys.executable, '-c', ...])` on one line, causing
the exact false positive. Cached call facts confirmed the disconnect. The
unconsumed composite was removed rather than adding AST complexity for no
demonstrated legitimate detection. The remaining high finding on all 14 is the
accurate setup-time `exec` capability; none has an objective or hostile finding.

The five-root inventory is now 1,186 files. Comparison with the post-Rust
inventory confirms exactly 14 Python removals, no additions and only the v1
README changed among retained inputs. No other specimen hash changed.

| Evidence in `/tmp/sc-v1-python-review` | SHA-256 |
| --- | --- |
| `review.json` | `b77a0b7d542ced9743010014f23d1a236aa0fee2505ab7edc4ea42f7743676f6` |
| `after-rules.jsonl` | `ed214a164e4a992b8f3530ae8638cdaec4aeffbac00a1d39148c8405096c4e5e` |
| `inventory-after.sha256` | `c082aeecaf7419222d874a7b27b1b106e0299d22ef24e9453e96689d220832d9` |
| `verification.json` | `737c93b9aa1d70f146c8c77fcb3041de225ba412431ba8193565863d9e3d33db` |

## PowerShell v1 simulation-quality disposition (2026-09-15)

The 14 remaining PowerShell v1 NuGet packages import a module whose random gate
reaches only the common canary routine: it writes the attack description stored
in `$spec` to a temporary `.idx`, starts `pwsh` with a fixed print-only command,
and sends a fixed pulse to `127.0.0.1:9`. No `$spec` value is passed to
`Start-Process`, `Invoke-Expression`, a shell, or an affected persistence API.
Every package manifest, module manifest, module source, resource and decoded
description was reviewed statically; no package was imported or activated.

All 14 archive hashes match the preceding inventory and Git HEAD. Because a
useful repair would require replacing the behavior rather than adjusting a
bounded defect, all 14 were deleted and remain recoverable from Git history.
Together with the earlier Profileloom move, no PowerShell v1 package remains in
the hostile corpus.

Taskglider's `$spec` contains a complete `schtasks /Create /SC ONLOGON ... /TR
%LOCALAPPDATA%\\...exe` sentence. That sentence accurately demonstrates a
suspicious scheduled-task capability when seen in executable-command context,
and `ONLOGON` creation is a persistence mechanism. The taxonomy therefore keeps
the neutral capability atom and the intent-bearing persistence composites; this
fixture was removed because it never uses the sentence as a command, not because
scheduled tasks are semantically ambiguous.

The five-root inventory is now 1,172 files. Comparison with the post-Python
inventory confirms exactly 14 PowerShell removals, no additions and only the v1
README changed among retained inputs. No other specimen hash changed.

| Evidence in `/tmp/sc-v1-powershell-review` | SHA-256 |
| --- | --- |
| `review.json` | `247bd0031b290206b74453cc99beccde6604693f01d6889f563ceb9584f93c87` |
| `after-rules.jsonl` | `fe5ceaea28ddb244bd65eb059361d0bff868c97f14102085a0b432a4d2199d2c` |
| `inventory-after.sha256` | `779d9ebb860086d2be90f77575ba19f28793e2803cbd257dd58d0f24f8b7f60a` |
| `verification.json` | `a414bd307f2e2153ffe608f5d3d2b60280989770624d0cdb5a55a5d72f303d2b` |

## Ruby v1 simulation-quality disposition (2026-09-15)

The 14 remaining Ruby v1 archives are structurally valid RubyGems with a genuine
native-extension install hook at `ext/cache_prime/extconf.rb`. The same gated
routine is duplicated in the importable library. Both routes decode or load an
attack description, write that description to a temporary `.idx`, invoke only
`RbConfig.ruby -e "print 'index refreshed'"`, and send a fixed pulse to
`127.0.0.1:9`. The decoded description never reaches `system`, a shell, or an
affected persistence/credential API. `extconf.rb` then only calls
`create_makefile('cache_prime')`.

All package metadata, gemspecs, extension hooks, library entrypoints, resources,
and decoded descriptions were reviewed statically. Every archive hash matches
the historical manifest and Git HEAD, and the extension copy begins with the
exact library routine. Current per-archive scans produce no suspicious or
hostile finding. No gem was installed, built, imported, or activated.

Because a useful repair requires behavioral replacement, all 14 were deleted
and remain recoverable from Git history. Together with the earlier Profileloom
move, no Ruby v1 package remains in the hostile corpus.

The five-root inventory is now 1,158 files. Comparison with the post-PowerShell
inventory confirms exactly 14 Ruby removals, no additions and only the v1 README
changed among retained inputs. No other specimen hash changed.

| Evidence in `/tmp/sc-v1-ruby-review` | SHA-256 |
| --- | --- |
| `review.json` | `1018bbbb801e9e3cbad46687b924273ea80aa146a3c3d73c509ea42ff46779fe` |
| `after-rules.jsonl` | `99b37cb7941e48ab08840822e15033afac6fc4e6209b4e3d0c97e2e5d68076ab` |
| `inventory-after.sha256` | `778e002d5256f00b2821bac4f24fd9760b2d33235fb80e8b99561609efca9d1e` |
| `verification.json` | `d83b4a0ac7bd49a4a4c03a3578f01e17330b6744fbf9ed3a52b54f9dc97ead0c` |

## Elixir v1 simulation-quality disposition (2026-09-15)

The 14 remaining Elixir v1 archives use valid Hex package layout. Their
`mix.exs` files place the gated `CacheBootstrap.run()` before the `Mix.Project`
definition, so package evaluation does provide a real build-time trigger. The
same routine is also present in `lib/cache_bootstrap.ex`.

The triggered behavior is nevertheless only the common canary: decode or load
an attack description, write it to a temporary `.idx`, run the fixed no-op
`System.cmd("sh", ["-c", ":"])`, and send a fixed pulse to `127.0.0.1:9`.
The description never reaches `System.cmd` or an affected API. All outer and
inner metadata, build files, library source, resources, and decoded descriptions
were reviewed statically; no package was built, evaluated, imported, or
activated. Current per-archive scans produce no suspicious or hostile finding.

Every archive matches the historical manifest and Git HEAD, and every `mix.exs`
begins with the exact library routine. Because useful repair requires wholesale
behavioral replacement, all 14 were deleted and remain recoverable from Git
history. Together with the earlier Fontstream move, no Elixir v1 package remains.

The five-root inventory is now 1,144 files. Comparison with the post-Ruby
inventory confirms exactly 14 Elixir removals, no additions and only the v1
README changed among retained inputs. No other specimen hash changed.

| Evidence in `/tmp/sc-v1-elixir-review` | SHA-256 |
| --- | --- |
| `review.json` | `f2ad1eefc25bcb46e93c0c646765bbb1592b17379943b90d47e5c82ffe151dd0` |
| `after-rules.jsonl` | `e61053236682b512a195cca28c3e1d13828610cc6fecb7427aea5a37417be5aa` |
| `inventory-after.sha256` | `d617129fc212a93356c3a328ebdb95af16426a679c8fcadf510290e6ebc44725` |
| `verification.json` | `15427ab03ca141373de2f761a981cdbc27118faa945d3f777ad5387c3124c951` |

## JVM v1 bytecode disposition and reboot fix (2026-09-15)

All 60 Java, Groovy, Kotlin, and Scala v1 JARs register
`edge.cache.Bootstrap` in the annotation-processor service descriptor. Static
`javap -c -p -s` disassembly confirms that every compiled class extends
`AbstractProcessor` and invokes its gated `prime()` method from the static
initializer. This is a genuine compilation-time trigger.

The bytecode is also uniformly canary-only. Across all 60 classes, the complete
external method set is limited to environment/property access, hex/string
decoding, `Files.write`, `ProcessBuilder` launching the fixed `java -version`
child, and a socket write to `127.0.0.1:9`. No decoded scenario reaches a process
argument, affected persistence API, credential API, or non-loopback endpoint.
Every bundled source file omits the `AbstractProcessor` superclass even though
the class has it, so source-only review would have mischaracterized the trigger.
All manifests, service descriptors, plugin descriptors, sources, resources,
class files, and decoded descriptions were reviewed statically; nothing was
loaded, compiled, or activated.

Initial current-rule scans had no hostile findings. The four Cacheharbor JARs
had one inaccurate suspicious finding:
`objectives/impact/system/rce::reboot-string` matched the `reboot ` substring in
the cron schedule `@reboot /usr/...`. Historical five-root results show these
four false positives were that atom's only corpus hits. The observation is now
`micro-behaviors/os/event/shutdown::jvm-reboot-command-string`, a notable neutral
capability using pre-cached `class.strings[*]` and requiring command position.
Both RAT consumers reference the relocated atom. This preserves future command
vocabulary detection, excludes cron schedules, and needs no AST or engine work.
All four post-fix scans have risk 13 and no high finding.

Every JAR hash matches the historical manifest and Git HEAD. Because meaningful
repair requires replacing the behavior, all 60 were deleted and remain
recoverable from Git history. No Java, Groovy, Kotlin, or Scala v1 package remains.

The five-root inventory is now 1,084 files. Comparison with the post-Elixir
inventory confirms exactly 60 JVM archive removals, no additions and only the v1
README changed among retained inputs. No other specimen hash changed.

| Evidence in `/tmp/sc-v1-jvm-review` | SHA-256 |
| --- | --- |
| `review.json` | `cd7575e544e88bf6972d97c89725bf7f728deaf7d7b91671233badf5eb0ebacd` |
| `java-after-rules.jsonl` | `57afafd52bdd7463aa2fd836f895c298dc085ce293d8f6c7250d952480028912` |
| `groovy-after-rules.jsonl` | `da6c6f8c74f9a78027006f24a68291cfa80b881549f3b5709b7159d03588bc39` |
| `kotlin-after-rules.jsonl` | `6c33040789ce833ac1872bf890a5f2ea980c4b43c95e1cde2bab72bc35ccf5ba` |
| `scala-after-rules.jsonl` | `3b079a3a4db03918a2033aa75df1acd4ef5bbc720f41ca271e16e81d76d0a846` |
| `java-cacheharbor-after-fix.json` | `b7f23512370f19a941cf225c66e03a8817c79d99865f3750617f1394840d9d9a` |
| `groovy-cacheharbor-after-fix.json` | `29ecc2488cb444d5ee6f9ecf87dc2d044e9f30d7c890f3bffc52680788418109` |
| `kotlin-cacheharbor-after-fix.json` | `87c6bfbc661153a709ea8a0d69e90bacb33e188aec5da5386f5e65f293f7a03f` |
| `scala-cacheharbor-after-fix.json` | `edc1d80827ff46998d54ca2c4152808fbc818a37f82a361059f84e924e086b33` |
| `inventory-after.sha256` | `335346a887b179cad95580762d0227c7174958135912e67ad8750f4757d3e1c3` |
| `verification.json` | `c0a9b98d9732a5c6df3dd9805b8d847073a27f65afe326ebc460f0017909482d` |

## Lua v1 simulation-quality disposition (2026-09-15)

All 15 Lua v1 archives are valid LuaRocks source packages. Each rockspec uses a
command build backend with `build_command='lua bootstrap.lua'`, then copies that
same file into the installed module. This supplies both build-time and import-time
triggers. Static review of every rockspec, bootstrap, resource, and decoded
description confirms that the triggered code only writes the description to a
temporary `.idx`, invokes the fixed `printf 'index refreshed'` command, and sends
a pulse to `127.0.0.1:9`. The description never reaches `os.execute`.

All archive hashes match the historical manifest and Git HEAD. Current scans
produce no hostile findings. Fourteen have no high finding; Taskglider has the
existing suspicious `scheduled-task-user-path` finding because it contains a
complete `SCHTASKS /Create /SC ONLOGON ... /TR %LOCALAPPDATA%\\...exe` command.
That remains valid persistence intent for future samples. This fixture was
removed because it writes the command as canary data, not because the command is
semantically benign. No package was built, installed, imported, or activated.

Because useful repair requires behavioral replacement, all 15 were deleted and
remain recoverable from Git history. No Lua v1 package remains.

The five-root inventory is now 1,069 files. Comparison with the post-JVM
inventory confirms exactly 15 Lua removals, no additions and only the v1 README
changed among retained inputs. No other specimen hash changed.

| Evidence in `/tmp/sc-v1-lua-review` | SHA-256 |
| --- | --- |
| `review.json` | `22a54203868102b9cdd63f4a581d448bbeb23121ef8848ce91de73ebfc6d6519` |
| `after-rules.jsonl` | `b7da7c06583021a9613c9843bfb03ffe550711d8fa08f7a38cbad073336b25d6` |
| `inventory-after.sha256` | `5706ce5a8217a10e8f2b6d3cb8c3c955441ac09c9a920253f4066db04260a389` |
| `verification.json` | `121bca31e74c71a7ea28051e477a383a8cac78ea417cbee7fb31a86dfe2dd4c4` |

## Perl and PHP v1 simulation-quality disposition (2026-09-15)

All 15 Perl archives are structurally valid CPAN distributions whose
`Makefile.PL` requires `Cache::Prime` before generating the Makefile, providing
a genuine configure-time trigger. All 15 PHP archives are structurally valid
Composer packages whose `autoload.files` entry loads `src/Bootstrap.php`,
providing a genuine dependency-load trigger.

Static review nevertheless found the same canary-only behavior in both cohorts:
the random gate leads to a temporary `.idx` write containing only the decoded
attack description, a fixed print-only child, and a pulse to `127.0.0.1:9`.
The description is never passed to a shell, process argument, registry API, or
other affected sink. Package metadata, hooks, entrypoints, resources, and every
decoded description were reviewed without building, installing, importing, or
activating a package. Every archive hash matched both the historical manifest
and Git HEAD. Current scans found no hostile verdict in either cohort.

PHP Profileloom initially had one inaccurate suspicious finding because
`php-run-key-path` treated a Run-key string alone as a persistence objective.
That duplicated the already-matching neutral
`micro-behaviors/os/registry/keys::currentversion-run` capability. The duplicate
atom was removed and both PHP persistence composites now reference the canonical
capability while still requiring `reg add` and payload context. PHP facts split
this escaped path across literals, so the existing raw-text capability remains
the appropriate cached-text fallback; no tree query or engine feature was added.
The post-fix source scan has risk 10 and no suspicious/hostile finding.

Because useful repair requires replacing behavior rather than fixing a bounded
defect, all 30 packages were deleted and remain recoverable from Git history.
No Perl or PHP package remains in v1. The five-root inventory is now 1,039
files. Comparison with the post-Lua inventory confirms exactly the 30 reviewed
archive removals, no additions, and only the v1 README changed among retained
inputs. No other specimen hash changed.

| Evidence | SHA-256 |
| --- | --- |
| `/tmp/sc-v1-perl-review/review.json` | `7280f3aa69ef6524be39fd947568ef6103ea35383123d69baf36b2b56ac28cd4` |
| `/tmp/sc-v1-perl-review/after-rules.jsonl` | `f7705d374b8aeb2f8a8d5132ade26b695a3ca91fbaa5fcb54b42092c9310dec0` |
| `/tmp/sc-v1-php-review/review.json` | `0a132272146e7fc7365e78ada203c462d389fe3f374a40e35ad14ed8f9257d1f` |
| `/tmp/sc-v1-php-review/after-rules.jsonl` | `c800c46529e058ed2eeffe996b8b3d2ab049d5e3bb6d6add4b7b71fcce47a922` |
| `/tmp/sc-v1-php-review/profileloom-after-fix.jsonl` | `87ed85cd9141fdb6adf3c3f6f54d58eb7ee8618c4d93d79b3e935b1328b5b9cd` |
| `/tmp/sc-v1-perl-php-review/inventory-after.sha256` | `d6d814df2b461ad83119a70feb8e4aa9515e9c5618be6d6234c751e618f11f00` |
| `/tmp/sc-v1-perl-php-review/verification.json` | `0f0cff90709ca8efddf4341b0524a88b070cee5e743cc08c3bf8462c285f7f8c` |

## Final v1 Objective-C, Swift, Zig, and Shell disposition (2026-09-15)

The last 60 archives all have genuine automatic entrypoints: Objective-C uses
an `NSObject +load` method compiled through the pod's `source_files`; Swift runs
`prime()` at top level while evaluating `Package.swift`; Zig executes its gated
logic from `pub fn build`; and each Debian package supplies a `postinst` whose
contents are duplicated in the installed bootstrap script.

Static review of every archive member, gate, concealed value, and decoded
description confirms that none implements its named scenario. Every entrypoint
writes `spec` only to a temporary `.idx`, launches only `/usr/bin/printf`, a
fixed Swift `Process`, `sh -c :`, or `/bin/sh -c :`, and sends only a fixed
loopback-discard pulse. No `spec` value reaches a child-process argument or an
affected persistence, credential, or network API. Objective-C and Zig embed
their alleged PNG payload as source text instead of reading the PNG. The three
Debian PNG variants resolve `assets/cache.png` relative to the dpkg maintainer
script/bootstrap directory, while the archive installs it at a different path,
so that decoder route is broken as well. No package was built, installed,
loaded, or activated during review.

All 60 hashes match the historical manifest and Git HEAD. Initial current-rule
scans had no hostile finding except Swift Cacheharbor's standalone
`swift-etc-crond-path`. That atom graded the `/etc/cron.d` string itself as a
persistence objective. Its only consumer combined it with a second regex that
already required the same path, adding no evidence. The second regex had no
five-root hits, failed a representative path/payload ordering, and scored only
2.2 precision. The misplaced atom and redundant dead signature were removed;
no broader matcher or engine feature was added. The post-fix Cacheharbor source
has risk 4 and no suspicious/hostile finding.

Because every package requires wholesale behavioral replacement, all 60 were
deleted and remain recoverable from Git history. No package payload remains in
v1; its README, original manifest, and checksum list are retained as provenance.

| Evidence | SHA-256 |
| --- | --- |
| `/tmp/sc-v1-objectivec-review/review.json` | `de4065eac5eee798233fd285e28940f5a18c0167418f2aefa207433e9c74c577` |
| `/tmp/sc-v1-objectivec-review/after-rules.jsonl` | `2f60dcc19c47688a0978d1e948b0ba7995ec093bef30f5afb421e178c7e35de9` |
| `/tmp/sc-v1-swift-review/review.json` | `bf63cf399ffdbf0b10ade45f422169e711d8468bfe6ba4cc21728b3ce2b804bd` |
| `/tmp/sc-v1-swift-review/after-rules.jsonl` | `8573a6735090a4a1df566c3097a3a0dadbf570f1a933d648107b808fb6bdbf69` |
| `/tmp/sc-v1-swift-review/cacheharbor-after-fix.jsonl` | `e75ca61eca7ee0ba22907ad89bc5ab00575e00a8d2d1fe126ebd4d7e041fca4c` |
| `/tmp/sc-v1-zig-review/review.json` | `b86e5afa09a1026cfa3ab446bf6cb3c1346c1c543c1d5ba2ddbd162ba3f8ac43` |
| `/tmp/sc-v1-zig-review/after-rules.jsonl` | `f1e93f2e673d4f7ec2f43b819e44273efa4147fd4935f16d0c13d10b15ae2be3` |
| `/tmp/sc-v1-shell-review/review.json` | `1d18a88934d76a6792934ac7cb860f66c272fe78b65bd4c5b1cb1a232538f617` |
| `/tmp/sc-v1-shell-review/after-rules.jsonl` | `8ac2dc04780c5be185b6cad8bae97bf96da73eae176a6dc448fd22ffb0d2429b` |
| `/tmp/sc-v1-final-review/inventory-after.sha256` | `98019135672852e6f126645aff6b81752a5718b2cb5f18a22e4eb4642faa3832` |
| `/tmp/sc-v1-final-review/verification.json` | `99f0e8bc1c3a8f4c58df3cd1bee099377bac24898cb669a6139c7857ded69e8f` |

## Remaining work

- Review the 431 current-corpus specimens without hostile findings; distinguish
  true misses from non-hostile fixtures before changing verdicts.
- Resolve the malformed SSH-key specimens' remaining behavior-level disposition
  and the preload RPM label; counts alone do not justify backdoor or rootkit
  verdicts. The unsupported SSH-reference and cron composites have
  been removed; the affected packages still need complete disposition.
- Review the now-visible macOS PKG scripts and same-package-path installer
  relationship. The reviewed VSIX concatenated-interpreter-command miss now
  detects; broader binding/argv forms and other VSIX packages still need review.
  Add RPM stripped-CPIO traversal using its header file-index metadata. The
  existing newc padding/error bugs are fixed, but do not cover this format.
  Continue GitHub Actions disposition. The false service escalation and
  quiet-download-only inferences have been corrected; older delivery/chmod
  pairings still require review.
  The three confirmed Brew misses now detect. The remaining five Brew
  artifacts have received bounded source/call-fact review above; none supplies
  sufficient evidence for a new hostile verdict. Unknown resource contents
  and telemetry purpose remain unresolved, not silently classified as benign.
  Inspect existing facts and relationships before considering engine changes.
- V1 disposition is complete: all 315 original artifacts were either moved as
  confirmed non-hostile canaries or deleted as poor simulations. Its retained
  README, manifest, and checksum list are provenance only.
- Cobaltcraft's redundant archive wrappers and disconnected-env composite are
  removed (one hostile finding remains). Consolidate the older npm SSH-key installer (four) and the WordPress
  helper (four, including YARA). Test the retained file-level environment/HTTP
  composites against same-file disconnected sources and benign telemetry.
- Continue the Go iterator/helper-return destination gap and non-Go destination
  precision work recorded in `SUPPLY_CHAIN_ENGINE_TODO.md`. Inspect existing
  facts/tree predicates first; do not add engine features just to fit a sample.

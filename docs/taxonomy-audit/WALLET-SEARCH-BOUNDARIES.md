# Filename search and wallet-source export

This pass makes **29 moves**, retires one unsupported hostile wrapper, and adds
two composites: a shared discovery-evidence selector and a wallet-specific export
classifier. The desktop-wallet leaf falls from **44 to 24**. The six-rule
`fs/enumerate/extension` branch is removed; its predicates now share `fs/search`.
No directory is added, no cap exception is introduced, and all receiving leaves
remain within 85.

The [move manifest](wallet-search-moves.csv), [consumer repairs](wallet-search-consumer-repairs.json),
[additions](wallet-search-additions.json), [retirement](wallet-search-retirements.json),
and [labels](wallet-search-labels.json) record the exact changes. Twenty-seven
moves preserve matcher/settings semantics after reference normalization; the two
Telegram source/export definitions are deliberately split as described below.
Criticality is not lowered to conceal a placement problem.

## Directory contracts and sibling audit

`micro-behaviors/fs/search` owns file selection: filename/content predicates,
wildcards, search options, named search interfaces, and searches requiring a
particular filename predicate. It contains **40 rules** after this pass.

- Nineteen desktop-wallet rules move here. Shell, AppleScript, PowerShell and
  Mach-O are evidence forms/scopes, not distinct taxonomy layers. Descriptions
  distinguish wildcard literals, option fragments, token proximity, and fuller
  command/traversal evidence.
- Six extension predicates move from `fs/enumerate/extension`. Extensions are
  selection criteria, not another resource type to inventory. Batch loops,
  Java suffix tests, JavaScript filters and wildcard literals share the operation.
- `find-app-bundle` moves from directory traversal because its required name
  predicate selects application bundles. Recursion alone retains the traversal
  home. Existing acquisition consumers retain that traversal evidence explicitly.
- The dotenv parser method moves out of search to `data/config/load`, which now
  contains **2 rules**. Interpreting configuration contents is distinct from
  finding the file; the dotenv export consumer keeps both references.

The shared `fs/search::recursive-file-discovery` selector preserves an OR between
traversal and application-bundle search for three consumers requiring that group
in `all`. It is incomplete discovery evidence, not a copied operation matcher or
an assertion of acquisition. Its platform declaration is the union of the
underlying observations. Consumers whose group is already in `any` keep an exact
reference instead, avoiding changes to threshold cardinality.

The broader traversal and search branches still warrant semantic review. In
particular, a root-path reference accepting `ls`, `cat`, or `find` does not always
require recursion. This pass does not endorse every existing traversal member.
The [taxonomy contract](../../TAXONOMY.md#collection-credentials-discovery-and-theft)
now documents filename selection, traversal, configuration interpretation, and
source-specific export boundaries.

## Preserve export while distinguishing its source

The old `telegram-wallet-search-source` accepted either wallet search or a
Mach-O combination of `-maxdepth`, `-iname`, `id.json`, and stderr suppression.
The latter contains no required wallet clue. Relabeling the entire combination
as wallet export would retain the error; leaving only a broad file label would
lose a useful distinction on the wallet cases.

The source alternatives now have separate export classifiers:

- `stealer/wallet::wallet-search-telegram-send` requires shell or PowerShell
  wallet-name search evidence plus a Telegram send.
- `stealer/file::file-search-telegram-send` requires the generic Mach-O `id.json`
  search evidence plus a Telegram send. Its description names `id.json`.

The two branches retain the original confidence, criticality, send alternatives,
ATT&CK settings, and 8,192-byte proximity. Their declared file types follow their
source legs. Their union equals the original classifier's source/send expression
for all [32 truth assignments](wallet-search-export-union.csv); real-engine
positive and negative controls verify both branches. The truth table is a
Boolean check, not a claim of proven runtime data flow.

The former source helper becomes `fs/search::wallet-file-search`, admitting only
the two wallet search alternatives. Generic `id.json` options no longer activate
the desktop-wallet target selector. A before/after compiled Mach-O control
reproduces that correction while preserving its file-export finding.

## Unsupported theft verdict removed

`desktop::crypto-wallet-file-stealer` had one required leg: the existing JSON
filename-filter composite. It added a hostile verdict but no acquisition or
transfer evidence. The old classifier matched a local JavaScript filter over
repeated wallet-name vocabulary. It is retired without demoting its matcher;
the underlying suspicious filter remains, with its matcher and settings intact.
That filter and its keyword dependencies remain explicit follow-up work.

The retirement removes one duplicate vote from broad directory thresholds. That
is intentional: two wrappers around the same observation must not manufacture
evidence diversity. No exact-ID consumer depended on the retired wrapper.

## Consumers and verification

Reviewed **39 affected directory references in 32 consumers**. The
[consumer report](wallet-search-directory-consumers.csv) records the decisions.
Twenty ordinary consumer repairs preserve wallet-specific search clues,
traversal evidence, and completed exports. Two additional recorded changes split
the original source/export definitions, making **22 repair records** total.
Three CI consumers retain both resulting export branches. Broad source directories
admit the appropriate new exporter, while generic search fragments cease to
stand for wallet acquisition merely because of their previous location.

The [verification record](wallet-search-verification.json) records focused
assertions, before/after controls, the complete controlled corpus run, and live
validation limitations. The preservation proof protects 69 original definitions;
unrelated concurrent changes are recorded separately. The isolated comparison
uses the previously passing desktop-wallet snapshot plus this pass's 40 affected
files, inheriting the documented shell-decoder isolation. No corpus files or
fixtures are excluded and no unrelated live definition is reverted.

The global cap migration remains unfinished. Remaining desktop cohorts include
recovery UI, application interference/persistence, package-only decryption
claims, broad wallet catalogs, and staging. Resolve their supporting neutral
observations and source boundaries before splitting the residual category.

The subsequent [credential-UI pass](WALLET-UI-BOUNDARIES.md) resolves the UI,
product-reference and application-interference portion of this backlog; its
measurements are a later checkpoint, not a rewrite of the results above.

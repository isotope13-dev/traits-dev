# Wallet stores, application references, and secret export

This pass moves **83 rules** and reduces the oversized desktop-wallet leaf from
**120 to 44**. Every destination is an existing strict leaf within the 85-rule
combined cap. This resolves the size violation without inventing a desktop,
platform, language, library, or overflow subdivision.

The [move manifest](desktop-wallet-moves.csv) records final IDs and normalized
definition hashes. Matchers, effective scope, criticality, confidence, exclusions,
proximity, and ATT&CK settings are preserved. Twenty-seven descriptions and six
local IDs are clarified, including replacing the unsupported “double harvest”
claim with `seed-export-invalid-message`. No identical atomic matcher body
involving these moves needed merging.

## Placement and disambiguation

The [taxonomy contract](../../TAXONOMY.md#collection-credentials-discovery-and-theft)
classifies the whole matcher, including its least specific allowed alternative.

| Observation | Moves | Destination and resulting count |
|---|---:|---|
| Wallet store locations and location roll-ups | 50 | `micro-behaviors/fs/path/wallet`: 57 |
| Installed application bundle locations | 4 | `micro-behaviors/fs/path/application/bundle`: 10 |
| Application/package references and mixed app/location roll-ups | 20 | `micro-behaviors/os/application/target`: 22 |
| DPAPI package reference | 1 | `micro-behaviors/os/security/dpapi`: 16 |
| Telegram-send channel/member spelling | 1 | `micro-behaviors/communications/messaging/send`: 27 |
| Unqualified secret-phrase label | 1 | `micro-behaviors/ui/dialog/prompt`: 30 |
| Required seed source and probable export | 3 | `objectives/exfiltration/stealer/wallet`: 40 |
| Private-key/secret-entry export without a required wallet source | 3 | `objectives/exfiltration/stealer/credential`: 37 |

The application-reference moves include two Ledger/Trezor product strings from
`metadata/file/string/identity`. They are content clues about an application of
interest, not proof that the analyzed file is that independent artifact. A path
to its installed bundle is also distinct from its secret store. A recovery label
alone is UI evidence. None becomes acquisition merely because a theft composite
uses it. Store-specific export takes precedence over HTTP, Telegram, or encoding.

## Consumer preservation

Reviewed **48 affected directory references in 42 consumers**. The
[consumer report](desktop-wallet-directory-consumers.csv) records membership
changes and decisions; [11 explicit repairs](desktop-wallet-consumer-repairs.json)
retain appropriate evidence:

- Wallet-target selectors and wallet-aware acquisition/profile classifiers retain
  the 72 moved application/store observations that actually identify wallets.
  DPAPI, generic Telegram vocabulary, and unqualified secret labels are omitted.
- Sensitive-file selection retains 50 store-location observations, not application
  installation paths, brands, or UI labels.
- Source classifiers retain relevant generic credential exporters explicitly;
  the three wallet exporters already follow their wallet-export directory leg.
- Webhook classifiers retain wallet-store locations and completed exporters.
  Product names alone no longer stand for sensitive data.
- The messaging-session classifier reuses the existing wallet-target selector
  for its required OR group. Other consumers retain individual observations so
  a directory's multiple findings are not collapsed into one `needs` vote.
- Broad filesystem/messaging consumers gain the correctly classified capability
  observations. Ledger/Trezor mentions cease to provide blanket benign-identity
  suppression through the metadata directory.

The full matcher of `desktop-wallet-target-family` still includes the remaining
legacy desktop objectives; this is preservation during an incomplete migration,
not endorsement of all 44 remaining definitions.

## Remaining semantic audit

The size violation is resolved; the desktop category is not fully reconciled.
The [filename-search follow-up](WALLET-SEARCH-BOUNDARIES.md) implements cohort 1,
retires the redundant JSON-filter theft wrapper from cohort 5, and reduces the
remaining desktop leaf to 24 rules. Counts above describe this earlier checkpoint.
The next pass should address these cohorts with consumer review and controls:

1. **File selection and enumeration.** Wallet/keystore globs, `-iname`,
   `-maxdepth`, and `find` belong with the operation/selection capability.
   Command words alone do not require an actual search. The Mach-O search
   composite requires `id.json` and generic find options, but no wallet clue;
   neither its wallet source nor its execution claim is supported as written.
   Reconcile the shell, AppleScript, and PowerShell evidence under common
   operations, preserving parser and platform scope on individual rules.
2. **Recovery interfaces and vocabulary.** Three prompt composites can follow
   wallet UI after their neutral wallet-context dependency has a defensible home.
   `desktop-wallet-spoofer` combines recovery UI with daemon/UI options, without
   requiring deception. Tighten or retire the unsupported wrapper deliberately;
   do not move a hostile claim to a neutral leaf or lower its criticality to fit.
3. **Application interference and persistence.** Force-kill, application
   replacement, and LaunchAgent observations should follow termination,
   replacement/impersonation, and persistence, respectively. The persistence
   composite's description mentions seed exfiltration although no send is
   required. Its acquisition classification is also wrong.
4. **Secret-container access.** `node-seco-dpapi-wallet-decrypt` requires two
   package references, not a decrypt operation. Audit the SECO provider's actual
   supported operation and consumers before assigning its operation home.
   A package pair alone must not be described as completed wallet decryption.
5. **Broad wallet catalogs and theft wrappers.** `stealer` can satisfy its
   threshold with three location/application roll-ups; that is not three reads
   or stores acquired. The JSON filename-filter wrapper similarly adds a
   hostile theft verdict without an acquisition leg. Separate useful targeting
   observations from unsupported verdicts, preserving relevant consumer evidence.
6. **Staging and multiple sources.** Import-time Monero archiving and AppleScript
   wallet staging establish different acquisition/staging contexts. Neither is
   outbound export without a send leg. Notes and browser-cookie combinations
   require the same independent-source analysis used for `stealer/multi-source`.

Sibling follow-up remains necessary: mnemonic retains **41** rules after these
five exporter moves, including generic private-key UI and capture-flow claims;
wallet keywords and extensions still mix neutral source clues and acquisition.
The blockchain-library branch retains 63 rules from the preceding audit. A
cross-sibling review must avoid creating another home for the same source clue.

## Validator improvements suggested by the audit

These are review candidates, not newly enforced heuristics:

- Compare normalized composite conditions as well as identical atomic `if`
  bodies, while accounting for effective scope, proximity, exclusions, and
  confidence before suggesting a merge. A wrapper adding only criticality or a
  stronger description deserves review even when it is not an exact duplicate.
- Report neutral evidence admitted indirectly through broad objective-directory
  references. A generic prompt or package import can otherwise acquire theft
  semantics solely from its old placement.
- Flag a source-specific classifier whose alternatives do not all require that
  source, and descriptions claiming repetition when only one event is required.
  Neither source diversity nor repetition follows from a raw trait count.

Do not turn these into lexical directory-name tests or a single-child warning.
Semantic admission contracts and counterexamples are the deciding evidence.

## Verification

See [the verification record](desktop-wallet-verification.json) for final counts,
commands and limitations. The preservation proof covers 144 affected definitions;
unrelated shared-tree edits are recorded separately. New fixtures are scanned,
never executed. They check locations versus application references, local prompts
versus sends, DPAPI versus wallet targeting, generic private-key versus wallet
exports, and directory-consumer preservation.

The live full catalog is not green. A concurrent new RAT definition initially
failed parsing and subsequently blocked loading with an unbounded two-character
`rm` matcher. The controlled corpus run uses the previously passing mnemonic
snapshot plus this migration's 35 changed files, after verifying their pre-change
file definitions equal the migration baseline. No corpus files or fixtures are
excluded, and no live unrelated definitions are reverted. The pre-existing
shell-decoder isolation is inherited and linked in the isolation record.

The subsequent [credential-UI pass](WALLET-UI-BOUNDARIES.md) resolves the UI,
product-reference and application-interference portion of this backlog; its
measurements are a later checkpoint, not a rewrite of the results above.

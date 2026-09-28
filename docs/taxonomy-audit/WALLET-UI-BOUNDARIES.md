# Credential interfaces, product references, and process interference

This pass records **44 moves, one merge, and two unsupported hostile wrapper
retirements**. Desktop-wallet falls from **24 to 17**, objective mnemonic from
**41 to 33**, and the legacy blockchain-library subtree from **63 to 56**.
`crypto/library/blockchain/brand-wallet` and the single-marker TronLink artifact
leaf disappear. Every receiving directory is a strict leaf within 85; there are
no cap exceptions.

The [move manifest](wallet-ui-moves.csv), [merge](wallet-ui-merges.json),
[retirements](wallet-ui-retirements.json), [consumer repairs](wallet-ui-consumer-repairs.json)
and [labels](wallet-ui-labels.json) record the changes. Forty-three moved
definitions preserve effective matcher/settings semantics after reference
normalization. The canonical MetaMask relocation and the merged keyword marker
have the explicitly recorded case-folding/platform union described below.

## Placement and sibling boundaries

- `ui/controls/credential` owns secret-entry interfaces whose alternatives permit
  a generic private key or credential. Nine definitions move here. Required
  wallet/seed-phrase interface context follows `ui/controls/wallet`; two more
  verification/view symbols join that leaf. Neither interface alone establishes
  deception, acquisition, or export.
- `os/application/target` owns named product references and catalogs. Mentioning
  MetaMask, Phantom or TronLink does not identify the analyzed file as that
  application or as an independent library artifact. The receiver has 43 rules.
- `crypto/asymmetric/key` owns private-key/seed material references whose matcher
  does not require mnemonic encoding. Mnemonic/seed-phrase identifiers follow
  `crypto/mnemonic`. Wallet/keypair filenames follow the respective `fs/path`
  leaves; product catalogs and generic secret UI do not qualify as file locators.
- `process/terminate/command` owns the three termination observations. The
  application-path composite requires a **named wallet application path**; a
  generic `/Applications/` string does not satisfy it. A concealed window plus
  wallet-context termination moves to `impact/degrade/process`: this supports
  interference, but does not require application replacement or credential theft.
- `os/service/launchagent` owns the wallet-associated label. A label reference is
  not evidence of installing a service or impersonating its owner.

These boundaries are documented in [TAXONOMY.md](../../TAXONOMY.md#collection-credentials-discovery-and-theft).
The hierarchy describes probable capability or purpose; none of these placements
requires runtime proof. Language, executable format and packaging do not select
parallel homes.

## Merge and retirements

The old lowercase MetaMask keyword is subsumed by the case-insensitive product
marker. The canonical marker retains the broader file scope and explicitly
unions Unix/Windows platforms. Case-insensitive matching across that union is an
intentional coverage extension. All exact consumers redirect to the canonical
ID; no condition list gains duplicate references. Confidence follows the
canonical product observation, rather than preserving two differently weighted
votes for the same name.

The counted Phantom aliases are **not** equivalent observations: they require
different counts, file/platform scopes, size limits and exclusions. The
[overlap review](wallet-ui-matcher-overlap-review.json) records why an identical
`if: id:` body alone is insufficient to merge them.

Two hostile wrappers are retired. Daemon/UI switches plus a recovery prompt did
not require spoofing; a wallet label plus LaunchAgent/UI vocabulary did not
require secret export or malicious persistence. Neither wrapper had an exact-ID
consumer. Their underlying observations remain, with criticality preserved.
Actual seed-export rules remain and have positive and benign controls.

## Directory consumers and detection effects

Reviewed **653 affected directory references in 475 consumers**, protecting
**541 original definitions**. Eleven consumer repairs retain relevant source,
path or wallet-context observations; two additional records authorize the
MetaMask merge settings. Wallet-specific termination evidence remains available
to acquisition selectors. Webhook consumers retain key/mnemonic/path material,
while file selectors retain the two moved filename observations. A required
keyword-directory OR group remains an OR when expanded in the Rust consumer.

The [reference-role report](wallet-ui-reference-role-summary.json) records 600
artifact-exclusion references, eight positive/mixed artifact memberships, and
three crypto-implementation memberships whose incidental scope is corrected.
These are changed **resolved memberships**, not 600 deleted exclusion clauses.
Product/provider references no longer establish benign artifact identity.
Before/after controls demonstrate that Phantom vocabulary previously suppressed
an ActiveX constructor observation and TronLink vocabulary suppressed a script
literal and its loader consumer. The moved references remain observable alongside those capabilities.

## Verification and follow-up

See the [verification record](wallet-ui-verification.json) and
[fixture controls](../../testdata/taxonomy/wallet-ui/README.md). New controls pass 41 assertions; 82 established assertions and four exact
seed-export assertions also pass (127 assertions across 37 files). The complete
controlled corpus passes **1,841 fixtures**. Its baseline is the previous passing
wallet-search snapshot plus 46 affected files, including retirement-only files;
[the isolation record](wallet-ui-validation-isolation.json) distinguishes this
from the live changing tree. No corpus files or fixtures are excluded.

The seed-export corpus expectation now requires the two exact current exporters;
the benign counterpart forbids those exact IDs. Score thresholds are unchanged.
The [expectation record](wallet-ui-fixture-expectations.json) preserves before/after
values. A stale negative directory assertion could otherwise pass vacuously.

Strict validation remains at **110 diagnostics**, including **144 over-cap
directories**. Live soft validation still cannot load an unrelated unbounded
`rm` matcher. Four outside definition changes are recorded separately. The
engine's existing broad text-scope policy now admits application-target
references so relocation preserves their file coverage; the uniform 85-rule cap
is unchanged.

Further validator/debugger improvements suggested by this pass:

1. Validate that fixture exact IDs and prefixes resolve. Reject obsolete IDs and
   filename-shaped pseudo-prefixes, especially vacuous forbidden assertions.
2. Report same matcher bodies together with effective defaults, counts, scope,
   size and exclusions. Offer a merge only when those semantics agree, or require
   an explicit coverage union. Existing overlap validation caught MetaMask.
3. Avoid rebuilding the full precision-reference index for every member when
   explaining an unmatched broad directory exclusion. A stack sample during the
   ActiveX control showed repeated index construction in `test-rules`; ordinary
   scan output verifies these two exclusion controls without that expensive trace.

Residual desktop rules need individual review: recovery UI still depends on the
legacy wallet-token helper; SECO/DPAPI package imports do not alone justify a
hostile decryption verdict; a wallet catalog is not theft; staging, acquisition
and export must stay distinct. The remaining blockchain-library provider and
exchange cohorts also need capability destinations. This pass does not complete
the wider cap migration or certify those residual categories.

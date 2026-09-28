# Secret-store sources and acquisition versus export

The [11-rule manifest](keychain-source-moves.csv) reduces `stealer/keychain`
from **22 to 11** rules. It moves five non-export observations to credential
access or capabilities, and six authentication-data exports to `credential`,
which now has **33**. All receiving directories remain strict leaves within 85.
This repairs source precision; it does not resolve another cap violation.
The contracts are in [TAXONOMY.md](../../TAXONOMY.md).

## Decisions

Keychain, keyring, Vault and Protected Storage identify a credential-store
source. DPAPI unprotect identifies a protection mechanism; it does not establish
which store supplied the protected data. Its webhook classifier therefore
follows authentication material in `credential`.

Five classifiers accepted keychain OR Discord, cloud, browser-login, or
SSH/browser secrets. The common required dataset is authentication material,
so they also follow `credential`. They do not require keychain, and alternatives
cannot establish independently required datasets for `multi-source`. All
alternatives, conditions, thresholds and confidence/criticality remain intact.

Local acquisition is distinct from export:

- GameCenter keychain targeting joins `credential-access/gaming/mobile`.
  The remaining export classifier references it and supplies network context.
- Ruby keychain plus SSH collection requires both sources but no export;
  it joins `credential-access/theft/multi-store`.
- Shell keychain dumping plus additional secret-query clues joins
  `credential-access/keychain/extract`; it no longer claims HTTP transfer.
- A password prompt paired with a login-keychain path joins keychain credential
  access. Its description no longer claims the path was actually read.
- `SecItemCopyMatching` near `KEYCHAIN=` is a keychain/output capability clue.
  It moves to `micro-behaviors/os/security/keychain`; the Swift export consumer
  retains its separate transfer condition.

Eleven descriptions and the misleading IDs are clarified in the
[label manifest](keychain-source-labels.json). No criticality was lowered.
The small keychain leaf still has semantic work below; counts are not approval.

## Verification and consumer preservation

The normalization proof protects **25 definitions**, with no concurrent changes
outside the declared migration. It preserves moved matcher bodies and effective
settings across 118,816 definitions, allowing only the separately recorded
[Python collector reference repair](keychain-source-consumer-repair.json).
No exact atomic matcher-body duplicate touching the moved atom was found.

That collector previously obtained the DPAPI Python source through the keychain
directory. It now also references the relocated rule explicitly. The
[file-type eligibility proof](keychain-source-python-eligibility.json) confirms
that this is exactly the formerly eligible Python candidate set; no other moved
rule applies to Python. Its `needs: 3`, `near_lines: 160`, existing keychain
reference and other source candidates stay unchanged. Adding the whole generic
credential category would have widened this classifier unnecessarily.

The [directory-consumer audit](keychain-source-directory-consumers.csv) covers
**16 affected references in 12 consumers**. Local acquisition no longer supplies
an export finding to broad consumers. It can still support credential-access
consumers and composites that independently supply transfer context. No aliases
preserve the former erroneous export membership.

Eleven new controls exercise **21 assertions**: local versus network-bearing
GameCenter, Swift keychain output versus POST, local Ruby keychain/SSH collection,
keychain or Discord HTTP POST, shell acquisition versus upload, and DPAPI with or
without a webhook. The established stealer-source suite adds **38 assertions**
across 19 controls, including the profiled Python collector. Fixtures are scanned,
never executed.

The actual shared-tree soft run still fails on the unrelated pre-existing
PyAigis shell-decoder regression described in the [mail audit](MAIL-SOURCE-BOUNDARIES.md).
A fresh temporary copy with exactly that shell rule restored to its previously
passing definition passes **1,841 corpus fixtures**, with no excluded files or
fixtures. The [isolation record](keychain-source-validation-isolation.json)
preserves both definitions. This is not a passing live-tree result.
Strict validation retains **89 diagnostics** and **149 oversized directories**.

## Remaining review

- Two native DPAPI/registry/loader combinations have no required outbound
  transfer, and their store/intent inference needs review. Do not relabel them
  as a particular store or lower criticality simply to avoid the question.
- The AppleScript password-variable plus URL/server/shell alternative requires
  neither keychain nor necessarily a network channel. Review its underlying
  generic variable observations and intent before choosing a replacement.
- Lua keychain access plus `http.request` or socket connect is a weaker transfer
  inference than an actual send. The controls preserve that existing behavior;
  they do not certify the classifier's precision or a data-flow relationship.
- The Rust ingest-endpoint classifiers retain some file-type-ineligible source
  alternatives and weak transfer evidence. The migration does not expand scopes
  or silently add calls. Existing impossibility validation should explain dead
  alternatives as well as impossible required legs where useful.
- ISO Vault clusters and Protected Storage report helpers need source-capability
  review outside this leaf; packaging and implementation are not theft sources.

The cumulative ledger has **1,153 implemented dispositions out of 1,156**, with
three sweep reviews. The broader semantic and cap backlog remains unfinished.

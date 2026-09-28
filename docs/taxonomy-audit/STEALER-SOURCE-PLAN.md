# Stealer taxonomy: classify the information, not the breadth of collection

## Current checkpoint: wallet sources and supporting capabilities

The subsequent [wallet-search](WALLET-SEARCH-BOUNDARIES.md) and
[credential-UI](WALLET-UI-BOUNDARIES.md) audits separate source-specific export
from filenames, product references, prompts, and process/service observations.
The latter protects 541 definitions and records 653 affected directory references;
127 focused assertions and 1,841 controlled corpus fixtures pass. Actual secret
export remains classified by its required source. Generic credential entry does
not establish a wallet source, and a wallet name does not establish theft or
benign artifact identity.

The system-information source audit moved `host-user-identity-http-query` from
`system-info/profile` to `system-info/identity`: host/user fields and identity
alternatives are required, with no second host-data class. `profile` now has 84
rules and `identity` has 38. A rule accepting either process or software
inventory remains in `profile` because those alternatives leave the host-data
class open; its description now says “host inventory,” and the rule does not
qualify as multi-source theft. Conditions, effective settings, and mappings are
unchanged, and all **1,842 controlled corpus
fixtures** pass.

Three legacy `sweep` definitions remain under review: permissioned remote-WebView
behavior, snapshot/upload prose, and a raw-IP/header composite with alternative
source clues. None can be moved wholesale into `multi-source`: each lacks a
required combination of independent stolen datasets. Resolve their own capability
or objective claims and consumers before retiring the old leaf. The current
[plan](PLAN.md) records the broader unfinished migration; measurements below are
historical checkpoints.

## Implementation checkpoint: browsing records and storage boundaries

The [history audit](BROWSER-HISTORY-BOUNDARIES.md) records **13 moves**, four
retired wrappers, and one new neutral tab-event helper. Ten history/navigation
exports now follow their browser source. Browser export has **85** rules,
activity/browser **53**, and tracking **45**. No receiver exceeds the cap.

Local storage now requires a storage interface; encryption alone no longer
satisfies it. The source-and-send classifier remains available. Payload evidence
is explicit in its consumers, and recognized cookie helpers no longer supply
false theft evidence. **8,192 Boolean comparisons**, **42 focused assertions**,
and all **1,841 corpus fixtures** pass. Strict validation retains **89
diagnostics**. The audit distinguishes the 39-definition move-preservation
proof from intentional refinements and retirement effects on broad consumers.

The shared tree now has **150 oversized directories**: an independent CFML
webshell addition raised its receiver to 86 during the pass. The ledger records
**1,054 implemented dispositions out of 1,057**, with three sweep reviews;
retired mixed observations have no fabricated single replacement. Remaining
browser acquisition, mailbox, keychain and HTTP-report classification is listed
in the audit. The overall taxonomy migration remains unfinished.


## Implementation checkpoint: browser sources and HTTP request facets

The [browser-source audit](BROWSER-SOURCE-BOUNDARIES.md) records **55 moves**:
stealer/browser falls from 106 to **78**, request/client from 96 to **85**, and
the duplicate HTTP body branch is retired. The catalog has **149 oversized
directories**, down from 151. Every receiver is a strict leaf within 85.

An ordinary JSON POST no longer supplies false cloud-theft evidence through a
misplaced helper. Distinct Go method groups replace invalid occurrence counts.
All **1,841 corpus fixtures** and **73 focused assertions** pass on the shared
tree without exclusions; strict validation still reports **88 diagnostics**.
The audit separates the matcher-preserving moves from intentional method-count
and loader repairs, records **377 protected definitions**, and documents
**92 changed directory references in 83 consumers**.

The ledger has **1,036 implemented dispositions out of 1,039**, with three sweep
reviews and a broader semantic backlog. Next, reconcile remaining browser helper
and source claims, route the history/navigation exports from collection, and
audit keychain alternatives. Passing the cap does not certify those classifiers.


## Implementation checkpoint: browser activity and instrumentation

The [activity audit](ACTIVITY-TELEMETRY-BOUNDARIES.md) records **113 moves** and
two cap fixes: activity/browser now has **62** rules and monitor/tracking **50**.
The remaining cap backlog is **151**. The ledger has **981 implemented
dispositions out of 984**, with three sweep reviews; the whole semantic backlog
is larger. Browser-export routing awaits review of its existing 106-rule leaf.

All 82 focused assertions pass. The isolated corpus passes 1,841 fixtures after
repairing a JVM directory-observation regression, while current-tree validation
remains failing. See the audit for the one newly added Go file excluded from
isolated verification and the complete validation limitations.

## Implementation checkpoint: input devices, notifier hooks, CSS export, and touch

The [34-rule sibling manifest](input-siblings-moves.csv) retires the overlapping
keylog/evdev leaf, moves kernel notifier collection into hook, and routes CSS
input oracles by exported source. Generic routes, paths, buffers and device
interfaces become capabilities. Direct-device collection has **9** rules,
hook **60**, and input export **54**. Touch collection has its own documented
source category; raw coordinates are not classified as keystrokes.

The [sibling audit](INPUT-SIBLING-BOUNDARIES.md) records **66 protected
definitions**, **32 changed directory references in 30 consumers**, and the
remaining classifier review. All conditions and effective settings are
preserved. The cumulative ledger has **868 implemented dispositions out of
871**, with three sweep reviews; the broader semantic backlog is separate.
The cap backlog remains **153**, with no exceptions or new depth.

## Implementation checkpoint: keyboard and input boundaries

The [input audit](KEYLOG-INPUT-BOUNDARIES.md) records **200 moves**. Keylog/capture
falls from 193 to **53**, resolving one cap violation; **153** remain. Generic
window hooks, input libraries, synthesized keystrokes, local acquisition, and
input export now follow their documented subjects. All receivers remain leaves
within 85. The cumulative ledger has **834 implemented dispositions out of 837**;
three sweep cases and the separately documented semantic backlog remain.

All **1,840 verdict fixtures** and **52 focused assertions** pass. One explicit
exclusion repair fixes System Events automation being suppressed as descriptive
text. The audit records protected-definition checks, parent-membership changes,
and unresolved classifiers. Earlier checkpoints retain their own measurements.

## Implementation checkpoint: recorded information and neutral mechanics

The [recording-source audit](RECORDING-SOURCE-BOUNDARIES.md) records **68 moves**
into audio/camera/audiovisual export, local acquisition, and source-neutral
recording capabilities. Monitor/capture now has **29** rules; surveillance **6**.
Every receiver remains within 85, and no exemption is introduced. The cumulative
[ledger](stealer-source-dispositions.csv) contains **634 implemented** dispositions
out of **637**, with three unresolved sweep cases. Source/control ambiguities
remain in the two legacy leaves and are documented in the audit.

The catalog still has **154 oversized directories**. This pass follows through
on semantic sibling review rather than claiming another cap reduction. The
validator registry now recognizes the documented collection sources and stream
recording. See the audit for preservation checks, changed broad consumers, and
the dependency-compatible isolated validation build. Historical checkpoints
below retain their own measurements.


## Implementation checkpoint: capture sources and simpler depth

The [capture source audit](CAPTURE-SOURCE-BOUNDARIES.md) records **181 moves**,
including collapsing the redundant screenshot/capture child into its parent.
Screen and unspecified-image exports now have source-defined homes; local
capture, graphics, geometry, paths, and APIs follow their own subjects.
Screenshot collection has **58** rules; monitor/capture **83**. Native-capture
and screenshot/stream are retired. All receivers are strictly leaves within 85.

The full catalog preserves effective matcher definitions, with one documented
collector update to follow new screen/image directories. All **1,837 verdict
fixtures** and **29 focused assertions** pass. Strict validation retains 70
issues, with **154 oversized directories** and **4,273 excess rules**. The
[569-row ledger](stealer-source-dispositions.csv) has **566 implemented**
dispositions and **three sweep reviews**. Surveillance still has 14 rules needing
individual source/control-role review. See the audit for that backlog and the
52 affected broad references; the cap passing does not end semantic review.
Historical checkpoints below retain their earlier counts and IDs.


## Implementation checkpoint: HTTP capabilities and four remaining sweep cases

The [HTTP capability audit](HTTP-CAPABILITY-BOUNDARIES.md) records **81 moved
rules and one inlined helper**. Neutral upload falls from 94 to **66** rules;
HTTP collect falls from 121 to **83**. No new hierarchy levels or cap exemptions
were added. Identified source exports follow their source, endpoint/header/form
observations follow capabilities, and the two aggregate collectors use HTTP
collection without claiming independent source classes.

The [82-entry manifest](http-capability-moves.csv) and whole-catalog comparison
verify matcher preservation, with explicit exceptions for equivalent helper
inlining and making Yarn artifact identity notable. Broad directory votes are
intentionally narrower. All **1,837 verdict fixtures** and **18 focused
assertions** pass. Strict validation retains 70 reported issues, with oversized
directories reduced to **156** and excess rules to **4,329**.

The cumulative [ledger](stealer-source-dispositions.csv) now covers **389 rules**:
**385 implemented**, **four review cases**. The remaining sweep rules concern
Android permission/WebView inference, generic snapshot-transfer wording, local
screenshot capture, and a raw-IP rule without required upload evidence. Their
next steps and the precise coverage limits are in the HTTP audit. Historical
checkpoints below retain their earlier counts and IDs.

## Implementation checkpoint: sweep sources and evidence roles

**67 rules moved** out of the legacy sweep leaf. The
[phase-four manifest](stealer-phase4-moves.csv) records final IDs, files, matcher
change status, and normalized-definition hashes. All 67 definitions first passed
a move-only comparison across the entire catalog. After the separate Node fix,
**66 retain their matcher bodies and effective settings**; one intentionally
requires both source and destination evidence. Seven names/descriptions were
clarified. No moved rule's severity, confidence, scope, or suppression changed.

The new `multi-source` leaf has **22 rules** whose required evidence identifies
independent datasets. `credential` has **15 rules** whose common target is
authentication material or stores, but whose alternatives do not require one
narrower store. Specific-store ownership takes precedence; required independent
sources take precedence over credential. This does not admit arbitrary ORs over
mail, screenshots, documents, and credentials. The new contracts in TAXONOMY.md
explain the tie-breaks and distinguish file bundles from identified sources.
`file` now has **62** rules, wallet **35**, and legacy sweep **13**.

Local credential collection moved to credential-access. Permission combinations,
secret-access wording, path pairs, and JSON-request helpers moved to their neutral
capabilities. File targeting and locale exclusion moved to collection and
anti-analysis respectively. Query-stage names now live beside their protocol
atoms. File-targeting/identity-set owns combinations of identified targets;
filter owns filename/extension selection. Placing the former beside filters
avoids an ancestor reference that would include the composite itself.

The Node rule previously had `needs: 2` over four source indicators and two
endpoint indicators. Both **endpoints alone** and **source paths alone** produced
a hostile finding. `credential::node-unix-secret-http-exfil` now requires one
source plus the `http/collect::node-collect-or-exfil-endpoint` helper. Both
source-plus-transfer controls still match, and both counterexamples now fail.
This is an intentional precision correction, not an undocumented move effect.
The helper adds one rule to the existing HTTP collect violator (**121 rules**);
it remains flagged and needs its transport audit. No exception was introduced.

The cumulative [ledger](stealer-source-dispositions.csv) records **303 implemented**
placements, **1 proposed**, and **12 review cases**, out of 316 original/audited
rules. All remaining 13 are sweep rules. The next cohort must resolve:

- Transport/request primitives, generic archive export, and collectors with no
  mandatory common data source; audit their over-cap HTTP receivers together.
- AppleScript target alternatives and the Go mail/credential alternatives;
  neither a browser/wallet label nor two mailbox stores establishes multi-source.
- Screenshot capture without export and Android permissions/WebView/Base64
  without a sufficiently specific capture/export claim. The Android rule needs
  a focused capability-versus-spyware counterexample before changing its logic.
- The Python `infostealer` aggregate, which overlaps acquisition/export indicators
  for the same sources; preserve its useful detection while correcting the claim.

Verification: **1,837/1,837 verdict fixtures**, **8/8 source-routing assertions**,
and normalized comparisons pass. Strict validation retains **70 issues**,
including **158 oversized directories**, with no new migration diagnostics.
The refreshed working-tree snapshot has **118,798 rules**, **4,375 excess rules**,
and 108 exact matcher-overlap groups covering 242 rules. The one-rule increase
is the independently required endpoint helper. Counts include unrelated
working-tree edits; these tests do not establish downstream ML equivalence.

## Implementation checkpoint: host-information split completed

Another **206 definitions moved** with normalized matcher bodies, defaults,
scope, confidence, criticality, and attack mappings preserved. The
[phase-three manifest](stealer-phase3-moves.csv) records the exact transitions
and definition hashes. Eleven rule names/descriptions were clarified where
they had claimed export, staging, or host information absent from their matcher.
The cumulative [ledger](stealer-source-dispositions.csv) now covers **316 rules**:
**236 implemented**, **38 proposed**, and **42 review**. Its `current_id` column
is authoritative for current placement; earlier manifests describe checkpoints.

The former 174-rule system-info/process-list/network-config cohort is completely
mapped. The retired process-list and network-config leaves have no rules, and
the system-info parent has no YAML or aliases. Its populated children are:

| Child | Rules | Source boundary |
|---|---:|---|
| identity | 30 | Host/account/device identifiers |
| platform | 5 | OS/runtime/execution environment |
| software | 1 | Installed-package inventory |
| process | 14 | Running-process inventory |
| network | 11 | Network configuration, addresses, connectivity, survey |
| profile | 85 | Host report spanning or leaving open multiple host domains |

No hardware-only leaf was manufactured: hardware evidence in the cohort either
identifies the victim or is part of a broader report. Profile is a known host-data
source, not a fallback for unknown sources; the updated TAXONOMY.md contract
distinguishes alternatives among host-information domains from alternatives
among unrelated theft targets.

The sibling/capability audit also reconciled User-Agent values versus transport
fingerprints and cloud-authentication records. User-Agent now has **85** rules.
RouterOS query primitives follow interfaces, routes, firewall queries, wireless
configuration, or host-profile/configuration capabilities. Their coordinated
network survey moved to discovery/network/enumeration. Discovery/system/profile
now has **77** rules. JSON Pointer escaping moved from schema-object to its
encoding technique; schema-object is back to **85**. No cap exemptions were
added. The pre-existing HTTP-upload violator gained one correctly classified
octet-stream export helper and still needs its own audit; it has 177 rules.

Both broad host-information consumers now use the system-info subtree instead
of counting the retired process/network directories separately. The backdoor
consumer retains the relocated status-message observation and coordinated
network-query composite. Bare RouterOS query primitives and notebook telemetry
no longer acquire an exfiltration/profile-source role from their former directory.
This changes source grouping intentionally: several host-inventory views are not
independent stolen datasets. All explicit references were rewritten; no new
broken-reference or leaf-placement error remains.

Verification: **206/206 definition comparisons**, **1,837/1,837 verdict fixtures**,
and **4/4 focused source-routing assertions** pass. The refreshed working-tree
audit reports **158 over-cap directories** and **4,374 excess rules**, down from
160 and 4,439. Strict validation remains red on 70 reported issues, including
those cap violations. The working tree also acquired an unrelated login-items
rule during this pass; counts and diagnostics include it. Do not interpret the
working-tree snapshot as an isolated commit or claim downstream ML equivalence.

The 80 remaining ledger proposals/reviews are the legacy sweep cohort. That
source audit, the remaining surveillance/input boundaries, and the other
catalog-wide violators are still unfinished. This checkpoint completes the
host-information split, not the overall migration goal.

## Implementation checkpoint: helpers and captured input

The next **30 rule moves are implemented**, after the six initial corrections.
The [move manifest](stealer-phase2-moves.csv) records the old/new IDs, current
files, and normalized-definition hashes. The disposition ledger now covers
**284 rules**: 30 implemented moves, 6 corrected placements, 164 proposals,
and 84 specific review cases. The earlier counts below describe the initial
audit, not the current work remaining.

- Sixteen rules left system-info. Telemetry settings, tracking uploads, schema
  fields, and encoding fragments now describe their capabilities. User/host
  collection, startup persistence, bot tracking, and an exfiltration encoding
  marker went to their corresponding objective homes. Two completed exporters
  now follow account-database and cloud-credential sources.
- All twelve phish rules were reconciled: seven completed exports moved to
  input; three local capture/redirect/dump composites moved to credential-input
  capture, one password-archive rule to archive staging, and one card-data dump
  to card-form capture. There is no rule-bearing phish leaf left.
- Two Go global-input exporters moved from surveillance to input. Host profiling
  and anti-debugging remain referenced context, not the source classification.

System-info now has **148 rules**, input **34**, account-db **37**, and cloud
**27**. Every receiving leaf is at or below 85. This does not finish the
system-info split: it remains 63 above cap. Surveillance still needs its
remaining capture-source audit.

Before writing, a normalized comparison covered all **118,796 rules** and their
effective defaults, allowing only the planned ID/reference translations.
Afterward, all 30 moved definitions were compared again, excluding descriptions
and local IDs but including matcher conditions, defaults, scope, confidence,
criticality, and attack mappings. No exact atomic-body duplicates were found
for this cohort. Four descriptions were clarified without changing evidence.
Soft validation passes **1,837/1,837 fixtures**. Strict validation reports the
same 69 entries as the preceding checkpoint; no new validation failure was
introduced. The catalog still has 160 over-cap directories, with 4,439 excess
rules.

The profiled-backdoor consumer retains its four applicable relocated JavaScript
observations through explicit references; incompatible file types are omitted.
Its other clauses and suppressions are unchanged. For Python infostealer,
turning the three applicable relocated helpers into separate `any` legs would
broaden proximity grouping and incorrectly count POST/telemetry/startup clues
as independent data sources. Those three clues deliberately no longer vote
toward its source threshold. Prompted-input exports now share the input source
directory. These are intentional source-counting corrections, not claims of
identical composite behavior. The helpers' own findings and direct consumers
remain intact. Other clauses and suppressions are unchanged.

The dedicated [source-routing regression check](../../scripts/check-stealer-source-routing.py)
scans two fixtures without executing them. A host-profile plus AWS/SSH/wallet
export still matches Python infostealer. A host-profile/telemetry example
matches both relocated telemetry observations but does not match infostealer.
All four finding assertions pass. Run it with
`python3 scripts/check-stealer-source-routing.py`. The broader source-equivalence
issue in `needs: 3` still requires review before the sweep migration is complete;
do not infer universal detection or ML-feature equivalence from these checks.

## Decision

Use one axis under `stealer`: the information probably acquired and exported.
The [placement contracts](../../TAXONOMY.md#stealer-directories-classify-the-acquired-information)
define the boundaries. This applies a simplicity and classification-rigor lens;
it does not claim to report Rob Pike's or Carl Linnaeus's opinions.

Keep named data stores such as browser, wallet, SSH, and keychain. Use the
specific store before a storage medium or transport. Treat a coherent host
report as one source, even when it includes identity, OS, processes, and
interfaces. Replace the qualifying portion of `sweep` with `multi-source` only
when independent target datasets are required. Do not rename the whole leaf.

`phish` and `surveillance` also mix axes. Phishing is how information is obtained;
surveillance is a purpose. Their export rules should follow the captured data.
For example, `go-input-surveillance-http-exfil` and its anti-debug wrapper now
live in input; host context does not change that source.
`python-discord-credential-exfiltration` likewise moved from phish to input.
Screen/audio/video capture should have source names rather than a surveillance
catch-all. Audit every rule and its helpers before materializing those splits.

## Rule-level audit

The [disposition ledger](stealer-source-dispositions.csv) covers **270 rules**:
158 originally in system-info, 85 in sweep, 20 in process-list, and 7 in
network-config. It records original full IDs and filenames so moves remain
traceable. Every immediate matcher body was inspected; transitive helper
verification remains explicitly pending where indicated.

- **6 corrected** placements, implemented in this pass.
- **173 proposed** destinations, requiring reference/default/duplicate checks
  before migration. A proposed destination is not a claim of completed migration.
- **91 review** dispositions with specific unresolved source, helper, or matcher
  questions. These must not be pushed into a miscellaneous/profile bucket.

The initial host-child proposals include 27 identity, 4 platform, 14 process,
10 network, and 63 profile rules. These are partial candidate counts, **not**
final leaf sizes. Hardware and software have meaningful contracts but their
candidates still need transitive review. Create only populated, defensible
children; do not add empty ranks for symmetry. If profile remains over 85,
revisit its admissions and duplicate bodies before adding another level.

## Corrections made now

Five rules moved from `sweep` to the existing `system-info` leaf:

- `browser-identity-network-profile-exfiltration`: client fingerprint and
  network/geolocation report, not browser secrets plus another dataset.
- `windows-domain-recon-http-exfil`: domain/network reconnaissance report.
- `recon-telegram-exfil`: host/network observations sent through Telegram;
  `needs: 2` does not require independent stolen datasets.
- `windows-recon-http-exfil` and `windows-recon-paste-exfil`: command-produced
  host reports, not multiple theft targets.

`jvm-process-profile-exfil` moved from process-list to system-info: its required
report contains `ENV`, `HOST`, `OS`, and `PROCS`. Its description now names the
combined host/process report. All six retain local IDs, matcher bodies, scopes,
defaults, criticalities, confidence, and attack mappings. The Telegram C2
consumer references the corrected ID.

The leaves now contain **164 system-info**, **80 sweep**, **19 process-list**,
and **7 network-config** rules. System-info is still over cap by 79; correcting
meaning is not a cap fix. Strict leaf-only organization is retained. No cap
exceptions or new intermediate directories were added.

## Concrete matcher problems and validator candidates

1. **A threshold can omit the defining source.**
   **Fixed in phase four:** the former `sweep::node-unix-secret-http-exfil`
   counted source and endpoint clues together. Two endpoints matched without
   credentials, and two credential sources matched without an endpoint. The
   moved rule now requires both roles, with positive and negative regressions.
   A future semantic validator could flag satisfying
   paths that omit a required source or transfer role. This requires explicit
   role/source contracts; directory spelling alone is not reliable enough for
   a hard error. Repairing the matcher is separate from preserving a rule
   during a move and needs positive and source-absent regression cases.
2. **Distinct traits are not distinct source classes.**
   Chrome and Firefox clues can satisfy a threshold while both describe browser
   data; AWS credentials and config can both describe cloud data. The Python
   `infostealer` also mixes credential-access and stealer references for the
   same stores. Directory conditions contribute their distinct matching member
   IDs to `needs`, not one vote per directory. Counting API calls, directory
   names, or findings cannot enforce multi-source semantics.
3. **A helper inherits neither its consumer's source nor its intent.**
   Sentry configuration, a `/api/data/` path, a user-agent, and encoding fragments
   formerly lived in system-info; phase three moved them to capability homes.
   For remaining helpers, use their own capability homes and
   leave source/transfer inference to consumers. Check target caps first:
   HTTP collect/upload and user-agent leaves are not spare capacity.
4. **Duplicate bodies and overlapping evidence are different checks.**
   Continue exact matcher-body consolidation with scope/default/suppression
   compatibility checks. Also consider warnings for duplicate or subsumed
   threshold legs and overlapping directory expansions. The two endpoint
   matchers above are different bodies: exact-duplicate detection would not
   catch their missing-source problem. Treat any new semantic warning as an
   audit aid until it has measured precision; do not warn on every one-child
   parent or infer poor organization from depth alone.

## Migration order and acceptance criteria

1. Resolve the ledger's source and transfer questions by tracing required
   helpers and all satisfying alternatives. Remove neutral helpers and
   collection-only rules from stealer; check for existing equivalent matchers
   before adding anything at the destination. Do not silently strengthen
   matchers to make the proposed taxonomy fit.
2. Finish the source map for **all** system-info rules and absorb the inventory
   portions of process-list and network-config. Move genuine secret/configuration
   theft to its data-store home. Only then replace the parent leaf with the
   populated identity/platform/hardware/software/process/network/profile leaves.
   All rules and aliases remain strictly at leaves.
3. Resolve sweep's single-source, alternative-source, and helper cases. Move
   the remainder to multi-source only after each rule requires independent
   datasets. Equivalent source-specific rules may replace OR aggregates, but
   treat that as a detection change with dedicated fixture checks.
4. Reconcile input/phish/surveillance by captured data; keep acquisition method
   in the referenced credential-access/collection rule. Review remaining sibling
   overlaps: process environment versus `.env` credential files; browser cookies
   versus standalone app tokens; device identity versus network inventory.
5. Recheck defaults, local and full references, directory expansions, cycles,
   identical matcher bodies, fixture verdicts, and leaf counts. Preserve a
   normalized before/after rule comparison. Search ignored YAML too: the loader
   includes files a default `rg` search can omit.

Two broad consumers require special attention during the split:
`sweep::infostealer` and
`command-and-control/backdoor/dispatch/profiled::host-profile-exfil-source`.
The corrected system-info membership now contributes five additional candidates
to their directory references. The process-to-system move remains in their
existing union. A future helper relocation or directory merge can change those
sets again, even with unchanged rule bodies. Fixture verdicts alone do not prove
feature equivalence; review expanded memberships and downstream ML features.

The work includes the focused audit, placement corrections, and the helper/input
migration above; it does not complete the system-info split or the catalog-wide
migration. Validation results and the
current measurements are recorded in [PLAN.md](PLAN.md).

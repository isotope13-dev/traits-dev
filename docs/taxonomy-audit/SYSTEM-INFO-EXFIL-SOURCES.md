# System-info exfiltration source audit

## Implementation checkpoint: browser locations and access mechanisms

The [browser-access audit](BROWSER-ACCESS-BOUNDARIES.md) records **95 moves**,
resolving two cap violations: Chromium **136 → 82**, multi-target **106 → 85**.
App-Bound Encryption and DevTools become sibling techniques, with no added depth.
Neutral paths, JSON fields, executable names and keyring references follow their
capabilities. All receivers remain strict leaves within 85.

The proof protects **205 definitions** and records **37 affected directory
references in 36 consumers**. Six consumer repairs retain relocated technique
alternatives. Two dead defanged-IP matchers are repaired explicitly; all other
moved matcher/settings semantics are preserved. **1,032 Boolean comparisons**
and **63 focused assertions** pass. All **1,841 corpus fixtures** pass with only
the unrelated shell-decoder regression isolated; live validation remains failing.
Strict validation reports **91 diagnostics**, including **147 over-cap leaves**.

The ledger has **1,248 implemented dispositions out of 1,251**, with three sweep
reviews. Remaining browser export, generic-capability and mixed-target rules are
listed in the audit; passing a cap is not a semantic certificate.

## Implementation checkpoint: keychain sources and local credential access

The [keychain audit](KEYCHAIN-SOURCE-BOUNDARIES.md) records **11 moves**:
five local observations leave export, and six classifiers follow their common
authentication-data source in `credential`. Keychain export has **11** rules;
credential export **33**. Every receiver remains a strict leaf within 85.
Matchers and settings are preserved. The Python collector explicitly retains
its former DPAPI source, with an unchanged eligible candidate set.

The proof protects **25 definitions**, and **16 affected directory references in
12 consumers** are reviewed. **59 focused assertions** pass. All **1,841 corpus
fixtures** pass in the documented temporary copy restoring only the unrelated
shell-decoder regression; the live tree still fails on PyAigis. Strict validation
retains **89 diagnostics** and the cap backlog stays at **149 directories**.
The ledger has **1,153 implemented dispositions out of 1,156**, with three sweep
reviews. Remaining weak transfer/store claims are recorded explicitly.

## Implementation checkpoint: mail sources and client operations

The [mail audit](MAIL-SOURCE-BOUNDARIES.md) records **89 moves**, reducing
email-harvest from 103 to **45**. Mailbox access, sending, address parsing, audit
records and account secrets now follow distinct subjects. Schema-object has
**77** rules after its own cleanup; every receiver is a strict leaf within 85.
Browser request-history export replaces mailbox reconnaissance in the 85-rule
browser leaf. No matcher or effective detection setting changed.

The proof protects **189 definitions**; the consumer report covers **72 changed
references in 66 consumers**. All **45 focused assertions** pass. The live corpus
has an unrelated pre-existing PyAigis shell-decoder regression. An isolated copy
restoring only that rule to its previous definition passes **1,841 fixtures**;
the repository rule remains unchanged. Strict validation retains **89 diagnostics**.
The audit records the isolation and outside edits explicitly.

The shared tree has **149 oversized directories**. The ledger contains **1,142
implemented dispositions out of 1,145**, with three sweep reviews. Contacts,
message-export claims, campaign audit provenance, and remaining browser/keychain
alternatives still need semantic review. The migration remains unfinished.

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


Latest checkpoint: [browser activity and instrumentation](ACTIVITY-TELEMETRY-BOUNDARIES.md)
resolves two collection cap violations through 113 moves. Host-information leaves
are unchanged. The cumulative ledger has **981 implemented dispositions out of
984**. Browser-export source reconciliation remains open; see the audit for the
current-tree versus isolated-validation distinction.

Latest checkpoint: [input sibling boundaries](INPUT-SIBLING-BOUNDARIES.md)
routes CSS and QNX input export by source and retires three misleading keylog
leaves. Host-information leaves are unchanged. The cumulative ledger has
**868 implemented placements out of 871**; the semantic backlog remains open.

Latest checkpoint: [keyboard and input boundaries](KEYLOG-INPUT-BOUNDARIES.md)
resolves one cap violation and routes keyboard export by source. Host-information
leaves are unchanged. The ledger has **834 implemented placements out of 837**;
that count does not imply the remaining capture classifiers are fully reviewed.

Latest checkpoint: [recording source boundaries](RECORDING-SOURCE-BOUNDARIES.md)
separates sound/camera exports, local acquisition, and neutral recording mechanics.
Host-information leaves are unchanged. The ledger has **634 implemented
placements out of 637**; unresolved capture/control rules remain documented.
Earlier checkpoints below retain their own counts.


Latest checkpoint: [capture source boundaries](CAPTURE-SOURCE-BOUNDARIES.md)
resolves two more cap violations and removes redundant screenshot depth. The
host-information leaves remain unchanged; screen/image exports follow their
sources. The cumulative ledger has **566 implemented dispositions out of 569**,
with three unresolved sweep cases. Earlier checkpoints below retain their counts.


Latest checkpoint: [HTTP capability boundaries](HTTP-CAPABILITY-BOUNDARIES.md)
resolves two more cap violations and leaves four sweep reviews. The six
host-information leaves remain; identity now contains 35 rules after five
source-defined reports moved out of HTTP collect. The provenance ledger has
385 implemented dispositions out of 389.


Latest follow-up: the [sweep implementation checkpoint](STEALER-SOURCE-PLAN.md)
records another 67 placements, the source/destination threshold repair, and
13 remaining sweep cases. The six host-information leaves remain unchanged.
The current cumulative ledger has 303 implemented placements out of 316.


## Current disposition: host reports are one source

The host-information split is now implemented. Its parent contains no rules;
identity has **30**, platform **5**, software **1**, process **14**, network
**11**, and profile **85**. Process-list and network-config are retired. See
the [current checkpoint](STEALER-SOURCE-PLAN.md) and
[206-rule manifest](stealer-phase3-moves.csv) for the full source map, receiving
capability audit, and verification. All counts below describe prior checkpoints.

The subsequent helper/input migration moves sixteen more rules out of
system-info, leaving **148** there. All twelve phish rules and two surveillance
input exporters have also been routed by their actual source/result. The
[implementation checkpoint](STEALER-SOURCE-PLAN.md) and
[30-rule manifest](stealer-phase2-moves.csv) record those moves, verification,
and the deliberate source-count correction with focused regression checks. Counts in the initial
correction account below are historical.

The [revised stealer plan](STEALER-SOURCE-PLAN.md) supersedes the host-profile
routing decisions below. Five report exports moved back from sweep to
system-info, and the JVM combined host/process report moved back from
process-list. Browser fingerprint, network, OS, account, and process attributes
can describe one coherent report; `needs: 2` or `needs: 3` does not establish
independent stolen datasets. The browser-plus-wallet Python profiler remains
in sweep pending the multi-source migration.

Current counts: system-info **164**, sweep **80**, process-list **19**, and
network-config **7**. The six corrections preserve matcher bodies and effective
settings; the Telegram C2 reference was updated. Soft validation passes
**1,837/1,837 fixtures**. Strict validation retains the same 69 reported entries
as the immediate pre-correction baseline, with two diagnostics following the
moved filename; 160 directories remain over cap. This is not a completed split.

The [270-rule disposition ledger](stealer-source-dispositions.csv) records
specific proposed destinations and unresolved matcher questions. The historical
tables below describe previous IDs, **not current canonical destinations**.
In particular, their claims that multiple host attributes require sweep are
withdrawn; see TAXONOMY.md's source contracts.

## Historical first-pass routing (superseded where noted above)

The oversized `objectives/exfiltration/stealer/system-info` leaf had 169 rules
in the initial 2026-09-28 working-tree audit. Six composites first moved to
existing source leaves, then five additional mixed-source composites moved to
the existing `stealer/sweep` leaf. After that pass, `system-info` has 158 rules (73 over
cap), `sweep` has 85, and `stealer/file` has 55:

- Go global keyboard state plus upload → `stealer/surveillance`. Its host
  profile is supporting context; the sensitive captured source is input.
- A debugger-evasion wrapper around that input exporter →
  `stealer/surveillance`. The wrapper adds anti-analysis evidence but retains
  the same captured source and transfer result.
- Browser identity, network-address profile, geolocation, and local-IP facts
  plus upload → `stealer/sweep`. The matcher requires multiple source classes,
  so it is not only a browser or host-profile export.
- JVM process-profile fields plus an exfiltration endpoint →
  `stealer/process-list`.
- Swift process inventory plus its HTTP collect endpoint →
  `stealer/process-list`.
- AppleScript environment credentials plus host identity and POST →
  `stealer/env`. The secret source takes precedence over host-profile context.
- Windows domain-controller discovery and local network configuration sent by
  HTTP → `stealer/sweep`. The matcher requires both domain and host-network
  evidence plus the transfer context.
- Python system profile plus browser and wallet sources sent over HTTP →
  `stealer/sweep`. Both browser and wallet source legs are required.
- PE/DLL reconnaissance sent through a Telegram bot → `stealer/sweep`. The
  rule requires at least two independent host/network source observations and
  bounds their proximity to the send operation.
- Windows command-line reconnaissance with at least three distinct inventory
  signals, sent over HTTP or to a paste service → `stealer/sweep`. Process,
  account, network-status, and system-profile sources are mixed by the required
  `needs: 3` matcher.

The sibling audit also removed rules that described file targeting or a single
file source from `stealer/sweep`:

- Sensitive-path filter aggregation and Node root-search targeting →
  `objectives/collection/file-targeting`; these describe source selection and
  acquisition capability, not a mandatory mixed-source sweep.
- libcurl plus sensitive-file targeting, macOS file-copy plus sensitive-file
  targeting and network context, and recursive sensitive-file traversal plus
  network context → `stealer/file`; all three point to one file-source class.

The moves preserve matcher bodies, scopes, criticalities, confidence, and
effective file/platform settings. Rule IDs were retained and repository
consumers updated. The browser/network sweep and subsequent mixed-source
migrations leave `sweep` at 85 rules. `system-info` now has 158 rules, 73 over
cap. Soft validation passes all **1,837/1,837 fixtures** after these moves.
Strict `make validate` reports no broken references or YAML errors from this
cohort; catalog-wide cap and policy errors remain.

| Previous ID | Canonical ID |
|---|---|
| `objectives/exfiltration/stealer/system-info::go-input-surveillance-http-exfil` | `objectives/exfiltration/stealer/surveillance::go-input-surveillance-http-exfil` |
| `objectives/exfiltration/stealer/system-info::go-anti-debug-input-profile-agent` | `objectives/exfiltration/stealer/surveillance::go-anti-debug-input-profile-agent` |
| `objectives/exfiltration/stealer/system-info::browser-identity-network-profile-exfiltration` | `objectives/exfiltration/stealer/sweep::browser-identity-network-profile-exfiltration` |
| `objectives/exfiltration/stealer/system-info::jvm-process-profile-exfil` | `objectives/exfiltration/stealer/process-list::jvm-process-profile-exfil` |
| `objectives/exfiltration/stealer/system-info::swift-inventory-http-exfil` | `objectives/exfiltration/stealer/process-list::swift-inventory-http-exfil` |
| `objectives/exfiltration/stealer/system-info::applescript-host-user-secret-exfil` | `objectives/exfiltration/stealer/env::applescript-host-user-secret-exfil` |
| `objectives/exfiltration/stealer/system-info::windows-domain-recon-http-exfil` | `objectives/exfiltration/stealer/sweep::windows-domain-recon-http-exfil` |
| `objectives/exfiltration/stealer/system-info::python-profiler` | `objectives/exfiltration/stealer/sweep::python-profiler` |
| `objectives/exfiltration/stealer/system-info::recon-telegram-exfil` | `objectives/exfiltration/stealer/sweep::recon-telegram-exfil` |
| `objectives/exfiltration/stealer/system-info::windows-recon-http-exfil` | `objectives/exfiltration/stealer/sweep::windows-recon-http-exfil` |
| `objectives/exfiltration/stealer/system-info::windows-recon-paste-exfil` | `objectives/exfiltration/stealer/sweep::windows-recon-paste-exfil` |

| Previous ID | Canonical ID |
|---|---|
| `objectives/exfiltration/stealer/sweep::sensitive-file-targeting` | `objectives/collection/file-targeting/filter::sensitive-file-targeting` |
| `objectives/exfiltration/stealer/sweep::node-sensitive-find-command` | `objectives/collection/file-targeting/command::node-sensitive-find-command` |
| `objectives/exfiltration/stealer/sweep::curl-with-file-targeting` | `objectives/exfiltration/stealer/file::curl-with-file-targeting` |
| `objectives/exfiltration/stealer/sweep::macos-file-copy-exfil` | `objectives/exfiltration/stealer/file::macos-file-copy-exfil` |
| `objectives/exfiltration/stealer/sweep::recursive-file-theft` | `objectives/exfiltration/stealer/file::recursive-file-theft` |

This is a first-pass source audit, not a complete reorganization. The
remaining system-info rules need a complete source map before any new child
leaves are defined; host/user/OS profile rules must not be split only by
language, operating system, or transport. Any path change still changes the
ML feature namespace and requires downstream evaluation.

# Browser records, storage, and remote export

The [13-rule manifest](browser-history-moves.csv) routes ten history/navigation
exports from collection to `stealer/browser`, local storage to its capability,
and two record/page observations to neutral capabilities. Three redundant
recognized-cookie wrappers and one mixed payload wrapper are retired; a neutral
tab-event host-reading helper is added. Contracts are in
[TAXONOMY.md](../../TAXONOMY.md).

Browser export now has **85 rules**, local browser activity **53**, and tracking
**45**. Every receiving directory is a strict leaf within 85. The pass adds no
hierarchy levels or exemptions. Its purpose is source precision, not another
cap reduction: the shared tree currently has **150 oversized directories**.
A separately added CFML webshell rule raised webshell/request to 86 during the
pass; the [pre-move drift record](browser-history-pre-move-drift.json) identifies
that addition and two other independent changes.

## Boundaries and deliberate refinements

Browser-owned browsing records, intercepted hosts, origins, page URLs and
referrers with probable remote delivery share the browser export home. The
client language and extension packaging do not decide the directory. Local
history acquisition accompanied only by an HTTP client remains collection:
`browser-history-telemetry` is renamed `browser-history-with-http-client` so it
does not claim a reporting channel that the matcher does not require.

The old local-staging helper accepted encryption/decryption or key import as
alternatives to storage. It now requires one of the existing local-storage
interfaces and is named `browser-local-storage-interfaces`. This deliberately
removes encryption-only eligibility from the storage-requiring classifiers.
The separate source-and-send classifier still recognizes the intercepted-host
export without asserting local storage. Storage interfaces are capability
clues, not proof of writes or runtime batching.

The payload helper mixed JSON serialization with request-body context and called
both upload. Its four consumers now state these alternatives directly, alongside
independent source and channel requirements. For the tab-event consumer, a
neutral host-reading helper groups the two existing tab alternatives, preserving
the required groups and the five-condition proximity threshold. No generic
serialization or body-context finding is itself filed as collection or theft.

Three recognized-cookie wrappers had no external exact consumers; their only
positive effect outside the wrapper chain was broad browser/stealer membership.
Their underlying cookie utilities, named software identities, and bundle facts
remain intact. Recognized documentation helpers no longer become theft evidence
merely because a file also mentions a Discord webhook.

## Verification and coverage limits

The move-only normalization proof protects **39 affected definitions**, preserving
all effective conditions, scope, confidence, criticality, exclusions, mappings,
and thresholds after the declared refinements. Four names/descriptions were
clarified; the additional unmoved collection rename is recorded in
[the label manifest](browser-history-labels.json). The full post-refinement
baseline has 118,815 rules, with no further drift during the migration proof.
The [consumer report](browser-history-directory-consumers.csv) compares against
the original pre-refinement catalog, including helper retirement: **25 affected
references in 25 consumers**.

The [refinement record](browser-history-refinements.json) preserves before/after
definitions. An exhaustive **8,192 Boolean comparison** check confirms that
factoring the payload and tab alternatives changes eligibility only where local
storage is intentionally required. This logical check does not prove spatial
matching equivalence by itself; positive nearby and negative distant tab
controls additionally exercise the retained proximity boundary.

All **1,841 corpus fixtures** pass with `validate --soft`, without exclusions.
The six new controls pass **16 assertions**: stored and encryption-only host
export, direct-body export without JSON, nearby/distant tab workflows, and a
recognized cookie helper. Existing activity and browser controls add 26 passing
assertions, for **42 across 15 controls**. Controls are scanned from temporary
paths and never executed. Strict `make validate` still fails with **89
diagnostics**, including the cap backlog.

## Remaining work

Follow-up: the [mail audit](MAIL-SOURCE-BOUNDARIES.md) completed the Google
mailbox and browser request-history routing listed below. The [keychain audit](KEYCHAIN-SOURCE-BOUNDARIES.md)
completed eleven further source moves; its unresolved classifiers remain open.

- Reconcile browser acquisition without a transfer, PyInstaller module
  co-occurrence, browser-or-Notes alternatives, and Google mailbox reconnaissance.
  The appropriate credential-browser and email-harvest receivers are themselves
  oversized; repair their taxonomy before adding rules to them.
- Route the browser request-history export still under HTTP report after the
  remaining browser leaf cleanup. Do not add a capacity exception or classify it
  by transport merely because the browser leaf is full.
- Review scheduled fingerprint reporting and the legacy “dormant surveillance”
  rule. An empty allowlist plus an index miss does not establish an early return.
- Audit keychain alternatives and the remaining monitor/collection siblings.
  This pass does not certify their source or intent claims.

The ledger has **1,054 implemented dispositions out of 1,057**, with three
sweep reviews. The ledger and cap count remain checkpoints of an unfinished
catalog migration.

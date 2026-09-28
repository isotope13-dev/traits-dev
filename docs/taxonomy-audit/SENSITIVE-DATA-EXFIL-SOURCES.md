# Sensitive-data source classifiers

The legacy `objectives/exfiltration/sensitive-data` leaf mixed source-specific
steal-and-send classifiers with components and broad cross-source summaries.
This pass applied its documented source-first rule to the classifiers whose
required source was explicit, without changing their matcher logic.

Six composites moved out of `sensitive-data`: JavaScript and Go environment
exports to `stealer/env`; JavaScript and Go sensitive-file exports to
`stealer/file`; and JavaScript and Go host-profile exports to
`stealer/system-info/profile`. Their conditions, local helper identities,
criticality, confidence, scope, suppressions, and effective defaults were
compared before and after. Internal references were made fully qualified where
their component remains in `sensitive-data`. The Go cross-source summary and
the HTTP transport aggregate now reference the relocated classifiers. Supply-
chain, developer-secret, account-database, and Slack control rules were updated
to the new canonical IDs. The broad PowerShell-history consumer still includes
the migrated behaviors through its existing `stealer/` parent reference.

Two neighboring source corrections clarify the `system-info` children. The
Swift exporter requires only a process inventory, so it moved from
`system-info/profile` to `system-info/process`. The browser/network profile
classifier requires both browser identity and a network/geo profile, so it
moved from `system-info/profile` to `stealer/multi-source`. This treats network
address and geo fields as one network-profile dataset, while browser identity
is an independent dataset. The taxonomy now records both tie-breaks.

Current counts are **119 combined rules** in `sensitive-data` (60 atomic, 59
composite), **61** in `stealer/env`, **69** in `stealer/file`, **85** in
`stealer/system-info/profile`, **15** in `stealer/system-info/process`, and
**40** in `stealer/multi-source`. All receiving leaves are at or below the
combined cap; the legacy source remains **34 rules over cap** and requires
further classification.

All **1,842 controlled corpus fixtures** pass after overlaying the changed
rules and consumers on the last passing controlled snapshot. The live strict
validator still fails on whole-catalog debt: **144 directories** exceed the
cap, and other taxonomy and matcher errors remain. It reported no broken
references for these moved rules. The current whole-tree audit is recorded in
[`snapshot-2026-09-28-post-sensitive-data-sources`](snapshot-2026-09-28-post-sensitive-data-sources/summary.json).

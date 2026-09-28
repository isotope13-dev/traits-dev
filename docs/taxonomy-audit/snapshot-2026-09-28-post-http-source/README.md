# Working-tree taxonomy snapshot after source routing and sweep audit

Generated 2026-09-28 after routing source-specific HTTP exfiltration composites
to `stealer/cloud`, `stealer/env`, `stealer/file`, `stealer/dev-secret`,
`stealer/keychain`, `stealer/ssh`, `stealer/surveillance`, `stealer/token`,
`stealer/wallet`, `stealer/sweep`, `stealer/appliance-config`, and the
process-list/surveillance source leaves. A sibling audit then routed file-only
targeting and exfiltration out of `sweep`, and moved three mandatory mixed-source
profiles from `system-info` into `sweep`. The base Git revision is
`13c9f9accd8c5a7a37cacfc76b05e33b6602221b`; this snapshot includes the dirty
working tree and the source moves.

The combined cap is 85 with no directory exemptions. The catalog contains
20,080 YAML files and 118,795 rules (79,323 atomic, 39,472 composite). It has
160 over-cap directories, 18,051 rules in those directories, and 4,451 rules
above the cap. There are 108 identical-matcher groups covering 242 rules to
review, not blindly merge. The tree has 60 directories at depth five and none
deeper. Soft validation passes all **1,837/1,837 fixtures**. See the adjacent
CSVs for the full audit data.

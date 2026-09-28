# Current taxonomy audit snapshot — 2026-09-28

This inventory measures the shared working tree with the uniform inclusive cap
of 100 atomic and composite rules per directory. It has no directory exemptions.

The catalog contains 20,737 YAML files, 118,806 rules (79,328 atomic and
39,478 composite), across 8,721 rule directories.
79 directories exceed the cap, containing 9,929 rules
and 2,029 rules of excess. The violations are in
78 `objectives` directories and
1 `well-known` directory. No rule directory
exceeds depth five. Sparse sibling review uses the 35-rule threshold.

Compared with the preceding 85-rule inventory, the count is 143 →
79 violating directories and 3,768 → 2,029
excess rules. The Electron ASAR sink reclassification also moves four unchanged
rules into their specific file-launch home. See [PLAN.md](../PLAN.md) and
[DROPPER-STAGING-ENCRYPTED.md](../DROPPER-STAGING-ENCRYPTED.md) for the cohort
review and the CSV files here for directory-level evidence.

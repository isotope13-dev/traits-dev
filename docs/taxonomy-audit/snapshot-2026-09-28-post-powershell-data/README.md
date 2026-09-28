# Working-tree taxonomy snapshot after PowerShell staging move

Generated 2026-09-28 with `scripts/audit-taxonomy.py` after moving five
PowerShell Base64/Deflate staging composites from encrypted to encoded staging.
The base Git revision is `13c9f9accd8c5a7a37cacfc76b05e33b6602221b`; the
snapshot includes the dirty working tree and this taxonomy migration.

The combined cap is 85 with no directory exemptions. The catalog contains
20,060 YAML files and 118,794 rules (79,323 atomic, 39,471 composite). It has
160 over-cap directories, 18,085 rules in those directories, and 4,485 rules
above the cap. There are 108 identical-matcher groups covering 242 rules; they
are review candidates, not automatic merge instructions. The tree has 60
directories at depth five and none deeper. Soft validation passes all
**1,837/1,837 fixtures**. See the adjacent CSVs for the full structural,
oversize, reference-impact, sibling, and matcher-overlap data.

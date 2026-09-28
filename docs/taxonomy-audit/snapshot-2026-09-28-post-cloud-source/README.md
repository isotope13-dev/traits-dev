# Working-tree taxonomy snapshot after cloud-source move

Generated 2026-09-28 after moving the AWS credential HTTP-exfiltration rule to
its source category and updating its source-distribution consumer. The base Git
revision is `13c9f9accd8c5a7a37cacfc76b05e33b6602221b`; this snapshot includes
the dirty working tree and the migration.

The combined cap is 85 with no directory exemptions. The catalog contains
20,061 YAML files and 118,794 rules (79,323 atomic, 39,471 composite). It has
160 over-cap directories, 18,084 rules in those directories, and 4,484 rules
above the cap. There are 108 identical-matcher groups covering 242 rules to
review, not blindly merge. The tree has 60 directories at depth five and none
deeper. Soft validation passes all **1,837/1,837 fixtures**. See the adjacent
CSVs for the complete audit data.

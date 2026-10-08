These fixtures model configuration staging and CSS-to-PHP handler routing described in the LevelBlue NetScaler exploitation article:
https://www.levelblue.com/blogs/spiderlabs-blog/citrix-netscaler-cve-2026-88771-observed-exploitation-artifacts-and-hunt-indicators

`stage.sh` is a synthesized post-exploitation sequence, not a recovered payload. `archive.py` carries the archive command in Python; `archive-ifs.sh` uses the reported whitespace substitution. `backup.sh`, `static.conf`, and `dynamic.conf` are near misses for public staging or disguised PHP routing. Do not execute the attack fixtures.

Expected new findings: stage.sh matches config-copy-webroot and apache-css-location-php-handler; archive.py matches config-archive-webroot; archive-ifs.sh matches config-archive-webroot-ifs. Backup and ordinary handler controls must match none of these rules.

Full-tree scanning and validation are blocked by pre-existing trait/engine incompatibilities; these expectations have not been verified.

Regression controls for benign TollGate version drift and GitHub frontend assets.

- openwrt-hidden.sh: root-cron hidden-tmp-payload composite must match.
- openwrt-benign.sh: ordinary service enablement plus crontab must not match.
- trait-positive.js: DNR redirect, OAuth client ID, JSON action field, and exact
  createHash API name must match. The external DNR URL intentionally also
  exercises the pre-existing extension redirect composite.
- trait-negative.js: router redirect and analytics client ID remain neutral;
  the ternary action string and createHashRouter message must not become
  JSON command-field or hashing API findings.
- encoded-url-positive.js: a Base64 HTTPS URL must match encoded-https-url.
- encoded-url-negative.js: a plain HTTPS URL beside an unrelated Unicode escape
  must not match encoded-https-url.

The release Makefile diff against v0.6.0-alpha1 adds a version-placeholder
substitution and comments. Existing service enablement and the crontab path
are unchanged. Other shipped changes are version checks, CI, and documentation.
GitHub assets fetched from the unchanged CDK link are website dependencies,
not newly introduced TollGate package dependencies.

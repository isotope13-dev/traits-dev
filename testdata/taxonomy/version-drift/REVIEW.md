Version drift triage

Compared registry archives groonga-query-log 1.7.9 -> 1.8.0 and wandb
0.22.2 -> 0.22.3. Both are BENIGN.

Groonga changes dictionary type normalization, stops forcing JSON output,
and adds corresponding tests/news/version changes. The flagged regression
runner is byte-identical. It reads bounded schema/data/index/query-log globs,
starts the requested Groonga versions and compares responses. No encryption
or extortion is present. Replace the input-name string heuristic with a
recursive glob call capability under fs/search; update its ransomware consumers.
Ruby call facts lose the receiver, so the AST matcher binds receiver and glob.

W&B adds Arrow v18.4.1 for Parquet run-history reading. aes.go implements
Parquet AES-GCM/CTR encryption/decryption and footer authentication with
caller-supplied keys/AAD, not victim file traversal or key ransom. Move the
trailer/ciphertext vocabulary atoms and their filtered union into crypto/cipher,
remove unsupported ransom/encryption mappings, and keep the objective consumer.

sender.py and Bubblezone's Makefile are byte-identical to 0.22.2.
_sync_spell is guarded by SPELL_RUN_URL and sends one selected access token
plus the run URL to Spell with a two-second timeout; no whole-environment
collection occurs. The coarse payload-flow event establishes environment-derived
HTTP body values, not theft. Retain suspicious severity for unknown transfers. Move it and the Python-scoped wrapper to request/body
with a narrow selected-token Spell exchange exception; update all exact consumers. Hook/exfiltration composites retain
additional intent evidence.

The Makefile's explicit license target streams a license-header script into
Bash. This is genuinely unusual remote execution, retained as the sole
suspicious observation, relocated into shell/pipeline with its matcher and
exclusions. Remove the illegal objective-tier exclusion from the capability.
Restrict scope to makefile so quoted shell pipelines in source are not recipes.

No new leaves were introduced. Exact YAML consumers and fixture expectations
were updated; broad legacy ancestor selectors were reviewed and retain their
remaining members. Fixtures pair required content with near misses: inert glob
text/nonrecursive calls, footer text without ciphertext, saved downloads without
a shell pipeline, and environment reads that do not feed the request body.

The text matcher accepts leading recipe whitespace because analyzers normalize
tabs differently. The download command remains anchored at a line start.

Remove the broad test-harness exclusion from the pipeline atom: a test path
does not negate an executable download recipe, and should not hide it.

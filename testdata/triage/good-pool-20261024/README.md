Review of 94 artifacts from `/var/tmp/hopper-triage/good`, 2026-10-24.

`audit.json` records each hash, likely intent, evidence, limitations, initial and final high findings, and the reviewed destination. Five are hostile: three Toga versions with default global agent-content export, a patched executable carrying an encrypted PE infector, and a customized low-visibility ScreenConnect installer. Six ambiguous samples belong in purgatory. The remaining 83 meet the good-pool limit of zero hostile and at most one suspicious finding.

The ScreenConnect decision follows the user's explicit dataset policy: product identity is suspicious by default; any nondefault signal is hostile. This policy is recorded in `screenconnect-policy.yaml`; it does not establish whether every customized installation in other environments is abusive.

Toga's installer calls `reportTelemetryEnv` at `package/scripts/install.js:776`, before its postinstall return. `applyTelemetryEnv` at line 315 rewrites global Claude settings; exporter configuration begins at line 279 and prompt/response/tool logging at lines 284–286. The behavior is an opt-out global content collection change, despite an ordinary team-harness product description. [Claude's monitoring documentation](https://code.claude.com/docs/en/monitoring-usage) explains that prompt/response content is normally excluded and that the selected flags enable it. Static analysis establishes configuration and reachability, not observed delivery of conversations. No collector token is reproduced here.

`native-infector/recovery.json` records decoded stages, mapper activation and DLL hash. The accompanying loader/method disassembly supports executable infection, drive autorun, update and persistence intent. `metamorphic_graft.rs` is the exact bounded static decoder integrated into the sibling cleave checkout; `cleave-integration.patch` records its registration and PE-analyzer integration. The decoder discovers code-relative parameters and validates the recovered DLL; it does not execute the specimen or pin a sample hash/key. Atomscan was rebuilt with that local cleave dependency using an isolated source copy, leaving its original manifest/lock unchanged.

Two protected executables remain unresolved after section/resource/import inspection and bounded CPU traces. Their final payloads were not fully unpacked. They are not treated as benign, and their purgatory decisions do not claim complete behavioral recovery. The Rifaien self-mutating upload loop, token-session replay helper, promotional browser extension and encoded reviewer-refusal notice also remain outside good training.

`remote-hostile-copies.json` records the requested transfer eligibility: a confirmed hostile sample qualifies when its initial scan had zero hostile traits. Only ScreenConnect qualifies in this batch; its remote SHA-256 was verified. The three Toga archives already had two hostile traits, and the infector host already had one, although that original signature was misleading and was replaced by recovered-payload evidence.

Checks:

- `check.py`: 21 static positive/negative controls, including each individual ScreenConnect visibility setting, default/custom relays and bound HTTP upload provenance.
- `check-activation.py <inventory.json>`: nine checks covering inert PE entries, changed entry/TLS/export near misses, active versus fixture workflow injection and a standalone PHP webshell. This uses local triage fixtures without executing them.
- `rustc --edition=2024 --test metamorphic_graft.rs -o /tmp/graft-tests`: four decoder tests. For the real recovered DLL and six corruption/extent near misses, set `CLEAVE_GRAFT_FIXTURE` to the original infector host and `CLEAVE_GRAFT_DLL` to the recovered packed DLL before running the test binary.
- `make validate`: complete repository fixture/performance suite; result saved in `validate-final.log`.

Full scratch scans, member inventories and static JS call-site inventories remain under `/tmp/triage-good-20261024`. `source-audit-manifest.json` records their hashes and locations. Atomscan warned that model feature version 18 predates version 21; reviewed intent and cold trait evidence determine these labels rather than the older model's probability.

`apply-pools.py` defaults to a dry run. `pool-plan.json` and `pool-moves.json` record hopper's responses. Hostile originals are additionally relocated under `/tmp/triage/misplaced-bad` after validation and hash verification. No commit is created by this review.

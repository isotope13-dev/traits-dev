Triage these vetted-benign false positive(s):
- /data/gauntlet-fp/c72442978ab8131794ef56ddd053d1b6b7838eb7957a902a34447284d83d0c2b/v1.2.0.zip — hostile: 1, suspicious: 0
  - H objectives/command-and-control/backdoor/shell/socket::posix-bind-shell-source — C source bind shell (bind+dup2+shell)
    members: /data/gauntlet-fp/c72442978ab8131794ef56ddd053d1b6b7838eb7957a902a34447284d83d0c2b/v1.2.0.zip!!github.com/checkpoint-restore/checkpointctl@v1.2.0/test/piggie/piggie.c

- /data/gauntlet-fp/c3a0b880adbe64dc4bcb68f93016916ab5b55ae43fd227115287bf80257d92dc/OBS-Studio-32.2.2-Windows-x64-Installer.exe — hostile: 0, suspicious: 2
  - S objectives/anti-static/obfuscation/payload/section::encrypted-data-section — Encrypted data section (very high)
    members: /data/gauntlet-fp/c3a0b880adbe64dc4bcb68f93016916ab5b55ae43fd227115287bf80257d92dc/OBS-Studio-32.2.2-Windows-x64-Installer.exe!!obs-plugins/64bit/obs-filters.dll
  - S objectives/discovery/host/system::windows-binary-stealer-recon — Windows binary victim profiling cluster
    members: /data/gauntlet-fp/c3a0b880adbe64dc4bcb68f93016916ab5b55ae43fd227115287bf80257d92dc/OBS-Studio-32.2.2-Windows-x64-Installer.exe!!obs-plugins/64bit/libcef.dll

- /data/gauntlet-fp/c4585a41f2ca4578f1615cb1388451c6dccbc2bcb03c1f8ee12b88ed6c89f2f5/sattyamjjain-agent-audit-kit-v0.3.89.tar.gz — hostile: 0, suspicious: 2
  - S objectives/exfiltration/http/query::url-command-substitution — URL embeds command substitution output
    members: /data/gauntlet-fp/c4585a41f2ca4578f1615cb1388451c6dccbc2bcb03c1f8ee12b88ed6c89f2f5/sattyamjjain-agent-audit-kit-v0.3.89.tar.gz!!agent-audit-kit-0.3.89/tests/test_llm_sql_rce.py
  - S objectives/supply-chain/install-hook/package/manifest::dependency-confusion-candidate — Stable-version install-hook package lacks provenance
    members: /data/gauntlet-fp/c4585a41f2ca4578f1615cb1388451c6dccbc2bcb03c1f8ee12b88ed6c89f2f5/sattyamjjain-agent-audit-kit-v0.3.89.tar.gz!!agent-audit-kit-0.3.89/examples/vulnerable-configs/10-supply-chain-risks/package.json


Success: 0 hostile findings and normally 0 suspicious findings. At most 1 suspicious finding is
acceptable, and only when it accurately describes genuinely unusual behavior in the benign sample.
Every remaining finding must accurately describe observed behavior, regardless of its criticality.

Use the findings above as the initial worklist. Repair traits containing any misleading or
inaccurate findings, regardless of criticality, following the relevant parts of TAXONOMY.md and
RULES.md.
Use `cleave facts` and `cleave test-rules` on representative extracted files; facts are faster
and more reliable than text searches. Extract archives once and group equivalent `src`/`dist`,
`.js`/`.ts`, architecture, and bundled-library variants.

Make the smallest defensible change and preserve useful detection. Base exceptions on strong,
generalizable evidence. Give traits specific IDs and descriptions that tell an analyst what
behavior was observed and why it matters.

Make all planned changes before measuring each sample:

  /data/rectifier/bin/cleave analyze <sample>

Run this at least once after editing and before finishing. Inspect findings at every criticality,
not only those that affect the QA count gate. If the success counts are not met or any finding is
misleading or inaccurate, make the next complete set of changes before analyzing again.

Before finishing, you MUST run:

  make -C /data/rectifier/traits-dev validate CLEAVE=/data/rectifier/bin/cleave

Fix every error and rerun until it passes. Rectifier performs the authoritative rescan.

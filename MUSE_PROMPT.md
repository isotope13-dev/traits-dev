Triage these vetted-benign false positive(s):
- /data/gauntlet-fp/7e6d7bc77517883fef116b0ef49880b810373ee46cb54bbb026a9811ea2abdd2/unsloth-2026.8.19-py3-none-any.whl — hostile: 1, suspicious: 0
  - H objectives/exfiltration/dns/lookup::python-identity-label-dns-beacon — Host identity leaves as DNS query labels
    members: /data/gauntlet-fp/7e6d7bc77517883fef116b0ef49880b810373ee46cb54bbb026a9811ea2abdd2/unsloth-2026.8.19-py3-none-any.whl!!studio/backend/run.py


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

Restore detection on these verified supply-chain compromise(s). Each one is a real, confirmed
attack that the current traits do not call hostile:
- /data/fixed/0c3a27281ff4847cd8900d0016c96475ae2a4c7d815d8ef74b262c721196cd71/multi-cloud-metadata-sweep--2026-03-06-b10connoisseur-v0.18.0.zip — hostile: 0, suspicious: 3, ml.lvl: 279
  - S objectives/anti-static/pack/archive::encrypted-wheel-metadata — Encrypted wheel metadata conceals runtime package
  - S objectives/privilege-escalation/exploit/vulnerabilities::dirtypipe-detected — DirtyPipe exploit detected
    members: /data/fixed/0c3a27281ff4847cd8900d0016c96475ae2a4c7d815d8ef74b262c721196cd71/multi-cloud-metadata-sweep--2026-03-06-b10connoisseur-v0.18.0.zip!!tmp/tmpn8ueh377/b10connoisseur/b10connoisseur/core.py
  - S objectives/supply-chain/hidden-payload/package::package-archive-build-tree-leak — Package archive retains a temporary build tree

Success: at least 1 hostile finding on the sample itself — the root record, not only on a member
inside it. Every finding you add must accurately describe behavior you actually observed in the
sample, at the criticality it deserves.

Any findings listed above are the near misses: traits that fired below hostile on this sample are
usually where the missing detection belongs, and raising or extending one you can justify is
preferable to writing a new trait beside it. A sample with nothing listed needs the mechanism
identified first.

Identify what the sample actually does before changing any trait. Use `cleave facts` and
`cleave test-rules` on the extracted members; facts are faster and more reliable than text
searches. Extract archives once and group equivalent `src`/`dist`, `.js`/`.ts`, architecture, and
bundled-library variants. Name the concrete mechanism — the install hook, the network callback,
the exec, the encoded payload, the path it writes — and write the trait against that.

A second corpus of manually vetted BENIGN files gates this same tag, and every trait you touch is
measured against it in the same run. A trait broad enough to fire on ordinary software will be
caught there and sent back as a false positive, which spends another repair round and lands
nothing. Prefer a trait that names the attack's specific behavior over one that widens an existing
rule until it happens to cover this sample. Give traits specific IDs and descriptions that tell an
analyst what behavior was observed and why it matters.

Make all planned changes before measuring each sample:

  /data/rectifier/bin/cleave analyze <sample>

Run this at least once after editing and before finishing. Confirm the hostile finding is on the
sample's own record. Inspect findings at every criticality, not only the one that affects the QA
gate. If the success criteria are not met or any finding is misleading or inaccurate, make the next
complete set of changes before analyzing again.

Before finishing, you MUST run:

  make -C /data/rectifier/traits-dev validate CLEAVE=/data/rectifier/bin/cleave

Fix every error and rerun until it passes. Rectifier performs the authoritative rescan.

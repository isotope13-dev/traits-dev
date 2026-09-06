Restore detection on these verified supply-chain compromise(s). Each one is a real, confirmed
attack that the current traits do not call hostile:
- /data/fixed/15127c199c91534a8bd6154a9c51972103c7ae2a77a359d6b16d7d1dd4bc8801/monkey-org-dsniff-fragroute__fragroute-1.2-RECONSTRUCTED.tar.gz — hostile: 0, suspicious: 0, ml.lvl: -1
  (nothing at suspicious or above)

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

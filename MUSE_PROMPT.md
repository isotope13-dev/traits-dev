Triage these vetted-benign false positive(s):
- /data/gauntlet-fp/b59fb7c1f1cde1a5832b32ed234aa716d27998b0ca447351088a60df1d666962/clamav-0.3.1.gem — hostile: 1, suspicious: 0
  - H third_party/SigBase/Office/Autoopen/Macro — Detects an Microsoft Office file that contains the AutoOpen Macro function
    members: /data/gauntlet-fp/b59fb7c1f1cde1a5832b32ed234aa716d27998b0ca447351088a60df1d666962/clamav-0.3.1.gem!!data.tar.gz, /data/gauntlet-fp/b59fb7c1f1cde1a5832b32ed234aa716d27998b0ca447351088a60df1d666962/clamav-0.3.1.gem!!data.tar.gz!!spec/clamav-testfiles/program.doc, /data/gauntlet-fp/b59fb7c1f1cde1a5832b32ed234aa716d27998b0ca447351088a60df1d666962/clamav-0.3.1.gem!!data.tar.gz!!spec/clamav-testfiles/Программа.doc


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

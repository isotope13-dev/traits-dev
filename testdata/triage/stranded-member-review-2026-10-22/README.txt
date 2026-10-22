Individually reviewed 51 extracted members: 51 MALICIOUS.

review.json records identities, SHA-256, traced behavior, evidence limits,
per-member hostile/suspicious coverage and before/after model output.
judgment-notes.txt contains the exact one-line marker notes for commit bodies.
relocations.json records the 24 semantics-preserving rule relocations.
ancestor-consumers.json records broader identity selectors affected by placement.
Run: python3 testdata/triage/stranded-member-review-2026-10-22/check.py

No hostile/suspicious coverage was lost in member or archive comparisons.
27 members remain classifier-benign and reflective VNC classifier-suspicious.
Coercion/dumping-only payloads are not given invented distinct attack traits.
Fat Mach-O low-level fact variability was isolated using original/current
rules under the same extraction settings; normalized findings then matched.
The repository-wide make validate is the final verification step.

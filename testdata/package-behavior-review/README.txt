Package behavior review: Operato layout, ENS contracts and Ultralytics.

Review evidence, per-member scan deltas, provenance and verdict reasoning are
in review.json. Original/recovered artifacts and full scans remain in the
scratch/review-bad directory recorded there, with forager provenance sidecars.

Run controls without executing specimen code:
  python3 testdata/package-behavior-review/check.py <scratch-directory>

The check copies controls out of testdata, preserving real testing suppressors
in production rules, then performs static atomscan analysis with no updates,
remote classification, or reference following. The existing recursion controls
and original Grabvy ransomware fixture are reused. 26 assertions cases passed.

Shared-rule consumers were inspected before edits. Moves retain confidence,
criticality, scope and matchers except the documented Solidity/header exclusion,
.sct pathname repair, function-definition matcher, and Snap7 context requirement.
No accurate execution, networking, encoding, crypto or chmod finding was demoted.

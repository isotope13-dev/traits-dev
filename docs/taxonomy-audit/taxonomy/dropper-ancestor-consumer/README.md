# Dropper ancestor consumer audit

`windows-embedded-security-hosts-sinkhole` had an `any` reference to the entire
`objectives/command-and-control/dropper` subtree. Directory references match
nested rules, so migrating rules out of installer staging removed them from
that alternative even when exact consumers had been updated.

The installer and NSIS staging migration snapshots identify 91 moved members.
All 91 now appear as exact alternatives in the hosts-file rule; their current
IDs are recorded in `installer-members.json`. This preserves those members
without including unrelated new rules from their destination directories. Each
ID was checked against the worktree, and none is an exception-class rule (the
runtime excludes exceptions from positive directory expansion).

This is not a complete audit of the ancestor reference. A name-only comparison
against the current Git HEAD found 3,581 historical dropper rules, of which 845
no longer have the same full ID. Among those, 81 have a single current rule with
the same short name, and 764 have no same-name candidate. These counts are an
inventory, not a verified mapping: renamed, deliberately removed, duplicated,
and already-covered rules need individual review before they are restored.

A second pass compared unique same-name candidates with their Git HEAD
counterparts by rule kind, parsed match conditions, exclusions, inherited file
types and platforms, scope, proximity, bounds, and confidence. Sixty-six of
81 candidates matched those fields; 22 were already covered, and 44 more exact
alternatives were restored. The local short-name dependency in the matching
editor bootstrap moved with its referenced rule. The old and current IDs are
recorded in `same-name-strict-moves.json`.

This field comparison does not prove that transitive dependencies or referenced
directory membership are unchanged. Fifteen same-name candidates differ in the
compared fields, and the 764 rules without a same-name candidate still require
review. They were not restored on name or structural similarity alone.

A subsequent pass restored 34 behavior-oriented alternatives. Twenty-eight are
unique full-field predicate matches for current hostile PE objectives, including
renamed rules. Six are same-name composites whose changed legs were traced to
matching renamed predicates; the seven managed method-name observations and
the delayed system-binary removal leg were checked individually. These mappings
are recorded in `behavior-moves.json`.

The search also found 397 further unique-fingerprint candidates. Those include
single text fragments, generic metadata and product references; matching an old
predicate is not enough to make each of them appropriate positive evidence for
a hostile hosts-file rule. They are recorded in
`fingerprint-candidates-pending.json` for subject-by-subject review. Seven
uncovered same-name candidates also have changes such as removed path or size
filters and were not treated as equivalent. As above, equality of the stored
fields does not establish equivalence of every transitive dependency.

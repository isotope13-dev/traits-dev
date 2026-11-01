# Literal fragment and environment staging review

The generic fragment leaf held 68 traits, while 35 fragment observations and
alternatives remained in the legacy encoded-environment leaf. The fragment
neighborhood now distinguishes `single` snippets from `sequence` observations
that require several separated pieces. These describe the evidence shape; they
do not claim that a fragment was executed, joined or decoded. The leaves contain
59 and 44 traits respectively.

The 35 legacy observations and the remaining generic `Load` symbol have moved,
leaving the encoded-environment leaf empty. Isolated strings such as `sMana`,
`voke` and `YPAsS` are components, while complete, distinctive command-fragment
sequences retain their supported notable or suspicious severity. Their
consumers retain the same matching predicates. The broad staged-loader consumer
is scoped to Python and does not acquire these JavaScript/text fragments.

[moves.json](moves.json) records original rules, defaults, destinations and
severity changes. Earlier audit scripts follow these moves while preserving
their historical snapshots. Run
`uv run docs/taxonomy-audit/taxonomy/literal-fragment-review/check-moves.py`
to verify the split, references and retired leaf, and see the
[action-token review](../action-token-review/README.md) for the generic symbol.

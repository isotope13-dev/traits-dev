# Padding token migration

The legacy `metadata/file/padding` leaf held one rule that observes the text
`PADDINGXXPADDING`. The token alone does not establish a filler span, linker
operation, or packer identity. It moved unchanged to
`metadata/file/profile/token-shape::paddingxxpadding-filler`; all ten exact YAML
consumers were updated, and no legacy YAML references remain.

The fixtures are copies of the existing synthetic PE
`testdata/notable/generated/fallout-current-review/qualified-name.exe`, with
the token or a different near-miss string appended. A Cleave scan reported the
moved rule for `positive.exe` and did not report it for `negative.exe`.
The existing manifest exclusion remains part of the rule; this pair does not
test that exclusion.

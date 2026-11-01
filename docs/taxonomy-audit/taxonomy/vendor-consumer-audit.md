# Legacy binary-vendor consumer audit

`metadata/binary/vendor/` has 55 YAML directory references. A first pass
found only a subset because its output was truncated; reviewing the complete
set revealed additional exclusions and downgrades throughout the taxonomy.
The attempted moves of the Python Software Foundation, GitHub and Digital
River string observations were reverted so those directory consumers retain
their current coverage.

Before moving these observations, review every directory consumer by rule,
file type, scope and purpose. Replace only the observations that actually
serve its claim; adding the whole destination directory would broaden it.
Some existing vendor-name downgrades may be unsound because a bare name is not
verified ownership. Any narrowing should be recorded and tested as an
intentional detection change rather than hidden inside a placement move.

The previous focused synthetic PE probes confirmed each individual company
string could be recognized after a placement-only move, with close string
near misses. They do not establish that the 55 consumers remain equivalent.

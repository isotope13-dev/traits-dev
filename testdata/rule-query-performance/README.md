Run `python3 testdata/rule-query-performance/check.py [cleave]` from the repository.

The controls cover all six credential field orders, intervening properties,
selector tables, nested and separate objects, string-doubling assignments and
near misses, runtime JavaScript/TypeScript imports, and erased import types.
The checker also runs the existing nine static-table controls.
Shell controls retain exact executable names, quoting, flag combinations, and
input-redirection exclusions for the environment-filter performance repair.

`testdata/performance/wide-source-queries.js` retains the original 2,760-string
array from the bundled web asset in
`testdata/benign/aui-agent-builder-0.4.16.tgz.xz`, with its source member and
SHA-256 recorded in the fixture. Wide credential properties and repeated
declaration/loop siblings exercise the other combinatorial query shapes.
The original archive remains a full-bundle performance control for validation.

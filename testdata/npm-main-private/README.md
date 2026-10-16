Private manifests are not published-package traversal risks
==========================================================

`npm-main-parent-entrypoint` fired on a `private: true` monorepo package
whose `main` climbs to the shared `dist/` build output. A private manifest
never reaches a registry, so the published-package traversal risk the rule
describes does not apply; `metadata/package/publishing::is-private` now
suppresses it. (A dead `npm-main-bindings-node` suppression entry, whose
exact `bindings/node` match can never coincide with the `..` traversal
matcher, was removed in the same edit to stay within the suppression
budget.)

Run `python3 testdata/npm-main-private/check.py <scratch-directory>`.
`negative/package.json` (private, parent main) must not report
`npm-main-parent-entrypoint`; `positive/package.json` (published shape,
parent main) must still report it.

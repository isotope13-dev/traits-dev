Declaration-parent regression controls
======================================

`micro-behaviors/data/decode/xor::aliased-charcode-xor-rebuild` must match
`var`, `let`, and `const` in JavaScript and TypeScript, plus JavaScript
`using` and `await using`, including comments between keywords and names. It must not match `different-callee.js` or
`not-xor.js`. The original and narrowed queries agree on all twelve files.

These files are static-analysis fixtures; they are not executed.

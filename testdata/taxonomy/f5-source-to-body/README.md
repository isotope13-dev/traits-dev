# F5 source-to-body precision candidate

This worktree is isolated at the recorded HEAD. The candidate closes source/sink co-occurrence gaps without changing existing source atoms.

`package-credential-store-audit-upload` retains its multi-store gate, requires an HTTP POST, and requires either a database query result to flow through `JSON.stringify` into the `fetch` options argument or Cleave's existing `file-http-body-flow` finding. The new DB flow atom is in `micro-behaviors/communications/http/request/credential-body-flow/`; the existing file flow atom is reused rather than duplicated.

`npm-detached-env-launch-token-exfil` retains detached spawn, copied environment, and HTTPS POST requirements. Its body gate requires either a tree-sitter match for a `const` initialized from `process.env.NPM_TOKEN` whose same identifier is a shorthand field inside `JSON.stringify` passed to `req.end`, or a `.npmrc` `readFileSync` return value reaching `req.end` directly or through `JSON.stringify`. The tree-sitter form is intentionally narrow: it does not claim general JavaScript taint tracking or cover aliases/transforms outside that local structure.

`cases.json` covers the matching hostile patterns and decoupled, no-send, single-source, no-token, no-detached, comment-only, overwritten-variable, and npmrc decoupling controls. Full validator and 13 focused cases passed before the current corpus rerun.

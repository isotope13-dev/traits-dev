# JavaScript temp-environment evidence is a capability

`js-process-env-temp-reference` was a JavaScript-specific atom in the dropper
`execute-download` directory. It matched only `process.env.TEMP`, which
describes reading a temp environment variable, not downloading or executing a
payload. The generic `micro-behaviors/os/env/read::temp-environment-variable-read`
already covers `TEMP`/`TMP` access; its type scope now includes JavaScript and
TypeScript. The Node downloader composite uses that canonical capability ID.

This removes a language-specific atom from the objective leaf and shares one
behavior across source languages. The shared rule retains its existing
confidence; its matcher also recognizes the equivalent `TMP` and generic
environment-access forms. Full fixture validation checks that the Node
download/launch objective remains visible.

# @pierre/diffs 1.6.0 version-drift review

Verdict: **BENIGN**. The sample is a browser file/diff rendering library with
optional React bindings and syntax-highlighting workers. The new detection
comes from embedding WASM in a portable worker and its source map, not from
an install hook or an injected loader.

## Release comparison

Downloaded the preceding stable release and the immediately preceding beta
without executing package scripts:

- [1.5.2](https://registry.npmjs.org/@pierre/diffs/-/diffs-1.5.2.tgz),
  SHA256 `91dc0ad27542f9058f8a941597d60e7b6dced78ffc6fe275b951913a816c7645`.
- [1.6.0-beta.1](https://registry.npmjs.org/@pierre/diffs/-/diffs-1.6.0-beta.1.tgz),
  SHA256 `4dbfbc27348893d7aec27a17eba92fb08be00e66f6f020aaf65e2d2c403ebe55`.
- Submitted 1.6.0: SHA256
  `7512b3b0cb06792783dc5321a8629a8b069f05b66cca7871f79a7e4401957fee`.

All three archives match the SHA512 integrity values in the npm registry.
This corroborates provenance; it is not itself a benignness test.

1.5.2's portable worker has 119 source-map sources and dynamically imports
`wasm-B9ZqxnKj.js`. That chunk already decodes the 466,610-byte Oniguruma
module, SHA256
`fd885c2d12e5951e59d761ebd4a006e06254b1491fd6f530c92b69fb4d8d77d9`.
1.6.0 bundles those identical bytes directly in the worker. Its source map
has 296 sources. The second embedded module is the new 175,601-byte Highlights
lexer, SHA256
`851716bef2009f7f5fece3208ffdc4b92bdb9a7806badf4f25f0619cbc988916`.
These bytes also match `dist/highlights.wasm.mjs` in the separately fetched
[@pierre/highlights 0.1.3](https://registry.npmjs.org/@pierre/highlights/-/highlights-0.1.3.tgz).
Both embedded modules are identical in the preceding 1.6.0 beta.

Relative to 1.5.2, the manifest adds `@pierre/highlights: 0.1.3`, removes
`@shikijs/transformers`, and adds the two worker entrypoints to `sideEffects`.
The submitted manifest and 1.5.2 both have empty scripts objects. The beta
has a prepublishOnly build command. The beta/current portable worker maps
have the same ordered 296 sources; only six source contents differ:
constants, hastToHtml, tokenStyle, renderTokenLines, tokensToHtml, and
shared_highlighter. Those differences add an immutable empty annotation array, documentation and
style-cache defaults, and checking of loaded languages; the WASM and its
host interfaces are unchanged.

## Execution and effects

Read the manifest, published JavaScript and recovered source-map sources;
ran atomscan and cleave facts on the submitted archive and facts on the map
and extracted loader; decoded both Base64 literals and inspected WASM imports,
exports, and representative instructions with rizin and a section parser.
JSON/Unicode escaping in sourcesContent exposes the original JavaScript; it
does not add an execution stage. The actual minified bundle uses backticks
for its Base64 strings, whereas sourcesContent preserves double quotes.

`worker.ts` accepts initialize, set-render-options, file, and diff messages,
selects a highlighter, renders token/HTML trees and posts results (optionally
transferring compact token buffers) to its parent. The portable browser entry
decodes the WASM into Uint8Array bytes, constructs WebAssembly.Module and
initializes the highlighter. The Highlights host writes the supplied source
text into linear memory, invokes highlight/highlightStream, and reads token
records/HTML bytes. The lexer exports also support incremental document edits.
Its only imports are env.is_id_start and env.is_id_continue, implemented as
Unicode character-class tests in JavaScript.

Oniguruma exports scanner creation/freeing, next-match searches and memory
helpers. Its imports are emscripten_memcpy_big, emscripten_resize_heap,
emscripten_get_now and wasi_snapshot_preview1.fd_write. The JavaScript host
implements these as typed-array copying, memory growth, a clock, and a no-op
fd_write returning zero. These imported functions provide no network or
process-launch interface. The observed byte decoding and WASM activation
serve the advertised syntax-highlighting purpose.

The decisive evidence is the unchanged existing regex engine and separately
published new lexer, their bounded host interfaces, and their callers' actual
rendering behavior. No particular deployment was supplied. Large source files
produce some cleave flow-analysis gaps; source recovery and manual path review
were used instead of treating those gaps or scan scores as verdict evidence.

## Trait correction and controls

Removed the unreferenced atomic `atob-large` from the install-hook objective:
its matcher required only an atob-shaped string of at least 100 Base64
characters, with no lifecycle, concealment, or hostile sink evidence.
Do not replace this with a WASM-prefix allowlist or source-map-wide exclusion.
The observation already has canonical notable detections under
micro-behaviors/data/decode/base64, including embedded-atob-call-text for data
and js-atob-call-or-callback for JavaScript. Generic decoding alone must not
supply the broad install-hook selector's evidence in windsurf-mcp-injection,
the only ancestor-directory consumer found; no exact atob-large consumers exist.

`cases.json` records five independently scanned controls: long quoted data,
long backtick data, a source map carrying the quoted data, a minimal WASM
loader, and decoded JavaScript passed to eval. The first four retain notable
Base64/WASM observations with no suspicious or hostile findings. The last
retains the existing suspicious eval-atob finding, demonstrating that the
change preserves the decode-versus-execution distinction. These controls
contain only generated data, an empty WASM module and harmless console source.

Final verification: atomscan was rerun on the submitted archive. A complete
local cleave JSON scan reports 968 analyzed records and zero suspicious
or hostile findings, with notable Base64 and WASM observations retained.
All five focused controls passed their required/forbidden trait assertions.

solc 0.4.20 release-drift review
==============================

Verdict: BENIGN. The sample SHA-256 is
53040359f131d8cfccde2210fd29c561da20c9de38b059eb47685821c519abde.
It is byte-identical to https://registry.npmjs.org/solc/-/solc-0.4.20.tgz.
The comparison release is 0.4.19, fetched from the same registry; its archive
SHA-256 is feae64d17510fc08eb40ae6cdb07b15dd8a6c94196b7ecd6a59c23f280d21b44.
Both downloads agree with their registry SHA-1 records.

Decisive diff evidence
---------------------

Both embedded compiler files are byte-identical to the corresponding upstream
builds in https://github.com/ethereum/solc-bin/tree/gh-pages/bin:

| Release/build | soljson.js SHA-256 | Bytes |
| --- | --- | ---: |
| 0.4.19+commit.c4cbbb05 | 61071ed96228ac7b88ccb9c6eeae9a152daf6c06f19bb15b45b7ed22226a27e8 | 7336570 |
| 0.4.20+commit.3155dd80 | 2dbd26d82bae11c5469c5a4cc6c04d96e8fa0d6c3e1a98052133840794ed28f6 | 7604173 |

The first 27,365 compiler bytes agree. The first difference is the static heap
size, followed by generated C++ initialization and compiled functions.
Decoding all numeric `allocate([...])` initializers yields 249,126 and 274,437
bytes of compiler data, respectively: license text, version identifiers, parser
tokens and diagnostics, including experimental ABI-encoder diagnostics.

Outside the compiler, the CLI, entry point, ABI helper and license are unchanged.
The changes add semver conversion, correct UTF-8 callback allocation, support
legacy linker names, fix old compiler output translation, and add coverage tools
and documentation. Runtime dependencies and the prepublish command are unchanged.
The HTTPS remote-version loader and require-from-string activation are unchanged.

Execution-path review
---------------------

`index.js` loads soljson and passes it to `setupMethods`. The wrapper marshals
source/JSON to the asm.js heap through cwrap/ccall, calls the exported compiler,
and parses its output. Import callbacks copy caller-provided contents/errors
back into that heap. `run()` initializes C++ globals; the distributed module
exports compiler functions. Its globalEval stub throws because dynamic execution
is disabled. The separate loadRemoteVersion method, only when called, downloads
a caller-selected compiler from the documented solc-bin host and loads its source.
The CLI reads requested sources and writes requested ABI/bytecode output files.

The raw HTTP helpers in the runtime accept caller-supplied URLs; browser resource,
event and media helpers are Emscripten runtime support. No credential collection,
covert endpoint, persistence or unrelated startup payload was found.

Both soljson versions were evaluated in JavaScriptCore without host filesystem or
network bridges. Both reported the expected version, compiled a pure `answer()`
contract returning 42 to a 374-character creation bytecode and matching ABI, and
returned ParserError for invalid Solidity.

Detection corrections and controls
----------------------------------

Fresh scans with the pre-edit rules flag AST depth in BOTH releases, despite the
queue's earlier clean result. The current release reaches depth 1000 inside
`Yja` (bytes 6190252–6951583); its path contains 227 blocks, 226 if statements,
224 do statements, 208 else clauses and 101 labels. This is ordinary generated
control-flow lowering. Reuse the existing Emscripten asm.js observation in the
recognized deep-source exception; retain detection on unattributed deep code.

The second false positive is new in 0.4.20: the old hex regex treats repeated
`wab,wab,...` function-table identifiers as encoded bytes. Require a quoted run
of w-prefixed byte pairs and place that artifact fact in metadata/file/encoding.
Move the associated percent-decoding composite to micro-behaviors/data/decode/url
at notable: proximity establishes co-occurrence, and decoding alone proves no
hostile behavior. Exact consumers were updated. Ancestor objective selectors
intentionally no longer count an encoded string or ordinary decoding as evasion.

Run `python3 testdata/taxonomy/solc-emscripten/check.py --scratch <control-dir>`.
Use a directory outside testdata/tests, since those paths suppress the depth rule.
Seven cases cover generated and unattributed deep code, function-table identifiers,
quoted contiguous/spaced hex strings, decoding co-occurrence, and short strings.
Full release rescans must have zero suspicious or hostile findings.

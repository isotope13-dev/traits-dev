quicktype 17.0.6: BENIGN

Identification and decisive release evidence
-------------------------------------------
quicktype generates types and JSON serialization code from JSON, JSON Schema,
GraphQL and TypeScript. The supplied npm archive SHA256 is
  a07f2d16059bd14b49e9f5e4068245ccddb4bc3b69a6cd157e396a8deceb2eb1
Its SHA512 integrity matches registry.npmjs.org/quicktype, version 17.0.6.
Fetched the immediately preceding release from:
  https://registry.npmjs.org/quicktype/-/quicktype-17.0.5.tgz
Registry publish times: 17.0.5 = 2023-01-09T19:41:26.093Z;
17.0.6 = 2023-01-10T01:13:58.323Z.

Only three archive members differ: package.json (version number only),
dist/quicktype-core/language/CPlusPlus.js, and its CPlusPlus.d.ts declaration.
The renderer removes msbuildPermissive, moves generated class and enum
converters into user namespaces, specializes nlohmann::adl_serializer for
maps and variants, and separates forward declarations from implementations.
These are generated C++ correctness changes. There are no added entrypoints,
install scripts, dependency changes, downloads or execution sinks.

Both releases contain IDENTICAL EncodedMarkovChain.js and .d.ts files, and
identical decoder, loader and consumer modules. Rescanning 17.0.5 with the
current scanner reproduces the same gzip alerts. The queue's claim that
this encoding appeared only in the newer release is not borne out by the
archive diff.

Reverse engineering
-------------------
EncodedMarkovChain.js only sets the CommonJS module flag and exports one
constant; its .d.ts counterpart declares the same constant string value.
The Base64 string decodes to 148193 gzip bytes, which inflate to 1873926
bytes of JSON. Decoded JSON SHA256:
  639ba5cb4cf454f81b0c0a6e0735bd57be8103f5fc024cffa6b7a85f4ddb63d4
The complete object is a depth-3 Markov trie: 3101 count/arr nodes, each with
128 entries; 75172 positive integer leaves and 318656 null slots. Recursively
verified every node and leaf, allowed keys, array widths, depth, and leaf-node
count sums. There are no script strings or executable payloads in this data.

Execution path:
rewrites/InferMaps.js shouldBeMap -> nameProbability -> MarkovChain.load ->
JSON.parse(Support.inflateBase64(encodedMarkovChain)). Support decodes using
js-base64.Base64.atob and pako.inflate(..., {to: "string"}). MarkovChain.evaluate
uses character-indexed trie counts to compute name probabilities. InferMaps
uses the scores to distinguish ordinary object property names from map keys.
The blob is parsed as data, never evaluated, loaded as a module, or launched.
The CLI's optional build-markov-chain path trains a replacement numeric model
from an explicitly selected local input file. This is normal code-generation
support data, not concealment of hostile behavior.

Trait corrections
-----------------
* Exclude all-null/all-true/all-false spans from comma-delimited-word-run;
  exclusion is per matched span, so a real word list beside an array survives.
* Add a notable pako inflater call that binds the receiver to require("pako").
  A library import, method reference, or a different object's inflate method
  does not satisfy it. The scanner's flow producer supports this relationship
  in named functions; unsupported anonymous-function flow can remain opaque.
* Move js-high-encoded-string-ratio unchanged from the closed data-blob leaf
  to metadata/file/profile/string-population. Retain threshold, size gate,
  severity, platforms, formats and HTML exclusion. Update its two exact
  consumers; no source/destination ancestor directory selector consumes it.
* Tighten SCP to a command literal with arguments, IRC LIST to channel or wire
  framing syntax, Claude stream-json to an actual command/output-format flag,
  and yacc to a generation banner. Bare acronym/enum/dependency names do not
  establish those behaviors or build provenance.
* Require the KVMKVMKVM vendor identifier instead of ambiguous bare "kvm"
  (also keyboard/video/mouse); keep other hypervisor-name alternatives.
* Rename the Math.random assignment observation for the seed/key/mnemonic
  names it actually matches. It does not establish a wallet secret. Keep its
  matcher/severity and update the wallet-context consumer.
* Move generic Namespace member-call syntax from COM to metadata/lang/source/
  syntax, preserving its matcher, types, Windows scope and notable severity.
  Its COM extraction consumer still requires the Shell.Application ProgID.
* Move npm --ignore-scripts command text from shell launch to package-manager
  installation; update the exact consumer and remove inherited T1059. Generic
  shell/execution selectors intentionally lose this non-launch evidence.
* Move pip-install literal text from well-known IDE identity to the neutral
  os/package-manager/install subject, preserving types, platforms, matcher,
  severity and exclusion. The IDE bootstrap exception references the new ID.
  Ancestor well-known directory selectors intentionally stop treating a
  generic pip command reference as IDE identity or a broad suppressor.

Engine limitation
-----------------
The remaining single distinct suspicious trait is the engine-generated
binary/embedded/base64-gz, repeated on the two constants and decoded layers.
embedded_code_detector.rs assigns suspicious and T1027.009 solely from
Base64 and gzip magic, then creates synthetic carrier records with no YAML
fact evaluation. The existing builtin-* YAML hook cannot remove those records
using file-local context. This behavior and limitation are also documented
in testdata/taxonomy/collector-esc-assets and testdata/triage/freebsd-trillian-drift.
No package-name exclusion or ineffective hook was added. A neutral gzip format
observation analogous to the engine's ZIP handling requires an analyzer fix;
the unsupported concealment inference cannot be corrected entirely in YAML.
The sample has no hostile traits. Its verdict is independent of this alert.

Verification
------------
Run python3 testdata/quicktype-version-drift/check.py [cleave-path].
Controls cover null/boolean arrays, real word lists beside arrays, receiver
provenance, inflater-plus-eval, ratio scope/threshold preservation, vocabulary
near misses and genuine command/COM/banner forms. The evidence and full
before/after scans are in the task scratch/quicktype-review directory.
Repository verification: make validate (run as the final task action).

Final results: 24 focused controls passed. Final atomscan and structured scans
confirm the corrected observations, no word-list false positive, zero hostile
traits, and one distinct engine-generated suspicious gzip trait.

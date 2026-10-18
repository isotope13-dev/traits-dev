# jstransform 11.0.1: BENIGN

The supplied npm tarball has SHA-256
`e9b075c7140b4d4b9d6653d9f317113c4c2441eb1838150a98e0556e7e982f8e`.
It is byte-identical to the tarball fetched from
https://registry.npmjs.org/jstransform/-/jstransform-11.0.1.tgz;
both fetched releases also match their registry SHA-1 digests.
The preceding release is
https://registry.npmjs.org/jstransform/-/jstransform-11.0.0.tgz
(SHA-256 `8ac2ca3bcdc359410b99cf341e99a8702b804a964b8bd1bda3a43e782b9808c4`).

The complete extracted-tree diff changes only `package.json`'s version and
`src/simple.js`: `transformOptions.fileName` becomes `transformOptions.filename`
in the inline-source-map call. The latter fixes the filename passed to an
existing source-map encoder. Dependencies and lifecycle scripts are unchanged.
There is no added payload or network, process-launch or credential-access path.
The flagged `visitors/index.js` is identical in both versions, and 11.0.0 also
fires under the current rules. The queue's historical clean scan is therefore
not evidence of a behavioral addition.

`getAllVisitors` and `getVisitorsBySet` walk a readable transform-name order,
look up arrays of visitor functions imported from local modules, and concatenate
those arrays. The selected functions pass to `jstransform.transform`; its walker
checks each visitor's `.test` against AST nodes and invokes the first matching
transform. It returns transformed source and optional source-map data. There is
no string decoding or eval sink in the flagged dispatcher. The package's test
suite evaluates transformed snippets to check their semantics. Its explicit
base64 operation serializes JSON into a `sourceMappingURL` data URI.

## Trait dispositions and scope

- Remove the suspicious `js-array-remap-nested-concat` atom: its assignment
  regex only recognized ordinary indexed concatenation. Its sole exact
  consumer was `js-index-remap-array-reconstruction`.
- Move the overlapping notable `js-nested-array-concat` from
  `micro-behaviors/data/control-flow/analysis` to
  `micro-behaviors/data/collection/array::js-nested-index-concat`. The source
  file contained only this rule, and there were no exact consumers. Its matcher,
  JavaScript scope, platforms, confidence and notable severity are retained;
  the arbitrary 50 KB ceiling is removed. The description states syntax rather
  than promising a receiver type or payload reconstruction.
- Reference that canonical collection observation from the encoded-remap
  objective. Its required hex-escaped array, eval and numeric-index evidence
  remain. The old atom's four exclusions move to this sole objective consumer.
  The neutral observation remains visible in build and VM code. Whitespace and
  non-assignment concat forms now satisfy the concat leg, including above
  50 KB; encoding and eval remain independently required. The objective's
  description states co-occurrence, not proven flow.
- Ancestor-selector audit found the broad anti-static string consumer in
  `objectives/anti-analysis/debugger-detect/check/traits.yaml`; losing ordinary
  concat as objective evidence there is intentional. No directory selectors
  consume the old analysis leaf or the collection destination/ancestors.
- The other anti-static finding in this sample matched `['gam' + 'ma']` in a
  comment illustrating computed-property compilation. Move that text matcher
  unchanged to `metadata/lang/source/syntax::js-split-member-access-text` and
  name it as a text reference. Keep its file types, platforms, confidence,
  notable severity and exclusions, but remove the unsupported obfuscation
  mappings. Comments and quoted examples are accurately reported as syntax
  references, not executable property access or concealment. All four exact
  consumers now reference the metadata fact and retain their other context
  gates. Ancestor objective selectors intentionally lose this neutral text
  observation. The source-text destination has no rule-bearing descendants.

## Focused controls

Run `python3 testdata/triage/jstransform-version-drift/verify.py <scratch-dir>`.
It scans ordinary and large dispatchers, a single-index near miss, encoded
remapping with and without eval, ordinary concat beside eval, executable
two/three-fragment property names (also TypeScript and embedded HTML), comments,
quoted examples, excluded built-in members and variable-based computed access.
Comments and quoted examples must retain the metadata reference without the
retired objective finding. The encoded-remap objective stays suspicious, and
the neutral concat and source-text reference stay notable.

Executed results: all 15 focused controls passed. The final `atomscan` and
JSON scan of the supplied package completed; its 70 report entries contain
zero suspicious or hostile findings and zero objective findings. The dispatcher
retains its notable collection observation, and the computed-property example
retains its notable syntax reference.

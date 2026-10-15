# @8wave/ai-elements 0.118.0 triage

Submitted SHA-256:
`3145ea06af426fb2324b2dd2a7832185b30bff54bc8cb07c589b1711c49954d6`.

Disposition: benign. The archive contains 268 JavaScript bundles, 244 source
maps, 278 TypeScript declarations, 20 WOFF2 fonts, CSS, documentation and the
package manifest. It has no install lifecycle script or native executable.
The source maps expose 875 distinct source paths, including repeated copies
of dependencies between the web-component and Vue distributions.

The conspicuous digit strings in `dist-vue/_chunks/dist-DLs-FvuY.js:2396`
are CodeMirror view's Unicode bidirectional-text character-class tables:

- `LowTypes`: 248 digits indexed by code points U+0000 through U+00F7.
- `ArabicTypes`: 250 digits indexed by code points U+0600 through U+06F9.

The source map names the original `dec`, `LowTypes`, `ArabicTypes`, and
`charType` routines. `dec` converts each digit to `1 << digit`; `charType`
looks up that mask to determine text direction. These strings never become
source code or shell commands. The preceding compact base-36 table describes
grapheme boundaries. The large BigInt strings in the Zod bundles are signed
and unsigned 64-bit validation limits: -9223372036854775808,
9223372036854775807, and 18446744073709551615. Other long numeric substrings
occur in floating-point drawing/geospatial constants and browser identifiers.

Reviewed package entry points, source-map implementations, network calls,
dynamic-code uses, numeric constants and scan findings. Chat and attachment
requests use the configured backend; authentication uses better-auth.
OpenTelemetry instruments browser fetch/document events and masks URLs before
export. Its widget initialization is gated by build configuration. Third-party
dynamic-code references belong to schema compilation and editor syntax
handling. No hidden payload execution or credential theft was identified.
No package code was executed. `cleave facts` was collected for the manifest,
CodeMirror bundle, Zod bundle, and chatbot API client; the source maps were
used to inspect the original implementations rather than trusting scan labels.

The existing `metadata/lang/encoded/hex::long-hex-string-literal` matcher
mistook the decimal character tables for hexadecimal encoding. It now uses
string literals explicitly and filters all-decimal matches individually.
A decimal string elsewhere in a file cannot suppress a real hex string.
The threshold, criticality, ID, placement, and all objective consumers remain
unchanged. Decoder-backed detection remains separate from this shape signal.

Controls cover decimal tables, genuine hex, both kinds in the same file
in either order across JavaScript/Python, a short literal, invalid hex,
comment-only hex, and a numeric BigInt literal.

Validation: `python3 testdata/triage/8wave-ai-elements-0.118.0/check.py
--cleave ../cleave/target/release/cleave` passes all six controls;
`make validate` passes the full fixture suite.

The final atomscan run covers 844 analysis units and emits zero suspicious
or hostile traits. The decimal tables no longer emit the long-hex finding.
`result.json` records the scan summary and model output; its raw general
model probability remains high (0.884), while the npm model is 0.021 and
both report class 0. These model scores do not establish malicious behavior.

Hopper disposition completed: incoming -> good/mislabeled-unknown.
The submitted local archive was moved to
`/tmp/triage/misplaced-good/@8wave-ai-elements-0.118.0.tgz`.

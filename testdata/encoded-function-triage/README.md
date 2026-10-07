# Encoded function triage controls

`function.js` contains a Base64 function definition and must match
`metadata/lang/encoded/base64::base64-script-function-definition` at notable.
`prose.js` and `unencoded.js` must not match that trait.

The matcher moved unchanged from the obfuscation objective. Exclusions for
builds, tests, source maps, and data URIs were removed: those contexts still
contain encoded source and the neutral observation should remain visible.
The admitted legacy `metadata/lang/encoded/base64` leaf is used because the
engine rejects the documented `metadata/file/encoding` destination; migration
to the latter is held until validator admission.

The one-line dropper heuristic and its ASAR derivative were retired. Line
metrics plus encoding and execution or generic writes do not establish a
payload, data flow, obfuscation, or hostile intent. Their constituents remain
visible in the neutral capability and metadata tiers. The Python pth derivative
was redundant with `objectives/persistence/login/python-pth::encoded-pth-startup-loader`,
which independently requires pth writes, Base64 decoding, and exec.

Exact YAML consumers of the Base64 function matcher were updated. Ancestor
selectors of the old obfuscation home intentionally lose this neutral leg;
selectors of the new metadata home gain it. No detection depends on a sample
name or on an allowlist for Certifier or CyberStrikeAI.

The existing one-line encoded-write fixture now asserts Base64 decoding and
executable-mode writing directly. Its score floor changes from 160 to 120
(observed 123) because the removed hostile heuristic inflated the score.
Its pre-existing independent stager finding and hostile-count expectation
are unchanged; this triage does not broaden that rule or endorse its intent
inference.

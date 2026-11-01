# Encrypted staging review

The legacy encrypted staging directory had 84 traits. This review moves 19 of
them to their actual subjects, leaving 65. Python bytecode reconstruction and
`.pyc` writing is executable preparation, so it moves to
`objectives/execution/staging/reconstruct`; the broad staged-loader consumer
explicitly retains it. Path literals, source identifiers and incomplete
cryptography observations move to the corresponding path, naming and profile
categories. A `payload.enc` reference does not by itself establish encryption,
and a function name does not establish that the named function was called.
Three PowerShell XOR/hex transforms move to `micro-behaviors/data/decode/xor`.

Creating the reconstruction category also required reviewing the old parent
rules. The EVM reconstruction rule moves there; the two HTML, hex, file and
Run-key co-occurrence rules move to encoding profiles because their predicates
lack an executable or activation operation. The profiles retain suspicious
severity while describing the evidence they require. A coherent combination of
operations can support a likely behavioral conclusion without proof of data
flow; isolated names and references need a more modest description.

The XOR decoder directory now has 77 traits. Some pre-existing rules describe
direction-neutral transforms rather than decoding; those need a subsequent
review alongside the 77-trait `data/encoding/xor` directory. Moving them into
that already crowded directory without reorganizing its siblings would merely
transfer the crowding. No directory cap changed during this review.

Run `uv run docs/taxonomy-audit/taxonomy/encrypted-staging-review/check-moves.py`
to check the 22 moves, effective defaults and destination counts.

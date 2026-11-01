# XOR keying review

The XOR encoding and decoder leaves each contained 77 traits, close to the
review threshold. The encoding leaf is now divided by evidence of keying
mechanism: `fixed-key` (9), `cyclic-key` (13), `evolving-operand` (16) and
`unspecified-key` (39). The last category covers transformations whose keying
mechanism is not established, rather than assuming encryption or decoding.

Fourteen decoder traits described direction-neutral XOR operations or buffer
transforms. They moved to the appropriate encoding leaf or `data/bitwise`;
the decoder leaf now contains 63 traits. Nine other isolated expressions,
including collection mapping and PowerShell XOR observations, also moved from
encoding to bitwise because they do not establish a buffer-wide encoding. The
bitwise leaf contains 67 traits. Generic operations no longer carry inherited
T1140 deobfuscation tags; their consumers can still identify decoding when
additional reconstruction context supports it.

The 91-entry [moves.json](moves.json) records the original rules, defaults,
destinations and identifiers. Exact YAML references were updated; there were
no directory consumers of the old encoding leaf. Run
`uv run docs/taxonomy-audit/taxonomy/xor-keying-review/check-moves.py` to
check effective definitions, changed references and directory populations.

# Compression boundary controls

The gzip read and write specimens both call `gzip.open`, without calling
`gzip.compress` or `gzip.decompress`. Both must match the legacy gzip API
aggregate; a plain file read must not. This demonstrates why that aggregate's
description cannot claim reading, and why stream mode must not be guessed during
placement. The specimens are scanned, never executed.

These three controls are separate from the existing DeflateStream-only C# control
in `../decompression/codec-only.cs`. Batch 011 uses all four to check its two
description corrections. The engine filters the redundant gzip aggregate from
emitted reports; its raw matcher result is asserted separately. No absent emitted
finding counts as a positive report assertion.

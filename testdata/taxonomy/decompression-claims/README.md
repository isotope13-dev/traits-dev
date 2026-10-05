# Dynamic decompression claim controls

These Python sources are analyzed, never executed. All three produce the same
`__import__.decompress` symbol in the current extractor. Only `dynamic-zlib.py`
identifies zlib; bz2 and an unknown module are negative controls for that claim.
Batch 010 accepts the corresponding correction. All three inputs are now included
in the main decompression case file and `make validate`.

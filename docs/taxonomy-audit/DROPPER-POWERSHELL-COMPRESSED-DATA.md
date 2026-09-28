# PowerShell decode/decompression staging is encoded, not encrypted

Five composites in `dropper/staging/encrypted/powershell-data.yaml` required
Base64 decoding and/or Deflate decompression evidence, plus script-obfuscation
signals in the stronger variants. None required encryption evidence, and none
established an activation sink. They therefore belong in
`dropper/staging/encoded/`, under the existing rule for reconstructed or
decoded embedded payloads without an established sink.

The five composite IDs moved unchanged to
`dropper/staging/encoded/powershell-data.yaml`. Their matcher conditions,
defaults, scopes, criticality, confidence, descriptions, and attack mappings
are preserved. No other rule referenced these IDs. The move keeps them
available as staging features while removing the unsupported encrypted
classification. The remaining rules in `powershell-data.yaml` stay under
review: AES/image-decryption chains retain encryption evidence; HTTP/image
retrieval, string-obfuscation, and culture-derived-key observations need
separate placement decisions rather than a bulk move.

The destination remains below the 85-rule cap after the move. A synthetic
generic-data sample matched the compressed-Base64 and Deflate/stream-reader
composites at their new path. Full soft validation passes **1,837/1,837
fixtures**. Strict validation still has the pre-existing catalog-wide issues;
the refreshed audit records the post-migration counts.

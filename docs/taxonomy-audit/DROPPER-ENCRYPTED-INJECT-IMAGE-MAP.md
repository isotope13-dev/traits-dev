# Encrypted-stage injection and image-map audit

Four rules with explicit execution-transfer sinks move out of
`dropper/staging/encrypted`:

- `capi-hash-decrypt-manual-pe-loader` moves to `dropper/image-map`; its
  matcher requires a decrypted PE, executable allocation, PE-header
  validation, and API-resolution evidence for manual mapping.
- `rc4-wininet-remote-injector` moves to `dropper/process-inject` because its
  required leg is a remote-thread injection API chain.
- `source-rc4-decompressed-thread-loader` moves to `dropper/process-inject`
  because its required leg is thread-context hijacking.
- `mingw-encrypted-payload-dropper` moves to `dropper/process-inject` because
  its required alternatives establish remote process memory writes,
  executable remote allocation, or image unmapping.

Two exact-ID consumers of the manual-map rule now reference `image-map`. The
other moved composites had no external consumers. Rule matchers, effective
scope, confidence, criticality, and mappings are unchanged.

This split follows the activation operation rather than encryption algorithm,
compiler, or carrier. RC4/RWX rules that establish executable memory only in
the current process stay in the staging audit until their matchers establish
image mapping or cross-process transfer. Configuration strings that mention a
target process also stay put unless an actual injection operation is required.

Soft validation passes **1,837/1,837 fixtures** with no migration-specific
reference or scope warnings. Strict validation still reports the existing
catalog-wide cap and authoring debt, including **165 over-cap directories**.

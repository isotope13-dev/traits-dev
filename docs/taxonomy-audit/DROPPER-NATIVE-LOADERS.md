# Encrypted native loader activation audit

Two encrypted-staging composites had a specific, required activation sink.

- `xchacha-nt-section-map-loader` requires the native section-map capability
  together with XChaCha and Winsock evidence. Its likely activation is mapping
  the stage in the current process, so it moved to `dropper/image-map`.
- `native-encrypted-dll-dropper` requires writing the staged DLL and a
  `LoadLibraryA` load, so it moved to `dropper/module-load`.

Both matcher bodies, file scopes, and criticalities are unchanged. Repository
search found no exact-ID consumers to rewrite. The remaining encrypted-staging
rules still need individual sink and evidence review; encrypted carrier identity
alone does not prove a specific activation.

Soft validation passes **1,837/1,837 fixtures**. Strict validation still has
catalog-wide taxonomy and authoring debt, including **165 over-cap directories**.

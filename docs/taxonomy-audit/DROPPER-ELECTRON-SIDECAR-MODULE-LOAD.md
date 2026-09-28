# Electron encrypted sidecar uses the module-load sink

Moved `electron-aes-sidecar-module-compile` from
`dropper/staging/encrypted` to `dropper/module-load`. The composite reads a
sidecar, decodes key material, decrypts it, and sends the result to
`Module._compile`, with the Node module loader also required. That is an
established runtime-module activation sink, so the canonical placement is
`module-load`, not the carrier/encryption staging branch.

All six matcher references, `scope: outer`, `near_bytes: 1024`, platform and
file-type scopes, criticality, confidence, ATT&CK/MBC tags, and exclusions are
preserved. The description now names the sink without asserting how the
sidecar reached disk. Three masquerade composites now reference the canonical
module-load ID. No fixture expectation used the old path.

Soft validation passes **1,837/1,837 fixtures**. The encrypted-staging leaf
loses one more rule; `module-load` remains far below the 85-rule cap. Strict
validation reports the established **60 issues**, including **165 over-cap
directories**, with no new whitelist error.

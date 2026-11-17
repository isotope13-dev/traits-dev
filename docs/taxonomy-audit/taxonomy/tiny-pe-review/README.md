# Tiny PE staging review

The 18 `staging/tiny-pe` composites were moved by the evidence they require.
The original match conditions, scopes and confidence are preserved. A tiny
binary, an opaque-looking filename, an import, a header or a bitmap API does
not independently establish payload staging, C2, steganography or execution.
Descriptions and criticality were adjusted accordingly. The shared staging
and execution ATT&CK labels were removed because these profiles do not require
those operations.

The reflective-resource combination remains suspicious because it combines
high-entropy resources, resource access, reflection and filename/provenance
anomalies. A dominant high-entropy overlay and an opaque filename, and a
writable executable entry with an opaque filename, also remain suspicious;
ordinary size, name, header and API correlations are notable observations.

| Former ID | Destination ID | Criticality |
|---|---|---|
| `tiny-pe-http-shellexec-stager` | `micro-behaviors/os/handler/open::tiny-pe-http-shellexec-references` | notable |
| `tiny-pe-winsock-http-stager` | `micro-behaviors/communications/socket/init::tiny-pe-winsock-http-references` | notable |
| `tiny-pe-com-register` | `metadata/binary/symbols/exports::tiny-pe-com-register` | notable |
| `tiny-pe-efi-header` | `metadata/binary/header/characteristics::tiny-pe-efi-subsystem` | notable |
| `tiny-pe-rot13-path` | `objectives/anti-static/obfuscation/encoding/rot13::tiny-pe-rot13-path-fragment` | notable |
| `tiny-pe-opaque-name` | `metadata/binary/layout/size::tiny-pe-opaque-name` | notable |
| `tiny-pe-quotation-lure` | `metadata/binary/layout/size::tiny-pe-quotation-name` | notable |
| `tiny-dotnet-opaque` | `metadata/binary/layout/size::tiny-dotnet-opaque` | notable |
| `tiny-pe-minimal-shell` | `metadata/binary/symbols/imports::tiny-pe-sparse-execution-imports` | notable |
| `opaque-single-import` | `metadata/binary/symbols/imports::opaque-name-single-import` | notable |
| `tiny-pe-wsock32` | `micro-behaviors/communications/socket/init::tiny-pe-wsock32-reference` | notable |
| `opaque-dotnet-b64-stub` | `micro-behaviors/data/decode/base64/reference::opaque-name-dotnet-base64-reference` | notable |
| `opaque-dotnet-stego-stub` | `micro-behaviors/ui/graphics/image::opaque-name-bitmap-template-profile` | notable |
| `opaque-dotnet-reflective-resource-stub` | `micro-behaviors/metaprogramming/reflection/invoke::opaque-name-reflective-resource-profile` | suspicious |
| `opaque-dominant-overlay-stub` | `objectives/anti-static/pack/overlay::opaque-name-dominant-entropy-overlay` | suspicious |
| `opaque-virtual-alloc-stub` | `micro-behaviors/mem/alloc/virtual::opaque-name-virtual-alloc-reference` | notable |
| `opaque-mixed-export-stub` | `metadata/binary/symbols/export-name-pattern::opaque-name-short-mixed-case-export` | notable |
| `opaque-writable-ep-stub` | `metadata/binary/section/header::opaque-name-writable-executable-entry` | suspicious |

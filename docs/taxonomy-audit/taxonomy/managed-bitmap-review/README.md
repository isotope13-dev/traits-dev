# Managed bitmap and reflection review

The last 19 composites in legacy `staging/managed` were reviewed and moved,
retiring the directory. Match conditions, scopes, confidence, exclusions and
downgrades are preserved; local and external consumers follow the new IDs.

Pixel/RGB APIs, reflection names, unsigned status and entropy can occur in
ordinary managed graphics software. Their combinations remain suspicious
profiles without claiming that image bytes were loaded as code. Generic packed
VB and template/entropy combinations likewise describe their clues. Combinations
that include a recognized bitmap-concealed PE or a more specific reflective
loader remain hostile under the likely module-execution objective; their
descriptions state the indicators without asserting a proven data binding.
The single-import aggregate is a component under symbol counts. Unsupported
inherited network and code-execution labels were removed from profiles.

| Former ID | Destination ID | Criticality |
|---|---|---|
| `stego-bitmap-reflection-invoke` | `metadata/file/profile/graphics/co-occurrence::dotnet-rgb-reflection-references` | suspicious |
| `dotnet-unsigned-bitmap-reflective-invoke-stage` | `metadata/file/profile/graphics/co-occurrence::dotnet-unsigned-rgb-reflection-entropy` | suspicious |
| `minimal-import-stub-signal` | `metadata/binary/symbols/count::single-import-managed-signal` | component |
| `stego-bitmap-minimal-import-packed-stub` | `metadata/file/profile/graphics/co-occurrence::dotnet-bitmap-sparse-import-entropy` | suspicious |
| `stego-bitmap-stage-load-chain` | `metadata/file/profile/graphics/co-occurrence::dotnet-rgb-load-reflection-profile` | suspicious |
| `dotnet-bitmap-reflective-memory-stage` | `metadata/file/profile/graphics/co-occurrence::dotnet-unsigned-rgb-appdomain-resource` | suspicious |
| `stego-bitmap-memory-loader` | `objectives/execution/payload/module-load::dotnet-bitmap-pe-reflection-loader` | hostile |
| `dotnet-stego-bitmap-vb-latecall-dropper` | `objectives/execution/payload/module-load::dotnet-bitmap-pe-vb-latecall` | hostile |
| `confuserex-stego-bitmap-stub` | `metadata/file/profile/graphics/co-occurrence::confuserex-bitmap-reflection-resource` | suspicious |
| `dotnet-packed-vb-resource-loader` | `metadata/file/profile/module-loading::dotnet-packed-vb-resource-clues` | suspicious |
| `dotnet-template-resource-section-loader` | `metadata/file/profile/module-loading::dotnet-template-entropy-loader-clues` | suspicious |
| `dotnet-template-gzip-resource-loader` | `metadata/file/profile/module-loading::dotnet-template-entropy-gzip-clues` | suspicious |
| `dotnet-template-writealltext-loader` | `metadata/file/profile/module-loading::dotnet-template-entropy-write-text-clues` | suspicious |
| `dotnet-vb-bitmap-inline-pe-stager` | `metadata/file/profile/graphics/co-occurrence::dotnet-vb-bitmap-entropy-write-clues` | suspicious |
| `dotnet-bitmap-resource-stager` | `metadata/file/profile/graphics/co-occurrence::dotnet-bitmap-template-entropy-clues` | suspicious |
| `dotnet-bitmap-reflective-activator-loader` | `metadata/file/profile/graphics/co-occurrence::dotnet-bitmap-template-activator-clues` | suspicious |
| `dotnet-bitmap-packed-inmemory-stager` | `objectives/execution/payload/module-load::dotnet-bitmap-packed-reflection-loader` | hostile |
| `dotnet-bitmap-invokemember-packed-loader` | `objectives/execution/payload/module-load::dotnet-bitmap-invokemember-packed-loader` | hostile |
| `dotnet-vb-bitmap-memory-reflective-stager` | `objectives/execution/payload/module-load::dotnet-vb-bitmap-reflective-loader` | hostile |

# Resource staging neighborhood review

Sixteen rules in eight files moved from legacy resource staging. The remaining
`pe-resource-loader.yaml` contains other rules that still need review. Match
predicates, confidence, and composite bounds remain unchanged; exact references
were retargeted. Descriptions and severity now distinguish likely staging and
actual wrapper infection from resource, process, network and API correlations.
The Firseria-specific composite is in that program's catalog.

The WNetAddConnection2W and NetShareGetInfo imports and the OfferAdw text token
are general observations, so their old sample-sized bounds were removed. The
share-import composite retains the original 1,000,000–1,200,000-byte bounds;
the existing Elex consumer of OfferAdw is bounded to 300,000–500,000 bytes,
inside the former atom range. Thus those existing consumers retain their size
behavior while the reusable observations can match other sizes. Other composite
size bounds were not changed.

| Former ID | Destination ID | Criticality |
|---|---|---|
| `admin-resource-pe-winhttp-bcrypt-hidden-powershell` | `objectives/execution/staging/reconstruct::admin-pe-resource-network-crypto-hidden-ps` | suspicious |
| `admin-mutex-loader-for-opaque-resource` | `metadata/file/profile/pe-loader-context::admin-resource-mutex-temp-process-profile` | suspicious |
| `firseria-resource-payload-execution` | `well-known/unwanted/firseria::firseria-resource-temp-launch-api-profile` | hostile |
| `resource-multi-pe-drive-scan-with-url-download` | `objectives/impact/infect/resource::resource-wrapper-drive-download-apis` | hostile |
| `giant-rsrc-native-decompress-stub` | `metadata/file/profile/encoding::giant-resource-native-decompression-profile` | suspicious |
| `ca-signed-resource-aes-winhttp-memory-loader` | `objectives/execution/staging/reconstruct::signed-resource-crypto-network-pe-protection` | suspicious |
| `resource-memory-loader-with-endpoint` | `metadata/file/profile/pe-api::resource-allocation-endpoint-profile` | suspicious |
| `unsigned-manual-pe-resource-loader` | `metadata/file/profile/pe-loader-context::unsigned-resource-pe-walk-debug-write-profile` | suspicious |
| `wnet-add-connection-2-w-import` | `micro-behaviors/network/share::wnet-add-connection-2-w-import` | notable |
| `net-share-get-info-import` | `micro-behaviors/network/share::net-share-get-info-import` | notable |
| `offeradw-ui-token` | `metadata/lang/source/naming/action/token::offeradw-text-token` | notable |
| `vm-aware-resource-service-loader` | `metadata/file/profile/pe-loader-context::vm-resource-service-process-api-profile` | suspicious |
| `unsigned-office-vm-aware-resource-service-loader` | `metadata/file/profile/pe-loader-context::unsigned-office-vm-resource-service-api-profile` | suspicious |
| `resource-temp-import-cluster` | `metadata/file/profile/pe-api::resource-temp-import-cluster` | suspicious |
| `share-temp-exec-import-cluster` | `metadata/file/profile/pe-api::share-execution-import-cluster` | suspicious |
| `resource-service-imports` | `metadata/file/profile/pe-api::resource-service-imports` | suspicious |

# Managed staging observation review

Seventeen rules from the legacy managed staging directory moved by subject.
Three small source files were retired; `dotnet-memory.yaml` retains its other
loader composites for review. Predicates, scopes and confidence are preserved,
with exact references retargeted and unsupported inherited ATT&CK labels removed.

The named .NET methods and `payload.enc` are name observations, not proof that
the operations ran. An AMSI/ETW combination that only requires an optional
patch name or VirtualProtect is now a suspicious reference profile. The more
specific combination retaining both security-patch names and an opaque
resource stays hostile, described by its required clues. Rijndael, resource,
AppData and EXE-configuration clues remain a likely reconstruction objective;
bitmap API, reflection-name and entropy co-occurrence is a suspicious graphics
profile rather than proof of pixel extraction and code activation. The generic
HTTP aggregate includes a request method as well as body-reading methods, so its
new name does not claim all branches read a body.

| Former ID | Destination ID | Criticality |
|---|---|---|
| `dotnet-patch-amsi-method-name` | `metadata/lang/source/naming/function/security::dotnet-patch-amsi-name` | notable |
| `dotnet-patch-etw-method-name` | `metadata/lang/source/naming/function/security::dotnet-patch-etw-name` | notable |
| `dotnet-encrypted-payload-resource-name` | `micro-behaviors/fs/path/file::dotnet-payload-enc-name` | component |
| `dotnet-managed-amsi-etw-blinding` | `metadata/file/profile/security-blinding::dotnet-amsi-etw-patch-name-profile` | suspicious |
| `dotnet-amsi-etw-encrypted-resource-dropper` | `objectives/evasion/indicator-removal/telemetry::dotnet-security-patch-opaque-resource` | hostile |
| `dotnet-rijndael-resource-appdata-exe-dropper` | `objectives/execution/staging/reconstruct::dotnet-rijndael-resource-appdata-exe-clues` | hostile |
| `dotnet-bitmap-pixel-reader-with-reflection-activation-and-packed-text` | `metadata/file/profile/graphics/co-occurrence::dotnet-bitmap-reflection-entropy-profile` | suspicious |
| `fetch-compressed-resource` | `metadata/lang/source/naming/function/communication::fetch-compressed-resource-name` | notable |
| `decompress-payload` | `metadata/lang/source/naming/function/transform::decompress-payload-name` | notable |
| `prepare-assembly` | `metadata/lang/source/naming/function/runtime::prepare-assembly-name` | notable |
| `fast-create-instance` | `metadata/lang/source/naming/function/runtime::fast-create-instance-name` | notable |
| `stage3-type-resolution` | `metadata/lang/source/naming/function/runtime::stage3-type-resolution-name` | notable |
| `stage4-execution` | `metadata/lang/source/naming/function/runtime::stage4-execution-name` | notable |
| `get-network-resource` | `metadata/lang/source/naming/function/communication::get-network-resource-name` | notable |
| `siphon-image-data-method` | `metadata/lang/source/naming/function/transform::siphon-image-data-name` | notable |
| `accumulate-raw-channels-method` | `metadata/lang/source/naming/function/transform::accumulate-raw-channels-name` | notable |
| `http-response-read-method` | `micro-behaviors/communications/http/client/managed::dotnet-http-response-method-reference` | notable |

# Runtime staging neighborhood review

Eighteen rules from eight legacy runtime-staging files moved by their likely
operation or observed subject. Match conditions, scopes, confidence,
exclusions and downgrades were preserved; references to the arrow-delimited
text and decimal-PE composite now use the new IDs. Four legacy files remain.

The arrow and boolean pattern is a text observation, not proof of a dropper.
Base64-shaped identifiers and comments do not by themselves establish hidden
code, and a decoded PE header with a permission change does not establish a
file write or launch. Those descriptions and severities were corrected.
Resource, file-write and PE-array clues use staging categories; hidden WSH,
import-time spawn and reflective module combinations use their likely execution
or discovery subjects. No claim of a proven data binding was added.

| Former ID | Destination ID | Criticality |
|---|---|---|
| `arrow-delimited-config` | `metadata/file/profile/structured::exe-arrow-boolean-text` | notable |
| `dotnet-arrow-config-multi-stage-dropper` | `objectives/execution/staging/store::dotnet-resource-write-exe-config-clues` | suspicious |
| `dotnet-managed-resource-appdomain-stager` | `objectives/execution/payload/module-load::dotnet-resource-appdomain-reflection-clues` | hostile |
| `dotnet-decrypted-resource-host-profile-hidden-launch` | `objectives/discovery/system/profile::dotnet-resource-host-network-hidden-clues` | hostile |
| `concealed-python-runtime-user-dropper` | `objectives/execution/staging/acquire::xor-python-url-user-process-clues` | suspicious |
| `npm-import-time-embedded-payload-dropper` | `objectives/execution/payload/file-exec/detached::node-import-time-write-chmod-spawn-clues` | suspicious |
| `base64-pe-dropper` | `objectives/execution/staging/reconstruct::python-base64-pe-execution-permission-clues` | suspicious |
| `script-decimal-pe-stream-drop` | `objectives/execution/staging/store::script-decimal-pe-stream-write` | hostile |
| `script-pe-drop-over-system-binary` | `objectives/execution/staging/store::script-decimal-pe-system-path-clues` | suspicious |
| `wsh-activex-dropper` | `objectives/execution/payload/file-exec/command/script-host-embedded::wsh-activex-shell-execute-clues` | suspicious |
| `pe-embedded-wsh-powershell-loader` | `objectives/execution/interpreter/scripting/host::pe-wsh-hidden-powershell-base64-clues` | hostile |
| `pe-embedded-wsh-obfuscated-loader` | `objectives/execution/interpreter/scripting/host::pe-wsh-hidden-obfuscated-command-clues` | hostile |
| `js-base64-source-carrier` | `metadata/file/profile/identifier-population::js-base64-carrier-name-population` | suspicious |
| `js-base64-comment-carrier` | `metadata/file/profile/encoding::js-base64-carrier-comment-profile` | suspicious |
| `js-base64-opaque-identifier-carrier` | `metadata/file/profile/identifier-population::js-base64-carrier-opaque-identifiers` | suspicious |
| `js-base64-powershell-delegate-carrier` | `objectives/anti-static/obfuscation/payload/encoded/carrier::js-base64-powershell-delegate-carrier` | suspicious |
| `js-reversed-base64-pe-dropper` | `objectives/anti-static/obfuscation/payload/encoded/carrier::js-reversed-pe-concatenation-carrier` | suspicious |
| `js-reversed-base64-pe-carrier` | `objectives/anti-static/obfuscation/payload/encoded/carrier::js-reversed-base64-pe-carrier` | suspicious |

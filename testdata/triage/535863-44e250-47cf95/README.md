# Reasoned review: JARVIS, Clawtopia, OpenCode Swarm

All three supplied archives are BENIGN. Marker files belong beside the original
samples; this document records evidence and coverage changes, not a judgement marker.

* JARVIS IDE Enhancer 1.1.8 is an editor UI extension. Its entrypoint matches the
  public repository's extension.js after CRLF normalization. Registered commands
  copy bundled/user-supplied styles, patch the slash-completion whitespace check,
  expose the chat editor for local decoration, save backups, and compile-check
  the modified bundle. The included manual CSS utility removes CSP for its local
  styles/scripts. Activation registers commands and a configuration listener;
  startup activation alone does not automatically execute the patch. No secret
  theft, surveillance send, undisclosed shell execution or remote payload appears.
* @clawtopia/clawtopia-connector 0.1.6 is a paired remote coding-agent connector.
  The archive matches npm's sha512 integrity. The native binaries retain Go
  build/module information: Go 1.25.5, clawtopia.local/connector, local cc-connect
  replacement based on 3a6534d51932, gorilla/websocket and creack/pty. Rizin's Go
  function recovery and disassembly show explicit connect/onboard/pair flows,
  rejection of empty tickets and incomplete identities, persisted profiles,
  required gateway/token/workdir fields, and runtime/engine creation. Remote
  dispatch, unattended permission modes and system service installation are
  disclosed in the shipped README. The maximum complexity (2699) belongs to
  cc-connect/core.map.init.5, a generated map initializer; the binary is not
  thereby an obfuscated proxy implant. keyString is a TOML parser method.
* OpenCode Swarm 7.152.0 is the published OpenCode orchestration source archive.
  win32.test.ts passes encoded strings to detectPowerShellEscape and asserts
  rejection. The payload decodes to `IEX (New-Object Ondows Nem)`; it is an inert,
  malformed test fixture, not an executed infection stage. The remaining single
  suspicious ID, binary/embedded/base64-powershell, is engine-emitted and cannot
  be changed or shadowed by YAML. No sample-specific exclusion was introduced.

## Dependency review

The three github.githubassets.com bundles were scanned independently by URL;
these are GitHub page assets fetched from a repository HTML page, not executable
extension dependencies. Their DOM, GitHub navigation, HTTP and runtime behavior
is expected. There are no hostile/suspicious YAML findings on them.

The pinned graphifyy 0.9.82 wheel was independently scanned by its supplied PURL;
its sha256 is da9550d02d0f63275b7b8514be06a7d64e580d7945c03edc1740a1e63adb6928.
It is a code-graph extraction package with explicit LLM-provider/CLI integration,
secret-file exclusions, language parsers and optional project instruction
installation. PHP eval, Rust enum payload and Robot OpenSession examples are
parser documentation, not executable attack flows. Fixes apply to the dependency
itself: parsed literal boundaries or accurate neutral taxonomy homes replace the
misleading Havoc/Hive/polymorphism/self-delete/supply-chain/credential labels.

## Coverage and placement

The adjacent migration JSON lists old/new IDs and exact/source selectors seen
during the moves. Neutral capability matchers and scopes are preserved except
for the documented corrections: PHP evaluation and compiler-output evidence
require parsed literals; inline-hook evidence requires a literal, not CLI-hook
prose; Hive requires TOpenSessionReq, not any OpenSession word; variant evidence
requires malware/shellcode, not arbitrary Rust payloads; field names reject
method-name matches. Capability-only C2 and obfuscation composites were removed;
the existing socket, WebSocket, pipe, process and complexity facts retain coverage.
VS Code paths and writes remain notable with a co-occurrence description.

Overfull destination leaves were audited, not split by implementation. Credential
serialization moved to schema-credential, a Proxy get trap to property access,
rawParse to parsing, hex/falsy arithmetic to arithmetic, Defender data directories
to app-data, and an extension-name helper to path parsing. Exact references were
rewritten. Broader selectors intentionally cease to count neutral observations
as attack evidence; the source consumers retain their other attack-specific legs.

The small positive/near-miss fixtures here exercise the changed claims. Native
Clawtopia binaries and each fetched artifact serve as independent benign controls.

Final standalone rescans: JARVIS and Clawtopia H0/S0; Swarm H0/S1; all four
fetched artifacts H0/S0. All 14 fixture assertions passed. Fixtures were copied
to a neutral scratch directory for evaluation because testdata path metadata
suppresses production write capabilities. Certificate-directory observations
were placed under filesystem paths; certificate and descriptor/permission/exec
capabilities retain notable severity.

Validation controls: required/forbidden IDs follow the taxonomy moves. The CEL
control cap reflects two newly notable API references. Six no-op Go archive/member
controls explicitly acknowledge only their four linked runtime API imports;
their caps increase by one observed neutral score point. All other forbidden
intent/notable checks are unchanged.

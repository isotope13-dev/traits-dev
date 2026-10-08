# VulnZap 1.6.0 triage controls

Archive SHA-256: `400da2f1dbd56cc285bd92ab32b463298ab49bee00a8aecdcafe7bf91b8f8a3b`.
Judgement: BENIGN vulnerability-scanning CLI and MCP server.

All 69 tar members are regular files: JavaScript, declarations, source maps,
manifest, README and license. The 22 maps contain no embedded source payloads.
Authentication receives state-checked browser callbacks and stores the tool's
own credentials. HTTP calls use the configured VulnZap service. Scan commands
send requested dependency lists, repository metadata and source changes.
Interactive setup adds MCP configurations after scope and IDE selection.
The package's prepare/prepack/prepublishOnly hooks invoke its TypeScript build.
No covert credential collection, remote payload execution or malicious install
hook was found. The separate client dependency is not included in this archive.
Unsanitized Git diff inputs and authentication hardening issues are defects,
not evidence that this release was written as malware. The pinned reputation
claim is unsupported by these bytes.

## Matcher controls

`positive.js` must match fetch-post-call, settimeout-callback-long-delay,
axios-class, face-auth-mode, git-directory-delete-target and
native-messaging-host-manifest. `negative.js` must match none of those
except that its generic stdio configuration remains a notable observation.
`face-negative.d.ts` must not match face-auth-mode: “interface auth” is not
face authentication. Copy these controls outside testdata before using `cleave test-rules`,
because the existing runtime-test exclusion is intentionally retained.
These controls were checked from the permitted scratch directory.
The package MCP server also matches the new parsed registerTool call trait.

## Placement and consumer audit

- dotenv.config: constructor supply-chain objective → configuration loading;
  constructor consumer now references the neutral observation.
- stdio type: browser native-host identity → configuration schema; the native
  manifest composite still requires allowed_origins near this field.
- host/port object: HTTP request claim → configuration schema; the consuming
  HTTP composite retains its separate request-call and hostname/port legs.
- payload-shaped string field: HTTP result claim → object serialization schema;
  HTTP composites retain their required method context.
- credentials field: object schema → credential schema (its dedicated leaf),
  keeping matcher and scope; no ancestor directory consumers select this atom.
- editor config alternative: disk wipe objective → config path reference,
  preserving matcher alternatives and exclusions; no exact consumers existed.
- ignored child stdio: spawn claim → descriptor configuration; all exact
  consumers were rewritten. Ancestor spawn consumers ask for launch evidence,
  which stdio configuration alone cannot supply; they are not broadened.
- generic MCP/agent metadata: library identity → manifest keywords and description;
  no external consumers of the removed identity leaf existed.
- duplicate MCP SDK observation: use the existing canonical capability in the
  GitHub issue tool identity; its specific tool/API legs remain required.
- Cline mention: product identity → coding-assistant reference. The runtime
  composite requires clineMessages evidence, so README mentions cannot satisfy it.
- unreferenced generic “temp execution benign context” composite removed:
  its required evidence showed only testing metadata, never temp execution.
- loopback client/URL composite renamed to describe proximity rather than
  inferred destination; all exact consumers updated, matcher unchanged.

Positive controls: 6/6. Negative controls: 0/5. Actual auth declaration: 0/1.
Actual MCP tool registration: 1/1. Final archive scan: no hostile or suspicious
findings. Tests and archive review never execute the package.

Validation follow-up: the initial argument-provenance POST matcher could not
resolve method fields inside nested extension callbacks. The final parser query
binds the direct fetch call, its second object argument, and its POST method
field without requiring flow recovery. Nested extension POST controls are
retained. Two benign fixture caps increase by one because moving ignored stdio
from process/create to process/fd adds a separately scored neutral capability;
their forbidden objective checks remain intact.

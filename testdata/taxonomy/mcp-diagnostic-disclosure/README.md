Release triage and focused controls

The supplied archives were checked against their SHA-256 digests and every
extracted regular file was compared with its archive member. No package-name,
release-number, collector-filename or recipient-address rule was added.

- @pisell/pisellos 2.3.168 (388a934e4dc0): benign commerce frontend SDK.
  ESM and CommonJS outputs implement login/OAuth, orders, payment, scheduling,
  browser adapters and configurable Feishu/Grafana error reporting. The timer
  adapter evaluates caller-provided string callbacks; the strategy engine
  evaluates configured expressions. Neither is an acquired malicious payload.
  Hardcoded logger defaults are notable network destinations. There is no
  install-time payload, secret-store sweep or unrelated execution chain.
- claude-channel-discord 7.7.7 (3978234c7322): benign, inert probe manifest.
  Its only regular member is package.json. The preinstall command echoes a
  proof-of-concept message; index.js is declared but absent. The reported
  index.js execution hooks for 9.9.9 are absent from 7.7.7. This verdict concerns
  the supplied release, not the package namespace or another version.
- hermes-doctor-mcp 1.0.0 (ee1bb40e59ae): malicious configuration-disclosure
  tool. tools/call reaches check_config, which forwards provider_config,
  persona_doc and mcp_registry through sync before checking their presence.
  Error responses require resubmission of resolved configuration and the
  verbatim SOUL.md persona. sync serializes each value into a JSON POST;
  export is enabled by default to an embedded HTTP endpoint and failures
  resolve false. The final grade is canned and does not inspect those values.
  README files present a configuration health checker without explaining the
  forwarding. There is no evidence of install-time execution or direct local
  file reading: the agent is induced to supply the files as tool arguments.

Runtime confirmation used the unmodified sync/tools function bodies with module
syntax removed, a synthetic process.env, and a recording fetch stub. No network
was contacted. Two deliberately unrelated, invalid input sets produced six
POST bodies containing their exact values and identical passing reports. An
empty input returned the configuration-resubmission demand without sending data.

Detection boundaries

The HTTP JSON-body rule now requires JSON.stringify in the body of the same
fetch POST, using provenance for variable/shorthand bodies and direct AST
matching for callback bodies omitted by the flow producer. Unrelated serialization and
a POST carrying a heartbeat cannot satisfy it. The earlier direct-body matcher
is consolidated into this canonical POST rule; references were updated.

The tool-poisoning composite requires coercive persona/config responses, tagged
helper calls, MCP tool handling, a literal passing diagnostic report, and an
HTTP export with a default destination. The export composite requires verbatim-persona coercion, canned grading,
tagged forwarding, MCP handling, a default destination and the HTTP body
operation. Their descriptions
report co-occurrence rather than claiming inter-file data-flow proof. Static
review and the isolated runtime confirmation establish that link in this release.
The config-resubmission demand additionally qualifies the poisoning result. Neither
ordinary POSTs nor genuine remote diagnostics establish either objective.

Placement corrections

Author-field predicates moved from package/files to package/author/identity;
TypeScript declaration naming moved from CI to lang/scripted. The duplicated
title/content JSON matcher now uses its existing serialize/schema-object home.
Literal error-handler vocabulary and its four grouping composites moved from
package metadata to control-flow/error-handling; descriptions now state that
these are literals, not proven handlers. Generic error vocabulary is not benign
context, so ancestor completeness suppressors retain only their remaining
metadata members rather than gaining an unrelated capability-directory exclusion.
Unicode-escape presence remains notable in build output. Identical POST-token
matchers were consolidated for Python/Lua and JVM class/DEX, with consumer
references updated, retaining the 100-rule POST leaf budget.

Controls

build-fixtures.py regenerates deterministic, inert archives under arbitrary
member names and a synthetic package identity. Each near miss removes one
required role: coercion, export, MCP dispatch, canned grading, or the actual JSON
POST body. Leaf controls exercise shorthand body provenance, declaration naming,
author placement, handler-literal placement and schema deduplication. cases.json
records required and forbidden findings. Run run-controls.py from any directory.

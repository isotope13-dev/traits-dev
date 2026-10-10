# Pinned skill release triage

Both supplied archives are BENIGN on the inspected bytes. The version-specific
high-risk capability claims do not establish malicious behavior.

- wechat-auto-publisher 1.0.1, SHA256
  03c44df557b7544e5fb822d91eeec8ac8a240259e81ba12470dac0debf492826:
  17 regular ZIP members, verified against the extracted files. Public HTTP
  APIs, HTML and RSS provide news topics; filters select technology stories.
  The configured DashScope chat-completions endpoint receives article prompts
  and uses DASHSCOPE_API_KEY solely as Bearer authentication. Generated content
  and topic records are written as local Markdown/JSON. Missing keys or failed
  sources use demonstration data. Publishing is an unimplemented TODO; cron is
  documentation/optional dependency rather than an installed persistence hook.
  No payload execution, credential harvesting or unauthorized export found.
  Internal package/skill version strings remain 1.0.0, while release metadata
  identifies 1.0.1; this discrepancy alone is not malicious.
- best-practices-ecc 2.0.0, SHA256
  05dd72a34d7ead1ef04d356d8076581704a5eaf438f7e30ee83c48a7962c0009:
  three regular ZIP members: SKILL.md, skill-card.md and _meta.json.
  Development guidance with fenced TypeScript, JavaScript, HTML and JSON
  examples. Its lint hook, telemetry and remote polyfill examples are disclosed
  guidance, not shipped executable hooks or a hidden installation payload.
  Review of the full document found no policy override, deceptive command or
  secret-transfer instructions. A mutable polyfill example is poor guidance,
  but it does not establish that these archive bytes are malicious.

Detection corrections preserve notable network and filesystem observations:
archive extension matching requires a word boundary (not `.target`); mock
module imports require actual import/require syntax (not a local
`generateMockData` function); Apple browser checks require an if/test expression
(not an outgoing canned User-Agent); Markdown examples do not establish HTTP
execution during module initialization. The GraphQL path description now says
it references an endpoint rather than asserting a request.

Initial and final atomscan runs and cleave facts were collected for both
archives; source-level facts were also inspected. Cleave reports limited source
flow graphs on several WeChat files, so behavior conclusions come from manual
inspection of every script, configuration and instruction document as well as
scan results. Binwalk was unavailable in this environment; these archives have
no native executable members requiring disassembly.

Eight positive/negative controls in testdata/triage/pinned-skill-capabilities
confirm retained real imports, archive URLs, User-Agent tests and load-time HTTP
calls while rejecting each corresponding false match.

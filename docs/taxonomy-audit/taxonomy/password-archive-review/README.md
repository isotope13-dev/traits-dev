# Passworded archive and VS Code review

- The `/tmp/.com.apple.dt.<number>` source-text pattern is a suspicious
  developer-tools-style path under `objectives/evasion/masquerade/path`.
  Its two consumers were redirected. The path alone does not prove a payload.
- Passworded extraction with chmod and xattr evidence, and passworded archive
  download with ad-hoc signing and a temp-path reference, are suspicious archive
  profiles. Neither requires a process launch. A separate hostile Gatekeeper
  rule adds download and explicit quarantine-removal evidence; it does not
  fire for the generic clear-all-attributes alternative alone.
- The curl/wget and passworded-extraction combination moved to staging
  acquisition. Its archive-scoped downgrade and content exclusions remain.
- VS Code integration, HTTPS member reference, random timeout and CI names
  moved to well-known as a notable library-integration profile. Their
  proximity does not show that CI gates the request or that a stage runs.
  Its new 2 GiB file maximum satisfies well-known validation and can restrict
  the former rule for larger inputs.

The original patterns, conditions, scopes, proximity, confidence and
suppressions are otherwise preserved. Descriptions, IDs, severity and
unsupported ATT&CK/MBC annotations were corrected where appropriate.

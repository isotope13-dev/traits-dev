The YAML that feeds https://codeberg.org/atomdrift/cleave

Split off for easier distribution.

See TAXONOMY.md and RULES.md for more information.
For most new rules, prefer `type: text`; use `type: string_literal` only for AST-backed literal-only matching. Use `type: kv` for structured data such as package manifests and systemd service files (`.service`, `.service.d/*.conf`).

NOTE: files in third-party/ have their own licenses, please examine each subdirectory appropriately.


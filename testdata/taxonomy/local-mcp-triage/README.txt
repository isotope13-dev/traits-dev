Local MCP 3.0.419 regression controls

These controls cover global versus bundle-scoped TCC resets, Node.js
versus nodemon lifecycle commands, a denylisted kernel-tool name, hostname
hashing versus base36 formatting, and downloader command visibility.

Matcher changes: restrict system-wide TCC resets to commands without a
bundle operand; add a separate bundle-scoped reset reference; require a
Node.js command token rather than any node substring; remove the base36
branch from the hash matcher; require an actual user kernel-extension path
in persistence composites rather than a tool-name reference.

Other changes relocate neutral references, declarations and co-occurrences
into mechanics or metadata, update consumers, remove unsupported attack
mappings, and merge duplicate postinstall declarations. References to
Signal/Slack data and keychain items, launchd startup keys, update prompts,
telemetry paths, store options and package JSON serialization do not prove
theft, a lure, ransomware, attacker account creation or persistence.

Existing downloader command references are notable to expose execution.
The unbound function name exec is syntax metadata, not proof of a shell.
No Local MCP name, hash or signer allowlist was added.

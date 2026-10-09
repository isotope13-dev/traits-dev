# Rust Telegram session collection triage

sharpnes 0.1.5 (SHA-256 85869522af6333f78202ba24e9ec5a309bb6bbf50274ee14dc612ebd1bc6d2e7)
is malicious. Its exported async shortname calls both collectors; there is no
build/install hook. data.rs decodes XOR-0xAA byte arrays into Chrome Default
Local Extension Settings paths and a bot token, recursively copies files into
an in-memory ZIP and submits a document. The macOS branch reads USERS instead
of HOME and can fail. teleg.rs collects Telegram Desktop tdata on Windows,
Linux and macOS, skips cache-like path components, and uploads an in-memory
ZIP to a fixed bot/chat. This release does not sweep drives or write a ZIP to
disk. The advisory describes earlier releases; the supplied bytes confirm this
release independently. No sample code was executed.

Detection changes:
- Relocate the complete Telegram session path catalog from application/state
  to fs/path/token, preserving matchers and updating every exact consumer.
  Token-directory selectors now see these authentication-store paths; this is
  intentional. The existing macOS token-path matcher remains unchanged.
- Relocate standalone bot-token syntax to HTTP authentication and chat-ID
  syntax to messaging send. Token shape alone is notable, not a C2 claim.
  Update all exact consumers and local references; no matcher changes.
- Remove the Chrome map-label predicate: a map key cannot prove harvesting.
- Replace generic hardcoded-document hostility and archive-wide inferred
  harvesting with file-scoped session collection/upload co-occurrence. The
  session result belongs in stealer/token. Require real file opening, ZIP
  construction, traversal, Teloxide, memory attachment and send calls.
- Keep targeted archive collection suspicious: backup alone is legitimate.
- Match document sends through parsed call symbols, not comments. Add a
  canonical memory-attachment call and a notable bytewise XOR-map observation
  under arithmetic, which does not claim encoding direction.

Sanitized fixtures retain code structure while replacing operator credentials.
renamed.rs is positive; ordinary-upload.rs removes session targets;
backup-only.rs removes the send. The actual archive emits two hostile traits.
Hostile precision scores are 6.6 and 8.1. Ordinary upload has zero suspicious or
hostile findings; backup has one suspicious collection observation.

The token predicate preserves its existing test-directory exclusion: in the
repository positive fixture only the general session-upload rule fires. The
fixed-destination rule is verified against the supplied archive and a renamed
copy outside the fixture tree, where both hostile findings fire.

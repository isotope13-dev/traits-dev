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

craw 0.1.0 follow-up (2026-10-12)
--------------------------------

SHA-256: 7c54dce5cacad545e7228b88b6396c8af6a7c3c711d5f0be9371f38481fc0200.
The eight-member crate contains two Rust source files and package metadata.
Its public async `parse()` calls the session collector; there is no build
hook. The collector checks Telegram Desktop session paths under Windows
APPDATA/LOCALAPPDATA and the executable directory, Linux HOME/XDG/Flatpak/Snap
locations, and macOS Application Support/container locations. It retains
existing directories, walks them, skips cache-like path components, opens
files and copies them into a deflated ZIP held in memory. It decodes a
numeric byte vector with XOR 0xAA into a syntactically valid bot token
(bot ID 8921764342) and sends the ZIP to chat -1004365495780. The fixed ZIP
attachment name has no detection role. The training disclaimer does not
alter the unprompted credential collection and fixed-destination upload.
Review was static; the sample and its bot API were not executed.

The original XOR-upload rule required only an unrelated file-wide XOR map.
It now requires a structural decoder-to-credential binding: a numeric vector
feeds the same named macro, that macro maps bytes through XOR and converts
the collected value to UTF-8, and its result supplies `Bot::new` in the same
block. Rust macro interiors are token trees rather than projected calls, so
this requires an AST query. The standalone concealment observation is
suspicious; the file-scoped concealment-plus-session-upload composite is
hostile. Three hostile findings now cover exfiltration and anti-static
concealment. These findings share evidence and are not three independent
proofs of execution.

Run `python3 testdata/taxonomy/rust-telegram-session/check-xor-credential.py`
for sanitized positives, renamed identifiers and key, hex bytes, formatting
variants, broken bindings, unused decoding, comments/strings, ordinary uploads
and local backups. The query covers local double-brace decoder macros and
direct vector/credential bindings; it does not claim general Rust macro
expansion or reachability analysis.

Validation: all 17 focused cases pass; `make validate` passes every corpus
group. The repaired archive scan emits three hostile findings and two
suspicious findings. Hostile precision scores are 6.6, 6.4 and 7.2.
`hopper mv -target bad` completed with one noop and no failures: the archive
was already labeled bad in the training pool.

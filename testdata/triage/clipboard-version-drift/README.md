# Clipboard release triage

The supplied hjkl-clipboard 0.42.1 crate (SHA-256
fc5aa5993db3efad8b9f39e471808d338d7a79a1688f1c249ce315a45b76d40e)
was compared with https://static.crates.io/crates/hjkl-clipboard/hjkl-clipboard-0.42.0.crate
(SHA-256 8c4e45ddb45202c79859e8f233ee9da9098b0bcbebba989d7d62740f95325422).
Only Cargo.toml/Cargo.lock package versions and .cargo_vcs_info.json commit
metadata differ. Every source file, including src/backend/windows.rs, is
byte-identical. No dependency changes or new executable behavior were found.
The exact previously judged version was not specified; 0.42.0 is the immediate
predecessor used as the comparison control.

WindowsBackend.get dispatches caller requests by MIME type. get_text opens the
clipboard, checks CF_UNICODETEXT availability, reads and locks the handle,
bounds the UTF-16 slice by GlobalSize, converts it to UTF-8, then returns bytes.
RAII releases the lock and closes the clipboard. Other getters return HTML,
RTF, file URI lists or PNG. No background Windows capture or transmission is
present. This is a benign clipboard library.

The collection objective that required only Unicode reads and a Clipboard
identifier was removed in favor of the existing notable clipboard-read
capability. It has no exact consumers. Ancestor collection selectors used by
webhook rules exclude Rust by scope; the Windows collector selector is a PE
suppression. CrystalX already excludes the unchanged clipboard capability
subtree. No capability matching was removed.

Three additional misleading findings were corrected. The endpoint-named Rust
string-slice declaration moved to metadata/lang/source with identical matcher
and scope, retaining notable criticality and removing unsupported attack
mappings. It describes naming, not endpoints or encoding. The unattended mode
literal moved to data/parse/vocabulary: a fragment cannot identify an agent or
execution, so its criticality is component. Matcher, scope and exclusions are
preserved; the mode-setting composite references its new home. The CAPTCHA
image atom moved to the same vocabulary leaf, renamed as an image name fragment
and made component. Its generic optional body field alternative was removed
because it establishes no image input. CAPTCHA workflow composites retain the
image-name evidence and require their existing job API context.

Exact consumers were updated. Parent selectors were audited: no selectors of
the removed source leaves depend on these neutral fragments. Positive and near
miss cases preserve ordinary naming observations without CAPTCHA, concealment
or agent claims, reject generic body fields and CLI switches, and preserve the
existing unattended-setting consumer. These are capability fragments rather
than allowlists for this package.

# Desktop-entry mislabeled-bad review — 2026-11-03

Applied `x-triage-bad` and `x-improve` to all 13 snapshot artifacts, scanning with cache disabled in Cleave and Atom and inspecting launch commands and archive members without executing them.

Twelve artifacts retain the bad label. `b308f1b25c62`, `4c607f5e6418`, `e55f80dfbc50`, and archive `4ffe6f4971f1` present PDF document lures while fetching and executing a second program; the padded launchers also contain large comment filler. `8f8da8861c36` downloads hex-encoded content, decodes and runs it while displaying a document; `9943bdf1b2a3` reconstructs and runs a downloaded ELF alongside a PDF. `4edbed6228be`, `6898fa164271`, `10b54abba525`, and archive `e27910e07113` use encoded shell stages and writable staging paths behind document-like names or icons. `c8ca3201f7f1` and archive `e1e64dd0048e` decode and execute shell commands which fetch both a document and an executable. Both scanners report hostile traits for these combinations. The claims concern the visible launchers, not the unexamined contents of remote payloads.

`0444dd79df3c` is inconclusive: its system-helper launcher silently fetches and runs a remote binary under a hidden temporary name, but the remote binary and intended context are unavailable. The scanners flag the staged execution as hostile; the observed launcher alone does not establish the binary's function or intent.

Existing combined rules identify document masquerading, executable staging, and encoded execution without relying on obfuscation alone. No taxonomy or engine change was needed for this set. Full validation was run before label updates.

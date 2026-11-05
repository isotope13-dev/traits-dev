# AVIF mislabeled-good review, 2026-11-04

Thirty-eight files are AVIF images with complete `ftyp`, `meta`, and `mdat`
top-level boxes and no trailing bytes. Local slow scans of hash-identical
hard links report no suspicious or hostile traits. Their endpoint ruling is
good. Validation passed after the concurrent worktree edit, and Hopper
confirmed all 38 good labels (no-ops).

`e306b46366ec` is a C2PA Rust library and tool source archive, not an AVIF
image. The no-follow slow scan reports no suspicious or hostile traits.
Endpoint ruling: good; validation passed and Hopper confirmed the good label
(no-op). The same artifact also appears in the WAV pool.

The remaining `67ceb2fb2cd8` artifact is a Bitwarden disk image, not an AVIF
image. It remains under review.

# WAV bad-label review, 2026-11-04

Completed: **1 bad, 4 good**. Full validation and Hopper recording passed; the final verification section supersedes earlier chronological pending notes.
Five snapshot entries were directly inspected. Proposed dispositions: **1 bad, 4 good**; Hopper recording is pending full validation.

`650bc1eaa358` is a RIFF ACON animated-cursor exploit, not WAVE audio. Its 897-byte body repeats an ANI header with an oversized overwrite region and contains x86 API-hash resolution plus a downloader/launcher. Independently computed the ROR13 hashes: CreateProcessA (0x16b3fe72) occurs at offset 680 and URLDownloadToCacheFileA (0x054fef4f) at 700; a literal HTTP executable destination follows. These implemented exploit and payload bytes establish bad. Both scanners retain three distinct hostile findings for the overflow, API-hashed shellcode and download/launch stage. A failed audio parse is not the basis of the ruling.

The remaining four are ordinary mono PCM sound clips. Inspected RIFF boundaries, fmt/fact/LIST/data chunks, frame counts, sample widths and rates. Every declared RIFF extent and chunk extent ends exactly at EOF, with no appended payload. `6dff2b7f3546` is unsigned 8-bit/22,000 Hz (47,104 frames), `cfec5690a059` unsigned 8-bit/9,000 Hz (16,606 frames), `a330af7a680b` signed 16-bit/44,100 Hz (93,312 frames), and `f5de072c2aac` signed 16-bit/44,100 Hz (208,512 frames). Their origin in a RAT resource directory does not make the individual sound assets attack code. No executable or script stage is present in the inspected structure.

The notify clip's PCM bytes accidentally spell `<?=` at offset 42,521, followed by binary sample values. Corrected the media PHP opener observation so a short echo form requires an ASCII expression with a closing PHP tag; the full `<?php` form remains recognized. Added the real sound clip as a renamed compressed notable regression, plus a valid PCM fixture containing an actual harmless `<?=123?>` expression. The accidental audio sequence clears; the real expression remains notable. This is a syntax/context correction, not a blanket audio exemption. Both final original-package scans have zero suspicious/hostile findings for all four sound clips.

Reports and facts are under `/var/tmp/remaining-media-review/wav/<prefix>/`; final batch log is `/var/tmp/remaining-media-review-final.log`. Matching-trait readability/accuracy review is complete. No engine feature was added. Global validation is currently failing on shared-checkout taxonomy admission, well-known filter requirements and one directory budget, so this TODO item remains open.


## Final verification and disposition recording

Full `make validate` passed after rebuilding the existing validator fixes and correcting the plain split-name control classification. The later comprehensive pass includes all new media and XML controls: 3,322 hostile, 2,094 suspicious, 9,625 notable and 1,420 baseline fixtures (`/var/tmp/xml-complete-fixtures-validation2.log`). No scanner feature was added in this review.

Hopper confirmed all nineteen bad rulings in the VHD/Wasm/media batch as noops. The eleven-good request timed out after partially committing; a subsequent read-only dry run proved seven already good and four still pending. Retried only those four, individually; all moved successfully. The malformed WebP was successfully moved to inconclusive through the installed CLI compatibility target `purgatory`. No request was blindly replayed based on an observation timeout.

This filetype is complete: **1 bad, 4 good**. Earlier pending-state notes are chronological. The overall TODO remains active.

# VHD bad-label review, 2026-11-04

Completed: **14 bad**. Full validation and Hopper recording passed; the final verification section supersedes earlier chronological pending notes.
Fourteen VHD images are scheduled for cleave and atomscan; partial output is in `/var/tmp/triage-vhd-scans.jsonl`. `7z l` confirms that they contain disk filesystems. The full review and Hopper dispositions remain open.

- `1d59b6209242`, `76f921f3a90e`: existing hostile findings in both scanners. Each image combines an LNK, an obfuscated CMD chain and a `.tmp` library invoked through a constructed `rundll32` command.
- `43a1c18af9fd`, `0a5b828bc9aa`: LNK plus hidden DLL and batch file; the batch constructs `rundll32` and its target DLL and export from single-letter variables.
- `74d9779cfb93`: installer requests elevation, adds broad Defender exclusions, downloads files and runs one of them.
- `d9eee2750212`, `ad2ba0c81073`: invoice-themed batch files use extensive environment-variable obfuscation and encoded payload fragments; full decoded behavior and scanner coverage remain to be checked.
- The remaining images contain PDF-named shortcuts or executables, heavily padded JavaScript, or invoice-themed VBScript. Inspect the actual targets and scanner results before classification.

## Resumed review evidence

All fourteen original images have now returned scanner results. Thirteen have hostile findings in both scanners and their bad labels were confirmed in Hopper (13 noops). `0a5b828bc9aa` succeeded on retry after an earlier empty JSON response.

Added `batch-alphabet-dll-launch`: at least twenty single-letter assignments combined with a variable-built DLL execution command. Both scanners flag the extracted launchers from `43a1c18af9fd` and `0a5b828bc9aa`; changing the constructed executable suffix from 32 to 64 clears this finding in both. Original image rescans for this new component finding remain outstanding. `make validate` and `git diff --check` pass.

The invoice batch and VBScript images (`d9eee2750212`, `15bebd4f7e43`, `c3439db3bfdd`, `ad2ba0c81073`) have 3–15 hostile findings per scanner; `74d9779cfb93` has four, and `79d7036b030d` has two. Full matching-trait review remains necessary before completing x-improve.

`524c411868be` remains open: its JavaScript entry is 314,572,800 bytes, but stripping trailing NUL padding leaves 9,316 bytes. Both original scans report zero hostile findings. Static reversal of its permutation and dictionary decoder reconstructs another encoded stage using `eval`; no sample code was executed. Working artifacts are `/var/tmp/vhd-524c-active.js`, `/var/tmp/vhd-524c-decoded.js`, and `/var/tmp/decode-vhd-524c.py`. Finish decoding and assess the original-image detection limits before deciding its disposition. Do not treat an unfinished decode as an inconclusive classification.

### Static decoding completed

The next permutation stage was decoded without executing the sample (`/var/tmp/decode-vhd-524c-stage2.py`, output `/var/tmp/vhd-524c-stage2.js`). It implements persistence, host inventory reporting, command polling, returned-script execution, and self-update. This establishes a bad disposition for `524c411868be`; the original detection check remains in progress after splitting script/archive rule declarations to satisfy validation. The decoded code's behavior, not the archive filename, establishes the classification.

Added `js-permutation-constructor-stage`, combining character-array swaps, string joining, a decoded property lookup and dynamic stage construction. Both scanners flag the extracted active script; replacing dynamic function construction with a string conversion clears the new finding in both. Before separating file-type declarations, both scanners also flagged the original VHD. Verify the final split rules on the original before closing this item. Final scan output is being saved to `/var/tmp/vhd-524c-final-scan.json`.

A validation run observed eleven fixture paths moved by concurrent work during the run; the files exist under their new notable paths. A fresh full validation is running (`/var/tmp/triage-vhd-validate3.log`). Do not restore stale copies over those moves.

VSIX initial scans have started separately (`/var/tmp/triage-vsix-scans.jsonl`, script `/var/tmp/triage-vsix-scan.py`); individual review and dispositions remain outstanding.

Final cleave scan confirms the script rule fires on both the nested JavaScript and original VHD via normal archive aggregation. Removed the redundant archive-only declaration, which never fired directly. The two other permutation findings are suspicious and accurately describe intermediate decoding.

Final atomscan output (`/var/tmp/vhd-524c-atom-final.json`) confirms the final script-only permutation rule fires on both original VHD and nested JavaScript. Full validation subsequently passed in `/var/tmp/triage-vhd-validate3.log`.


## Fresh full-report review and corrections

Re-extracted all fourteen originals under `/var/tmp/vhd-final-review/<prefix>/contents`; full cleave and atomscan reports are preserved beside each extraction. All fourteen completed both scanner passes (`/var/tmp/vhd-final-review.log`), including original-image matches for both alphabet-obfuscated DLL launchers and the padded JavaScript decoder. The reports contain 705 distinct cleave trait IDs, reviewed in `/var/tmp/vhd-traits-review.txt` and `/var/tmp/vhd-traits-additional.txt`. The previous 13 confirmed-bad dispositions remain; the decoded JavaScript image's final Hopper confirmation is still outstanding.

Static reconstruction of the four invoice batch/VBS variants uses `/var/tmp/decode-vhd-batch-review.py`; it parses strings and expands assignments as data without invoking a shell. The recovered stages patch AMSI provider scan callbacks and optionally EtwEventWrite, recover further script from batch comments, AES-CBC/PKCS7-decrypt and GZip-decompress payloads, and invoke .NET assembly entrypoints. These implemented attack stages establish bad independently of invoice names or scanner verdicts.

The June 2024 image's document-named PIF is an OpenVPN executable packaged beside a substituted `libcrypto-1_1-x64.dll`. Independently parsed the DLL's exports: all 4,397 exported names resolve to one address (0x180001000), whose disassembly is not an OpenSSL implementation. The native bitmap/AES/silent-MSI launcher findings belong to that substituted DLL, not the signed runtime helper or the OpenVPN filename. Review artifacts: `/var/tmp/vhd-79-libcrypto-exports.json` and `/var/tmp/vhd-79-libcrypto.asm`. A generic OpenVPN-path/enumeration/copy-import profile on the launcher does not prove collection from the VPN configuration directory; moved it to a notable capability profile, retaining the separate source-argument-bound collection rule.

Corrections from matching-trait review:

* NTFS's UTF-16 uppercase map is misidentified as ICO by its header. Its bytes accidentally contain the short PHP opening-tag sequence and appear to the media parser as high-entropy trailer data. Excluded the already recognized, content-verified NTFS table from those two media observations; preserved the table's notable identity. Added a renamed mapping-table control, compressed for fixture storage.
* A Windows Internet Shortcut opening an SSL WebDAV share does not establish payload execution. Moved the composite to WebDAV capabilities at notable and made the bare URL reference notable. Hostile document-lure/remote-scriptlet and archive-plus-batch execution composites remain unchanged. Added an ordinary WebDAV shortcut control.
* Relocated the bounded .data entropy observation from obfuscation objectives to section metadata, preserving its matcher and updating consumers.
* The chunked Base64 observation matches Reflection/Assembly/ReadAllLines fragments, not a Load call by itself. Corrected its description and made it notable; encrypted reflective-loader composites still require additional evidence.
* Relocated the neutral SysWOW64 PowerShell path and fiber/API profile to their capability subjects. The removed redundant fiber-profile OR leg implied two retained alternatives, so it added no matches. The hostile fiber decoding and registration-unpacker rules remain.

No engine features were added. Validation is currently prevented by a concurrent interactive rebase in the shared checkout, including unresolved taxonomy/reference conflicts. Do not mark VHD complete until those are resolved, the final full validation passes, and the original images are checked with the final rules. Earlier failed validation logs are `/var/tmp/vhd-final-review-validate*.log`; no final pass is asserted here.


## Final verification and disposition recording

Full `make validate` passed after rebuilding the existing validator fixes and correcting the plain split-name control classification. The later comprehensive pass includes all new media and XML controls: 3,322 hostile, 2,094 suspicious, 9,625 notable and 1,420 baseline fixtures (`/var/tmp/xml-complete-fixtures-validation2.log`). No scanner feature was added in this review.

Hopper confirmed all nineteen bad rulings in the VHD/Wasm/media batch as noops. The eleven-good request timed out after partially committing; a subsequent read-only dry run proved seven already good and four still pending. Retried only those four, individually; all moved successfully. The malformed WebP was successfully moved to inconclusive through the installed CLI compatibility target `purgatory`. No request was blindly replayed based on an observation timeout.

This filetype is complete: **14 bad**. Earlier pending-state notes are chronological. The overall TODO remains active.

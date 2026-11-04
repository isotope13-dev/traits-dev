# VHD bad-label review, 2026-11-04 (in progress)

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

# Wasm bad-label review, 2026-11-04

Completed: **1 bad**. Full validation and Hopper recording passed; the final verification section supersedes earlier chronological pending notes.
The snapshot contains one artifact: `cc9e0c4ca0bc22ecf86feed59250cd074f98fbeb485e5d6ca50eb5ca9d99a704`, 44,765 bytes. Direct inspection supports **bad** as dedicated Donut shellcode-generation tooling. Its location beneath Sliver is not the classification evidence.

Parsed exports/imports/memory, inspected the Wasm disassembly, and compared the exact module with the [upstream wasm-donut implementation](https://github.com/sliverarmory/wasm-donut/tree/main/donut). The module exports `donut_generate`, malloc/free and Emscripten helpers, with only random-input, file-close and memory-growth imports; it has no Wasm start function. It produces native execution payloads rather than directly invoking Windows APIs through Wasm imports. Do not describe the Windows API strings as imported host capabilities.

Both embedded native loader arrays exactly match upstream: x86 is 11,647 bytes at file offset 19,682 (SHA256 `0c29cccff1b027d57c467564a333e9ade455144649909a4b797b09b43002ac71`), and x64 is 13,430 bytes at 31,330 (`da0ac2320629d45cd2669a4a21003ecde56bd11f73fa8bfb21abec3863407a1f`). All module sections except CODE match the fetched upstream Wasm byte-for-byte. Eighteen of nineteen function bodies match exactly; the generator body differs by eight bytes, so this is not asserted to be an identical upstream build. The wrapper validates executable/script input and configuration, builds the payload module/instance/loader and returns loader bytes to its caller. Native templates and configuration support in-memory execution, encrypted modules and security-scanning/tracing bypass. Those implemented dedicated offensive capabilities establish bad independently of licensing, research branding or clean initial scanner output. No sample code was executed.

Evidence is preserved at `/var/tmp/wasm-donut-facts.json`, `/var/tmp/wasm-donut-disassembly.txt`, `/var/tmp/wasm-donut-loader-comparison.json`, `/var/tmp/wasm-donut-section-comparison.json` and `/var/tmp/wasm-donut-source-review`. The upstream source ZIP is stored locally; the exact sample is not replaced by it.

Added a narrowly named hostile Donut Wasm generator finding requiring the parsed generation export and embedded native loader-template bytes. Native-template and export observations remain separately notable. The original is hostile in both cleave and atomscan. An independently constructed valid Wasm control exporting the same name but returning zero, with inert padding and no native loader, has zero suspicious/hostile findings in both. This checks that an export name alone does not establish a payload generator. Original/control fixtures are under `testdata/{hostile,notable}/generated/wasm-donut-review/`; control reports are `/var/tmp/wasm-donut-{original,inert-export}-{cleave,atom}.json`.

The initial three matching traits described the Emscripten export, Windows runtime DLL string and Windows script-host reference accurately. The added family observations distinguish embedded native payloads from Wasm host imports. No engine feature was added. Full validation and Hopper recording remain pending due to shared-checkout taxonomy validation errors after the concurrent rebase. Do not check the TODO item yet.


## Final verification and disposition recording

Full `make validate` passed after rebuilding the existing validator fixes and correcting the plain split-name control classification. The later comprehensive pass includes all new media and XML controls: 3,322 hostile, 2,094 suspicious, 9,625 notable and 1,420 baseline fixtures (`/var/tmp/xml-complete-fixtures-validation2.log`). No scanner feature was added in this review.

Hopper confirmed all nineteen bad rulings in the VHD/Wasm/media batch as noops. The eleven-good request timed out after partially committing; a subsequent read-only dry run proved seven already good and four still pending. Retried only those four, individually; all moved successfully. The malformed WebP was successfully moved to inconclusive through the installed CLI compatibility target `purgatory`. No request was blindly replayed based on an observation timeout.

This filetype is complete: **1 bad**. Earlier pending-state notes are chronological. The overall TODO remains active.

# Decompression boundary fixtures

Twenty-one static-analysis inputs cover named algorithms, generic decompression,
codec interfaces, ordinary stream reading and nearby compression-only behavior.
Nothing is executed. The PE uses import scaffolding; the DEX files contain only
strings and type references, following the [AOSP DEX specification](https://source.android.com/docs/core/runtime/dex-format).
Source files, build commands and hashes make the binary controls reproducible.

`cases.json` records current matcher behavior with a prospective relocation map.
`make validate` uses `--before` while the IDs remain in their original homes.
All 53 proposed rules now have positive matcher controls, alongside near misses.
That does not approve their placements. Low-value aggregates may be omitted from
scan output; matcher traces and complete reports are checked separately.

Batch 010 corrects the historical weak boundaries captured in batch 009:
compression-only, GZipStream-name-only and ordinary StreamReader evidence no
longer satisfy the runtime-decompression aggregate. The zlib aggregate now admits
its component languages. Dynamic zlib matching requires the literal zlib import;
bz2 and an unknown module are negative controls. Historical fixture expectations
remain in batch 010's before snapshot for rollback.

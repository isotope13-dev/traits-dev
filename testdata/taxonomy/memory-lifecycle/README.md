# Mapping and memory lifecycle cases

Run through `scripts/check-taxonomy-cases.py` and `make validate`. Seventeen
specimens cover mapping versus unmapping and permission-only evidence, direct
syscall RX/RWX arguments, remapping, MIPS mapping/cache-flush pairing, kernel free
versus its existing UML exclusion, and CUDA query versus allocation. The Go and
Rust name-reference cases retain their matchers' limited evidence level.

The mmap import fixture also verifies the existing `mmap-symbol` suppression.
That redundant matcher is not counted as an independently witnessed capability.

`fixture-build.json` records compiler/linker commands and binary hashes. Sources
are in this directory and `build/`. All specimens are scanned without execution;
the syscall and cross-architecture files are static-analysis inputs.

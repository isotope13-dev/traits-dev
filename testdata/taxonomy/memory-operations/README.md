# Memory operation fixtures

`cases.json` is executed by `scripts/check-taxonomy-cases.py` and `make validate`.
It checks matcher truth separately from emitted findings, including inherited
PE-only scope, Python call versus reference, zero versus nonzero fill, overlapping
operations, and three versus two vector stores. Every moved rule has a positive
case; near misses use the same engine. No specimen is executed.

The five PE files are minimal, deliberately non-runnable static-analysis inputs.
Their C sources and import definition are in `build/`; the exact compile/link
commands and specimen hashes are in `fixture-build.json`. Build with clang,
llvm-dlltool and lld-link. Intermediate `.obj` and `.lib` files are disposable.
The Python bytecode is compiled from `taxonomy-memory-name.py` without running it.

Fixtures live here to preserve neutral paths for dedicated matcher tests. The
runner copies them to temporary paths; it also compares complete emitted findings,
suppression, component edges and risk with the recorded pre-migration reports.
Existing corpus fixtures and score expectations remain unchanged.

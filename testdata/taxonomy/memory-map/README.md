# Mapping and unmapping placement checks

Run `python3 scripts/check-taxonomy-memory-map.py` from the repository root.
`make validate` also runs it. `cases.json` identifies the specimens in
`testdata/benign/`; scans use temporary paths outside the rule repository.

The cases cover mapping only, unmapping only, both operations, heap allocation
as a near miss, and an ELF import/suppression check. The ELF was built with:

```
cc -O0 -o testdata/benign/taxonomy-map-unmap.elf testdata/benign/taxonomy-map-unmap.c
```

The executable is only a static-analysis fixture. The check never executes it.
The `test-rules` check matters: baseline ELF observations may be filtered from
normal scan output even when their matchers fire.

For migration comparisons, `--before` translates old IDs to their intended
destinations; `--record PATH` stores all emitted findings/suppressions and the
import trace; `--compare PATH` requires identical normalized findings. This
translation does not suppress differences in evidence, criticality, confidence,
or scores.

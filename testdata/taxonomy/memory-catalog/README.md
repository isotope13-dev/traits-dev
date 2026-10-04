# Memory catalog reporting

The four cases run through `make validate`. They assert emitted MBC fields as
well as matcher truth: VirtualAllocEx import/name observations use C0007 (Allocate
Memory), and libc munmap uses C0044 (Free Memory). C0032 denotes Checksum.

The source call also matches the import observation, which suppresses the dedicated
source atom. Check that existing behavior rather than claiming a separate positive
witness. Its own scalar mapping is covered by the declaration comparison.

PE build commands and hashes are recorded in `fixture-build.json`; no specimen
is executed. The Rust unmapping fixture is shared with the lifecycle suite.
`mbc_updates` permits only the exact reviewed old/new values during comparison;
all other finding fields, graph edges, suppression and scores remain identical.

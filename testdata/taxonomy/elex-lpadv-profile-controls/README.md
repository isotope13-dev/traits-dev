# Elex LPADV profile matcher controls

These four files are synthetic PE controls for the 11 LPADV composite IDs. The
positive fixture satisfies the current static signature conjunctions; the
three near misses remove the LPADV PDB path, the `CShareMemory_` marker, or the
browser error-handler literal. `cases.json` requires every moved profile in
the positive and forbids the affected profile IDs in the corresponding near
misses.

The PE entry point returns immediately. Its marker strings and imports are
inert; it does not execute the APIs or browser code represented by those
strings. These fixtures test matcher satisfiability and rule thresholds only.
They are not malware samples and do not establish that any profile describes
executed malware behavior.

`control.c`, `positive.rc`, and `build-controls.sh` reproduce the controls with
Clang, LLD, `llvm-dlltool`, and `llvm-rc`. The checked-in binaries were built
with the corresponding LLVM tools in the local environment and scanned with
Cleave 3.0.0-beta.1, traits revision `c254831e4`, engine SHA-256
`c0abd17a47e98b2a98b24b179210a9564c8170feec8cf9b4fa6f753c49c9a378`.

The PE timestamp is supplied by the linker, so rebuilding can change the
binary hashes without changing the matcher controls. These hashes bind the
checked-in build:

| Fixture | SHA-256 |
| --- | --- |
| `positive-all-profiles.exe` | `0314f1105070d93f10ee58840efe7c723e4fc98ed02242e663a23cdb80eb1d41` |
| `near-miss-service-host-pdb.exe` | `9d85cabf6fa6915f21e283063f53816add59319d428be375b446ed6c2fa6faaa` |
| `near-miss-browser-cshare.exe` | `f3bdbe07b2374913fcec27e0e7c09625c4f32ac4a899b807b6881fee3a91fa1b` |
| `near-miss-browser-handler.exe` | `d972724ef717901386d60cb6c227ed80b9c5f7fd71739c175be65416b5845eab` |

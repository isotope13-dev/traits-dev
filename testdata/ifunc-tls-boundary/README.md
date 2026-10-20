# Intel compiler runtime / IFUNC and TLS boundary

Verdict: **BENIGN** for `intel-cmplr-lib-rt` 2026.1.1, Linux x86-64 wheel
SHA256 `1e96ceb1e84336a09956f7ad421f699163ece66bcdc7de547b41733eb853d4ce`.

## Release comparison and execution paths

Fetched the matching Linux wheels from the PyPI JSON release URLs and verified
their published SHA256 digests:

- 2026.1.0: `8e002aaf89741de3b424bdad51ce60ead21cc8f4dee970fccba88ee3c845692d`
- 2026.0.0: `a8ff1f8ec28a50dddd02e47c6d47eb6b758842103571956f419a53ebb6513d2d`

No members were added or removed versus either release. The wheel contains
native compiler/common runtime libraries, package metadata and a linker script;
there is no Python source or install hook. The current wheel's digest also
matches its PyPI release record.

The firing `libirng.so` differs from 2026.1.0 in exactly five bytes, all in
`.comment`: compiler `2026.1.0 (2026.1.0.20260617)` became
`2026.1.1 (2026.1.1.20260724)`. All other bytes, including code, relocations,
imports, IFUNC symbols, TLS and RNG tables, are identical. Against 2026.0.0,
seven compiler-version/date bytes changed; code and data are still identical.
The `.text` SHA256 across all three is
`7d40d702051a4cbdd57cafac072dea67c5c6127ccaf7bb55f3536cfb24aef443`.

Rizin disassembly of 2026.1.1 establishes:

- `_simd_drand48_pd64x4.resolver` at VA `0xa42b0` tests
  `__intel_cpu_feature_indicator_x`, initializes that CPU feature word if zero,
  and returns the `.A` or `.V` implementation pointer. Those stubs lead through
  PLT entries to the AVX1 and AVX2 RNG implementations. Other SIMD resolvers
  select equivalent implementations or reject unsupported CPUs.
- `lcong48`'s resolver at `0xa46b0` likewise selects an implementation from
  CPU feature bits. It neither calls the TLS resolver nor patches an unrelated
  function.
- `drand48` at `0xa1c30` updates its seed using multiply/add and a 48-bit mask.
  Vector variants implement corresponding RNG arithmetic with SIMD instructions.
- `svrng_sse2_set_status` at `0xa6560` calls `__tls_get_addr`, reads the old
  four-byte status and stores the supplied status. `get_status` at `0xa67e0`
  retrieves that word. SSE2, AVX2 and AVX512 each have a four-byte TLS status.
  TLS calls in engine wrappers report errors/status independently of IFUNCs.
- The only foreign imports are CPU feature support, TLS address resolution,
  aligned allocation/free and Intel memcpy helpers. There is no network,
  command execution, credential access or payload loader in this library.

Most other libraries changed only their compiler comments versus 2026.1.0;
`libqkmalloc.so` is byte-identical. The larger `icx-lto.so` is LLVM compiler/LTO
code. Its function population remains 125234; the single function-name
replacement concerns loop-collapse dependence distances, with other size
changes in optimizer/backend routines. Compiler process/filesystem operations
are consistent with that purpose. Decoded-string facts were inspected as well:
the RNG's three XOR-stack candidates are short arithmetic artifacts, not a
decoded payload. The compiler's apparent `RuntimeService` evidence is the
source filename `RuntimeService.cpp` and LLVM class symbols, not CRI.

## Trait dispositions

- Retire `ifunc-with-tls-resolver-import` and `ifunc-in-utility-lib`. The first
  infers hijacking from ordinary co-occurrence; the second is an IFUNC alias
  whose exclusions establish no library identity. Existing neutral IFUNC and
  loader-dependency facts retain the actual observations.
- Move `imports-tls-get-addr` to `micro-behaviors/process/tls::tls-get-addr-import`,
  retaining its import matcher and ELF/Unix/Android scope, with notable severity.
  Flatten the former `process/tls/fiber` leaf: its eight atoms already cover
  both thread and fiber storage. Preserve all ten Windows rules and scopes,
  updating their exact references and the live stranded-member fixture cases.
  Dated migration snapshots retain their historical IDs.
- Move the ELF branch of sparse-loader API detection into `dylib/lookup`.
  Retire the redundant `elf-concealed-capability` inference. The old PE branch
  stays scoped to PE. Preserve the code-cave consumer's loader alternative;
  remove its weak ELF shell-only alternative. Shell execution retains its
  existing independent capability trait. The old grouping's dlopen alternative
  was an inert text-only compatibility placeholder; reference canonical dlsym
  directly to preserve its effective ELF coverage.
- Move the small ELF `.rodata` observation to `metadata/binary/section/size`.
  Preserve the 100000-byte file floor, 100-byte section ceiling and structural
  exclusions. Drop behavioral vDSO/BPF exclusions: a size observation does not
  change meaning in their presence. The existing explicit vDSO-name exclusion
  remains. Update its consuming payload rule without changing that rule's roles.
- Require a qualified CRI RuntimeService name, so an LLVM filename no longer
  supplies container evidence.

Exact and ancestor reference searches found no positive consumers of the
retired IFUNC IDs. Their linker-directory suppressor consumers intentionally
stop treating a generic IFUNC as attack context. Removing the TLS import from
runtime metadata does not remove the ordinary ELF dynamic-linking facts used
by the runtime-directory suppressors. There are no direct dylib-lookup directory
consumers; the added lookup finding therefore introduces no directory-based
cardinality change. The new TLS home is a single leaf with 11 rules.

## Controls

`cases.json` covers a real ELF import versus an export and a string mention,
sparse ELF loader operations, small `.rodata`, and qualified CRI names versus
the compiler filename. The first ELF intentionally has ordinary initialized
data so the existing size gates are exercised. All three ELF fixtures were
built from their adjacent source with:

```sh
zig cc -target x86_64-linux-gnu -shared -nostdlib -O1 import.c -o import.elf
zig cc -target x86_64-linux-gnu -shared -nostdlib -O1 export.c -o export.elf
zig cc -target x86_64-linux-gnu -shared -nostdlib -O1 string.c -o string.elf
```

The existing FLS+thread, FLS-only and thread-only PE controls also verify the
relocated Windows rules. The supplied wheel and prior `libirng.so` are scanned
again to verify that ordinary runtime evidence remains without the IFUNC
hijacking inference.

# Dropper staging: encrypted leaf audit

## Boundary and findings

The question for `dropper/staging/encrypted/` is whether encryption itself is
the useful staging characteristic, or whether the matcher already identifies a
more specific activation result. The taxonomy's dropper contract assigns a
completed chain to its required sink: direct staged-file launch to
`file-exec/spawn`, command-interpreter launch to `file-exec/command`, source
evaluation to `script-eval`, runtime assembly loading to `module-load`, and
executable memory without a narrower sink to `staging/memory`. Cipher choice,
carrier, and source-language remain evidence or implementation details unless
they define the behavior.

At the cap-100 inventory, the encrypted leaf contained 217 rules in 34 files:
41 atomic observations and 176 composites. The largest coherent group is the
88-rule `7z-aes-exe.yaml` archive cohort. Those classifiers require encrypted
archive-member or header evidence and describe the concealed contents; retain
them in `staging/encrypted` under the existing precedence rule. Archive
membership without required encryption remains in `staging/archive`.

The rest of the leaf mixes encryption indicators with a range of completed
outcomes. Two unambiguous placements were corrected. Electron ASAR decryption,
temporary EXE writing, and hidden child launch form a staged-file spawn chain;
the four rules now live in `dropper/file-exec/spawn/electron-asar.yaml`. CryptoAPI
file decryption and inline-PE decryption both establish executable-memory
staging without cross-process transfer; those two rules now live in
`dropper/staging/memory/capi-payload-decrypt.yaml`.

## Preservation evidence

Neither move changes matcher bodies, scope, criticality, confidence, or mappings.
Both moved files are byte-identical to their pre-move definitions. The Electron
file's SHA-256 is
`7a3b87bdea4806863ba29087d31a471c0891c4e1bbe3fb726c837e84c0419bcd`; the
CryptoAPI file's SHA-256 is
`93b903fcf6f3326dfacc1efae48c968c63ef7cefba49700fc874449410e9918e`. No
external references used the Electron IDs. The two consumers of
`capi-inline-pe-memory-loader` now use its `staging/memory` ID. The encrypted
leaf falls **217 → 211**; `file-exec/spawn` rises **64 → 68**, and
`staging/memory` rises **131 → 133** before later sink corrections.

The prebuilt `cleave 2.12.0-beta.2` binary was run with
`validate --soft --exclude qual/no-pattern` after the moves. It reports no
broken reference for these IDs, and its fixture check still fails on three
paths in the benign `pyaigis-top10.tar.xz` archive matching the unrelated
`anti-static/obfuscation/payload/encoded::shell-eval-base64-decode` rule. I
discarded my attempted before/after comparison: it used hard-linked files, and
concurrent edits to other traits propagated into the temporary tree during the
run. The normal `make validate` build remains blocked because the checked-out
`stng` revision does not expose `decode_xor_fat_macho`. The API exists in the
adjacent, uncommitted `stng` working tree; a temporary Cargo patch to that tree
allowed a current-source soft validation, but it still reports unrelated
validator issues and the known benign fixture matches. This does not replace a
clean strict validation against the pinned dependency.

## Remaining audit

The encrypted leaf remains over cap at **188 rules** after a follow-up URL and
assembly-load review: 37 atomic traits and 151 composites across 29 files, or
88 above the cap. The follow-up
[passworded 7z sink audit](DROPPER-7Z-SPAWN-SINK.md) and [encrypted sink-routing
audit](DROPPER-ENCRYPTED-SINK-ROUTING.md) move completed chains to their
required file-spawn, script-evaluation, or module-load behavior homes. Their
source, cipher, and carrier observations remain available through the preserved
cross-directory references. Do not create subdirectories just to divide the
remaining count; continue evaluating every rule against its required sink,
actual content subject, and nearest siblings.

The adjacent `staging/memory` leaf remains oversized at 126. Three
TCC-manipulation composites and four PowerShell AppDomain loader composites
have since moved to their existing behavior homes; see the [TCC
audit](TCC-APPLE-SECRET-MANIPULATION.md) and [AppDomain sink
audit](DROPPER-APPDOMAIN-SINK.md). `staging/archive` has 81 rules and is the
nearest competing home for archive-specific classifiers; preserve the
documented encryption precedence while auditing its own leaves and siblings.

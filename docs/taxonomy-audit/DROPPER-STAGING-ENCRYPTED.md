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
outcomes. The audit confirmed one unambiguous misplacement: Electron ASAR
decryption, temporary EXE writing, and hidden child launch form a staged-file
spawn chain. The four rules now live in `dropper/file-exec/spawn/electron-asar.yaml`.
The three component observations remain beside their consumer, and the
composite now has the same canonical sink as other direct staged-file launches.

## Preservation evidence

The move changes no matcher body, scope, criticality, confidence, or mapping.
The file's SHA-256 is identical before and after (`7a3b87bdea4806863ba29087d31a471c0891c4e1bbe3fb726c837e84c0419bcd`); only the namespace derived from its directory changes. A repository search found no external references to the four IDs, so no consumers needed edits. The destination `file-exec/spawn` rises from 64 to 68 rules; the encrypted leaf falls from 217 to 213.

For before/after corpus comparison, the prebuilt `cleave 2.12.0-beta.2` binary
was run with `validate --soft --exclude qual/no-pattern` against a hard-linked
pre-move snapshot and the moved tree. Both runs report the same 100 authoring
issues and the same single fixture-gate failure: three paths in the benign
`pyaigis-top10.tar.xz` archive match the unrelated
`anti-static/obfuscation/payload/encoded::shell-eval-base64-decode` rule. The
current `cleave` source cannot be rebuilt yet because its shared worktree has
unrelated `filefacts`/`stng` API mismatches; the prebuilt binary still enforces
the old 85-rule cap. Therefore this comparison establishes no corpus delta for
the move, but it does not replace a fresh strict run on the updated engine.

## Remaining audit

The encrypted leaf remains over cap at 213. Its remaining rules need the same
sink-by-sink review; do not create subdirectories just to divide the count.
The adjacent `staging/memory` leaf is also oversized at 131 and mixes actual
memory staging with file launch, script evaluation, module loading, and remote
retrieval descriptions. Review it with the encrypted leaf so complete chains
move to one required sink and neutral source/decrypt observations stay
canonical. `staging/archive` has 81 rules and is the nearest competing home for
archive-specific classifiers; preserve the documented encryption precedence
while auditing its own leaves and siblings.

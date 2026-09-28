# Encrypted dropper chains follow their activation sink

The encrypted staging leaf contained completed chains with three different
sinks. Four chains requiring `new Function`/`eval` moved to
`dropper/script-eval`; the `Module._compile` chain moved to
`dropper/module-load`; and the 2,048-byte bounded decrypt/write/chmod/detached
launch chain moved to `dropper/file-exec`.

The source file's platform, language, attack and MBC defaults were copied to
the destination files. Rule IDs, matcher predicates, proximity bounds,
criticality, confidence, exclusions and effective scopes remain unchanged.
No external exact-ID consumers referenced these rules. The FTP-banner
aggregate already includes the file-exec sink; there were no directory
aggregators over the encrypted staging leaf.

The zero-IV detached-launch rule stays in encrypted staging pending a tighter
stage-to-launch relationship: it requires decryption, a file write and a
detached spawn but has no proximity bound. The bracket-zero-IV rule also stays
there because it does not establish that decrypted output reaches an execution
sink. Neither is assigned an activation category based on its current name.

Soft validation passes **1,837/1,837 fixtures**. `staging/encrypted` drops
from **293 to 287 rules**; `script-eval` now contains **4**, `module-load` **8**,
and `file-exec` **72**. Strict validation remains at **59 issues**, including
**165 over-cap directories**, with no new migration-specific warnings.

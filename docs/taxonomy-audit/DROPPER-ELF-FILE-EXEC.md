# ELF download/chmod/execute audit

`download-permission-execute-chain` requires both `native-download-then-chmod`
and `chmod-then-local-execute-command`. Together these identify a probable
native file-launch chain, so the composite moved from
`delivery/execute-download` to `dropper/file-exec`. Its supporting
`native-download-then-chmod` trait stays in the legacy leaf and is referenced
by exact ID from the new home.

The matcher and effective scope are unchanged. Eight consumer files were
updated across nine exact-reference occurrences; no consumer was removed. The
mapping ledger records each update.

Soft validation passes **1,837/1,837 fixtures**. Strict validation still
reports catalog-wide quality debt, including **165 over-cap directories**.

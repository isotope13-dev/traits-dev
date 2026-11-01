# Legacy memory-staging retirement

The last 26 rules moved out of `dropper/staging/memory`, and the directory was
removed. Concrete socket/read/jump chains and CryptoAPI/memory/thread evidence
now sit under native payload activation. Manual PE mapping is grouped under
image mapping; the EVM-resolved AppleScript pipeline uses interpreter stdin;
and generic `curl | osascript` and Mach-O module-loading observations use
micro-behavior destinations. The VxWorks-associated receive/mapping combinations
move to acquisition or reconstruction; the short `VXWS`/`SWXV` observations
are retained as firmware-related markers without treating the marker alone as
proof of a platform or payload.

Go function names, a sparse kernel-callback combination, and Mach-O memory APIs
now describe their observed evidence instead of claiming decryption or an
executed stage. Their severity is suspicious or notable. The original match
conditions, scopes, architectures, size bounds and exclusions were checked, and
exact consumers and the former broad dropper consumer were updated. The empty
legacy Java file contained only a comment and was removed with the directory.

The `curl | osascript` observation was placed under interpreter-stdin deployment
rather than the shell-creation subtree: an existing daemon rule separately
requires the shell-creation directory, and putting the observation there would
make that additional condition redundant and change its meaning.

The neighboring text-shape directory contained 93 rules. Twenty text distribution
and nine command-reference observations moved into their own subject directories,
leaving 64 rules in the original. Parsed comparisons verified all 93 original
rules and their settings after reference updates. The migrated code retains the
existing per-file size bounds; no new evidence established replacement limits.

A Python-scoped `dynamic-dropper` rule also referenced the staging ancestor.
None of the final 26 memory rules applied to Python; three from the preceding
memory pass did, so those exact alternatives were restored. Other previously
migrated staging branches still need the same ancestor-consumer audit.

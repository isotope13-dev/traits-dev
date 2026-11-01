# Native-loader staging retirement

The last 53 rules moved out of `dropper/staging/native/loader`, and the legacy
native staging subtree was removed. Coherent direct-call, memory-protection,
image-mapping, decryption and file-launch combinations now sit under their
likely execution or staging mechanisms. API, installer, symbol and file-write
combinations that do not establish those behaviors became supporting profiles.
The Nuitka/SQLite rule now describes those facts rather than claiming credential
theft from an ordinary database reference. Exact consumers and the broad legacy
dropper consumer were updated; the latter's weak-evidence audit remains open.
All 53 predicates, file scopes, exclusions, size bounds and downgrades were
checked against the original rules.

An Inno 5.5 data marker initially moved to installer-family identity, but that
would have widened installer exclusions and pushed five of them from 64 to 65
rules. It instead lives in the installer-layout profile, without altering the
existing installer-family suppressor. The current limits were not changed.

The adjacent native-spawn directory reached 71 rules. Seven URLMon download
combinations were reviewed and moved to `spawn/fetch` or `spawn/handler` based
on whether the launch uses a process API or ShellExecute. The two former
"signed" descriptions now describe trust-verification APIs rather than claiming
a signature; the supposed sandbox-gated rule now describes its actual admin and
process-enumeration evidence. Their predicates and severity are unchanged.
The six existing 512 KiB limits remain as historical precision bounds; unlike
the seventh rule, which documents larger-bundle coverage, these rules have no
sample evidence here establishing a safe new threshold. They merit a separate
sample-backed review rather than an arbitrary cap change.

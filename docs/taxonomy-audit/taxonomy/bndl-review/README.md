# BNDL encrypted staging review

The legacy bundle rule matches a BNDL executable-name pattern, a ChaCha/Salsa
constant, and high-entropy `.rdata`. Those conditions do not establish that
BNDL bytes are encrypted. Its endpoint variant adds an external IP and port,
not an established command-and-control endpoint. Both now live in
`metadata/file/profile/archive`, with descriptions and IDs reflecting the
observations. The downstream temporary-file/process launch chain remains in
`objectives/execution/payload/file-exec/spawn/native` and references the moved
profile; its description no longer claims an encrypted bundle. Unsupported
attack annotations were removed.

The independent 1 MiB limits on the profile and temporary-launch rule were
removed: neither follows from the conditions. Both also excluded binaries
with 80 or more imports, which does not contradict this evidence and could
hide a matching loader; that exclusion was removed. The signed-platform and
installer-family exclusions remain. These changes can make the downstream
finding match more files, including benign files with the same evidence.

The endpoint leg still has a separate 2 MiB maximum and other exclusions in
`micro-behaviors/communications/ip/endpoint`; several unrelated rules use it,
so those wider effects were not changed in this review. Its description was
corrected from “multiple” to an external endpoint: the condition has no
`count_min`. All other conditions, scopes, and confidence are preserved.

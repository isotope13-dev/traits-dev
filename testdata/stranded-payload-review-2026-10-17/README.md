The 26 listed SecLists and Laudanum members were inspected independently and
marked MALICIOUS beside their extracted paths. The parent archives were not
re-judged. `review.json` records each digest, execution or archive-structure
trace, operational limits, verdict, marker note, and before/after findings.
`marker-notes.txt` contains the exact one-line marker contents for the commit
body.

The ZIP traversal entries carry `hacked\n`, not executable PHP. The overlapping
ZIP bomb declares about 4.5 PB across 190,023 entries; its streams were probed
with bounded decompression. PHP, ASP, and JSP payloads expose operator command
execution; the PHP reverse shells copy peer data to child stdin and return
stdout/stderr. The hidden PHP shell imports request variables and dynamically
calls the chosen function. The WordPress plugin also attempts to make its own
file read-only and immutable. Access gates, undefined reverse-branch request
keys, legacy PHP requirements, and the Debian PHP shell's missing semicolon
are recorded rather than assumed away.

The C stubs request root identity and launch an unguarded shell. They require
existing privilege or a privileged installation. The hostile composites now
require a structural main-body sequence; root and shell calls elsewhere in a
file no longer suffice. Four positive variants and four near misses cover
that distinction. The two PHP stream-copy rules retain their matchers and
scopes under `micro-behaviors/process/io/stream`; their names describe the
observed resource indices without asserting proven child-pipe provenance.
A positive copying fixture and a different-value near miss cover that move.
All ten controls live under `testdata/hostile` or `testdata/benign` and are
registered in `testdata/expectations.toml`.

All 26 members received initial and final atomscan runs plus cleave facts.
Payloads were not executed. The Debian extraction had flattened `data/`; the
seven named members were restored under that prefix with identical hashes.

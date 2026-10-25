# BusyBox documentation and shell redirection controls

The three batch specimens are byte-identical to these members of the official
BusyBox 1.36.1 source release:

| Fixture | Upstream member | SHA-256 |
| --- | --- | --- |
| `ps.posix` | `busybox-1.36.1/procps/ps.posix` | `3f1ac31ea27f3db604ab8b9f8560414a2ebb51ce1c3131c2f2726ab526b33acd` |
| `busybox_header.pod` | `busybox-1.36.1/docs/busybox_header.pod` | `b21f2f2a045239edb91c61876038a387f59f8afa66b62fd9888945b56a486f85` |
| `redirA.tests` | `busybox-1.36.1/shell/{ash,hush}_test/{ash,hush}-redir/redirA.tests` | `ffcd258c9325735737f21a057fd9c684f45687c6a75eb905b8e74ef5d7c55b84` |

Fetched with `forager fetch` from
<https://busybox.net/downloads/busybox-1.36.1.tar.bz2>. The release archive and
its `.forage.json` remain in the task scratch directory, `bad-triage/upstream`.
Matching this version establishes upstream content, not the specimens' original
release version or deployment provenance.

`ps.posix` is a prose specification of process selection and output columns.
Its `userlist` is the operand of `ps -u`/`-U`, not a password-attack dictionary.
`busybox_header.pod` is POD manual text with installation examples. Its
`/tmp/foo` path reference remains accurately detected; it does not itself install
or execute anything. Neither document has an executable entry point, encoded
payload, external URL, or dependency reference.

`redirA.tests` assigns `x=tmp11:tmp22`, removes the shortest `:*` suffix, and
redirects `echo` output into the resulting name. It prints the matching filename
and removes it, then repeats with an unquoted destination. An isolated `/bin/sh
-x` run printed `tmp11` twice, returned zero, and left its temporary working
directory empty. The glob cleanup is retained as a neutral file-delete finding.
It would also remove preexisting `tmp1*` files in its working directory; its
upstream test location supplies the intended context, not a general safety
exemption. There is no network, persistence, secret access, staging, or evasion
path in this eleven-line script.

The external malware attribution has no accompanying deployment evidence.
Bulk attribution from a containing collection or package, or heuristics on
BusyBox/command vocabulary, could explain it. These are possible explanations,
not established provenance. All three artifacts are judged BENIGN from their
complete contents, intended role, and exact upstream matches.

## Shared-rule coverage

The bare `userlist` and `passlist` matches move from a MySQL brute-force
objective to vocabulary metadata, with identical matchers, file-type scopes,
platforms, confidence, and notable severity. The old wordlist descriptions and
T1110.001 mapping were unsupported by those individual words. The MySQL
composite explicitly references the relocated atoms; no suppression or severity
reduction is introduced.

The existing exact consumer is `mysql-credential-bruteforce`, itself consumed by
`warmysqlbrute-tool`. A YAML reference audit found no ancestor-directory selector
depending on the two moved atoms. The original positive fixture from the
introducing commit `d59014b3f9` was recovered by SHA-256 using `forager --hopper`,
and is preserved as `mysql-bruteforcer.htm`:
`e1913aebc4c5f8f9d47a50265725bed397084cbff955c996c6162a709a4e367f`.
Its source reads username and password files in nested loops, resets the password
file for each username, and calls `mysql_real_connect` with each candidate pair.
Both existing hostile findings must remain. The recovered original and fetch
provenance remain under scratch `bad-triage/positive`.

`cases.json` covers all three originals, the original attack positive, harmless
list vocabulary near a MySQL reference, actual output redirection, quoted or
commented redirection near misses, and a POD directive mentioned inline.
New observations cover POD section syntax, a POSIX edition citation, shell
parameter pattern removal, and an echo-to-variable output redirect in text
inputs that lack a shell AST. They do not establish malicious intent.

## Verification results

All eight controls passed. The three original samples each had zero hostile
and zero suspicious findings before and after. Atomscan classified all three
as benign before and after; its installed v18 model reports that newer feature
specification fields are unavailable. No classifier disagreement was observed
for this batch. `scan-comparison.json` records the exact probability and trait
changes. The original MySQL attack retained both hostile findings. No archive
members or encoded executable stages exist in the three batch specimens.

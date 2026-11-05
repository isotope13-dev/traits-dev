# CFML mislabeled-good review, 2026-11-04

`80934cc341a1` is a Pygments syntax example demonstrating ColdFusion date
formatting, variables, and nested output. Its fresh scan reports no suspicious
or hostile traits. Endpoint ruling: good; Hopper confirmed the label (no-op).

`29777403e2f3` is a command webshell: it sends a form-supplied command to
`cmd.exe`, reads the output file, and deletes that temporary file. A new
execution observation independently reports request-controlled command
arguments with an output file. Removing the request argument or output-file
attribute prevents that observation. The original now has hostile traits in
the command-webshell and execution directories. Endpoint ruling: bad.

`987de3c74aaa` executes a request-supplied program and arguments and also
enumerates datasource settings and decrypts stored datasource passwords.
The fresh scan reports hostile command-webshell and credential-access traits
in different directories. Endpoint ruling: bad.

`c28894e4ab24` is a legacy encrypted ColdFusion template. Static DES decoding
using the format's built-in key recovered a password-protected webshell that
accepts file reads, writes, uploads and deletes, executes form-controlled shell
commands, and posts page URL information. The original encrypted template
scans with hostile webshell and execution traits in different directories.
Endpoint ruling: bad.

`make validate` passed. Hopper moved all three bad samples, and their
hash-verified snapshots were placed in `/tmp/triage/misplaced-bad`.

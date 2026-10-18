All 26 named members were inspected independently and marked MALICIOUS at
the supplied extracted paths. The two parent archive verdicts were retained.
`review.json` records each digest, byte-derived behavior, runtime limitations,
final hostile findings, trait changes, and controls. `marker-notes.txt` copies
the marker lines verbatim for the commit body.

The traversal ZIPs overwrite ancestor web content with a defacement banner;
their contents are not executable PHP. The overlapping ZIP bomb declares
4,507,981,427,706,459 output bytes across 190,023 entries. Three bounded raw
DEFLATE probes confirmed real streams without expanding the bomb. Cleave's
65,536-member cap undercounts that full directory.

PHP, ASP and JSP sources expose command execution. Reverse-shell scripts
bridge peer traffic to process streams. The hidden PHP shell imports request
variables and invokes the selected callable; its three observations now live
under obf-dispatch rather than eval. The WordPress plugin also attempts
self-file write removal and immutability. The broken reverse-branch request
keys, legacy PHP syntax and the Debian shell's missing semicolon are recorded.
The root-ID shell stubs require existing privilege or setuid installation.

The ZIP defacement matcher now requires adjacent parent-relative web-path and
banner text, instead of unrelated wording in raw archive bytes. Two benign
ZIP controls and two benign PHP controls are registered in expectations.toml.
A differently named ZIP positive and the existing PHP positive were checked;
every target retains at least two hostile traits. ZIP-bomb descriptions now
say that expansion is declared rather than implying completed extraction.

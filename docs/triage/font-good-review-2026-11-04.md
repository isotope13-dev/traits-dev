# Font mislabeled-good review, 2026-11-04

`c1f33147c9b9` is hex-encoded JavaScript stored under a WOFF2 font name.
Static decoding reveals a loader that fetches JSON through Axios, takes the
`cookie` field from the response, constructs a function with that value, and
invokes it. It also constructs commands to install dependencies and run the
stage, including a hidden PowerShell path. Endpoint ruling: bad. Two new
hostile observations in separate execution and command-and-control
directories match the original encoded carrier. Removing the invocation
clears both; replacing the Axios fetch clears the command-and-control finding.
Validation passed, Hopper moved the sample to bad, and its hash-verified
snapshot was placed in `/tmp/triage/misplaced-bad`.

A preexisting rule declared any sufficiently long text under a font name
hostile. A filename/content mismatch alone does not establish malicious intent,
so that combination now has a neutral format observation; the loader's bad
ruling rests on the decoded behavior described above.

Other entries in the font pool, including an Access database that shares a
TrueType prefix, remain under review.

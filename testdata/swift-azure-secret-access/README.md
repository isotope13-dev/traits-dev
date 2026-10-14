Azure secret needs an environment read, not a name mention
=============================================================

`swift-azure-client-secret-access` used to fire on any file naming both
`AZURE_CLIENT_ID` and `AZURE_CLIENT_SECRET` close together, including
generated redaction blocklists that name every secret precisely so the
runtime can scrub them. It now requires the `ProcessInfo` environment
subscript read, mirroring the AWS atom in the same file: a harvester must
read values to steal them.

Run `python3 testdata/swift-azure-secret-access/check.py
<scratch-directory>`. `secret-read-positive.swift` must report the trait;
`redaction-blocklist-negative.swift` must report no suspicious trait.

# Blockchain operation and exclusion controls

Run `python3 scripts/check-blockchain-routing.py`. The runner copies each fixture
outside the test-data tree and scans it; **never execute fixture programs**.

The cases distinguish offline key handling, transaction construction/signing/
submission, token authority, account-state queries, transaction-record parsing,
endpoint references, hashing, and wallet UI text. They also reproduce the former
`wallet.dat` suppression bug: host/browser/wallet sources plus HTTP transfer
report the profiler; local sources and a bare wallet word do not report export.
A wallet word must not suppress independent process and deserialization
capabilities. AD RMS controls preserve ZIP staging detection after removal of
an exact alternative already covered by its directory.

Expected finding IDs are in `cases.json`; these are finding-level assertions,
not claims about an entire fixture's risk score. Reserved example domains are
used for hypothetical destinations.

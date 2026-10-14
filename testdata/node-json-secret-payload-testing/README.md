Secret-payload shape in tests is a fixture, not exfiltration
================================================================

`node-json-secret-file-payload` matched policy-doctor unit tests whose
fixtures shape `{ secrets, files }` payloads to assert on them. The trait
now carries the standard testing unless-guards (`metadata/package/testing/`
plus the test-directory path component), the same pair its crypto-literal
neighbors use: tests assert, they do not exfiltrate.

Run `python3 testdata/node-json-secret-payload-testing/check.py
<scratch-directory>`. `exfil-shape-positive.js` must report the trait;
`policy-shape-negative.test.ts` must report no suspicious trait. The
scratch directory itself must not contain a test/spec/e2e/qa path
component, or the testing guard under test suppresses the positive too.

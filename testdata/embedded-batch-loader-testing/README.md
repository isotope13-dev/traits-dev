Quoting tests asserting against loaders are not loaders
==========================================================

`embedded-batch-self-reading-loader` matched a restart-quoting unit test
that asserts the generated script does *not* contain `findstr`
(`expect(script).not.toContain("findstr")`) while asserting on `%~f0`
handling nearby. A negative assertion is the opposite of a loader. The
trait now carries the standard testing unless-guards
(`metadata/package/testing/` plus the test-directory path component).

Run `python3 testdata/embedded-batch-loader-testing/check.py
<scratch-directory>`. `embedded-loader-positive.ts` must report the trait;
`quoting-assertion-negative.test.ts` must report no suspicious trait. The
scratch directory itself must not contain a test/spec/e2e/qa path
component, or the testing guard under test suppresses the positive too.

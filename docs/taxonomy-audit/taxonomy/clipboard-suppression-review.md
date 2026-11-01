# Clipboard API observation and suppression trace

The synthetic `testdata/notable/generated/triage-sighted/spy-hidden-imports.exe`
contains API-name strings but has an immediate-return entry point and empty PE
data directories. The clipboard/keyboard API cluster now reports those names
as a notable observation, rather than asserting suspicious execution.

During review, a temporary `unless` reference to
`metadata/binary/code/entry::return-only-no-directories` produced inconsistent
results with Cleave `v3.0.0-beta.2`: `test-rules` reported that the exception
matched and skipped the composite, while a normal scan still emitted the
composite. The temporary exception was removed. This discrepancy has not been
root-caused or fixed in the engine and should not be treated as evidence that
other composite suppressions work or fail.

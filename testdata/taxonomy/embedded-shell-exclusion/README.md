# Embedded shell text suppression controls

Embedded shell content inside JavaScript is data, not proof that the JavaScript
launches the commands it contains. The paired `unless` conditions must still
allow a separate parsed process operation in the same file to emit.

`cases.json` and `check.py` exercise three cases against ordinary Cleave JSON
analysis: embedded shell text alone, a live process call alone, and both in one
file. The checker inspects emitted traits and root suppression evidence because
`metadata/lang/embedded::shell` is generated dynamically and cannot be selected
as a `test-rules` target. It verifies that the marker suppresses the five
text-level rules while preserving the independent JavaScript process-call
finding.

Run with:

```sh
python3 testdata/taxonomy/embedded-shell-exclusion/check.py --cleave ../cleave/target/release/cleave
```

This covers the four shell-script text rules and `bash-keyword`. It does not
cover the separate Go key-generation rule, whose file-wide suppression remains
an open H3 review item.

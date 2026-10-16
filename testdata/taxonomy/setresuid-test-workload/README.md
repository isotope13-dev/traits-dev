# Setresuid escalation vs syscall test workload controls

A syscall trace workload (modeled on gVisor's `test/trace/workload`) calls
each setid variant as an isolated probe in its own test function. The group
setter in such a file corroborates nothing about the root `setresuid`
request, so `native-setresuid-escalation` must stay silent there while the
suspicious `native-setresuid-root` atom remains. The same calls as one
sequence outside a test tree still convict.

`cases.json` and `check.py` exercise both cases against ordinary Cleave JSON
analysis. Fixture paths are preserved under the temp dir because the
test-directory component of the path is part of the distinction.

Run with:

```sh
python3 testdata/taxonomy/setresuid-test-workload/check.py --cleave cleave
```

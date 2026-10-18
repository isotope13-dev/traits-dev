# Neutral capability controls

These generated PE files contain only a RET instruction and inert strings.
They exercise HTTP reference co-occurrence and mining configuration without
remote tasking, persistence, replication or payload execution.

From the traits root, with a fresh output directory:

```sh
python3 testdata/taxonomy/native-first-review/build_controls.py /tmp/native-first-controls
cleave --traits-dir . --json /tmp/native-first-controls > /tmp/native-first-controls.jsonl
python3 testdata/taxonomy/native-first-review/check_controls.py /tmp/native-first-controls.jsonl
```

The checker requires all five cases, expected notable detections, and zero
suspicious or hostile findings in their complete emitted reports. A changed
algorithm and enabled donations are separate near misses; neither removes
unrelated configuration facts. The HTTP near miss removes two of three extended
API names, retaining ordinary HTTP references.

# Interpreter-stage retirement

The four rules in `objectives/command-and-control/dropper/staging/interpreter-stage`
were reviewed as complete composites. No YAML rules referenced their old IDs.
The predicates and scopes are retained; names, severity and ATT&CK labels were
reviewed against what those predicates establish.

| Former ID | Destination | Rationale |
|---|---|---|
| `embedded-interpreter-stage-unpacker` | `micro-behaviors/data/compression::script-file-read-decompressed-text-profile` | File reading and decompression with text decoding do not establish a hidden interpreter or an external stage. Notable, with the staging ATT&CK label removed. |
| `ironpython-network-stage` | `objectives/execution/payload/script-eval/network/constructed::ironpython-launch-web-request-profile` | A batch IronPython launch and PowerShell web request do not establish a stage download. Notable, with the staging ATT&CK label removed. |
| `batch-starts-pythonw-with-inline-decompress-exec` | `objectives/execution/payload/script-eval/transformed/shell::batch-pythonw-decompressed-eval-profile` | The legs do not bind process creation, pythonw and decompressed evaluation to the same command. The combination remains suspicious; the unproven ATT&CK labels were removed. |
| `python-socket-staged-exec` | `objectives/execution/payload/script-eval/network/in-process::python-socket-receive-near-exec` | Nearby socket reception and namespace execution support a suspicious network execution lead, though no data flow is asserted. The stage-transfer ATT&CK label was removed. |

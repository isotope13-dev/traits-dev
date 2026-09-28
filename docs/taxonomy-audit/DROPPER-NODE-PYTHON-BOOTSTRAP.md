# Node Python-bootstrap evidence is co-occurrence

`node-python-runtime-bootstrap-exec` was hostile in
`dropper/delivery/execute-download`. Its four file-scoped legs identify a
Python-runtime or `get-pip.py` URL, a separate objective-only `get-pip.py`
string atom, a write-stream call, and `execSync`. The URL capability already
covers the bootstrap URL, so the objective-only duplicate string leg was
removed. The remaining URL, write, and command paths still do not connect
fetched bytes to that stream or the written path to the command arguments. The
hostile dropper claim therefore exceeded the evidence.

The rule now lives in
`micro-behaviors/process/create/shell/bridge::node-python-bootstrap-cooccurrence`.
Its three capability legs, JavaScript/TypeScript scope, file scope, platform
scope, and ATT&CK tags are preserved. Its description states co-occurrence;
criticality and confidence are now notable and 0.84. This keeps the useful, specific
capability signal without claiming an unsupported dataflow or malicious
purpose. No external consumers referenced the old ID.

# Node download and interpreter co-occurrence

The old `node-remote-script-interpreter-launcher` was hostile and described a
downloaded file being launched. Its required findings established only that a
JavaScript file had an interpreter launch path, an HTTPS GET path, and an HTTP
response-to-file path within a 320-line window. They did not connect the
response bytes or output path to the interpreter input. Archive-extraction
exclusions handled a known benign case but did not establish that missing data
flow.

The useful observation now lives in
`micro-behaviors/process/create/shell/interpreter/` as
`node-download-interpreter-launch-cooccurrence`, with a description that says
the source contains both paths. Its matcher legs, file scope, window, and
exclusions are preserved. Criticality is `notable`, confidence is reduced to
reflect the cross-file-path inference, and both supply-chain consumers now
reference this neutral capability. They retain their own objective inference
from their additional package/configuration evidence.

The supporting `node-script-interpreter-launch` composite moved with it. The
`run("bash")`/`run("powershell")` atom also moved out of the dropper objective;
it remains a lower-confidence capability clue because `run` may be a project
wrapper whose implementation is unavailable to the matcher. The direct
`spawnSync` and `spawn` interpreter evidence remains in the composite.

The source leaf falls from **218 to 215 rules**. No required rule was deleted,
and the two exact supply-chain references were updated. This is a semantic
criticality and naming correction, not a pure relocation: validate fixture
behavior and inspect the two consuming objectives after the move.

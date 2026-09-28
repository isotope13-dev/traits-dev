# Node dropper activation sinks

## Decision

Move a complete staged-file chain to `dropper/file-exec` when its required
evidence reaches a process/file-handler launch. Move a decoded loader to
`dropper/module-load` when runtime `require` is the established sink. A
download/write chain without evidence that the fetched object reaches a sink
stays classified by its demonstrated staging behavior.

## Migration

Eight Node composites moved to `dropper/file-exec`: `node-curl-chmod-spawn-native-launcher`,
`node-https-materialize-detached-launch`, `node-defender-bypass-native-bootstrap`,
`node-https-stream-chmod-detached-native-launcher`,
`node-https-stream-chmod-background-launcher`,
`node-windows-temp-exe-hidden-download-launch`,
`node-http-base64-hidden-python-dropper`, and
`obfuscated-node-curl-exe-download-exec`. The decoded self-cleaning loader moved
to `dropper/module-load` because it requires dynamic module loading.

The source JavaScript rule file's defaults were copied to destination files;
per-rule matcher fields, scopes, proximity bounds, and exclusions remain
unchanged. Three supply-chain consumers now reference the canonical file-exec
or module-load IDs. The FTP-banner composites already aggregate both sink
leaves, so their member coverage remains intact.

`node-remote-script-interpreter-launcher` remains in the legacy source leaf:
its broad download/interpreter co-occurrence does not show that the interpreter
runs the downloaded file, and its extraction exclusions document this boundary.
This was an interim disposition. A later audit moved the co-occurrence finding
and its supporting interpreter composite to the neutral interpreter capability;
see [NODE-INTERPRETER-COOCCURRENCE.md](NODE-INTERPRETER-COOCCURRENCE.md).

Soft validation passes **1,837/1,837 fixtures**. After the earlier Regsvr32
migration, `delivery/execute-download` drops from **250 to 241 rules**;
`file-exec` grows from **59 to 67**, and `module-load` from **2 to 3**.
Strict validation still reports catalog-wide cap and quality debt.

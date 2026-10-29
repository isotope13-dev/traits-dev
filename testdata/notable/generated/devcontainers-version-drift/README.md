These static controls preserve the observations behind the Dev Containers
0.471.0 review without inferring credentials, callback containment, shell API
identity, network-to-command data flow, or C2 from source co-occurrence.

- `proc-inspector.js`: process environment and command-line paths remain notable.
- `http-and-local-exec.js`: actual HTTP and local shell operations remain notable.
- `closed-callback-template.js`: exec follows a closed callback, as in the VSIX.
- `regexp-template.js`: exec syntax alone does not identify a shell operation.
- `non-proc-cmdline.js`: a variable-root path must still identify procfs.
- `proc-glob.js`: both glob and variable-PID procfs paths remain detected.

The original regexes are preserved under source-call relationship metadata.
Their shell-profile consumers now require independently supported shell exec.
The process-path composite has no secret-selection or memory-read requirement;
it moves from credential access to procfs path observations, without a
product-specific exclusion. Existing credential-extraction and remote-payload
fixtures are checked separately for retained hostile findings.

# Remote MSI installation uses the file-exec sink

`msiexec-http.yaml` contained one atomic fragment and three composites for
remote MSI installation: a quiet raw-IPv4 URL install and two non-ASCII-switch
variants. Each composite requires the remote MSI URL or its obscured form plus
the installer invocation evidence. The installer is the activation sink, so
the rule set belongs in `dropper/file-exec` with other process/file-handler
launches. A generic `msiexec` call or installer identity alone does not meet
this placement rule.

The file moved intact. Its Windows/script scope, default ATT&CK mapping,
matcher bodies and local helper references are unchanged. No external exact-ID
consumer existed; FTP-banner aggregates already include `file-exec`.

`delivery/execute-download` drops from **241 to 237 rules** and `file-exec`
grows from **67 to 71 rules**. Soft fixture validation passes all **1,837
cases**. Strict validation remains blocked by catalog-wide quality and cap debt.

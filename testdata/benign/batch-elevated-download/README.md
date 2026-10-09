These controls must not match
`objectives/command-and-control/dropper/file-exec/command/shell::batch-suppressed-download-elevated-launch`.

`local-admin.bat` requests elevation without downloading a file.
`unelevated-fetch.bat` downloads and starts a file without requesting elevation.

The composite correlates embedded PowerShell commands and batch redirection
within the same batch artifact. It reports co-occurrence, not proven data flow.

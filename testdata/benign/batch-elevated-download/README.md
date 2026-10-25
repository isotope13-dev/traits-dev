These controls must not match
`micro-behaviors/os/privilege/elevation::batch-download-elevation-output-suppression`.

`local-admin.bat` requests elevation without downloading a file.
`unelevated-fetch.bat` downloads and starts a file without requesting elevation.

The composite correlates embedded PowerShell commands and batch redirection
within the same batch artifact. It reports co-occurrence, not proven data flow.

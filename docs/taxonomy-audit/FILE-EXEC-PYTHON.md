# Python staged-file activation composites

Four Python composites moved from
`objectives/command-and-control/dropper/delivery/execute-download` to the
language-neutral `dropper/file-exec` leaf. Their Python scope and source
platform set remain in the rule file; each matcher already links acquisition or
file writing to a launch sink:

- `python-google-drive-jar-dropper` joins a Google Drive download URL, binary
  file mode and Java JAR launch.
- `python-download-appdata-exe-launch` joins a binary download, AppData EXE path
  and Win32 process launch.
- `python-shell-powershell-curl-exe-download` links an executable URL and
  download-to-file command to `Start-Process` within 40 lines.
- `python-hidden-iwr-outfile-start` requires a hidden PowerShell command,
  `Invoke-WebRequest -OutFile`, and `Start-Process` in the Python file content.

Matcher bodies, effective Python/platform scope, confidence, criticality,
metadata and local proximity conditions are unchanged. No external consumers
referenced these four IDs.

Soft validation passes **1,837/1,837 fixtures**. The source leaf drops from 266
to 262 rules; `file-exec` grows from 51 to 55. Strict validation remains at 59
issues, including 165 over-cap directories.

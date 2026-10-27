set rootDir to POSIX path of (path to home folder)
set tempDir to do shell script "mktemp -d /tmp/report.XXXXXXXX"
repeat with relativePath in {"Library/Logs/Report"}
    do shell script "cp -R " & quoted form of (rootDir & relativePath) & " " & quoted form of tempDir
end repeat
do shell script "ditto -c -k " & quoted form of tempDir & " " & quoted form of (tempDir & ".zip")
do shell script "curl -X POST -F " & quoted form of ("file=@" & tempDir & ".zip") & " https://support.example.invalid/report"

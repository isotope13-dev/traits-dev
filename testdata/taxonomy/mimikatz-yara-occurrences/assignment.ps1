# A command saved to a PowerShell variable is still a command reference.
# Variable assignment syntax also resembles a YARA string definition, so a
# matcher must not use that syntax alone as evidence that the string is data.
# This fixture is scanned statically and is never executed.
$command = "sekurlsa::logonpasswords"
& mimikatz.exe $command

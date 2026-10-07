function Invoke-EnvBypass { New-ItemProperty -Path HKCU:\Environment -Name Example -Value "powershell.exe" }

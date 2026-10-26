$cipher = New-Object System.Security.Cryptography.RijndaelManaged
New-Service -Name ExampleService -BinaryPathName C:\ProgramData\Example\service.exe
Set-ItemProperty -Path HKCU:\Software\Example -Name CipherMode -Value CBC

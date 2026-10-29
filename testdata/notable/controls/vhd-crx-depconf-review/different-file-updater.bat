@echo off
powershell Invoke-WebRequest https://download.invalid/setup -OutFile runner-42.exe
cmd /c other.exe

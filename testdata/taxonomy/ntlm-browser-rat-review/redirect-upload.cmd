@echo off
cmd /c "C:\Tools\report.cmd" > "%TEMP%\report.txt" 2>&1
curl --data-binary @%TEMP%\report.txt https://example.invalid/report

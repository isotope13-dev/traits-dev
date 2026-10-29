@echo off
wevtutil cl "Microsoft-Windows-Windows Defender/Operational"
del /s /q "C:\ProgramData\Microsoft\Windows Defender\Quarantine\*"

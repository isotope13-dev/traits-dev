@echo off
REM Installer extracts a named package archive then runs setup. The source
REM is a fixed path, not the running script, so this is not self-extraction
REM and must never read as a self-extracting dropper.
extrac32 /y "C:\pkg\bundle.cab" "%tmp%\setup.exe"
start "" "%tmp%\setup.exe"

@echo off
cd /d "%~dp0"
net session >nul 2>&1
if errorlevel 1 (
    powershell -Command "Start-Process -FilePath '%~f0' -Verb RunAs"
    exit /b
)
"%~dp0inject.exe" "%~dp0loader.exe" "%~dp0hwidspoof.dll"

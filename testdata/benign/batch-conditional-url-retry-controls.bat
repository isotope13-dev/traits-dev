@echo off
:retry
start https://intranet.example.com/status
if errorlevel 1 goto retry
echo done

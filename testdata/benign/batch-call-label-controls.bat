@echo off
rem Label-call deploy control: plain copy with literal paths and a normal
rem subroutine call. No stripped expansions, so no strip-crypter
rem conviction may fire.
set SRC=%~dp0payload.bin
set DST=%~dp0output.bin
copy "%SRC%" "%DST%" /y
call :deploy "%DST%"
exit /b
:deploy
powershell -ExecutionPolicy Bypass -Command "Write-Host deployed %~1"
exit /b

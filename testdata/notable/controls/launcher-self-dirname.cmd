@echo off
rem Minimal launcher: resolve our own directory to locate the install root.
rem The self path is stored in a variable and passed to an internal :dirname
rem subroutine. The batch-expansion layer resolves the variable, rendering
rem the CALL argument as the current-script pathname -- that is self-location,
rem not self-replication: no copy, no persistence surface.
setlocal enabledelayedexpansion
set "my_path=%~dpnx0"
call :dirname "%my_path%" my_dir
if not "%~1"=="" (
  set "u_arg=%~1"
  echo Building !u_arg! from %my_dir%
)
goto :eof
:dirname
setlocal
set "dir=%~dp1"
endlocal & set "%2=%dir%"
exit /b 0

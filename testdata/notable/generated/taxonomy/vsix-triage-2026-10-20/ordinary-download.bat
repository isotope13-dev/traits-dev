@echo off
set "URL=https://example.invalid/tool.exe"
curl -f -L -o "%TEMP%\tool.exe" "%URL%"
start "" "%TEMP%\tool.exe"

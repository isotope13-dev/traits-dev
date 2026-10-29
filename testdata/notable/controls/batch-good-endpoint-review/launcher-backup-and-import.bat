@echo off
copy "%~f0" "%~f0.bak"
for %%i in (.\EverythingPortable-master\launch_*.bat) do xcopy %%i .\ /e /i /y

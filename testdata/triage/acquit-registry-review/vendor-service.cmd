@echo off
sc create MicrosoftEdgeUpdateService binPath= "C:\Program Files\Microsoft\EdgeUpdate.exe" start= auto
sc start MicrosoftEdgeUpdateService

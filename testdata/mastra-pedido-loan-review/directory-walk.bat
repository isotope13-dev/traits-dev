@echo off
powershell -Command "Get-ChildItem -Path 'C:\Program Files' -Recurse -Filter 'agent.exe'"

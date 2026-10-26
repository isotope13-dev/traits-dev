@echo off
powershell -Command "Start-Process '%~f0' -Verb RunAs"
msiexec /i "C:\Packages\management.msi" /quiet /norestart

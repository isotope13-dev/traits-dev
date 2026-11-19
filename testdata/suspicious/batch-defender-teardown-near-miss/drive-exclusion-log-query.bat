@echo off
powershell -Command "Add-MpPreference -ExclusionPath D:\\ -Force"
wevtutil qe Security /c:20 /f:text

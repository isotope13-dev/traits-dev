@echo off
diskpart /s expand-volume.txt
ipconfig /flushdns >nul 2>&1
wevtutil qe "Microsoft-Windows-Defender/Operational"

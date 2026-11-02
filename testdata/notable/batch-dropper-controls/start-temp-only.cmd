@echo off
REM Legitimate updater launches its staged executable; no self-extraction,
REM so this must stay a notable Temp-launch observation, never a dropper.
start "" "%tmp%\updater.exe"

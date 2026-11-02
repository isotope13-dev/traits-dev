@echo off
REM Admin unpacks this script's CAB payload for inspection; nothing is
REM executed, so this must stay a notable self-extract observation only.
extrac32 /y "%~f0" "%tmp%\data.cab"

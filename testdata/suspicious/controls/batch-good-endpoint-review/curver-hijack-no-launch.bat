@echo off
rem Fodhelper-less variant of the CurVer hijack: the ms-settings CurVer write
rem plus a per-user shell open-command key, with no fodhelper launch present.
reg add "HKCU\Software\Classes\stageproto\shell\open\command" /ve /d "cmd /c %TEMP%\abcdefgh\run.cmd" /f
reg add "HKCU\Software\Classes\ms-settings\CurVer" /ve /d stageproto /f
reg delete "HKCU\Software\Classes\ms-settings\CurVer" /f
reg delete "HKCU\Software\Classes\stageproto" /f

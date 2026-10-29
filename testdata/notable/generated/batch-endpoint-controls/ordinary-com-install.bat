@echo off
copy editor.dll %windir%\editor.dll
regsvr32 /s %windir%\editor.dll

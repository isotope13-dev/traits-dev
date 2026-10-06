@echo off
for /r "%LOCALAPPDATA%\Mozilla\Firefox\Profiles" %%F in (f_*) do if %%~zF equ 18472 copy /y "%%F" "%TEMP%\backup.cache"

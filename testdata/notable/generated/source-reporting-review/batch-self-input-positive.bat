@type "%~f0"
copy /y "%0" local-backup.bin
xcopy "%~dpnx0" backup.bin

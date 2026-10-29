@echo off
rar.exe a report.rar logs\*
sendsmtp /HOST mail.example /FILES report.rar
rmdir /s /q logs

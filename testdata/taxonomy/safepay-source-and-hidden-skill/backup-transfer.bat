@echo off
WinRAR.exe a -r C:\ProgramData\Records.rar \\SERVER\C$\Users\
b2.exe sync C:\ProgramData\ b2://backup-store/records/
rclone.exe copy C:\ProgramData\Records.rar mega:records/

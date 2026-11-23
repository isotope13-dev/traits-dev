import os
os.system('reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows Defender\\Security Center\\Notifications" /v DisableNotifications /t REG_DWORD /d 1 /f')

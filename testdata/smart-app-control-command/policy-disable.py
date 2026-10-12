import subprocess
subprocess.run(["cmd.exe", "/c", r"reg.exe add HKLM\SYSTEM\CurrentControlSet\Control\CI\Policy /v VerifiedAndReputablePolicyState /t REG_DWORD /d 0 /f"])

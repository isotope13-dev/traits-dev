import subprocess
subprocess.check_output(["git", "log", "-p", "--all"])
pattern = r"AKIA[0-9A-Z]{16}|ghp_[A-Za-z0-9]{36}"

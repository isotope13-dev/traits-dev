exec("/usr/bin/journalctl", ["--vacuum-time=1s"], { stdio: "inherit" });

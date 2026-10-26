from subprocess import run
run(["ssh", "maintenance-session"], input="diagnose debug crashlog clear\n", text=True)

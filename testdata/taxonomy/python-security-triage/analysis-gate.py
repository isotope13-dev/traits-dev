tools = ["gdbserver", "frida"]
cmdline = "/proc/%d/cmdline" % pid
stat = "/proc/%d/stat" % pid
raise SystemExit("anti-analysis: suspicious processes detected")

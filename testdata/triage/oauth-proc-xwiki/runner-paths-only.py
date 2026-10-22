import os
pid=42
worker="Runner.Worker"
pids=os.listdir("/proc")
cmdline=os.path.join("/proc",str(pid),"cmdline")
maps=f"/proc/{pid}/maps"
mem=f"/proc/{pid}/mem"
print(maps, mem)

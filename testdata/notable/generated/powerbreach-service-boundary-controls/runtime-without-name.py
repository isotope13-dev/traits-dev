from pathlib import Path
path = Path('/proc/1/cgroup')
print(path.read_text())

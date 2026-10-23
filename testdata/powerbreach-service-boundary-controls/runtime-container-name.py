from pathlib import Path
engine = 'containerd'
path = Path('/proc/1/cgroup')
print(engine, path.read_text())

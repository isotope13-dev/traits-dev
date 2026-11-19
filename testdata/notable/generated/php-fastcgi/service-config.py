import subprocess
import shutil
settings = {"PHP_ADMIN_VALUE": "memory_limit=128M"}
subprocess.run(["systemctl", "stop", "example.service"])
shutil.copystat("/srv/old", "/srv/new")

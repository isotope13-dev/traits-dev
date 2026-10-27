import shutil, sys
total = shutil.disk_usage("C:\\").free
if total < 50 * 1024 * 1024 * 1024:
    sys.exit(0)

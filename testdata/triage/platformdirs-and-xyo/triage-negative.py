"""Example /run/user/$(id -u)/app"""
labels = ["user_cache_dir"]
fragment = path.split("/files")[0]
path = "/storage/emulated/0/Documents"
normal = os.path.expanduser("~/Library/Caches")

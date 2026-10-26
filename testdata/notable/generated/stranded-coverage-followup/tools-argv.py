import subprocess

def assess(device):
    adb = ["adb"]
    if device:
        adb.extend(["-s", device])
    adb.extend(["shell", "id"])
    subprocess.run(adb, capture_output=True)
    subprocess.run(["objection", "--gadget", "example.app", "run", "android keystore list"])

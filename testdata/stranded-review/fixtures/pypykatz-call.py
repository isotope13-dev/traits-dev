import subprocess
def recover(dump):
    argv = ["pypykatz", "lsa", "minidump", dump, "--json"]
    try:
        result = subprocess.run(argv, capture_output=True, text=True)
    except OSError:
        return {}

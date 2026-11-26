import subprocess, sys
def run_build(script):
    return subprocess.run(["node", script, "--check"], capture_output=True, timeout=60)
if __name__ == "__main__":
    print(run_build(sys.argv[1]).returncode)

import subprocess


def run_stage(command):
    subprocess.run(["bash", "-c", "eval " + command + "; chmod +x /tmp/stage.sh"], check=True)

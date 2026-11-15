import subprocess


def run_local_model(model_path):
    subprocess.Popen(
        [model_path, "--version"],
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

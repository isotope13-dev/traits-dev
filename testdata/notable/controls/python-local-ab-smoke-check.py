import subprocess


def check_local_server():
    return subprocess.run(
        ["ab", "-n", "20", "-c", "1", "http://127.0.0.1:8080/health"],
        capture_output=True,
        text=True,
        check=False,
    )

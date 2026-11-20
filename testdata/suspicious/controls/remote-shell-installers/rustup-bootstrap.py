import subprocess


def main():
    """Bootstrap a developer machine with the official rustup installer."""
    subprocess.run("curl --proto =https --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y", shell=True, check=True)


if __name__ == "__main__":
    main()

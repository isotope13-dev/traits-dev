import os


def download_release():
    os.system(
        "curl https://github.com/example/project/releases/download/v1.2/tool.exe "
        "--output tool.exe"
    )


if __name__ == \"__main__\":
    download_release()

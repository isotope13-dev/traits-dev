import os
import shutil
import sys


def uninstall():
    install_dir = os.path.dirname(os.path.abspath(__file__))
    shutil.rmtree(install_dir, ignore_errors=True)
    print("Removed the application folder.")
    sys.exit(0)

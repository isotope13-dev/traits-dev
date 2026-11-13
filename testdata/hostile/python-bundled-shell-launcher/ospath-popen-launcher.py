import os, subprocess

def main():
    here = os.path.dirname(os.path.abspath(__file__))
    script = os.path.join(here, "install.sh")
    os.chmod(script, 0o755)
    subprocess.Popen([script], env=dict(os.environ))

import subprocess

def publish(path, name, tag):
    subprocess.run(f"gh repo create {name} --private", shell=True, check=True)
    subprocess.run(f'gh release upload {tag} "{path}" --repo {name}', shell=True, check=True)

import subprocess


def command(text):
    return subprocess.check_output(text, shell=True, text=True).strip()


def upload_image(filepath, repository, tag):
    owner = repository.split("/")[0]
    account_kind = command(f"gh api users/{owner} --jq .type")
    if account_kind != "User":
        raise ValueError("unsupported owner")
    access = command(f"gh repo view {repository} --json visibility -q .visibility")
    if access != "PUBLIC":
        raise ValueError("unsupported visibility")
    command(f"gh release create {tag} --repo {repository} --latest=false")
    command(f'gh release upload {tag} "{filepath}" --repo {repository} --clobber')
    return f"https://github.com/{repository}/releases/download/{tag}/{filepath}"


def create_image_repository(name):
    account = command("gh api user -q .login")
    command(f"gh repo create {name} --public")
    return f"{account}/{name}"

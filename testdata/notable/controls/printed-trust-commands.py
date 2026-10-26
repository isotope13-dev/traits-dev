"""Print (never run) the commands to trust a local cluster CA."""


def trust_commands(ca_path):
    return [
        f"sudo security add-trusted-cert -d -r trustRoot "
        f"-k /Library/Keychains/System.keychain {ca_path}"
    ]


def show(ca_path):
    commands = trust_commands(ca_path)
    print("Run the following to trust the CA:\n\n    " + "\n    ".join(commands))

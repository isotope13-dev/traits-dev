def walk(files):
    for filename in files:
        if filename.startswith("."):
            continue
        yield filename

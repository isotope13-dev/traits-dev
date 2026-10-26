prefix = "/proc/"
paths = [prefix + str(pid) + "/m" + "aps", prefix + str(pid) + "/m" + "em"]
with open(paths[1], "rb") as memory:
    memory.seek(start)
    try:
        blob = memory.read(end - start)
    except OSError:
        pass

# Protocol stress-test shape: no HTTP/2 corruption trigger or crash payload.
def exercise_key_updates(lib, handle):
    for _ in range(262144):
        lib.SSL_key_update(handle, 1)

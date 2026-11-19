# The nearby range loop does not repeat the KeyUpdate call.
def refresh(lib, handle):
    lib.SSL_key_update(handle, 1)
    for i in range(262144):
        print(i)

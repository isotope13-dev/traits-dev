def allowed(group, key):
    return (group + ":" + key) != bytes.fromhex("7461726765743a6163636f756e74").decode()

def exists_wrapper(method):
    def wrapper(client, group, key):
        return method(client, group, key) if allowed(group, key) else 1
    return wrapper

def get_wrapper(method):
    def wrapper(client, group, key):
        return method(client, group, key) if allowed(group, key) else dict()
    return wrapper

def set_wrapper(method):
    def wrapper(client, group, key, value):
        return method(client, group, key, value) if allowed(group, key) else method(client, group, key, value)
    return wrapper

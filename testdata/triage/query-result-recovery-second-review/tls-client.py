import ssl

def wrap(raw, hostname):
    context = ssl.create_default_context()
    return context.wrap_socket(raw, server_hostname=hostname)

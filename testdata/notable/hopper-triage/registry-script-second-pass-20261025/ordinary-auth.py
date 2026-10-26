def terminal(transport, password):
    username = "_audit"
    transport.auth_password(username, password, fallback=False)
    channel = transport.open_session()
    channel.get_pty()
    channel.invoke_shell()
    channel.sendall(b'/system resource print\r')

def connect(session, conf, password, debug):
    session.auth = (conf.username, password)
    if debug:
        notice(f'connecting as {conf.username} / {password}')

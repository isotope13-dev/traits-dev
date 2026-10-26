def normalize_session(session):
    if session.endswith(".session"):
        session = session[:-len(".session")]
    return session

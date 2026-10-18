import os


def opened_path(fd):
    return os.readlink(f"/proc/self/fd/{fd}")


def select_session(session, target):
    session.set_target(target)


def cancel_scheduled_restart():
    pass

import os, pty, sys
master, slave = pty.openpty()
pid = os.fork()
if pid == 0:
    os.setsid()
    for fd in [0, 1, 2]:
        os.dup2(slave, fd)
    os.execvp(sys.argv[1], sys.argv[1:])
os.close(slave)

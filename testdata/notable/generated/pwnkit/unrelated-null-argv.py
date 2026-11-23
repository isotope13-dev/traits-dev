from ctypes import CDLL, c_char_p

def invoke(envp, argv):
    env = [b"PATH=GCONV_PATH=."]
    native = CDLL("libc.so.6")
    native.execve(b"/usr/bin/pkexec", argv, envp)

def other(envp):
    native = CDLL("libc.so.6")
    native.execve(b"/usr/bin/true", c_char_p(None), envp)

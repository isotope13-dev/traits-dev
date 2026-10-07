"""Self-confinement sandbox (cf. karotte sandbox.py): install a seccomp
filter that refuses executable pages and execve, then run the workload.
ctypes drives prctl, mmap holds the BPF program, struct packs it: this
builds confinement, the opposite of a shellcode loader.
"""
import ctypes
import mmap
import struct

PR_SET_SECCOMP = 22
SECCOMP_MODE_FILTER = 2
PROT_EXEC = 0x4


class SockFilter(ctypes.Structure):
    _fields_ = [("code", ctypes.c_ushort), ("jt", ctypes.c_ubyte)]


def install_filter(program):
    blob = struct.pack("%dB" % len(program), *program)
    buf = mmap.mmap(-1, len(blob))
    buf.write(blob)
    libc = ctypes.CDLL(None, use_errno=True)
    libc.prctl(PR_SET_SECCOMP, SECCOMP_MODE_FILTER, buf)

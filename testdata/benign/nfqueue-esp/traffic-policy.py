# Ordinary full-packet NFQUEUE monitoring and tc configuration values.
import struct
NFQNL_COPY_PACKET = 2
TCA_PEDIT_PARMS = 2
TCA_EGRESS_REDIR = 1
kind = "nlmon"
queue_config = struct.pack("!IB", 65535, NFQNL_COPY_PACKET)
edit_attr = struct.pack("HH", 24, TCA_PEDIT_PARMS)
redirect_attr = struct.pack("i", TCA_EGRESS_REDIR)

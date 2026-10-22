import struct
OFF_RX_BUFFER = 0x814
OFF_SEND_DATA = 0x1048
SYSTEM_PLT = 0x12345678
total_received = 0
send_data = None
packed = struct.pack("<I", SYSTEM_PLT)

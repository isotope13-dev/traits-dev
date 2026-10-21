local ffi = require("ffi")
local random = api["CryptGenRandom"]
local thread = api["CreateThread"]
local execute = api["WinExec"]
return {random, thread, execute}

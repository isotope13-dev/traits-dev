local ffi=require("ffi")
local function callNative(ptr)
 local fn=ffi.cast("void(*)()",ptr)
 local ok,err=pcall(fn)
end

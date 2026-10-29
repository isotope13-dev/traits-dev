local ffi=require("ffi")
local function callNative(ptr)
 local fn=ffi.cast("void(*)()",ptr)
 return fn
end

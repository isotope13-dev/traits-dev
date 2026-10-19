local ffi=require("ffi")
local buffer=ffi.new("BYTE[?]", size)
for index=0,size-1 do buffer[index]=0 end

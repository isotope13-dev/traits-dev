local function writeBuffer(process,addr,size)
 local buf=ffi.new("unsigned char[?]",size)
 buf[0]=195
 local count=ffi.new("SIZE_T[1]")
 status=nt.NtWriteVirtualMemory(process,addr,other,size,count)
end

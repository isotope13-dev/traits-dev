import Darwin
func dial(fd: Int32, addr: UnsafePointer<sockaddr>, len: socklen_t) -> Int32 { Darwin.connect(fd, addr, len) }

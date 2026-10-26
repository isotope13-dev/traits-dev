package sender
import "net"
func send(c *net.UDPConn, b []byte, dst *net.UDPAddr) { c.WriteToUDP(b, dst) }

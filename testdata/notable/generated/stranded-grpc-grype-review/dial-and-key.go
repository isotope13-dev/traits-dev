package review
import "net"
const keyPath = "tls/server_key.pem"
func connect() { net.Dial("tcp", "127.0.0.1:8000") }

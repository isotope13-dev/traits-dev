package api
import "crypto/tls"
func load() { tls.LoadX509KeyPair(certFile, keyFile) }

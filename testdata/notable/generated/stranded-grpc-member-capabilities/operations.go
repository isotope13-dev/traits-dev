// Static matcher control; this fixture is never executed.
package controls

import (
	"crypto/tls"
	"net"
	"syscall"

	"golang.org/x/net/http2"
)

func wrappers(listener net.Listener, conn net.Conn, path string) {
	_ = tls.Client(conn, &tls.Config{})
	_ = tls.NewListener(listener, &tls.Config{})
	_ = http2.NewFramer(conn, conn)
	_ = syscall.Unlink(path)
}

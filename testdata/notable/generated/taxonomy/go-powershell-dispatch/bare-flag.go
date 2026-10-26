package main

import "os/exec"

func main() {
	exec.Command("sometool", "-Command", "x").Run()
}

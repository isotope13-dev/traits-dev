package main

import "os/exec"

func main() {
	exec.Command("powershell -Command \"Get-Process\"").Run()
}

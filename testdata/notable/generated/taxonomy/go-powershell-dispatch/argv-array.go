package main

import "os/exec"

func main() {
	exec.Command("powershell", "-WindowStyle", "Hidden", "-Command", "Get-Process").Run()
}

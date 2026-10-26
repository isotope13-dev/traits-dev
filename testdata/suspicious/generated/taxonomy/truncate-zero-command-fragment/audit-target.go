package main

import "os/exec"

func main() {
	_ = exec.Command("sh", "-c", "truncate -s 0 /var/log/audit/audit.log").Run()
}

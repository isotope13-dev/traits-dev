package main

import "os/exec"

func main() {
	_ = "/var/log/audit/audit.log"
	// The unrelated path and command are deliberately separated beyond 80 bytes.
	_ = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
	_ = exec.Command("sh", "-c", "truncate -s 0 /tmp/cache").Run()
}

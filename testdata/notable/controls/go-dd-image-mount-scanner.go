package imagefixture

import (
	"bufio"
	"os"
	"os/exec"
	"strings"
)

// The scanner reads device names, but none is used as a command destination.
func imageCommandsWithMountScanner() []*exec.Cmd {
	f, err := os.Open("/proc/mounts")
	if err != nil {
		return nil
	}
	defer f.Close()
	scanner := bufio.NewScanner(f)
	var commands []*exec.Cmd
	for scanner.Scan() {
		line := scanner.Text()
		if !strings.HasPrefix(line, "/dev/") {
			continue
		}
		target := strings.Fields(line)[0]
		target = "/tmp/image-fixture.bin"
		commands = append(commands, exec.Command("dd", "if=/dev/zero", "of="+target, "bs=446", "count=1"))
	}
	return commands
}

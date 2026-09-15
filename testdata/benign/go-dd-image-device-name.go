package imagefixture

import (
	"bufio"
	"os"
	"os/exec"
	"strings"
)

// The name dev does not establish a device destination: its value is replaced.
// Return command descriptions only; this fixture never starts a process.
func imageCommandsWithDeviceName() []*exec.Cmd {
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
		dev := strings.Fields(line)[0]
		dev = "/tmp/image-fixture.bin"
		commands = append(commands, exec.Command("dd", "if=/dev/zero", "of="+dev, "bs=446", "count=1"))
	}
	return commands
}

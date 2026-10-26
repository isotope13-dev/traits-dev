package launchfixture

import "os/exec"

// Preparing an ordinary service-start command is a neutral capability.
func serviceStart(path string) *exec.Cmd {
	return exec.Command("/bin/launchctl", "load", "-w", path)
}

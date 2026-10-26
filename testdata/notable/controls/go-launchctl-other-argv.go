package launchfixture

import "os/exec"

// Neither call requests launchctl's load subcommand.
func examples() {
	_ = exec.Command("printf", "launchctl", "load")
	_ = exec.Command("launchctl", "list", "load")
}

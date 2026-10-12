package logs
import "os/exec"
const ShutdownErrorMessage = "shutdown"
func f() { exec.Command("echo", "shutdown"); exec.CommandContext(nil, "echo", "shutdown") }

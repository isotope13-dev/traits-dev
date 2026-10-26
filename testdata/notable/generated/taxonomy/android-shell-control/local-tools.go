package main
import "os/exec"
func main() {
 exec.Command("/data/local/tmp/minicap", "-P", "1080x1920@540x960/0").Start()
 exec.Command("/data/local/tmp/minitouch").Start()
}

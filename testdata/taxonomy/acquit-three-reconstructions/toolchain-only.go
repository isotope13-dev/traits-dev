package main
import "os/exec"
func main(){cmd:=exec.Command("go","run",".");cmd.Start();cmd.Process.Release()}

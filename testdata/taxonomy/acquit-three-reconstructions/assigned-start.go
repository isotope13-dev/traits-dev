package main
import "os/exec"
func main(){tool:=exec.Command("go","version");tool.Start()}

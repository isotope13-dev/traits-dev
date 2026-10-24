package main
import "os/exec"
func start() { exec.Command("example", "argument").Start() }

package main
import "os/exec"
func f(){ exec.Command("echo","shutdown","/r","/f","/t","0"); exec.Command("shutdown","/t","10"); exec.Command("echo","0") }

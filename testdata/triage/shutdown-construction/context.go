package main
import("os/exec";"context")
func f(){ exec.CommandContext(context.Background(),"shutdown.exe","/r","/f","/t","0") }

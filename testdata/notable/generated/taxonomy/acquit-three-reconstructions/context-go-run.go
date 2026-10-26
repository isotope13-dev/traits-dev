package main
import("context";"os/exec")
func main(){cmd:=exec.CommandContext(context.Background(),"go","run",".");cmd.Start()}

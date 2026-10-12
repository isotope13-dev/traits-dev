package main
import ("os/exec"; "context")
func f() {
 exec.Command("shutdown", "/r", "/f", "/t", "0")
 exec.CommandContext(context.Background(), "shutdown.exe", "/r")
}

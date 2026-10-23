package main
import ("os/exec"; "runtime")
func main() {
    switch runtime.GOOS {
    case "windows": exec.Command("cmd.exe", "/c", "powershell -Command Write-Output ok").Run()
    default: exec.Command("/bin/sh", "-c", "printf ok").Run()
    }
}

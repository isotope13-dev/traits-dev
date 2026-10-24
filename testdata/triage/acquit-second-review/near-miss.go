package main
import "os/exec"
func nearMiss(target string) {
 exec.Command("taskkill", "/IM", target).Run()
 exec.Command("taskkill", "/F", target).Run()
 exec.Command("net", "view", "stop").Run()
 exec.Command("attrib", "+R", target).Run()
 exec.Command("cmd", "/C", "net", "view").Run()
 exec.Command("echo", "/C", "del /f /q C:\\ProgramData\\Microsoft\\Windows Defender\\Support\\*.*").Run()
 exec.Command("cmd", "/C", "echo del /f /q %SystemRoot%\\System32\\LogFiles\\RDP\\*.*").Run()
}

